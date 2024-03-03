from datetime import date, datetime, timedelta  # To define date range of data
import requests  # To define http request to be make
import pandas as pd  # Convert data received from copernicus API in easier format
# Convert Pandas dataframe in Geo pandas will allow us to use metadata and geoemtry.
import geopandas as gpd
from shapely.geometry import shape  # To convert raw Geometry data

# copernicus User email
copernicus_user = "usuario"
# copernicus User Password
copernicus_password = "contraseña"
# WKT Representation of BBOX of AOI
ft = "POLYGON ((-1.016235 42.175617, -1.016235 43.165123, 2.241211 43.165123, 2.241211 42.175617, -1.016235 42.175617))"
# Sentinel satellite that you are interested in
data_collection = "SENTINEL-2"


# Dates of search
# Fecha de inicio de la búsqueda (15 de agosto de 2015)
start_date = datetime(2015, 8, 15)
end_date = datetime.today()

# Convertir las fechas a strings en el formato esperado ("YYYY-MM-DD")
start_date_string = start_date.strftime("%Y-%m-%d")
end_date_string = end_date.strftime("%Y-%m-%d")

# Imprimir las fechas para verificar
print("Fecha de inicio de la búsqueda:", start_date_string)
print("Fecha de fin de la búsqueda:", end_date_string)

# Función de configuración para obtener el token de acceso de Copernicus según el nombre de usuario y la contraseña proporcionados en las variables anteriores


def get_keycloak(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
    }
    try:
        r = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data=data,
        )
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Keycloak token creation failed. Reponse from the server was: {r.json()}"
        )
    return r.json()["access_token"]


# Finalmente, crearemos código para usar todas las variables y el token de acceso para acceder a la API y obtener datos.

json_ = requests.get(
    f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{ft}') and ContentDate/Start gt {start_date.strftime('%Y-%m-%d')}T00:00:00.000Z and ContentDate/Start lt {end_date.strftime('%Y-%m-%d')}T00:00:00.000Z&$count=True&$top=1000"
).json()

# Obtener el conjunto de datos disponible
p = pd.DataFrame.from_dict(json_["value"])
if p.shape[0] > 0:  # If we get data back
    p["geometry"] = p["GeoFootprint"].apply(shape)
    # Convert pandas dataframe to Geopandas dataframe by setting up geometry
    productDF = gpd.GeoDataFrame(p).set_geometry("geometry")
    # Remove L1C dataset if not needed
    productDF = productDF[~productDF["Name"].str.contains("L1C")]
    print(f" total L2A tiles found {len(productDF)}")
    productDF["identifier"] = productDF["Name"].str.split(".").str[0]
    allfeat = len(productDF)

    if allfeat == 0:  # If L2A tiles are not available in current query
        print(f"No tiles found for {end_date_string}")
    else:  # If L2A tiles are available in current query
        # download all tiles from server
        for index, feat in enumerate(productDF.iterfeatures()):
            try:
                # Create requests session
                session = requests.Session()
                # Get access token based on username and password
                keycloak_token = get_keycloak(
                    copernicus_user, copernicus_password)

                session.headers.update(
                    {"Authorization": f"Bearer {keycloak_token}"})
                url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({feat['properties']['Id']})/$value"
                response = session.get(url, allow_redirects=False)
                while response.status_code in (301, 302, 303, 307):
                    url = response.headers["Location"]
                    response = session.get(url, allow_redirects=False)
                print(feat["properties"]["Id"])
                file = session.get(url, verify=False, allow_redirects=True)

                with open(
                    # location to save zip from copernicus
                    f"location/to/save/{feat['properties']['identifier']}.zip",
                    "wb",
                ) as p:
                    print(feat["properties"]["Name"])
                    p.write(file.content)
            except:
                print("problem with server")
else:  # If no tiles found for given date range and AOI
    print('no data found')
