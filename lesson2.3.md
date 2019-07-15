## Day 1 - Lesson 2

## Push Container Image to Image Registry

In this lesson, you will learn take the image that you built in [Lesson 1.4](./lesson1.4.md) and push that image to Ford's container registry - Quay. There are also instructions for how to push the image to the local Docker registry. 

#### Exercise

<!--
Ensure you have your image already built before moving on. If you destroyed the VM or powered off your PC, you might have to run the build script again. 
```bash
[vagrant@m1 ~]$ sudo podman images | grep -E 'springboot-hello-world.*0.0.1' -c
1

#If this is 0, you must run the build script again
[vagrant@m1 ~]$ /home/vagrant/containers/springboot/image/build.sh
```
-->

<!--
#### Push container image to local registry

To keep this example simple and running locally, CaaS localdev is configured to pull the app's container image from a locally running Docker image registry included with localdev. You could similarly host the image on Ford's [image registry](https://registry.ford.com).

So push a copy of the container image you previously built (which was saved in the local Buildah/Podman registry) to the local Docker image registry. For example:

```bash
sudo podman push \
    springboot-hello-world:0.0.1 \
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
-->

#### Push Container to Quay or Local Registry

If you are following this guide as part of the workshop, we will push the image we created to the DevEnablement organization in Quay. If you are following this workshop on your own, you will push the container image to the local registry (docker-daemon). 

Recall in the `build.sh` script, we defined the IMAGE_NAME to be `springboot-hello-world` and the VERSION to be `0.0.1`. Normally, you would change these values in `build.sh` to match the repository you will push to in Quay. For the purposes of the workshop, however, we will push the image to the `workshop` repository in the `devenablement` organization, and you will use a version number assigned to you.

[Click here](https://gist.github.ford.com/JPOTTE46/388b8eb535811c9e98ccae7aeb0e3d22) to copy the command to login with the Quay credentials provided to you for the workshop. 

```bash
# Pushing the container to Quay
# The command below is just an example - copy the actual command from the link above
[vagrant@m1 ~]$ sudo podman login -u="USERNAME" -p="PASSWORD" registry.ford.com

# Push your image to Quay using your version number
[vagrant@m1 ~]$ sudo podman push \
                    springboot-hello-world:0.0.1 \
                    registry.ford.com/devenablement/workshop:YOUR_VERSION_NUMBER
```

If you are follwing this outside of the workshop and do not have credentials to Quay, push the image to your local Docker registry. 

```bash
# Pushing the container to local registry
sudo podman push \
    springboot-hello-world:0.0.1 \
    docker-daemon:registry.ford.com/devenablement/workshop:0.0.1

Getting image source signatures
Copying blob sha256:050c734bd2868bcd3b69ab0ca033aa3bc95a00a4a1e5317e732394e1c36ef59e
 203.90 MB / 203.90 MB [====================================================] 2s
 ...
Writing manifest to image destination
Storing signatures
```

#### Update deployment.yaml

In the `sample/springboot/manifest/deployment.yaml` file, there is a reference to the image at line 59. 

```yaml
containers:
      - name: springboot-hello-world
        # image will be pulled from localdev Docker Registry if present
        image: registry.ford.com/devenablement/workshop:0.0.1 # <---------- Update version here
        imagePullPolicy: IfNotPresent
```

If the image referenced here is located in the local docker registry, then that image will be used when deploying to Openshift. Looking at the command for pushing the image to the local docker registry, we can see we have named it `registry.ford.com/devenablement/workshop:0.0.1`, so no changes are needed to the `deployment.yaml` file.

However, if there is no image in the local registry, Openshift will attempt to access the image located at the location provided, which in this case, is `registry.ford.com/devenablement/workshop:0.0.1`. You will need to update this to reflect the name of the image you pushed to Quay by changing the version number `0.0.1` to your version number and save the change.

<!--

#### Create app on CaaS

Now deploy the app to the localdev instance of CaaS. First we need to creat a new project. 

```bash
# Create a new project to hold the app and keep things organized.
oc new-project springboot-hello-world
```

If you are referencing in image in Quay and not the local docker registry, you need to first deploy your secrets to Openshift which are contained in the [pullsecret.yaml]() file. 

```bash
oc create -f /home/vagrant/containers/springboot/manifest/pullsecret.yaml
```

```bash
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

<!--
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
-->
---  

Continue to [Lesson 2.4](./lesson2.4.md).

Return to [Table of Contents](https://github.ford.com/DevEnablement/caas-workshop/tree/workshop-reformat#agenda)