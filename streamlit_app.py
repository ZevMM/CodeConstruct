import streamlit as st
import requests
import json
from requests.auth import HTTPBasicAuth
from io import BytesIO


payload = {
    'username': 'alice',
    'password': 'secret'
}
resp = requests.post('https://api.spaceforce.sh/login/oauth/access-token', data= payload)
token = json.loads(resp.text)["access_token"]
headers = {
    'Authorization': f'Bearer {token}'
}

response = requests.get(f'https://api.spaceforce.sh/satellites/oauth/{634}/live', headers=headers)
image_stream = BytesIO(response.content)

resp = requests.get(f'https://api.spaceforce.sh/tags')
tags = json.loads(resp.text)

resp = requests.get(f'https://api.spaceforce.sh/categories')
cats = json.loads(resp.text)

resp = requests.get(f'https://api.spaceforce.sh/owners')
owners = json.loads(resp.text)

categories = {
    "Tags": tags,
    "Categories": cats,
    "Owners": owners
}

results = [
"Result 1: Information A",
"Result 2: Information B",
"Result 3: Information C"
]
#response = requests.get('https://api.spaceforce.sh/satellites/private/', auth=HTTPBasicAuth('alice', 'secret'))
#print(json.loads(response.text)[0])
#resp = requests.get('https://api.spaceforce.sh/satellites/public/')
#print(resp.text)


import streamlit as st

# Function to run when any checkbox is checked
def run_function():
    st.success("At least one checkbox is checked!")

# Title of the app
st.title("Space Force Satellite Search")

# Sidebar for checkboxes
with st.sidebar:
    st.header("Filter")
    
    # Track the checked items
    checked_items = []

    # Create sections with checkboxes dynamically
    for category, items in categories.items():
        with st.expander(category):
            if category not in st.session_state:
                st.session_state[category] = [False] * len(items)
            for idx, item in enumerate(items):
                checked = st.checkbox(item, value=st.session_state[category][idx], key=f"{category}{idx}")
                st.session_state[category][idx] = checked  # Update session state
                if checked:
                    checked_items.append(item)

    # Check if any checkbox is checked
    if any(st.session_state.checkboxes):
        run_function()

    # Radio buttons for selecting a single result
    selected_result = st.radio("Select a result:", results)


# Main area for the image
st.header("Live Image")
st.image(image_stream, caption="", use_column_width=True)

def run_function():
    pass
