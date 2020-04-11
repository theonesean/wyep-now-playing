import requests, time, sys

from authvars import *

# TEST IF APP IS ALREADY AUTHORIZED

try:
    ACCESS_TOKEN
    REFRESH_TOKEN
    tokens_exist = True
except:
    tokens_exist = False

# AUTHORIZATION WORKFLOW
# will only run if tokens are not in `authvars.py`

if not tokens_exist:

    # device authorization
    device_params = {
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'scope': 'listening.readonly'
    }

    device_headers = {
        'Accept': 'application/json'
    }

    device_result = requests.post('https://authorization.api.npr.org/v2/device', 
        data=device_params, 
        headers=device_headers).json()
    
    print()
    print("Go to", device_result['verification_uri'], 
        "in the next 30 seconds",
        "and enter the code", device_result['user_code'])
    print()

    print('Sleeping for 30 seconds...', end='')
    for x in range(0, 30):
        print('.', end='')
        time.sleep(1)
    print('Waking up...')
    print()

    # token authorization
    token_params = {
        'grant_type': 'device_code',
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'code': device_result['device_code'],
        'scope': 'listening.readonly'
    }

    token_headers = {
        'Accept': 'application/json'
    }

    token_result = requests.post('https://authorization.api.npr.org/v2/token',
        data=token_params,
        headers=token_headers).json()

    print('Adding tokens to authvars.py...')

    # test if token results exist
    if 'access_token' in token_result and 'refresh_token' in token_result:
        with open('authvars.py', 'a') as authf:
            authf.write("ACCESS_TOKEN = '" + token_result['access_token'] + "'")
            authf.write("REFRESH_TOKEN = '" + token_result['refresh_token'] + "'")
        ACCESS_TOKEN = token_result['access_token']
        REFRESH_TOKEN = token_result['refresh_token']
        print('Tokens added successfully.')
    else:
        print('Token authorization failed with error', token_result['error'])
        print(token_result['message'])
        print()
        sys.exit(0)