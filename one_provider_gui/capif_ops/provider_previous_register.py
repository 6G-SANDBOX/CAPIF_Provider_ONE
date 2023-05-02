import requests
import json
import configparser
import os
from termcolor import colored

class PreviousRegister():

    def __register_exposer_to_capif(self, capif_ip, capif_port, username, password, role, description, cn):

            #print(colored("Registering exposer to CAPIF","yellow"))
            #url = "https://register:8084/register".format(capif_port)
            url = "http://{}:{}/register".format(capif_ip,capif_port)

            payload = dict()
            payload['username'] = username
            payload['password'] = password
            payload['role'] = role
            payload['description'] = description
            payload['cn'] = cn

            headers = {
                'Content-Type': 'application/json'
            }

            try:
                # print(colored("''''''''''REQUEST'''''''''''''''''","blue"))
                # print(colored(f"Request: to {url}","blue"))
                # print(colored(f"Request Headers: {headers}", "blue"))
                # print(colored(f"Request Body: {json.dumps(payload)}", "blue"))
                # print(colored(f"''''''''''REQUEST'''''''''''''''''", "blue"))

                response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)
                response.raise_for_status()
                response_payload = json.loads(response.text)

                # print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                # print(colored(f"Response to: {response.url}","green"))
                # print(colored(f"Response Headers: {response.headers}","green"))
                # print(colored(f"Response: {response.json()}","green"))
                # print(colored(f"Response Status code: {response.status_code}","green"))
                # print(colored("Success to register new exposer","green"))
                # print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                return response_payload['id'], response_payload['ccf_publish_url'], response_payload['ccf_api_onboarding_url']
            except requests.exceptions.HTTPError as err:
                raise Exception(err.response.status_code)


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
                # print("''''''''''REQUEST'''''''''''''''''")
                # print("Request: to ",url) 
                # print("Request Headers: ",  headers) 
                # print("Request Body: ", json.dumps(payload))
                # print("''''''''''REQUEST'''''''''''''''''")

                response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)

                response.raise_for_status()
                response_payload = json.loads(response.text)

                # print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                # print(colored(f"Response to: {response.url}","green"))
                # print(colored(f"Response Headers: {response.headers}","green"))
                # print(colored(f"Response: {response.json()}","green"))
                # print(colored(f"Response Status code: {response.status_code}","green"))
                # print(colored("Get AUTH Success. Received access token", "green"))
                # print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                return response_payload['access_token']

            except requests.exceptions.HTTPError as err:
                raise Exception(err.response.text, err.response.status_code)


    def execute_previous_register_provider(self):

        config = configparser.ConfigParser()
        config.read('capif_ops/config_files/credentials.properties')

        username = config.get("credentials", "exposer_username")
        password = config.get("credentials", "exposer_password")
        role = config.get("credentials", "exposer_role")
        description = config.get("credentials", "exposer_description")
        cn = config.get("credentials", "exposer_cn")

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
            providerID, ccf_publish_url, ccf_api_onboarding_url = self.__register_exposer_to_capif(capif_ip, capif_port, username, password, role, description,cn)
            demo_values['providerID'] = providerID
            demo_values['ccf_publish_url']= ccf_publish_url
            demo_values['ccf_api_onboarding_url']= ccf_api_onboarding_url
            #print("provider ID: {}".format(providerID))

            with open('capif_ops/config_files/demo_values.json', 'w') as outfile:
                json.dump(demo_values, outfile)

            if 'providerID' in demo_values:
                access_token = self.__get_capif_auth(capif_ip, capif_port, username, password)
                demo_values['capif_access_token_exposer'] = access_token

            with open('capif_ops/config_files/demo_values.json', 'w') as outfile:
                json.dump(demo_values, outfile)
        except Exception as e:
            status_code = e.args[0]
            if status_code == 409:
                print()
            else:
                print(e)

        return True
