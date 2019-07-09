## Day 1 - Lesson 2

## Deploy Application to Openshift/CaaS localdev

Now that the image has been saved either to the local registry or to Quay, we will push that image to Openshift and run our application. 

#### Create Application on CaaS

1. To deploy our application to the localdev instance of Openshift, we need to create a new project. 

```bash
# Create a new project to hold the app and keep things organized.
[vagrant@m1 ~]$ oc new-project springboot-hello-world
```

> NOTE: You can only create a project this way in localdev. Visit the [Ford Cloud Portal](https://www.cloudportal.ford.com/openshift) if you wish to get a project/namespace in the production instance of Openshift

2. If you are referencing in image in Quay and NOT the local docker registry, you need to first deploy your secrets to Openshift which are contained in the `pullsecret.yaml` file. These credentials are periodically changed, so please view the [pullsecret.yaml file in Github](https://github.ford.com/JPOTTE46/samples/blob/master/springboot/manifest/pullsecret.yaml) to ensure your secret matches. If not, copy and paste the new secret to your `pullsecret.yaml` file. 

```bash
[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/springboot/manifest/pullsecret.yaml
secret/devenablement-workshop-pull-secret created
```

> NOTE: If you do not create your secrets first, you will have to delete original pod(s). Existing pods will not get secrets cascaded to them

3. After deploying the secret, or if we are using a local registry, we can create our application using the `deployment.yaml` file. 

```bash
# Deploy the app.
[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/springboot/manifest/deployment.yaml
deployment.apps/springboot-hello-world created
service/springboot-hello-world created
route.route.openshift.io/springboot-hello-world created
poddisruptionbudget.policy/springboot-hello-world created
horizontalpodautoscaler.autoscaling/springboot-hello-world created

# Check for any errors.
[vagrant@m1 ~]$ oc get all -l app=springboot-hello-world
```

5. Access the Openshift Console and navigate to the springboot-hello-world application. You can select the [running pod](https://api.oc.local:8443/console/project/springboot-hello-world/browse/pods) and view the logs of the application. 

- Additionally, access the [Swagger UI](https://springboot-hello-world.app.oc.local/swagger-ui.html#/hello-controller) - in Chrome - to test the endpoint. It may take a minute for the application to build, so refresh the page to see the Swagger UI. 

<!---
The manifest created a deployment, replica set, and pod. You can get the pod IP address with the `oc describe` and curl an instance of the app with that IP address on port 8080.

```
$ oc describe pods
Name:               python-668c7fc9b-4s4pf
Namespace:          python
...
...
Start Time:         Mon, 25 Feb 2019 21:09:38 +0000
Annotations:        openshift.io/scc=restricted
Status:             Running
IP:                 10.131.80.60 <--------------------- IP of the python app
Controlled By:      ReplicaSet/python-668c7fc9b

$ curl --head 10.131.80.60:8080
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 65
Server: Werkzeug/0.14.1 Python/2.7.13
Date: Mon, 25 Feb 2019 21:18:47 GMT
```

The app manifest also created a service in front of the pod. You can get the service IP address with `oc describe` and curl the service.

```
$ oc describe services
Name:              python
Namespace:         python
Labels:            app=python
Annotations:       <none>
Selector:          app=python
Type:              ClusterIP
IP:                172.30.112.202 <---------- The service IP
Port:              http  8080/TCP <---------- The service port
TargetPort:        8080/TCP
Endpoints:         10.131.80.60:8080 <------- Here's the backend IP again
Session Affinity:  None
Events:            <none>

$ curl --head 172.30.112.202:8080
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 65
Server: Werkzeug/0.14.1 Python/2.7.13
Date: Mon, 25 Feb 2019 21:24:09 GMT
```
-->

6. The app manifest created a route object in front of the app. Show the route address with `oc get`.

```bash
[vagrant@m1 ~]$ oc get routes
NAME                    HOST/PORT                            PATH    SERVICES                 PORT   TERMINATION    WILDCARD
springboot-hello-world  springboot-hello-world.app.oc.local          springboot-hello-world   8080   edge/Redirect  None
```

7. Curl the route as a test to see that the app is reachable. For example:

```bash
curl --head --insecure --location springboot-hello-world.app.oc.local/api/v1/hello

HTTP/1.1 302 Found
Cache-Control: no-cache
Content-length: 0
Location: https://springboot-hello-world.app.oc.local/api/v1/hello

HTTP/1.1 200
X-Request-Info: timestamp=1559133674; execution=1;
X-Application-Info: name=${spring.application.name}; version=unspecified;
...
Content-Length: 44
Date: Wed, 29 May 2019 12:41:14 GMT
Set-Cookie: 4f939fb11c90700077a542505da8476d=b79c4b7022647a05b55da5ac3545ec80; path=/; HttpOnly; Secure
```

There is a good bit going on with that curl command above; `--head` sends an HTTP HEAD instead of a GET (don't send back a body), `--insecure` is necessary on localdev because the certificate that is returned is self-signed (this will not be the case in Ford's production CaaS), `--location` causes curl to follow redirects and in this case an initial, unencrypted call is being redirected to HTTPS.

8. Feel free to view all of the objects associated with the app with `oc get` or use `oc describe` to review them in detail.

```bash
# List objects with label app=springboot-hello-world
oc get all -l app=springboot-hello-world
```

9. Now, delete all of the Openshift objects. 

```bash
# Delete all objects with the springboot-hello-world label
oc delete -f /home/vagrant/containers/springboot/manifest/deployment.yaml
```
---  

Continue to [Lesson 2.5](./lesson2.5.md).

Return to [Table of Contents](https://github.ford.com/DevEnablement/caas-workshop/tree/workshop-reformat#agenda)