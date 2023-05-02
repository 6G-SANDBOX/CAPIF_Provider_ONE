#!/bin/bash

docker exec -it $(docker ps -q -f "name=one_provider_gui") bash