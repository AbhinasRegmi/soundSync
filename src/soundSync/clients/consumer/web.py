"""
We will search for the template file index.html inside templates directory.
And serve the file with http.
If the file doesn't exits error will be raised.
"""

import os
import webbrowser
from pathlib import Path
from soundSync.config import settings
from http.server import SimpleHTTPRequestHandler, HTTPServer

root_path = Path(__file__).resolve().parent

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:

        if self.path == '/':
            self.path = '/templates/'

            if os.path.exists(os.path.join("templates", "index.html")):
                return super().do_GET()
        
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'404 NOT FOUND')


def start_web_server(open_browser: bool = True) -> None:
    """
    This server doesn't support static files. 
    All css and js should be inside the html file.
    """
    server_address = ('', settings.WEB_HTTP_PORT)
    httpd = HTTPServer(server_address, CustomRequestHandler)

    print(f"Server started: http://{settings.WEB_HTTP_FULL_URL}")
    if open_browser:
        webbrowser.open(settings.WEB_HTTP_FULL_URL)

    httpd.serve_forever()


if __name__ == "__main__":
    start_web_server()