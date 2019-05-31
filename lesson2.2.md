# Lesson 2, Running Apps in CaaS

### Deploy Application to CaaS localdev

In this lesson, you will deploy the container image that you built to CaaS localdev and run it. These instructions deploy the container to CaaS localdev on your workstation, but you could just as easily deploy the image to Ford's CaaS production instance.

#### Background on CaaS manifest files

The Spring sample app has a CaaS manifest file at [`manifest/deployment.yaml`](https://github.ford.com/JPOTTE46/samples/blob/master/springboot/manifest/deployment.yaml). The file is a configuration for how OpenShift should run the app and defines the app's OpenShift objects to be created. Feel free to review the manifest using the link above, a text editor, or in the terminal with `cat /home/vagrant/containers/springboot/manifest/deployment.yaml`. You can learn more about [objects](https://docs.openshift.com/container-platform/3.11/architecture/core_concepts/index.html#architecture-core-concepts-index) and [manifests](https://docs.openshift.com/container-platform/3.11/dev_guide/templates.html) in the OpenShift [Dev Guide](https://docs.openshift.com/container-platform/3.11/dev_guide/index.html).

The Spring sample app's manifest defines 5 kinds of OpenShift objects.

- Deployment
- Service
- Route
- PodDisruptionBudget
- HorizontalPodAutoscaler

In the Deployment object, you can define your app containers compute resources. Review the documentation on [compute resources](https://docs.openshift.com/container-platform/3.11/dev_guide/compute_resources.html#dev-compute-resources) in the OpenShift Dev Guide. In this object, you can also define probes to check the health of your app container. Review the documentation on [application health](https://docs.openshift.com/container-platform/3.11/dev_guide/application_health.html) in the OpenShift Dev Guide.

The Service object configures an internal load balancer that will load balance traffic across multiple instances of your app container. The service object will be dynamically assigned an IP address and will proxy traffic to the app container. Review the documentation on [services](https://docs.openshift.com/container-platform/3.11/architecture/core_concepts/pods_and_services.html#services) in the OpenShift Dev Guide.

The Route object configures a host name that is associated with the Service object allowing external clients to reach your app container through a URL. Review the documentation on [routes](https://docs.openshift.com/container-platform/3.11/architecture/networking/routes.html) in the OpenShift Dev Guide.

The PodDisruptionBudget object ensures that OpenShift will maintain a minimum number of app instances during platform maintenance events. Review the documentation on [disruption budgets](https://docs.openshift.com/container-platform/3.11/admin_guide/managing_pods.html#managing-pods-poddisruptionbudget) in the OpenShift Dev Guide.

The HorizontalPodAutoscaler object configures OpenShift to automatically increase and decrease the number of app instances based on CPU utilization. Review the documentation on [autoscaler](https://docs.openshift.com/container-platform/3.11/dev_guide/pod_autoscaling.html) in the OpenShift Dev Guide.


#### Exercise

Ensure you have your image already built before moving on. If you destroyed the VM or powered off your PC, you might have to run the build script again. 
```bash
[vagrant@m1 ~]$ sudo podman images | grep springboot-hello-world -c
1

#If this is 0, you must run the build script again

[vagrant@m1 ~]$ /home/vagrant/containers/springboot/image/build.sh
```

#### Push container image to local registry

To keep this example simple and running locally, CaaS localdev is configured to pull the app's container image from a locally running Docker image registry included with localdev. You could similarly host the image on Ford's [image registry](https://registry.ford.com).

So push a copy of the container image you previously built (which was saved in the local Buildah/Podman registry) to the local Docker image registry. For example:

```bash
sudo podman push \
    registry.ford.com/devenablement/springboot-hello-world:0.0.1 \
    docker-daemon:registry.ford.com/devenablement/springboot-hello-world:0.0.1

Getting image source signatures
Copying blob sha256:050c734bd2868bcd3b69ab0ca033aa3bc95a00a4a1e5317e732394e1c36ef59e
 203.90 MB / 203.90 MB [====================================================] 2s
 ...
Writing manifest to image destination
Storing signatures
```

You can confirm that the localdev docker registry now contains the `registry.ford.com/devenablement/springboot-hello-world` image.

```bash
docker images

REPOSITORY                                                TAG      IMAGE ID        CREATED          SIZE
registry.ford.com/devenablement/springboot-hello-world    0.0.1    a88663823aa4    11 minutes ago   506 MB
```

#### Create app on CaaS

Now deploy the app to the localdev instance of CaaS by referencing its manifest. For example:

```bash
# Create a new project to hold the app and keep things organized.
oc new-project springboot-hello-world

# Deploy the app.
oc create -f /home/vagrant/containers/springboot/manifest/deployment.yaml

# Check for any errors.
oc get all -l app=springboot-hello-world
```

Access the [Swagger UI](https://springboot-hello-world.app.oc.local/swagger-ui.html#/hello-controller) - in Chrome - to test the endpoint. It may take a minute for the app to build, so refresh the page to see the Swagger UI. 

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

The app manifest created a route object in front of the app. Show the route address with `oc get`.

```bash
[vagrant@m1 ~]$ oc get routes
NAME                    HOST/PORT                            PATH    SERVICES                 PORT   TERMINATION    WILDCARD
springboot-hello-world  springboot-hello-world.app.oc.local          springboot-hello-world   8080   edge/Redirect  None
```

Then curl the route as a test to see that the app is reachable. For example:

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

Feel free to view all of the objects associated with the app with `oc get` or use `oc describe` to review them in detail.

```bash
# List objects with label app=springboot-hello-world
oc get all -l app=springboot-hello-world

# Delete all objects with the springboot-hello-world label
oc delete all -l app=springboot-hello-world
```

---  

Continue to [Lesson 2.3](./lesson2.3.md).