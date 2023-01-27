from phew import server, connect_to_wifi
from phew.template import render_template
from phew.server import file_exists, serve_file

from secret import ssid, password
from config import name
from serial import bufferSTDIN

connect_to_wifi(ssid, password)

# Main page
@server.route("/", methods=["GET"])
def index(request):
    return render_template("index.html", name=name), 200

# Manage PC commands
@server.route("/manage", methods=["POST"])
def short(request):
    print(request.form.get("action", None))
    return "Short", 200

# Public files and 404 page
@server.catchall()
def catchall(request):
    file = "public" + request.uri
    if(file_exists(file)):
        return serve_file(file)
    
    return "Not found", 404

server.run()