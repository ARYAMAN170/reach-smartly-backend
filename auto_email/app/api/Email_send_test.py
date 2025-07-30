from google_api import create_service

client_secret_file = 'gmail_api.json'
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
service = create_service(client_secret_file,API_SERVICE_NAME,API_VERSION,SCOPES)