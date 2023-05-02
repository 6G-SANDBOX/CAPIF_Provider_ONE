# CAPIF_Provider_ONE

This is the implementation of a Provider (AEF) for the Opennebula service

## Prerequisites
Before executing the following code it is necessary to have raised an instance of [CAPIF](https://github.com/EVOLVED-5G/CAPIF_API_Services).

## Set Up
This repo is designed to be executed from docker, to create the images and raise the instance it is only necessary to execute the following command:
```
./run.sh

```

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
