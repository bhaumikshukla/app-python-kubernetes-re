# Python Application with Kubernetes

## App
Developed a simple python based application using Flask. It is connecting to mysql database and returning the records in json format as response.

Application performs:
- REST Endpoint at `/guests ` and returns the following output everytime after reading from database

`GET /guests`

```
[
    {
        "email": "unnati@def.com",
        "firstname": "Unnati",
        "lastname": "Shukla"
    },
    {
        "email": "bhaumik@def.com",
        "firstname": "Bhaumik",
        "lastname": "Shukla"
    }
]
```

## Components
There are the components included in the solution
- Python
- Mysql
- Minikube & Kubectl
- Docker
- Helm


## What the solution includes
- Choose Flask on Python for its simplicity for building REST API
- Using MySQL as database, loading initital data from ConfigMap and attached a PVC (500mb)
- Kubernetes YAML files are located in “deployments directory”
- Helm Chart is located as under “deployments/helm” directory
- Using K8S secret to store database credentials.

## STEPS
### Installation
I've prepared the helm chart. it will be easy for you to install and run the application which start communicating with DB. Helm has not any hardcoded secrets for DB. 

#### Setup minikube. [Guide](https://minikube.sigs.k8s.io/docs/start/)
```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
``` 



#### Install helm
```
brew install helm
````

## Run instructions

First you need to clone the repository

```
git clone https://github.com/bhaumikshukla/app-python-kubernetes-re.git
```

Start minikube
```
minikube start --vm=true --driver=hyperkit
```

Enable ingress
```
minikube addons enable ingress
```

### Create a secret
``` 
kubectl create secret generic mysql-pass --from-literal=password='my_secret_pw'
```


### Run the Helm
```
helm install example ./helm --set app.host=<fqdn> --set app.db_pw_secret=mysql-pass
```          
OR
```
cd deployments
helm install example ./helm  -f helm/values.yaml
```


## Usage

Feel free to use the postman to check the  endpoint `/guests` is running. Make sure to take care about mentioning `host` in Header of the request.

Get the IP address to request
```
kubectl get ing
```

This will show the IP address of the Ingress
example:
```
NAME          CLASS    HOSTS             ADDRESS        PORTS   AGE
api-ingress   <none>   api.bshukla.com   192.168.64.2   80      14h
```

Sample Request:
```
curl --location --request GET 'http://192.168.64.2/guests' \
--header 'Host: api.bshukla.com'
```

Response I receive is:
```
[
    {
        "email": "unnati@def.com",
        "firstname": "Unnati",
        "lastname": "Shukla"
    },
    {
        "email": "bhaumik@def.com",
        "firstname": "Bhaumik",
        "lastname": "Shukla"
    }
]
```
