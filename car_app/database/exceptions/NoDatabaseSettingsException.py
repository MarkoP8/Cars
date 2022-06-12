class NoDatabaseSettingsException(Exception):
    
    def __init__(self):
        super().__init__("There is no section [database] in settings.")