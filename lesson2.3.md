# Lesson 2, Running Apps in CaaS

### Best Practices for CaaS Manifests

Through the CaaS manifest you have significant control over how CaaS will run your application. App teams can define, test, and revise the resources allocation to an application without any action from an operations team.

#### Avoid defaults

If you do not specify a value in the manifest, CaaS will use a ridiculous default, i.e. 10 MB of RAM. So if your app exhibits unexpected behavior or poor performance, check that you have explicitly defined values such as CPU, memory, readiness health endpoints, etc... in the app's manifest.

The manifests in the samples repository should get you started. For more details, read the [Developer Guide](https://docs.openshift.com/container-platform/3.11/dev_guide) on the OpenShift website.

---  

Continue to [Lesson 3](./lesson3.1.md).