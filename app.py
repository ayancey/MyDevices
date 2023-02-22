import routeros_api
from bottle import route, run, template

connection = routeros_api.RouterOsApiPool("10.45.1.1", username="admin", password="***REMOVED***", plaintext_login=True)
api = connection.get_api()


@route("/")
def index():
    return template("devices", devices=sorted(api.get_resource('/ip/dhcp-server/lease').get(), key=lambda d: d["address"]))


run(host='0.0.0.0', port=8080)
