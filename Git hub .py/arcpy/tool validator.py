import arcpy
import os


class ToolValidator(object):
    """Class for validating a tool's parameter values and controlling
    the behavior of the tool's dialog."""

    def __init__(self):
        """Setup arcpy and the list of tool parameters."""
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        """Refine the properties of a tool's parameters. This method is 
        called when the tool is opened."""
        # Agrego descripción del primer parámetro
        self.params[0].description = "Introduce aquí la carpeta con tus archivos GPX"
        self.params[1].description = "Introduce aquí la carpeta donde guardarás la Gdb"
        self.params[2].description = "Pon aquí el nombre de tu Gdb"

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed. This method is called whenever a parameter
        has been changed."""
        # Validar el primer input, la carpeta de GPX
        if self.params[0].altered:
            input_workspace = self.params[0].value
            if not input_workspace:
                self.params[0].setErrorMessage(
                    "La carpeta de GPX no puede estar vacía.")
                return
            if not arcpy.Exists(input_workspace):
                self.params[0].setErrorMessage("La carpeta de GPX no existe.")
                return
            # Verificar que haya archivos con extensión .gpx en la carpeta
            if not any(filename.lower().endswith('.gpx') for filename in arcpy.ListFiles(input_workspace)):
                self.params[0].setErrorMessage(
                    "La carpeta está vacía. Por favor, asegúrate de que existan archivos con extensión .gpx en la misma.")
                return
            # Verificar que todos los archivos en la carpeta tienen la extensión .gpx
            for filename in arcpy.ListFiles(input_workspace):
                if not filename.lower().endswith('.gpx'):
                    self.params[0].setErrorMessage(
                        "Alguno o todos los archivos de esta carpeta no tienen extensión .gpx. Por favor, revísalo y vuelve a cargarlos.")
                    return

    def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
