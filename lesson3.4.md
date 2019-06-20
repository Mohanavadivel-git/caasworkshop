# Lesson 3, Advanced Topics

## Application Logging

The Openshift Enterprise is deployed with the EFK stack to aggregate logs for a range of Openshift Enterprise services. As application developers, you can view the logs of the projects for which you have view access. The EFK stack aggregates logs from hosts and applications, whether coming from multiple containers or even deleted pods. 

The EFK Stack consists of:
 - Elasticsearch: An object store where all logs are stored
 - Fluentd: Gathers logs from nodes and feeds them to Elasticsearch
 - Kibana: A web UI for Elasticsearch

### View Logs in Kibana

To view logs in Kibana, you must be a member of the namespace in Openshift. You can follow along with the steps below using the namespace that you are a member of and using search parameters that apply to your application or service. 

1. Go to [https://kibana.app.caas.ford.com/](https://kibana.app.caas.ford.com/)

#### Indexes

2. If this is your first time using Kibana, you will be re-directed to the Management tab where you will be asked to choose or create an Index Pattern. An index pattern identifies one or more Elasticsearch indices that you want to explore with Kibana. Below is an example of what an index looks like. 

```
project.devenablement-dev.3f491109-75b6-11e9-afd8-30e171556d10.2019.06.19
```

This index contains a prefix `project`, which is the case for all projects in Openshift. It also contains the namespace used in this example, which is `devenablement-dev`. The next part is the namespace ID, which is `3f491109-75b6-11e9-afd8-30e171556d10`. The final part of the index is the date that specific log entry was created. 

To select an index pattern, search for your namespace name in the Management tab. You will come across an index that looks similar to this: 

```
project.devenablement-dev.3f491109-75b6-11e9-afd8-30e171556d10.*
```

This contains project, namespace name, and namespace ID components that were just mentioned. The `*` indicates a wildcard, which essentially says to include all the logs from this namespace as part of this index. Using this, we can now create our Index Pattern by clicking on "Create Index Pattern." Here, you will enter your index pattern with the `*` after the namespace ID as shown above and select a time filter field name. 

![Create an Index Pattern](https://github.ford.com/Containers/localdev/blob/master/docs/images/Kibana_IndexPattern.png)

When you create your index pattern, there is a star icon that you can click to set it as your default index pattern. 

3. When we have created our index pattern, we can view all the fields that the container and application outputs. Simply click on the index pattern name and you can view and filter all the fields. 

#### Discover

4. We will now look at the Discover tab where you can view the entirety of the logs for your namespace. Depending on the number of applications or pods running in your namespace, and the extent of the logs that are output, this may be a large amount that you want to create filters and queries for. 

5. Looking at the search bar, we see the `*` wildcard is being used, which means all the logs are being shown. We can search using the [Lucene query syntax](https://www.elastic.co/guide/en/elasticsearch/reference/5.6/query-dsl-query-string-query.html#query-string-syntax) to find specific logs for this application. In this example for our Springboot applicaiton, we are going to search for the log where the application starts. 

In the search bar, we enter the follow:
```
message:("Started HelloworldApplication")
```
Here, the message refers to the field that we viewed in step 3 when we viewed the index pattern's list of fields. The content after the `:` refers to the message we are looking for. For more complicated searches, view the Lucene query syntax linked above for syntax guidelines. 

6. When the search is completed, we can view the results in a table or in JSON format. Below is an example of the JSON output from one entry of our search results. 

```json
{
  "_index": "project.devenablement-dev.3f491109-75b6-11e9-afd8-30e171556d10.2019.06.19",
  "_type": "com.redhat.viaq.common",
  "_id": "ZjEwYjQ2NzAtZTJiMS00ODgxLTk2OTYtNDJhMTE3YWU2OTY5",
  "_version": 1,
  "_score": null,
  "_source": {
    "docker": {
      "container_id": "007c86f13c743133836dd74a46feae1f65a10e82f27bb37998fce2add0f5fe1e"
    },
    "kubernetes": {
      "container_name": "springboot-hello-world",
      "namespace_name": "devenablement-dev",
      "pod_name": "springboot-hello-world-855b5b4ddc-skxks",
      "pod_id": "aa7adc97-92c1-11e9-9d03-30e171556d10",
      "labels": {
        "app": "springboot-hello-world",
        "pod-template-hash": "4116160887"
      },
      "host": "worker7.caas.ford.com",
      "master_url": "https://kubernetes.default.svc.cluster.local",
      "namespace_id": "3f491109-75b6-11e9-afd8-30e171556d10"
    },
    "message": "2019-06-19 18:40:31.903  INFO 1 --- [           main] c.f.d.helloworld.HelloworldApplication   : Started HelloworldApplication in 15.788 seconds (JVM running for 18.326)\n",
    "level": "info",
    "hostname": "worker7.caas.ford.com",
    "pipeline_metadata": {
      "collector": {
        "ipaddr4": "19.2.17.126",
        "ipaddr6": "fe80::9041:bff:fecb:1e79",
        "inputname": "fluent-plugin-systemd",
        "name": "fluentd",
        "received_at": "2019-06-19T18:40:58.475509+00:00",
        "version": "0.12.43 1.6.0"
      }
    },
    "@timestamp": "2019-06-19T18:40:31.903398+00:00",
    "viaq_msg_id": "ZjEwYjQ2NzAtZTJiMS00ODgxLTk2OTYtNDJhMTE3YWU2OTY5"
  },
  "fields": {
    "@timestamp": [
      1560969631903
    ],
    "pipeline_metadata.collector.received_at": [
      1560969658475
    ]
  },
  "highlight": {
    "message": [
      "2019-06-19 18:40:31.903  INFO 1 --- [           main] c.f.d.helloworld.HelloworldApplication   : @kibana-highlighted-field@Started@/kibana-highlighted-field@ @kibana-highlighted-field@HelloworldApplication@/kibana-highlighted-field@ in 15.788 seconds (JVM running for 18.326)\n"
    ]
  },
  "sort": [
    1560969631903
  ]
}
```

Looking through the fields, we can see kubernetets logging fields usch as our namespace name and ID defined in `kubernetes.namespace_name` and `kubernetes.namespace_id`. We can also see some application level logs such as `level` and `message`. We see in this example, the level of this message is `info` and also can see our message contains "Started HelloworldApplication", which was given in our search criteria. 

7. We can limit the fields to be included in our search results as well. On the left hand side, we can view the selected fields. For example, say we just wanted to view the pod name, and message. We can hover over those fields and select "add" and the table will re-format to ONLY show those fields. The image below shows a re-formatted table based on selected fields. 

![Create an Index Pattern](https://github.ford.com/Containers/localdev/blob/master/docs/images/Kibana_SelectFields.png)

#### Visualize

The visualize tab allows us to view data in several different ways. We can select between basic charts like pie and bar graphs, data charts like tables and gauges, maps, time series, markdowns, word clouds, etc. Here we will create a basic line graph showing the amount of unique pods per day. 

8. If you have no current visualizations, click "Create a visualization." We will select a line graph. Search and select your index. We will change the default for the Y-Axis from `Count` to `Unique Count`. Choose `kubernetes.pod_name` as the field. In the `buckets` section, we will select `X-Axis` and choose `Date Histogram` as the data aggregation, select `Date Histogram` as the aggregation, `@timestamp` as the field, and `auto` as the interval. 

9. Save this visualization as `Pods per day`

> NOTE: The time selection you have currently set in the top right of the page will dictate how your graph is currently viewed. 

10. Highlight different ranges on the graph to see how the data zooms in to those ranges. Choose different fields and different aggregators to see how the graphs formulate. Use a filter to look for specific things. For example, you can define a filter to search your logs for errors and keep a count of errors. You can select the field to be searches if your application contains search and get a count of unqiue searches per day. 

#### Dashboard

Your dashboard is a custom collection of all your visualizations that you can arrange and share. Add individual visualizations that you have saved. If you have not created a dashboard, you will be prompted to create one or add one. 

11. Create a new dashboard and add a visualization. Select the `Pods per day` chart. 

12. Click the share button at the top to see the different sharing options available. Copy and paste the sharing URL and see it take you directly to your dashboard. 

#### Timelion

Timelion is a time series data visualizer that enables you to combine totally independent data sources within a single visualization. It’s driven by a simple expression language you use to retrieve time series data, perform calculations to tease out the answers to complex questions, and visualize the results.

Review the [timelion getting started guide](https://www.elastic.co/guide/en/kibana/5.6/timelion-getting-started.html)

#### Dev Tools

The Dev Tools page contains development tools that you can use to interact with your data in Kibana. There are number of different interactions you can use withing the Dev tools: 

- Use the Console UI
  - UI that allows you to interact with the REST API of Elasticseach
  - Contains an editor section and a response/output section
- Profiler API
  - Insepect and analyze your search queries
  - Includes search profile tool to visualize the metadata of your queries

Review the [Dev Tools Guide](https://www.elastic.co/guide/en/kibana/5.6/devtools-kibana.html)

---

You have reached the end of the workshop :clap: