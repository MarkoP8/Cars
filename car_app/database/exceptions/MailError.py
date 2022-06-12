class MailError(Exception):

    def __init__(self):
        super().__init__("Mail nije validan")