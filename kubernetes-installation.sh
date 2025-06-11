#!/bin/bash

kubernetes_installation(){
PATCH_PORT=15000
KUBERNETES_VARIANT=k3s
URL=https://get.$KUBERNETES_VARIANT.io | sh -
curl $URL
}

kubernetes_patches(){
sudo kubectl patch svc traefik -n kube-system   --type='json'   -p='[{"op": "replace", "path": "/spec/ports/0/port", "value": '$PATCH_PORT'}]'
sudo kubectl apply -n portainer -f https://downloads.portainer.io/ce-lts/portainer.yaml
}

kubernetes_installation
kubernetes_patches
