from phew import server, connect_to_wifi
from phew.template import render_template
from phew.server import serve_file

from secret import ssid, password
from config import name

connect_to_wifi(ssid, password)

@server.route("/", methods=["GET"])
def index(request):
    return render_template("index.html", name=name), 200

@server.route("/style.css", methods=["GET"])
def index(request):
    return serve_file("style.css")

@server.route("/favicon.ico", methods=["GET"])
def index(request):
    return serve_file("favicon.ico")

@server.catchall()
def catchall(request):
  return "Not found", 404

server.run()