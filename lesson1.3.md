# Lesson 1, App Container Images

### Container Image Registries

The big picture...

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This lesson focuses on building a container image for your app. The activities in this lesson correspond to boxes 1, 2, and 3 in the above diagram. If you have no experience with container images, you should check out the [Get Started](https://docs.docker.com/get-started/) tutorial on Docker's website.

#### Exercise

The CaaS team maintains a repository of sample apps that will run on CaaS. We will clone this repo locally, and then go through the sample python app building an app container image.

1. Clone the [samples repo](https://github.ford.com/Containers/samples).
```
# Change directory to your project workspace if you have a preferred one.
$ cd ~/workspace

# Clone the samples git repo.
$ git clone git@github.ford.com:Containers/samples.git

```
1. Configure synchronized folders using to these [instructions](https://github.ford.com/Containers/samples/tree/master/python#configure-synchronized-folders).
   - This will allow you to access your local copy of the samples repo from within the localdev VM.
1. Build the container image for the python app using these [instructions](https://github.ford.com/Containers/samples/tree/master/python#build-container-image).
1. Run the container image to test it using these [instructions](https://github.ford.com/Containers/samples/blob/master/python/README.md#running-the-container-image-locally).

---  

Continue to [Lesson 1.4](./lesson1.4.md).