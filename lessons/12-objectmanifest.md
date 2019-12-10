## Manifests

In this lesson, we will break down some of the other manifest files and Openshift objects talked about in the previous lesson. 

### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: <CDSID>-service
  labels:
    app: <CDSID>-deployment-config
spec:
  type: ClusterIP
  selector:
    app: <CDSID>-deployment-config
  ports:
  - protocol: "TCP"
    name: http
    port: 8080
    targetPort: 8080
```
- Define the ports you want to be accessible for your application and the protocol it will be accessed by

### Route

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  labels:
    app: <CDSID>-deployment-config
  name: <CDSID>-route
spec:
  host: <CDSID>.app.caas.ford.com
  port:
    targetPort: 8080
  tls:
    termintaion: edge
    #termination: passthrough
    insecureEdgeTerminationPolicy: Redirect
  to:
    kind: Service
    name: <CDSID>-service
    weight: 100
  wildcardPolicy: None
```
- To: Reference the service object you want to tie your route to
- TLS
  - Termination: Edge (encryption terminates at the route) or passthrough (encryption continues all the way to the Pod)
  - Termination Policy: Only allowed with edge termination. Tells Openshift whether to allow, re-direct, or disable traffic through insecure schemes (HTTP)
- Host: The URL to access your application. You can have multiple hosts for a single route object. 

### Pod Disruption Budget
```yaml
apiVersion: policy/v1beta1
kind: PodDisruptionBudget
metadata:
  labels:
    name: <CDSID>-deployment-config
  name: <CDSID>-disruption
spec:
  selector:
    app: <CDSID>-deployment-config
  minAvailable: 1
  ```
- Define the minimum available pods you want during maintenance events 

### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  labels:
    app: <CDSID>-deployment-config
  name: <CDSID>-autoscaler
spec:
  scaleTargetRef:
    apiVersion: extensions/v1beta1
    kind: DeploymentConfig
    name: <CDSID>-deployment-config
  maxReplicas: 3
  minReplicas: 1
  cpuUtilization:
    targetCPUUtilizationPercentage: 75
```
- Max Replicas: The maximum amount of replicas your application can scale up to
- Min Replicas: The minimum amount of replicas your application can scale down to 
- TargetCPUUtilization: The percentage of CPU your application must use up before it will scale up and spawn another pod

### Exercise - Deploy Route and Service

To view our running application we only need a route and a service at the moment. 

1. Open the `Route.yaml` and `Service.yaml` files. Replace any instance of `<CDSID>` with your CDSID. 

2. Create the objects: 

```bash
$ oc create -f ./manifests/service.yaml
service/<CDSID>-service created

$ oc create -f ./manifests/route.yaml
route.route.openshift.io/<CDSID>-route created
```

3. Go to the [services](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/services) section of the console and select your service. At the bottom of the page, you should see your service has identified your running pods. 

4. Go to the [routes](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/routes) section of the console and select your route.

https://MY-CDSID.app.caas.ford.com/

We now have a fully running application that is accessible via a route and service that handles load balancing. 

### Best Practices for CaaS Manifests

Through the CaaS manifest you have significant control over how CaaS will run your application. App teams can define, test, and revise the resources allocation to an application without any action from an operations team.

In this workshop, all these Openshift objects have been combined in one manifest. You might find it more practical to separate these into separate manifests (i.e. deployment.yaml, service.yaml, route.yaml, etc). This might be a better option for version control and viewing history. You will likely change your deployment object many times, for example, but you will generally only create a service object once and not edit it much.  

### Avoid defaults

If you do not specify a value in the manifest, CaaS will use a ridiculous default, i.e. 10 MB of RAM. So if your app exhibits unexpected behavior or poor performance, check that you have explicitly defined values such as CPU, memory, readiness health endpoints, etc... in the app's manifest.

The manifests in the samples repository should get you started. For more details, read the [Developer Guide](https://docs.openshift.com/container-platform/3.11/dev_guide) on the OpenShift website.

---

Continue to [deployment updates](./13-deploymentchange.md).

Return to [Table of Contents](../README.md#agenda)
