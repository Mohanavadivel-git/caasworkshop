# Day 3, Advanced Topics

By now you have a basic understanding of how to:
- Build a container image for your app
- Push that image in Ford's image registy for future use
- Run that image on Ford's CaaS platform

Today's lessons will focus on more complicated use cases as well as additional topics that will keep your app running well after you've launched it (sometimes called 'Day 2 Operations'). For example, configuring a vanity URL and monitoring your app's performance.

### Monitoring Apps

If your app is deployed on CaaS, you get basic monitoring of your app's resource utilization by default. The platform provides a real-time monitoring dashboard built using the Prometheus and Grafana tools without additional cost.

![Grafana Screenshot](images/monitoring1.png)

#### Exercise

1. Bring up the CaaS monitoring dashboard in a web browser. Go to https://grafana-openshift-monitoring.app.caas.ford.com. You might want to bookmark this link for future use.
1. Click the drop-down menu in the upper left and select the `K8s / Computer Resources / Namespace`. This brings up a dashboard where you can filter by namespace.
1. Let's view the resource utilization of apps in the Quay namespace. Use the namespace dropdown to select `quay-enterprise`.
1. Here you can review the CPU and memory quota and utilzation of all pods associated with the Quay namespace. Use the tools in the upper right to adjust the timeframe.

### Storage
  - Persistent storage options, TBD

### Vanity URLs and TLS
  - Requesting a Vanity URL, TBD
  - TLS termination options, TBD
  
### Jenkins Usage
  - TBD