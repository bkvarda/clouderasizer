#### Multipurpose tool for discovering and collecting metrics from Cloudera Manager Hadoop clusters.

#### Usage
Tool used to both collect metrics and programatically build PPT reports based on a collection of metrics. Primary use has changed to focus more on the reporting aspect. 

#### Installation
Working on making this easier. Current dependencies can be installed using pip [Note: python-pptx after 0.5.8 broke some APIs that are used]:
```
pip install cm_api
pip install python-pptx==0.5.8
```

#### Options
For full list of options, run:
```
python clouderasizer.py -h
```
#### Metric Discovery
To search for available Cloudera Manager  metrics, run the following command with a list of search terms separated by spaces:
```
python clouderasizer.py metrics --search hbase region server
```
If you run the command with no search terms, everything will be returned. Most metrics will be listed, but some will not be seen. In general, available metrics for this tool will come from a TSQL query that is structured like:
```
SELECT some_metric WHERE serviceType = 'SOME_SERVICE' AND clusterName = 'SOME_NAME'
```
The only exclusion currently is a query of all metrics to the 'IMPALA_QUERIES' table in CM, in which case you would use the --query_type IMPALA to grab metrics. Time frame of a query can be specified using the --start_time and --end_time flags. By default, a time period of 1 year is used. 

#### Metric Collection
Once you have decided on a metric or metrics you are interested in, you can collect it:
```
clouderasizer.py collect --metrics some_metric_name
```
By default, this command will simply print a representation of the metric to the screen. If a metric name is collected for more than one entity (IE at the service level such as HDFS and also at the cluster level such as ClusterName01) both metrics will be collected as a list of metric objects. You can collect just a single entity's metric by specifying the entity name:
```
clouderasizer.py collect --metrics some_metric --entity_name HDFS
```
Metrics can be outputed as a file containing the JSON payload. The file is saved in the output location specified in clouderasizer.conf or by using the --output_location flag. To save as JSON:
```
clouderasizer.py collect --metrics some_metric --entity_name HDFS --save_as JSON
```
Numerous metrics can be collected in the same command. I can't think of a great reason to do this and haven't tested it much so use at your own risk. 

#### CollectionPlans
A collectionplan is a file that describes a series of metrics that should be collected together. It allows for a structured definition of metrics to collect but also the ability to have different metric collection bundles for different purposes. As an example, maybe you have a general plan for collecting from a variety of services for a general health check, or perhaps maybe you have collection plans that are more detailed for specific services. An example collectionplan looks like this:
```
[
  {
   "metric_name": "total_cpu_system_rate_across_hosts",
   "service_name": "None",
   "query_type": "None",
   "output_as": "JSON"
  },
  {
   "metric_name": "total_dfs_capacity_used_across_datanodes",
   "service_name": "HDFS",
   "query_type": "None",
   "output_as": "JSON"
  },
  {
   "metric_name": "total_bytes_read_rate_across_datanodes",
   "query_type": "None",
   "service_name": "HDFS",
   "output_as": "JSON"
  },
  {
   "metric_name": "total_bytes_written_rate_across_datanodes",
   "query_type": "None",
   "service_name": "HDFS",
   "output_as": "JSON"
  },
  {
   "metric_name": "total_pending_containers_across_yarn_pools",
   "query_type": "None",
   "service_name": "YARN",
   "output_as": "JSON"
  }
]
```
Collectionplans are placed in the collectionplan folder and are in JSON format. To list available collectionplans, run:
```
clouderasizer.py collectionplan --list
```
To execute a collection plan, run:
```
clouderasizer.py collectionplan --execute some_plan.json
```
Note that some_plan.json is not a relative path, it is the name of the plan in the collectionplan directory. When a collectionplan is executed, the resulting output is a zip file with the name of the plan plus the date and time. By default, it is saved in the output directory but that is configurable using a flag or in clouderasizer.conf. The collectionplan output can be leveraged to create a PPT with a single command. 

#### PPT Generation
This tool can build PowerPoint presentations automatically given a zip file of metrics. The requirements are:
- Input must be a .zip file containing a folder which contains individual metrics as single files. All individual metrics must be for a single entity.
- Metrics need to be in JSON format, a single file containing a single metric. Metrics must be the same as those supported by the 'collect' option using this CLI tool. 
- Metrics need to have been collected from Cloudera Manager using the python CM API bindings, this tool (using collect --output_as JSON or as a collectionplan) or using a tool like cURL to grab the metric from CM and output it as a file containing the JSON payload. No other methods are supported and may not work. 

Given a .zip in the proper format, you can turn your metrics into a pretty presentation with charts using this command:
```
clouderasizer.py pptplan --generate some_metrics.zip 
```
The .ppt is saved in the output location specified in clouderasizer.conf or specified by flags. 

