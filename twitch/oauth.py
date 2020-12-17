import webbrowser
import requests
from http.server import SimpleHTTPRequestHandler, HTTPServer


def get_token(client_id: str) -> str:
    """Return a user token.

    First, we send the user to a webpage for them to login to Twitch and
    authorize our access. Then, we host a http server (from http.server from
    the standard library) and wait for a redirect to localhost:8080.
    The web browser gets some javascript to give us the token.
    At that point, a message appears telling the user to close their
    web browser.

    Paremeters:
        client_id (str): The client id to your twitch application.

    Returns:
        str: This is the OAuth/Bearer token Twitch gave you.
    """

    class CustomHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()

            if self.path == '/':
                self.wfile.write(b'<script>document.location.href = "http://localhost:8080/" + document.location.hash.split("#access_token=")[1].split("&")[0]</script>')

            else:
                self.server.token = self.path[1:]
                self.wfile.write(b'<h1>You may close the window now.</h1>')

    class CustomServer(HTTPServer):
        token = None

    url = 'https://id.twitch.tv/oauth2/authorize?client_id={}&redirect_uri=http://localhost:8080&response_type=token&scope='

    webbrowser.open(url.format(client_id))
    with CustomServer(('localhost', 8080), CustomHandler) as httpd:
        while httpd.token is None:
            httpd.handle_request()
        return httpd.token


# Checks if an access token is valid
def check_token(token: str) -> bool:
    """Check if a token is valid.

    Parameters:
        token (str): The OAuth token you want to check is valid.

    Returns:
        bool: Whether or not that token was valid.
    """

    return requests.get('https://id.twitch.tv/oauth2/validate',
                        headers={'Authorization': f'OAuth {token}'}
                        ).status_code == 200


# Revokes an access token
def revoke_token(client_id: str, token: str):
    """Revoke a token.

    Parameters:
        client_id (str): The client id of your Twitch application
        token (str): The token you wish to revoke
    """

    requests.post(f'https://id.twitch.tv/oauth2/revoke?client_id={client_id}&token={token}')
