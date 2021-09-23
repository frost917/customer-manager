import os 

backendData = dict()
backendData['ADDR'] = os.getenv('BACKEND_ADDR')
backendData['CA_CERT'] = os.getenv('CA_CERT')