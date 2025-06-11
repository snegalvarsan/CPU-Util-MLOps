#!/bin/bash

sudo docker save flask-app-flask:latest -o flask-app.tar
sudo kubectl label node $(hostname) kubernetes.io/hostname=homeserv
sudo ctr image import flask-app.tar
sudo kubectl apply -f ~/MLopsDir/manifests/postgres/
sudo kubectl apply -f ~/MLopsDir/manifests/flask-app
