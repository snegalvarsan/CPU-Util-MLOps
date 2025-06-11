#!/bin/bash

SLEEP_TIME=20

REPOSITORY_NAME=CPU-Util-MLOps
general_setup(){
 sh $HOME/$REPOSITORY_NAME/installation-setup.sh
 sh $HOME/$REPOSITORY_NAME/kubernetes-installation.sh
 cd $HOME/$REPOSITORY_NAME/MLopsDir/PostgresContainer/
 sudo docker compose up -d
 cd $HOME/$REPOSITORY_NAME/MLopsDir/Flask-App
 sudo docker compose up -d
 sleep $SLEEP_TIME
 sudo docker compose down
}

deployment(){
 cd $HOME/$REPOSITORY_NAME
 sh $HOME/$REPOSITORY_NAME/deploy.sh
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
