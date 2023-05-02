import requests
import json
import configparser
import os
from termcolor import colored


class RemoveProvider():

    def __offboard_provider_to_capif(self, capif_ip, api_prov_dom_id, log_level):

        print("Offboarding provider to CAPIF")

        url = 'https://{}/api-provider-management/v1/registrations/{}'.format(capif_ip, api_prov_dom_id)
        
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            if log_level == "debug":
                print(colored("''''''''''REQUEST'''''''''''''''''","blue"))
                print(colored(f"Request: to {url}","blue"))
                print(colored(f"Request Headers: {headers}", "blue"))
                print(colored(f"''''''''''REQUEST'''''''''''''''''", "blue"))

            response = requests.request("DELETE", url, headers=headers, cert=('capif_ops/certs/AMF_dummy.crt', 'capif_ops/certs/AMF_private_key.key'), verify='capif_ops/certs/ca.crt')
            response.raise_for_status()

            if log_level == "debug":
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                print(colored(f"Response to: {response.url}","green"))
                print(colored(f"Response Headers: {response.headers}","green"))
                print(colored(f"Response: {response.json()}","green"))
                print(colored(f"Response Status code: {response.status_code}","green"))
                print(colored("Success, removed provider from CAPIF","green"))
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))

        except requests.exceptions.HTTPError as err:
            message = json.loads(err.response.text)
            status = err.response.status_code
            raise Exception(message, status)


    def execute_remove_provider(self, log_level):

        config = configparser.ConfigParser()
        config.read('capif_ops/config_files/credentials.properties')

        with open('capif_ops/config_files//demo_values.json', 'r') as demo_file:
            demo_values = json.load(demo_file)

        capif_ip = os.getenv('CAPIF_HOSTNAME')


        #Publish service in CAPIF
        try:
            if 'api_prov_dom_id' in demo_values:
                self.__offboard_provider_to_capif(capif_ip, demo_values['api_prov_dom_id'], log_level)
        
                print("Provider removed")
                with open('capif_ops/config_files//demo_values.json', 'w') as outfile:
                    json.dump(demo_values, outfile)
        except Exception as e:
            print(e)
        return True
