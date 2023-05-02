from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, get_jwt
import ssl
from werkzeug import serving
import socket, ssl
import OpenSSL
from OpenSSL import crypto
import jwt
import pyone

app = Flask(__name__)

jwt_flask = JWTManager(app)


with open("capif_ops/certs/cert_server.pem", "rb") as cert_file:
            cert= cert_file.read()

crtObj = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
pubKeyObject = crtObj.get_pubkey()
pubKeyString = crypto.dump_publickey(crypto.FILETYPE_PEM,pubKeyObject)

app.config['JWT_ALGORITHM'] = 'RS256'
app.config['JWT_PUBLIC_KEY'] = pubKeyString

one = pyone.OneServer("URL", session="user:password")

@app.route("/createVM", methods=["POST"])
@jwt_required()
def vm_create():

    request_data = request.get_json()

    name_vm = request_data['name']

    vm_attrs = {
        'name': name_vm,  # the name of the new VM
        'template': 'small',  # the name or ID of the template to use for the VM
        'memory': 1024,  # the amount of memory to allocate for the VM in MB
        'cpu': 1,  # the number of CPU cores to allocate for the VM
        'vcpu': 1,  # the number of virtual CPU cores to allocate for the VM
        'disk': [
            {
                'size': 10,  # the size of the root disk in GB
                'driver': 'qcow2'  # the disk driver to use (optional)
            }
        ]
    }

    vm_id = one.vm.allocate(vm_attrs)
    return jsonify(f"Creating vm with id: {vm_id}")

@app.route("/checkVM/<vm_id>", methods=["POST"])
@jwt_required()
def vm_check(vm_id):

    vm_info = one.vm.info(vm_id)
    state = int(getattr(vm_info, 'STATE'))

    if state == 3:
        return jsonify("VM is active")
    else:
        return jsonify("VM is not active yet")

@app.route("/removeVM/<vm_id>", methods=["POST"])
@jwt_required()
def vm_remove(vm_id):

    one.vm.action("terminate-hard", vm_id)

    return jsonify("Removing VM")


if __name__ == '__main__':
    serving.run_simple("0.0.0.0", 8088, app)