import amphora_client
import requests

source_url = "https://gist.githubusercontent.com/xtellurian/9efcf3d6ba8e6e7feae5dd051e3b54a6/raw/7b4fc27082ec759025f40dc2d7a57003147f5630/aem-5min.json"

# EXTRACT
PARAMS = {'key':"value"} 

r = requests.get(url = source_url, params = PARAMS)
data = r.json()
print(data)

# TRANSFORM

# print(f'there are {len(data['5MIN')} samples')

# LOAD