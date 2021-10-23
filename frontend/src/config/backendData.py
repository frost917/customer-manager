import os 

backendData = dict()
backendData['ADDR'] = os.getenv('BACKEND_ADDR')

if os.getenv("DEBUG") == 'True':
    backendData['CA_CERT'] = False
else:
    backendData['CA_CERT'] = os.getenv('CA_CERT')