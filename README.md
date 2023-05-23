# CAPIF_Provider_ONE

This is the implementation of a Provider (AEF) for the Opennebula service

## Prerequisites
Before executing the following code it is necessary to have raised an instance of [CAPIF](https://github.com/EVOLVED-5G/CAPIF_API_Services).

## Set Up
This repo is designed to be executed from docker, to create the images and raise the instance it is only necessary to execute the following command:
```
./run.sh

```

- Before executing the run.sh command, note that it supports one parameter, this parameter is the CAPIF hostname, by default this field is 'capifcore'. Modify it if necessary or add the hostname when executing the run.sh command

    ```
    ./run.sh <other_hostname>

    ```

- It is important to have the following environment variables in the docker-compose file:
    ```
   - REGISTER_HOSTNAME = register
   - EASY_RSA_HOSTNAME = easy-rsa
   - CAPIF_PORT=8080
   - EASY_RSA_PORT=8083
   - REGISTER_PORT=8084

   extra_hosts:
      - host.docker.internal:host-gateway
      - capifcore:host-gateway
      - register:host-gateway
      - easy-rsa:host-gateway

    ```
    These environment variables refer to the certificate signing and registration services. By default, these are the ports and names that the CAPIF script uses when launching the different services. If during the deployment of CAPIF you modify these parameters, you must modify them so that they correspond to the new ones.

    If the hostname environment variables are modified, the extra host must also be modified so that the hostnames correspond and be able to reach the services deployed in docker.

Now it is only necessary to enter inside the container by executing this command



```
./terminal_to_py_aef.sh

```

Once inside the container you can run the provider command GUI by running

```
./python main.py

```

## Interacting with the GUI
The provider is prepared to make the necessary previous provisions automatically.
The different .json files that must be saved in CAPIF are also added. To make the necessary provisions you just have to execute the following commands within the GUI

```
register_provider

```

```
publish_service

```
*If the first command returns a 401, it means that the token to interact the first time with CAPIF has expired, run the following command

```
provider_get_auth

```

## Run ONE Service

This service has Apified some of the functions of ONE. To start the service run the following command:

```
python service/service_oauth.py

```

The endpoints that are implemented are the following

```
/createVM [POST]

Request Body:
{
  "name": "my_vm"
}

/checkVM/<vm_id> [POST]
/removeVM/<vm_id> [POST]

```
