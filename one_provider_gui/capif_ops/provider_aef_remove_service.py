import requests
import json
import configparser
import os
from termcolor import colored


class RemoveService():

    def __remove_service_api_to_capif(self, capif_ip, apf_id, service_api_id, log_level):

        print("Removing api service from CAPIF")

        url = 'https://{}/published-apis/v1/{}/service-apis/{}'.format(capif_ip, apf_id, service_api_id)

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            if log_level == "debug":
                print(colored("''''''''''REQUEST'''''''''''''''''","blue"))
                print(colored(f"Request: to {url}","blue"))
                print(colored(f"Request Headers: {headers}", "blue"))
                print(colored(f"''''''''''REQUEST'''''''''''''''''", "blue"))

            response = requests.request("DELETE", url, headers=headers, cert=('capif_ops/certs/APF_dummy.crt', 'capif_ops/certs/APF_private_key.key'), verify='capif_ops/certs/ca.crt')
            response.raise_for_status()


            if log_level == "debug":
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                print(colored(f"Response to: {response.url}","green"))
                print(colored(f"Response Headers: {response.headers}","green"))
                print(colored(f"Response: {response.json()}","green"))
                print(colored(f"Response Status code: {response.status_code}","green"))
                print(colored("Success, remove api service from CAPIF","green"))
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))

        except requests.exceptions.HTTPError as err:
            message = json.loads(err.response.text)
            status = err.response.status_code
            raise Exception(message, status)


    def execute_remove(self, log_level):

        config = configparser.ConfigParser()
        config.read('capif_ops/config_files/credentials.properties')

        with open('capif_ops/config_files//demo_values.json', 'r') as demo_file:
            demo_values = json.load(demo_file)

        capif_ip = os.getenv('CAPIF_HOSTNAME')


        #Publish service in CAPIF
        try:
            self.__remove_service_api_to_capif(capif_ip, demo_values['apf_id'], demo_values["service_api_id"], log_level)

            with open('capif_ops/config_files//demo_values.json', 'w') as outfile:
                json.dump(demo_values, outfile)

            print("Service Api Id: {}, removed".format(demo_values["service_api_id"]))
            demo_values.pop("service_api_id")


        except Exception as e:
            print(e)
        return True
