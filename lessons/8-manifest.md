## Manifests

### The Big Picture - Step 4

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

In this lesson, we will break down the individual components of a full manifest that includes a deployment, service, route, pod disruption budget, horizontal pod autoscaler, and a reference to a secret. 

### Deployment

#### *Basic Definition*

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: springboot-hello-world
  labels:
    app: springboot-hello-world
spec:
  replicas: 1
  selector:
    matchLabels:
      app: springboot-hello-world
  template:
    metadata:
      labels:
        app: springboot-hello-world
```
- Name: Define your deployment name which will also be the name of the application
- Labels: You can use labels to better query your Openshift objects. For each Openshift object, we are definining an `app` label with the value of our app name. For every object that contains the label `app=springboot-hello-world`, we can query based on that label. 
- Replicas: Number of instances to start your application with
#### *Affinity Rules*
```yaml
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - springboot-hello-world
            topologyKey: "kubernetes.io/hostname"
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - springboot-hello-world
              topologyKey: failure-domain.ford.com/zone
```
- Pod Affinity: Define what should be in the same node or same data center
- Pod Anti-Affinity: Define what should be in different nodes or different data centers
- Required Rule: Requires that this rule be met, otherwise, the pod will not start
- Preferred Rule: Prefers that this rule be met, but if not, will start the pod anyways 
- Topology Key: The key the cluster uses to differentiate between nodes and data centers
  - kubernetes.io/hostname - The topology key for nodes
  - failure-domain.ford.com/zone - The topology key for data centers
#### *Image Reference*
```yaml
      imagePullSecrets:
      - name: devenablement-workshop-pull-secret
      containers:
      - name: springboot-hello-world
        image: registry.ford.com/devenablement/workshop:0.0.3
        imagePullPolicy: IfNotPresent
```
- ImagePullSecret: The secret for your container image repository in Quay. Generally this is a config or JSON file downloaded from Quay. We will deploy this secret in the next lesson. 
- Image: The URL to your repository in Quay
- imagePullPolicy: Whether or not to use cache. `IfNotPresent` means the system will try to use the image available in cache. This allows for speedier pod starts. A value of `Always` will always pull the image fresh from the registry. A value of `Never` assumes the image is always available locally or in cache. 
#### *Ports and Environment*
```yaml
        ports:
          - name: http
            containerPort: 8080
        env:
        - name: TCP_PORT
          value: "8080"
        - name: NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: POD_IP
          valueFrom:
            fieldRef:
              fieldPath: status.podIP
        - name: SERVICE_ACCOUNT
          valueFrom:
            fieldRef:
              fieldPath: spec.serviceAccountName
```
- Define ports and environment variables
#### *Resources*
```yaml
        resources:
          requests:
            memory: "250Mi"
            cpu: "400m"
          limits:
            memory: "400Mi"
            cpu: "600m"
```
- Requests: The guaranteed resources your container will have allocated to it. 
- Limits: The upper-bound limit resources your container can vertically scale up to 
> Note: The total limits of all your pods must fit within your namespace's quota
#### *Probes*
```yaml
        livenessProbe:
          httpGet:
            path: /api/v1/hello
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 30
          periodSeconds: 20
          successThreshold: 1
          failureThreshold: 5
          timeoutSeconds: 5
        readinessProbe:
          httpGet:
            path: /api/v1/hello
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 30
          periodSeconds: 20
          successThreshold: 1
          failureThreshold: 5
          timeoutSeconds: 5
```
- Liveness Probe: Check if the container in which application is configured is running
- Readiness Probe: Determines if your application is ready to service requests 
- Probe Types: Probes can be HTTP(S) checks, simple commands, entire scripts, or TCP socket checks
- For interval definitions, see the [Kubernetes Dev Guide](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/#configure-probes)

### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: springboot-hello-world-service
  labels:
    app: springboot-hello-world
spec:
  type: ClusterIP
  selector:
    app: springboot-hello-world
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
    app: springboot-hello-world
  name: springboot-hello-world
spec:
  host: springboot-hello-world.apps.caas.ford.com
  port:
    targetPort: 8080
  tls:
    termintaion: edge
    insecureEdgeTerminationPolicy: Allow
  to:
    kind: Service
    name: springboot-hello-world
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
    name: springboot-hello-world
  name: springboot-hello-world-disruptionbudget
spec:
  selector:
    matchLabels:
      app: springboot-hello-world
  minAvailable: 1
  ```
- Define the minimum available pods you want during maintenance events 

### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  labels:
    app: springboot-hello-world
  name: springboot-hello-world-autoscaler
spec:
  scaleTargetRef:
    apiVersion: extensions/v1beta1
    kind: Deployment
    name: springboot-hello-world
  maxReplicas: 3
  minReplicas: 1
  targetCPUUtilizationPercentage: 80
```
- Max Replicas: The maximum amount of replicas your application can scale up to
- Min Replicas: The minimum amount of replicas your application can scale down to 
- TargetCPUUtilization: The percentage of CPU your application must use up before it will scale up and spawn another pod

### Best Practices for CaaS Manifests

Through the CaaS manifest you have significant control over how CaaS will run your application. App teams can define, test, and revise the resources allocation to an application without any action from an operations team.

In this workshop, all these Openshift objects have been combined in one manifest. You might find it more practical to separate these into separate manifests (i.e. deployment.yaml, service.yaml, route.yaml, etc). This might be a better option for version control and viewing history. You will likely change your deployment object many times, for example, but you will generally only create a service object once and not edit it much.  

### Avoid defaults

If you do not specify a value in the manifest, CaaS will use a ridiculous default, i.e. 10 MB of RAM. So if your app exhibits unexpected behavior or poor performance, check that you have explicitly defined values such as CPU, memory, readiness health endpoints, etc... in the app's manifest.

The manifests in the samples repository should get you started. For more details, read the [Developer Guide](https://docs.openshift.com/container-platform/3.11/dev_guide) on the OpenShift website.

---

Continue to [Deploying Your Application](./9-deploy.md).

Return to [Table of Contents](../README.md#agenda)