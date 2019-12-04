## Deploy Application to Openshift/CaaS localdev

### The Big Picture - Step 4

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

Now that the image has been saved either to the local registry or to Quay, we will push that image to Openshift and run our application. 

#### Create Application on CaaS

1. If you are referencing an image in Quay and NOT the local docker registry, you need to first deploy your secrets to Openshift which are contained in the `pullsecret.yaml` file. These credentials are periodically changed, so please view the [pullsecret.yaml file in Github](https://github.ford.com/JPOTTE46/samples/blob/master/springboot/manifest/pullsecret.yaml) to ensure your secret matches. If not, copy and paste the new secret to your `pullsecret.yaml` file. 

```bash
[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/springboot/manifest/pullsecret.yaml
secret/devenablement-workshop-pull-secret created
```

- Do not retain secrets locally or in version control (i.e on github or accurev). Delete these files on your machine after deploying them. 
- You must deploy secrets before pod creation. Pods **CANNOT** dynamically retrieve secrets - the secrets must exist in your namespace before pod creation. 

2. After deploying the secret, or if we are using a local registry, we can create our application using the `deployment-1.yaml` file. 

```bash
# Deploy the app.
[vagrant@m1 ~]$ oc create -f /home/vagrant/containers/springboot/manifest/deployment-1.yaml
deployment.apps/springboot-hello-world created
service/springboot-hello-world created
route.route.openshift.io/springboot-hello-world created
poddisruptionbudget.policy/springboot-hello-world created
horizontalpodautoscaler.autoscaling/springboot-hello-world created
```

3. Access the Openshift Console and navigate to the springboot-hello-world application. You can select the [running pod](https://api.oc.local:8443/console/project/my-namespace/browse/pods) and view the logs of the application. 

4. You can view individual components of your application in the console or use the [oc CLI](https://docs.openshift.com/container-platform/3.11/cli_reference/basic_cli_operations.html). For example, `oc get` or `oc describe` commands will return information about the objects you choose. Run the `oc get` command below to get all the Openshift objects that have a label `app` with a value of `springboot-hello-world`. 

```bash
[vagrant@m1 ~]$ oc get all -l app=springboot-hello-world
```

5. View the [application's endpoint](https://springboot-hello-world.app.oc.local/api/v1/hello) to check that the app is up and running. You can also run a curl command to check its status. 

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

You will notice the curl goes from a 302 to a 200. Recall our route object defined an `insecureEdgeTerminationPolicy` with a value of `Redirect` (line 160 of `deployment-1.yaml`). This curl shows the redirect. If we changed the value of `Redirect` to `Allow`, the HTTP traffic will be allowed, and curling the endpoint would immediately return a 200 status code with no redirect occurring. 

<!--
4. The app manifest created a route object in front of the app. Show the route address with `oc get`.

```bash
[vagrant@m1 ~]$ oc get routes
NAME                    HOST/PORT                            PATH    SERVICES                 PORT   TERMINATION    WILDCARD
springboot-hello-world  springboot-hello-world.app.oc.local          springboot-hello-world   8080   edge/Redirect  None
```

5. Curl the route as a test to see that the app is reachable. For example:

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

6. Feel free to view all of the objects associated with the app with `oc get` or use `oc describe` to review them in detail.

```bash
# List objects with label app=springboot-hello-world
oc get all -l app=springboot-hello-world
```
-->
---  

Continue to [an Overview of Volumes](./10-VolumesIntro.md).

Return to [Table of Contents](../README.md#agenda)