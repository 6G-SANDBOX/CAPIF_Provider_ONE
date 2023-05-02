
import requests
import json
import configparser
import os
from termcolor import colored

# Get environment variables


from OpenSSL.SSL import FILETYPE_PEM
from OpenSSL.crypto import (dump_certificate_request, dump_privatekey, load_publickey, PKey, TYPE_RSA, X509Req, dump_publickey)

class RegisterProvider():

    def __create_csr(self, name):

            # create public/private key
            key = PKey()
            key.generate_key(TYPE_RSA, 2048)

            # Generate CSR
            req = X509Req()
            req.get_subject().CN = name
            req.get_subject().O = 'Telefonica I+D'
            req.get_subject().C = 'ES'
            req.set_pubkey(key)
            req.sign(key, 'sha256')


            csr_request = dump_certificate_request(FILETYPE_PEM, req)

            private_key = dump_privatekey(FILETYPE_PEM, key)

            return csr_request, private_key


    def __register_api_provider_to_capif(self, capif_ip, ccf_url, access_token, log_level):

        print("Registering api provider to CAPIF")

        url = 'https://{}/{}'.format(capif_ip, ccf_url)
        json_file = open('capif_ops/config_files/api_provider_domain.json', "rb")
        payload_dict = json.load(json_file)
        payload_dict["regSec"]=access_token

        for api_func in payload_dict['apiProvFuncs']:
            public_key, private_key = self.__create_csr(api_func["apiProvFuncRole"])
            api_func["regInfo"]["apiProvPubKey"] = public_key.decode("utf-8")
            private_key_file = open("capif_ops/certs/"+api_func["apiProvFuncRole"]+"_private_key.key", 'wb+')
            private_key_file.write(bytes(private_key))
            private_key_file.close()

        payload = json.dumps(payload_dict, indent=2)

        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json'
        }



        print(colored(f"Request Body: {payload}", "yellow"))

        try:

            if log_level == "debug":
                print(colored("''''''''''REQUEST'''''''''''''''''","blue"))
                print(colored(f"Request: to {url}","blue"))
                print(colored(f"Request Headers: {headers}", "blue"))
                print(colored(f"''''''''''REQUEST'''''''''''''''''", "blue"))

            response = requests.request("POST", url, headers=headers, data=payload, verify='capif_ops/certs/ca.crt')
            response.raise_for_status()
            response_payload = json.loads(response.text)

            if log_level == "debug":
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))
                print(colored(f"Response to: {response.url}","green"))
                print(colored(f"Response Headers: {response.headers}","green"))
                print(colored(f"Response: {response.json()}","green"))
                print(colored(f"Response Status code: {response.status_code}","green"))
                print(colored("Success, registered api provider domain to CAPIF","green"))
                print(colored("''''''''''RESPONSE'''''''''''''''''","green"))

            for func_provile in response_payload["apiProvFuncs"]:
                if log_level == "debug":
                    print(func_provile['regInfo']['apiProvCert'])
                certification_file = open("capif_ops/certs/"+func_provile["apiProvFuncRole"]+'_dummy.crt', 'wb')
                certification_file.write(bytes(func_provile['regInfo']['apiProvCert'], 'utf-8'))
                certification_file.close()

            return response_payload

        except requests.exceptions.HTTPError as err:
            message = json.loads(err.response.text)
            status = err.response.status_code
            raise Exception(message, status)




    def execute_register_provider(self, log_level):

        print(log_level)
        config = configparser.ConfigParser()
        config.read('capif_ops/config_files/credentials.properties')

        capif_ip = os.getenv('CAPIF_HOSTNAME')

        with open('capif_ops/config_files/demo_values.json', 'r') as demo_file:
            demo_values = json.load(demo_file)

        try:
            if 'ccf_api_onboarding_url' in demo_values and 'providerID' in demo_values and "capif_access_token_exposer" in demo_values:

                capif_access_token = demo_values['capif_access_token_exposer']
                ccf_api_onboarding_url = demo_values['ccf_api_onboarding_url']

                response = self.__register_api_provider_to_capif(capif_ip, ccf_api_onboarding_url, capif_access_token, log_level)

                for api_prov_func in response["apiProvFuncs"]:
                    if api_prov_func["apiProvFuncRole"] == "AEF":
                        demo_values["aef_id"] = api_prov_func["apiProvFuncId"]
                    elif api_prov_func["apiProvFuncRole"] == "APF":
                        demo_values["apf_id"] = api_prov_func["apiProvFuncId"]

                api_prov_dom_id = response["apiProvDomId"]
                demo_values["api_prov_dom_id"] = api_prov_dom_id

                print(colored(f"API provider domain Id: {api_prov_dom_id}","yellow"))
                with open('capif_ops/config_files/demo_values.json', 'w') as outfile:
                    json.dump(demo_values, outfile)
        except Exception as e:
            status_code = e.args[0]
            if status_code == 403:
                print("API provider domain already registered.")
            else:
                print(e)

        return True
