from http.server import HTTPServer, CGIHTTPRequestHandler
import webbrowser

server_address = ("", 8000)
httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
webbrowser.open('http://localhost:8000/cgi-bin/wall.py')
httpd.serve_forever()
