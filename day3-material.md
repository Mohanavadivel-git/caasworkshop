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
The CaaS platform provides the subdomain `*.app.caas.ford.com` that can be used to build a unique URL for an app. (Satish - Is this domain internal-facing only??) This will satisfy many uses; however, if the app is customer-facing, app teams may desire a [vanity URL](https://en.wikipedia.org/wiki/Vanity_domain).

At a high-level, to establish a new vanity URL, an app team will need to:
1. Create a request for Ford's DNS team to create a DNS CNAME alias using your vanity URL.
  - This alias should forward traffic to `caas.app.ford.com`.
  - You will also need to specify if this vanity URL should be exposed to the public internet (aka external-facing).
1. Create an OpenShift route object which refers to your vanity URL.
1. Create a request for a TLS certificate associated with your vanity URL.
1. Configure your app to serve the TLS certificate to clients requesting the vanity URL.

#### Exercise

To submit a request to the DNS team:
1. For the purposes of this class, please DO NOT click submit, but let's take a look at the DNS request form and how to fill it out.
1. Open the [Network Operations DNS Tool](https://tools.netops.ford.com/dns).
1. Click Create (look for the giant Gear Icon).
1. Set Environment accordingly. Typically, this would be set to "Hosting/Servers".
1. Set Category=Alias.
1. Set Location. If you need the vanity URL external-facing, set Location=External DNS. If you need the vanity URL internal-facing, set location=Internal DNS. If you need both, submit one DNS request for each resulting in a total of two requests.
1. Set Hostname=`caas.app.ford.com`. This is where traffic destined for the vanity URL will be forwarded (the CaaS platform).
1. Set Subnet or IP=`19.13.2.3` for internal-facing and `136.2.64.8` for external-facing.
1. Set Alias=`<YOUR_VANITY_URL>`. For example, `www.electrictrucks.ford.com`.
1. Complete the remainder of the form. DO NOT click submit for this class, but if you were actually going to submit a real DNS request, you would click submit.

Here is an example DNS request for internal-facing vanity URL.

![DNS Request Screenshot](images/dns1.png)

If approved, the DNS team will configure this vanity URL on Ford's DNS servers. This means traffic destined for the vanity URL will be forwarded to the CaaS platform. In the next exercise, we will create an OpenShift route object with a vanity URL so that when traffic arrives at the platform, it will be able to route it appropriately.

#### Exercise

Create an OpenShift route object which refers to your vanity URL.
1. Building on the sample app, open the `manifest/python.yaml` file for editing.
1. Add the vanity URL to the existing route object and save the file. See below.
1. Deploy the app to CaaS again.

```
---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  labels:
    app: python
  name: python
spec:
  host: python.app.oc.local
  host: www.saffron.ford.com  <---------------- ADD THIS
  port:
    targetPort: 8080
  tls:
    termintaion: edge
    insecureEdgeTerminationPolicy: Redirect
```

Now when traffic destined for `www.saffron.ford.com` arrives at the CaaS platform, it will be forwarded to the `python` app. This concludes the steps necessary to route traffic to the app. The next steps are related to configuring TLS security for the app using the vanity URL.
  
### Jenkins Usage
  - TBD