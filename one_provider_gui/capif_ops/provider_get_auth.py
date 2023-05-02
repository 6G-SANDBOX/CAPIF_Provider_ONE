import requests
import json
import configparser
import os
from termcolor import colored

class PreviousAuth():

    def __get_capif_auth(self, capif_ip, capif_port, username, password):

            #print("Geting Auth to exposer")
            url = "http://{}:{}/getauth".format(capif_ip, capif_port)

            payload = dict()
            payload['username'] = username
            payload['password'] = password

            headers = {
                'Content-Type': 'application/json'
            }

            try:
                response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

                response.raise_for_status()
                response_payload = json.loads(response.text)

                return response_payload['access_token']

            except requests.exceptions.HTTPError as err:
                raise Exception(err.response.text, err.response.status_code)


    def execute_get_auth(self):

        config = configparser.ConfigParser()
        config.read('capif_ops/config_files/credentials.properties')

        username = config.get("credentials", "exposer_username")
        password = config.get("credentials", "exposer_password")

        capif_ip = os.getenv('CAPIF_HOSTNAME')
        capif_port = os.getenv('CAPIF_PORT')

        if os.path.exists("capif_ops/config_files/demo_values.json"):
            #os.remove("capif_ops/config_files/demo_values.json")
            with open('capif_ops/config_files/demo_values.json', 'r') as demo_file:
                demo_values = json.load(demo_file)
        else:
            demo_values = {}

        #First we need register exposer in CAPIF
        try:
            if 'providerID' in demo_values:
                access_token = self.__get_capif_auth(capif_ip, capif_port, username, password)
                demo_values['capif_access_token_exposer'] = access_token

            with open('capif_ops/config_files/demo_values.json', 'w') as outfile:
                json.dump(demo_values, outfile)

            print("Provider auth Success!")
        except Exception as e:
            status_code = e.args[0]
            if status_code == 409:
                print("User already registed. Continue with token request\n")
            else:
                print(e)

        return True
