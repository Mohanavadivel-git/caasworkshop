# Openshift Objects

There are many more objects in CaaS besides `BuildConfigs` and `Deployments`. These objects help build and deploy your container image. Accessing and maintaining your application is done through various other objects.

You can learn more about [objects](https://docs.openshift.com/container-platform/3.11/architecture/core_concepts/index.html#architecture-core-concepts-index) and [manifests](https://docs.openshift.com/container-platform/3.11/dev_guide/templates.html) in the OpenShift [Dev Guide](https://docs.openshift.com/container-platform/3.11/dev_guide/index.html).

### Object Diagram

<p align="center">
  <img src="https://github.ford.com/DevEnablement/caas-workshop/blob/master/images/RouteServiceDiagram.PNG" width="700" height="450">
</p>

### Openshift Objects

This list is **NOT** a complete list of objects, but it does include the objects you will most likely work with. 

- Service
- Route
- PodDisruptionBudget
- HorizontalPodAutoscaler
- Secret
- ConfigMap

The **Service** object configures an internal load balancer that will load balance traffic across multiple instances of your app container. The service object will be dynamically assigned an IP address and will proxy traffic to the app container. Review the documentation on [services](https://docs.openshift.com/container-platform/3.11/architecture/core_concepts/pods_and_services.html#services) in the OpenShift Dev Guide. Generally, your service will not change. 

The **Route** object configures a host name that is associated with the Service object allowing external clients to reach your app container through a URL. Review the documentation on [routes](https://docs.openshift.com/container-platform/3.11/architecture/networking/routes.html) in the OpenShift Dev Guide.

The **PodDisruptionBudget** object ensures that OpenShift will maintain a minimum number of app instances during platform maintenance events. Review the documentation on [disruption budgets](https://docs.openshift.com/container-platform/3.11/admin_guide/managing_pods.html#managing-pods-poddisruptionbudget) in the OpenShift Dev Guide.

The **HorizontalPodAutoscaler** object configures OpenShift to automatically increase and decrease the number of app instances based on CPU utilization. Review the documentation on [autoscaler](https://docs.openshift.com/container-platform/3.11/dev_guide/pod_autoscaling.html) in the OpenShift Dev Guide.

The **Secret** object type provides a mechanism to hold sensitive information, such as passwords, OpenShift Container Platform client configuration files, `dockercfg` files, private source repository credentials, and so on. Review the documentation on [secrets](https://docs.openshift.com/container-platform/3.9/dev_guide/secrets.html) and [using image pull secrets](https://docs.openshift.com/container-platform/3.11/dev_guide/managing_images.html#using-image-pull-secrets) in the Openshift Dev Guide.

The **ConfigMap** object provides mechanisms to inject containers with configuration data while keeping containers agnostic of Openshift Container Platform. It is similar to Secrets, but designed to more conveniently support working with strings/files that do not contain sensitive information. For example, this may be values for your application.properties of a Springboot application. 

---  

Continue to [manifest definitions](./12-objectmanifest.md).

Return to [Table of Contents](../README.md#agenda)