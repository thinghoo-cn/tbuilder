"""
search "python http server with basic auth"
simplified from this gist
https://gist.github.com/mauler/593caee043f5fe4623732b4db5145a82
"""

import http.server
import socketserver
import base64


def get_handler(AUTH_KEY):
    class BasicAuthHandler(http.server.SimpleHTTPRequestHandler):
        def do_HEAD(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def do_AUTHHEAD(self):
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="FileServer"')
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def do_GET(self):
            """Present frontpage with user authentication."""
            if self.headers.get("Authorization") == None:
                self.do_AUTHHEAD()
                self.wfile.write(b"no auth header received")
            elif self.headers.get("Authorization") == "Basic " + AUTH_KEY:
                super().do_GET()
            else:
                self.do_AUTHHEAD()
                self.wfile.write(self.headers.get("Authorization").encode())
                self.wfile.write(b"not authenticated")

    return BasicAuthHandler


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


def start_http(USERNAME, PASSWORD, port):
    AUTH_KEY = base64.b64encode("{}:{}".format(USERNAME, PASSWORD).encode()).decode()
    address = ("", port)

    handler = get_handler(AUTH_KEY=AUTH_KEY)
    print("server listening at", address)
    with ThreadingHTTPServer(address, handler) as httpd:
        httpd.serve_forever()
