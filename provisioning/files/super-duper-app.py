#!/usr/bin/env python
import socket
import BaseHTTPServer

class MyAppsHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        """ Respond to a GET request. """
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

        myhost = socket.gethostname()

        s.wfile.write("<html><head><title>My super duper app.</title></head>")
        s.wfile.write("<body><p>Hi there, I'm served from {host}.</p>".format(host=myhost))
        s.wfile.write("</body></html>")

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(('', 8080), MyAppsHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
