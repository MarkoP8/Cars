class NoRequiredOptionException(Exception):
    
    def __init__(self, field_name):
        super().__init__(f"Field \"{field_name}\" is required, but not found.")