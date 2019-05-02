# Lesson 2, Running Apps in CaaS

### Deploy Application to CaaS localdev

In this lesson, you will deploy the container image that you built to CaaS localdev and run it. These instructions deploy the container to CaaS localdev on your workstation, but you could just as easily deploy the image to Ford's CaaS production instance.

#### Background on CaaS manifest files

The python sample app has a CaaS manifest file at `manifest/python.yml`. The file is a configuration for how OpenShift should run the app and defines the app's OpenShift resources to be created. Feel free to review the manifest for the sample app you plan to deploy in a text editor or in the terminal with `less /home/vagrant/containers/python/manifest/python.yml`. You can learn more about [resources](https://docs.openshift.com/container-platform/3.11/architecture/core_concepts/index.html#architecture-core-concepts-index) and [manifests](https://docs.openshift.com/container-platform/3.11/dev_guide/templates.html) in the OpenShift [Dev Guide](https://docs.openshift.com/container-platform/3.11/dev_guide/index.html).

The python sample app's manifest will create 5 kinds of OpenShift resources.

- Deployment
- Service
- Route
- PodDisruptionBudget
- HorizontalPodAutoscaler

#### Exercise


#### Push container image to local registry

To keep this example simple and running locally, CaaS localdev is configured to pull the app's container image from a locally running Docker image registry included with localdev. You could similarly host the image on Ford's [image registry](https://registry.ford.com).

So push a copy of the container image you previously built (which was saved in the local Buildah/Podman registry) to the local Docker image registry. For example:

```
sudo podman push \
    registry.ford.com/devenablement/python:0.0.1 \
    docker-daemon:registry.ford.com/devenablement/python:0.0.1

Getting image source signatures
Copying blob sha256:3444e243271421dbf2df714b76c0ce39daf5c2861f7761e7f03f171d4c60bf2a
 203.78 MiB / 203.78 MiB [==================================================] 5s
 ...
Writing manifest to image destination
Storing signatures
Successfully pushed registry.ford.com/devenablement/python:0.0.1@sha256:109a30737aac44e6b3a9f718d770...
```

You can confirm that the localdev docker registry now contains the `registry.ford.com/devenablement/python` image.

```
docker images

REPOSITORY                                TAG      IMAGE ID        CREATED          SIZE
registry.ford.com/devenablement/python    0.0.1    767ba4f075af    11 minutes ago   639 MB
```

#### Create app on CaaS

Now deploy the app to the localdev instance of CaaS by referencing its manifest. For example:

```
# Create a new project to hold the app and keep things organized.
oc new-project python

# Deploy the app.
oc create -f /home/vagrant/containers/python/manifest/python.yaml

# Check for any errors.
oc get all -l app=python
```
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

The app manifest created a route resource in front of the app. Show the route address with `oc get`.

```
oc get routes

NAME      HOST/PORT             PATH      SERVICES   PORT      TERMINATION     WILDCARD
python    python.app.oc.local             python     8080      edge/Redirect   None
```

Then curl the route as a test to see that the app is reachable. For example:

```
curl --head --insecure --location python.app.oc.local

HTTP/1.1 302 Found
Cache-Control: no-cache
Content-length: 0
Location: https://python.app.oc.local/

HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 65
Server: Werkzeug/0.14.1 Python/2.7.13
Date: Mon, 11 Mar 2019 21:38:10 GMT
Set-Cookie: d546a7595cc7638a3c8a0b2a8989c2e2=1dd59f720884749cfeb2b347e77de707; path=/; HttpOnly; Secure
Cache-control: private
Connection: keep-alive
```

There is a good bit going on with that curl command above; `--head` sends an HTTP HEAD instead of a GET (don't send back a body), `--insecure` is necessary on localdev because the certificate that is returned is self-signed (this will not be the case in Ford's production CaaS), `--location` causes curl to follow redirects and in this case an initial, unencrypted call is being redirected to HTTPS.

Feel free to view all of the resources associated with the app with `oc get` or use `oc describe` to review them in detail. Then you can delete the resources when you are finished.

```
# List resources with label app=python
oc get all -l app=python

# Delete all resources with label app=python when you're done.
oc delete all -l app=python
```

---  

Continue to [Lesson 2.3](./lesson2.3.md).