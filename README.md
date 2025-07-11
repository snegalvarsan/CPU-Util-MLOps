# MLOps Deployment Framework

This repository contains scripts and resources to automate the setup of a lightweight MLOps framework on an Ubuntu system. It includes tools and configurations to install Kubernetes, deploy a basic K8s dashboard, and run MLOps components like a monitoring Flask app and machine learning scripts.

## 🛠️ Setup Instructions

> **Step 1: Clone the Repository**
```bash
cd $HOME
git clone https://github.com/snegalvarsan/CPU-Util-MLOps.git
cd CPU-Util-MLOps
````

> **Step 2: Run the setup script**

```bash
sh ./setup-all.sh
```

This script performs the following:

* Installs required system packages and dependencies
* Installs Kubernetes on your local machine
* Deploys the Kubernetes dashboard
* Sets up and deploys the MLOps monitoring services

![image](https://github.com/user-attachments/assets/3f6a0b67-95c5-487a-be37-de127be2b845)
![image](https://github.com/user-attachments/assets/eba77f32-5b2e-4ff9-997d-a013798b1813)

## Prerequisites

* Ubuntu-based OS (Tested on Ubuntu 20.04+)
* Root/sudo access
* Internet connection for downloading packages.

Feel free to contribute or raise issues!


