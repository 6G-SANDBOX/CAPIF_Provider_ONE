import requests 
import json
import os

class CaOps():
    def get_ca_root(self):
        easy_rsa_hostname = os.getenv('EASY_RSA_HOSTNAME')
        url = f"http://{easy_rsa_hostname}:8083/ca-root"

        headers = {

            'Content-Type': "application/json"
        }
        response = requests.request("GET", url, headers=headers)
        response_payload = json.loads(response.text)

        cert = response_payload["certificate"]
        ca_root_file = open('certs/ca.crt', 'wb+')
        ca_root_file.write(bytes(cert, 'utf8'))
        ca_root_file.close()