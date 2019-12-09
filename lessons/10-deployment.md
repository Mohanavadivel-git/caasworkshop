## Deployment Manifest

The `Deployment` object provides the definition for deploying our container image in CaaS. `Deployments` are the object that spins up individual pods. You could opt to define a `pod` definition, but that requires more hands on work to constantly update and configure the pods. `Deployments` can do this automatically and handle the task of bringing up our requested number of pods. 

#### *Basic Definition*

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <CDSID>-deployment
  labels:
    app: <CDSID>-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: <CDSID>-deployment
  template:
    metadata:
      labels:
        app: <CDSID>-deployment
```
- Name: Define your deployment name which will also be the name of the application
- Labels: You can use labels to better query your Openshift objects. For each Openshift object, we are definining an `app` label with the value of our app name. For every object that contains the label `app=<CDSID>-deployment`, we can query based on that label. 
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
                - <CDSID>-deployment
            topologyKey: "kubernetes.io/hostname"
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - <CDSID>-deployment
              topologyKey: failure-domain.ford.com/zone
```
- Pod Affinity: Define what should be in the same node or same data center
- Pod Anti-Affinity: Define what should be in different nodes or different data centers
- Required Rule: Requires that this rule be met, otherwise, the pod will not start
- Preferred Rule: Prefers that this rule be met, but if not, will start the pod anyways 
- Topology Key: The key the cluster uses to differentiate between nodes and data centers
  - kubernetes.io/hostname - The topology key for nodes
  - failure-domain.ford.com/zone - The topology key for data centers

See the [pod affinity guide](./something) for more information on affinity rules. 

#### *Image Reference*
```yaml
      imagePullSecrets:
      - name: devenablement-workshop-pull-secret
      containers:
      - name: <CDSID>-deployment
        image: registry.ford.com/devenablement/workshop:<CDSID>
        imagePullPolicy: Always        
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
            memory: "50Mi"
            cpu: "50m"
          limits:
            memory: "100Mi"
            cpu: "100m"
```
- Requests: The guaranteed resources your container will have allocated to it. 
- Limits: The upper-bound limit resources your container can vertically scale up to 
> Note: The total limits of all your pods must fit within your namespace's quota

#### *Probes*
```yaml
        livenessProbe:
          httpGet:
            path: /
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 30
          periodSeconds: 20
          timeoutSeconds: 5
        readinessProbe:
          httpGet:
            path: /
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 30
          periodSeconds: 20
          timeoutSeconds: 5
```
- Liveness Probe: Check if the container in which application is configured is running
- Readiness Probe: Determines if your application is ready to service requests 
- Probe Types: Probes can be HTTP(S) checks, simple commands, entire scripts, or TCP socket checks
- For interval definitions, see the [Kubernetes Dev Guide](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/#configure-probes)

## Exercise - Deploy Application

1. Open the `deployment.yaml` file. Replace all the `<CDSID>`'s with your CDSID. (Lines 4, 6, 11, 15, 30, 40, 56, and 57). Use Ctrl+H (CMD+H on Mac) to replace all at once. 

2. We can deploy our application using the `deployment.yaml` file. 

```bash
$ oc create -f ./manifests/deployment.yaml
deployment.apps/<CDSID>-deployment created
```

3. Access the Openshift Console and navigate to your deployment. You can select the [running pod](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/pods) and view the logs of the application. 

---  

Continue to [Openshift objects](./11-objects.md).

Return to [Table of Contents](../README.md#agenda)
