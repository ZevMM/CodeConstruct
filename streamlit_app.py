import streamlit as st
import requests
import json
from requests.auth import HTTPBasicAuth
from io import BytesIO
import streamlit as st

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("./space.jpg")
    }
   .sidebar .sidebar-content {
        background: url("./space.jpg")
    }
    </style>
    """,
    unsafe_allow_html=True
)

payload = {
    'username': 'alice',
    'password': 'secret'
}

resp = requests.post('https://api.spaceforce.sh/login/oauth/access-token', data= payload)
token = json.loads(resp.text)["access_token"]
headers = {
    'Authorization': f'Bearer {token}'
}

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

    # Radio buttons for selecting a single result
    sel_tags = ([v for i, v in enumerate(categories["Tags"]) if st.session_state['Tags'][i]])
    sel_cats = ([v for i, v in enumerate(categories["Categories"]) if st.session_state['Categories'][i]])
    sel_owner = ([v for i, v in enumerate(categories["Owners"]) if st.session_state['Owners'][i]])

    params = {
        'offset': 0,
        'limit': 10,
        'tags': sel_tags,
        'categories':sel_cats,
        'owner': sel_owner
    }

    response = requests.get('https://api.spaceforce.sh/satellites/private/search', params= params, auth=HTTPBasicAuth('alice', 'secret'))
    results = [(i["object_name"], i["norad_cat_id"]) for i in json.loads(response.text)]
    selected_result = st.radio("Select a result:", results)


curr = 634
data = {}


if selected_result:
    curr = int(selected_result[1])

try:
    #response = requests.get(f'https://api.spaceforce.sh/satellites/oauth/{curr}/live', headers=headers)
    data = json.loads(requests.get(f'https://api.spaceforce.sh/satellites/private/{curr}', auth=HTTPBasicAuth('alice', 'secret')).text)
except Exception as e:
    print(e)

if response.status_code == 200:
    with open("downloaded_image.png", "wb") as f:
        f.write(response.content)
else:
    print("Error:", response.status_code, response.text)

st.header("Live Image")
try:
    st.image("downloaded_image.png", caption="", use_column_width=True)
except:
    st.image("satellite.png", caption="", use_column_width=True)






st.write("")  # Add some space

# Bottom bar section
st.subheader(data["object_name"])
st.markdown("---")
for key, value in data.items():
    st.write(f"**{key}**: {value}")


