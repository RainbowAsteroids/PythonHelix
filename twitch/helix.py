import json
import requests


def search(query: str, client_id: str, token: str, live_only=True) -> dict:
    url = 'https://api.twitch.tv/helix/search/channels?query={}&live_only={}'
    r = requests.get(
        url.format(query, int(live_only)),
        headers={
            'client-id': client_id,
            'Authorization': 'Bearer '+token,
        }
    )

    data = json.loads(r.text)

    search_data = {}

    if 'error' in data.keys():
        raise ConnectionError('Got back error json. '+r.text)

    for channel in data['data']:
        search_data[channel['display_name']] = channel['id']

    return search_data


def get_stream(login_name: str, client_id: str, token: str) -> dict:
    r = requests.get(
        f'https://api.twitch.tv/helix/streams?user_login={login_name}',
        headers={
            'client-id': client_id,
            'Authorization': 'Bearer '+token,
        }
    )

    return json.loads(r.text)['data'][0]


def get_user(login_name: str, client_id: str, token: str) -> dict:
    r = requests.get(
        f'https://api.twitch.tv/helix/users?login={login_name}',
        headers={
            'client-id': client_id,
            'Authorization': 'Bearer '+token,
        }
    )

    return json.loads(r.text)['data'][0]
