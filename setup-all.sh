#!/bin/bash

SLEEP_TIME=20

general_setup(){
 sh $HOME/installation-setup.sh
 sh $HOME/kubernetes-installation.sh
 cd $HOME/MLopsDir/PostgresContainer/
 sudo docker compose up -d
 cd $HOME/MLopsDir/Flask-App
 sudo docker compose up -d
 sleep $SLEEP_TIME
 sudo docker compose down
}

deployment(){
 cd $HOME
 sh $HOME/deploy.sh
}

kubectl_commands(){
 sudo kubectl get pods
 sudo kubectl get nodes
 sudo kubectl get svc -A
 sudo kubectl get pvc -A
}

general_setup
deployment
kubectl_commands
