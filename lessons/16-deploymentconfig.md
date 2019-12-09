## Deployment Config

A `DeploymentConfig` is different than a `Deployment`. A `DeploymentConfig` spins up `Deployments`. What we will do is set up a trigger in our `DeploymentConfig` so that every time our image is updated in Quay, a new `Deployment` will be automatically spun up by the `DeploymentConfig`. 

---

### Deploy Deployment Config

1. Open the `deploymentconfig.yaml` file. Replace <CDSID> with your CDSID. 

2. Deploy the `DeploymentConfig` object. 

```bash
$ oc create -f ./manifests/deploymentconfig.yaml
```

3. Go to the [deployments](https://api.caas.ford.com/console/project/devenablement-workshop-dev/browse/deployments) section in Openshift. Notice the separate section for `DeploymentConfigs`. We can watch the logs and the pods to see how the `DeploymentConfig` spins up a `Deployment` which spins up our pods. 

---  

Continue to [Openshift Objects](./13-objects.md).

Return to [Table of Contents](../README.md#agenda)
