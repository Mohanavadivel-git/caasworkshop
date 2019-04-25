# Lesson 1, App Container Images

### Building Container Images with Localdev

The big picture...

![CaaS Workflow](https://github.ford.com/Containers/localdev/blob/master/docs/images/CaaS-LocalDev.png)

This lesson focuses on building a container image for your app. The activities in this lesson correspond to boxes 1, 2, and 3 in the above diagram. If you have no experience with container images, you should check out the [Get Started](https://docs.docker.com/get-started/) tutorial on Docker's website.

#### Exercise

The CaaS team maintains a repository of sample apps that will run on CaaS. You will clone this repo locally, and then go through the process of building a container image with one of the sample apps.

1. Clone the [samples repo](https://github.ford.com/JPOTTE46/samples) 
```
# Change directory to your project workspace if you have a preferred one.
$ cd ~/workspace

# Clone the samples git repo.
$ git clone git@github.ford.com:JPOTTE46/samples.git

```
2. Go through the samples repository README and configure synchronized folders using to these [instructions](https://github.ford.com/JPOTTE46/samples#configure-synchronized-folders).
   - This will allow you to access your local copy of the samples repo from within the localdev VM.
3. Build the container image for a sample app (let's use the python app) using these [instructions](https://github.ford.com/JPOTTE46/samples#building-the-container-image).
4. Run the container image to test it using these [instructions](https://github.ford.com/JPOTTE46/samples#running-the-container-image-locally-to-test).

---  

Continue to [Lesson 1.3](./lesson1.3.md).
