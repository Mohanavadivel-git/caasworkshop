## Day 1 - Lesson 2

## Manifests and Openshift Objects

#### Background on CaaS manifest files

The Spring sample app has a CaaS manifest file at [`manifest/deployment.yaml`](https://github.ford.com/JPOTTE46/samples/blob/master/springboot/manifest/deployment.yaml). The file is a configuration for how OpenShift should run the app and defines the app's OpenShift objects to be created. 

You can learn more about [objects](https://docs.openshift.com/container-platform/3.11/architecture/core_concepts/index.html#architecture-core-concepts-index) and [manifests](https://docs.openshift.com/container-platform/3.11/dev_guide/templates.html) in the OpenShift [Dev Guide](https://docs.openshift.com/container-platform/3.11/dev_guide/index.html).

Another yaml file is located at [`manifest/pullsecret.yaml`](https://github.ford.com/JPOTTE46/samples/blob/master/springboot/manifest/pullsecret.yaml). This file contains the Kubernetes secret to access the image that we will push to Quay. It will be referenced in the deployment.yaml file. 

> NOTE: If you have previously cloned the samples repo, you may need to pull the latest changes to ensure you have the correct credentials in the `pullsecret.yaml` file. Please view your `pullsecret.yaml` file and ensure it matches the one at the github link above. 

### Object Diagram

<p align="center">
  <img src="https://github.ford.com/DevEnablement/caas-workshop/blob/master/images/RouteServiceDiagram.PNG" width="700" height="450">
</p>

#### Openshift Objects

The Spring sample app's manifest defines 6 kinds of OpenShift objects. `Secret` is the only one which is located in a different yaml file in this example. `ConfigMap` is not defined in the deployment, but will be created separately in a later lesson. 

- Deployment
- Service
- Route
- PodDisruptionBudget
- HorizontalPodAutoscaler
- Secret
- ConfigMap

In the **Deployment** object, you can define your app containers compute resources. Review the documentation on [compute resources](https://docs.openshift.com/container-platform/3.11/dev_guide/compute_resources.html#dev-compute-resources) in the OpenShift Dev Guide. In this object, you can also define probes to check the health of your app container. Review the documentation on [application health](https://docs.openshift.com/container-platform/3.11/dev_guide/application_health.html) in the OpenShift Dev Guide.

The **Service** object configures an internal load balancer that will load balance traffic across multiple instances of your app container. The service object will be dynamically assigned an IP address and will proxy traffic to the app container. Review the documentation on [services](https://docs.openshift.com/container-platform/3.11/architecture/core_concepts/pods_and_services.html#services) in the OpenShift Dev Guide.

The **Route** object configures a host name that is associated with the Service object allowing external clients to reach your app container through a URL. Review the documentation on [routes](https://docs.openshift.com/container-platform/3.11/architecture/networking/routes.html) in the OpenShift Dev Guide.

The **PodDisruptionBudget** object ensures that OpenShift will maintain a minimum number of app instances during platform maintenance events. Review the documentation on [disruption budgets](https://docs.openshift.com/container-platform/3.11/admin_guide/managing_pods.html#managing-pods-poddisruptionbudget) in the OpenShift Dev Guide.

The **HorizontalPodAutoscaler** object configures OpenShift to automatically increase and decrease the number of app instances based on CPU utilization. Review the documentation on [autoscaler](https://docs.openshift.com/container-platform/3.11/dev_guide/pod_autoscaling.html) in the OpenShift Dev Guide.

The **Secret** object type provides a mechanism to hold sensitive information, such as passwords, OpenShift Container Platform client configuration files, `dockercfg` files, private source repoistory credentials, and so on. Review the documentation on [secrets](https://docs.openshift.com/container-platform/3.9/dev_guide/secrets.html) and [using image pull secrets](https://docs.openshift.com/container-platform/3.11/dev_guide/managing_images.html#using-image-pull-secrets) in the Openshift Dev Guide.

The **ConfigMap** object provides mechanisms to inject containers with configuration data while keeping containers agnostic of Openshift Container Platform. It is similar to Secrets, but designed to more convienently support working with strings/files that do not contain sensitive information. For example, this may be values for your application.properties of a Springboot application. 

---  

Continue to [Lesson 2.3](./lesson2.3.md).

Return to [Table of Contents](https://github.ford.com/DevEnablement/caas-workshop/tree/workshop-reformat#agenda)