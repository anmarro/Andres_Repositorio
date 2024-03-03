from datetime import datetime, timedelta
import requests
import os

# Copernicus User email
copernicus_user = "anmarro80@hotmail.com"
# Copernicus User Password
copernicus_password = "IRMAbajo1980@"
# WKT Representation of BBOX of AOI
ft = "POLYGON ((-1.016235 42.175617, -1.016235 43.165123, 2.241211 43.165123, 2.241211 42.175617, -1.016235 42.175617))"
# Sentinel satellite that you are interested in
data_collection = "SENTINEL-2"

# Your client credentials
client_id = 'sh-5a733650-c2e9-4bbe-9ad1-4da4e2d43512'
client_secret = 'DvaBpy7NZ1AV8ROa4Ult33N1jCJYKQvT'

# Function to get access token from Copernicus


def get_access_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    try:
        r = requests.post(
            "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data=data
        )
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Token retrieval failed. Response from the server was: {r.json()}")
    return r.json()["access_token"]


# Set start and end dates
start_date = datetime(2015, 7, 1)
end_date = datetime(2015, 12, 31)

# Initialize directory for saving images
save_dir = r"C:\PIRINEOS\SENTINEL DESCARGADAS"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Loop through each month from start_date to end_date
current_date = start_date
while current_date < end_date:
    # Get start and end dates for the current month
    month_start = current_date.replace(day=1)
    next_month = month_start + timedelta(days=31)
    month_end = next_month - timedelta(days=1)

    # Get access token
    access_token = get_access_token()

    # Query Copernicus API
    response = requests.get(
        f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{ft}') and ContentDate/Start ge {month_start.strftime('%Y-%m-%d')}T00:00:00.000Z and ContentDate/End le {month_end.strftime('%Y-%m-%d')}T23:59:59.999Z&$count=True&$top=1000",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Convert response to JSON
    json_response = response.json()

    # Check if any products are found
    if "value" in json_response:
        print(f"Processing data for {month_start.strftime('%B %Y')}...")
        # Download products with less than 10% cloud cover
        for product in json_response["value"]:
            if "CloudCover" in product and product["CloudCover"] is not None and product["CloudCover"] <= 10:
                url = product["Location"]
                filename = os.path.join(
                    save_dir, f"{product['Identifier']}.zip")
                with open(filename, "wb") as f:
                    print(f"Downloading {filename}...")
                    f.write(requests.get(url).content)
            else:
                print("Skipping product without cloud cover information.")

    # Move to next month
    current_date = next_month

print("Download completed.")
