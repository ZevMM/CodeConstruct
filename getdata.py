import requests
import json

#resp = requests.get('https://api.spaceforce.sh/satellites/public/')
#print(resp.text)

from requests.auth import HTTPBasicAuth

payload = {
    'username': 'alice',
    'password': 'secret'
}

resp = requests.post('https://api.spaceforce.sh/login/oauth/access-token', data= payload)
token = json.loads(resp.text)["access_token"]
print(token)

#response = requests.get('https://api.spaceforce.sh/satellites/private/', auth=HTTPBasicAuth('alice', 'secret'))
#print(json.loads(response.text)[0])


headers = {
    'Authorization': f'Bearer {token}'
}

# Make the GET request
response = requests.get(f'https://api.spaceforce.sh/satellites/oauth/{634}/live', headers=headers)

print(response.content)

from io import BytesIO
# Create a binary stream
image_stream = BytesIO(response.content)
st.image(image_stream, caption='My Image')