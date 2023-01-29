# Phew web server imports
from phew import server, connect_to_wifi
from phew.template import render_template
from phew.server import file_exists, serve_file

# Info required for connecting and hosting web server
from web.secret import ssid, password
from web.config import name, threads

# Main page
@server.route("/", methods=["GET"])
def index(request):
    return render_template("index.html", name=name, threads=threads), 200

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


def connectToWireless():
    connect_to_wifi(ssid, password)

def startServer():
    server.run()
