import re
import requests
anchor_url = 'PUT ANCHOR URL HERE'
url_base = 'https://www.google.com/recaptcha/'
match = re.search(r'([api2|enterprise]+)/anchor\?(.*)', anchor_url)
if not match:
    raise ValueError("Invalid anchor URL format")
url_base += match.group(0) + '/'
params = match.group(2)
response = requests.get(
    url_base + 'anchor',
    headers={'content-type': 'application/x-www-form-urlencoded'},
    params={params}
)
if response.status_code != 200:
    raise Exception(f"Failed to fetch anchor page: {response.status_code}")
token_match = re.search(r'"recaptcha-token" value="(.*?)"', response.text)
if not token_match:
    raise ValueError("Failed to find recaptcha token in response")
token = token_match.group(1)
params_dict = {}
for pair in params.split('&'):
    key, value = pair.split('=')
    params_dict[key] = value
post_data = f"{params_dict['v']}{token}{params_dict['k']}{params_dict['co']}"
key_match = re.search(r'value="(.*?)"', post_data)
if not key_match:
    raise ValueError("Failed to extract key from post_data")
key = key_match.group(1)
print(key)
