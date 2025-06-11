#!/bin/bash

docker_keyring_setup(){
 sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor --yes -o /usr/share/keyrings/docker-archive-keyring.gpg
 echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
}

docker_installation(){
 sudo apt update -y
 sudo apt install -y docker-ce docker-ce-cli containerd.io
}

docker_enable(){
 sudo systemctl start docker
 sudo systemctl enable docker
}

docker_check_status(){
 sudo docker --version
 sudo usermod -aG docker $USER
}

docker_keyring_setup
docker_installation
docker_enable
docker_check_status
