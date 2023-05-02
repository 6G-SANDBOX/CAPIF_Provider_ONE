import requests
import json
import configparser
import os
from termcolor import colored


class PublishService():

    def __publish_service_api_to_capif(self, capif_ip, apf_id, aef_id, log_level):

        print("Publishing api service to CAPIF")

        url = 'https://{}/published-apis/v1/{}/service-apis'.format(capif_ip, apf_id)
        payload = open('capif_ops/config_files/service_api_description_one.json', 'rb')
        payload_dict = json.load(payload)
        for profile in payload_dict["aefProfiles"]:
            profile["aefId"] = aef_id

        headers = {
            'Content-Type': 'application/json'
        }

        payload = json.dumps(payload_dict, indent=2)
        print(colored(f"Request Body: {payload}", "yellow"))

        try:
            if log_level == "debug":
                print(colored("''''''''''REQUEST'''''''''''''''''","blue"))
                print(colored(f"Request: to {url}","blue"))
                print(colored(f"Request Headers: {headers}", "blue"))
                print(colored(f"''''''''''REQUEST'''''''''''''''''", "blue"))

            response = requests.request("POST", url, headers=headers, data=json.dumps(payload_dict), cert=('capif_ops/certs/APF_dummy.crt', 'capif_ops/certs/APF_private_key.key'), verify='capif_ops/certs/ca.crt')
            response.raise_for_status()
            response_payload = json.loads(response.text)


            if log_level == "debug":
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                print(colored(f"Response to: {response.url}","green"))
                print(colored(f"Response Headers: {response.headers}","green"))
                print(colored(f"Response: {response.json()}","green"))
                print(colored(f"Response Status code: {response.status_code}","green"))
                print(colored("Success, registered api service to CAPIF","green"))
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
            return response_payload['apiId']
        except requests.exceptions.HTTPError as err:
            message = json.loads(err.response.text)
            status = err.response.status_code
            raise Exception(message, status)


    def execute_publish(self, log_level):

        config = configparser.ConfigParser()
        config.read('capif_ops/config_files/credentials.properties')

        with open('capif_ops/config_files//demo_values.json', 'r') as demo_file:
            demo_values = json.load(demo_file)

        capif_ip = os.getenv('CAPIF_HOSTNAME')


        #Publish service in CAPIF
        try:
            if 'apf_id' in demo_values:
                service_api_id = self.__publish_service_api_to_capif(capif_ip, demo_values['apf_id'], demo_values['aef_id'], log_level)

                demo_values['service_api_id']= service_api_id
                print("Service Api Id: {}".format(service_api_id))
                with open('capif_ops/config_files/demo_values.json', 'w') as outfile:
                    json.dump(demo_values, outfile)
        except Exception as e:
            print(e)
        return True
