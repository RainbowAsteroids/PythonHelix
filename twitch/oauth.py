import webbrowser
import requests
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Gets an OAuth token, using an implementation of implicit code OAuth
def get_token(client_id: str) -> str:
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
        while httpd.token == None: httpd.handle_request()
        return httpd.token

# Checks if an access token is valid
def check_token(token: str) -> bool:
    return requests.get('https://id.twitch.tv/oauth2/validate', headers={'Authorization':f'OAuth {token}'}).status_code == 200

# Revokes an access token
def revoke_token(client_id: str, token: str) -> bool: 
    return requests.post(f'https://id.twitch.tv/oauth2/revoke?client_id={client_id}&token={token}').status_code == 200