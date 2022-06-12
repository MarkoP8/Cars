class SettingsFileNotExistException(Exception):
    
    def __init__(self, path=""):
        super().__init__(f"File \"{path}\" was not found.")