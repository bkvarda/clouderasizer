import json
from cm_api.api_client import ApiResource
from collections import deque

#returns a json data object
def output_json(ts_list):
    json = ts_list.to_json_dict(preserve_ro=True)
    return json

#returns a collection of collections with CSV formatted rows
def output_csv(ts_list):
    csvs = deque()
    for ts in ts_list.timeSeries:
        csv = deque()
        header =  "timestamp" + "," + "min" + "," + "max" + "," +  str(ts.metadata.metricName) + "(" + str(ts.metadata.unitNumerators[0]) + ")"
        csv.append(header)
        for point in ts.data:
            row = str(point.timestamp.isoformat()) + "," + str(point.aggregateStatistics.min) + "," + str(point.aggregateStatistics.max) + "," + str(point.value)
            csv.append(row)
        csvs.append(csv)
    return csvs

#prints metrics to the console
def print_data(ts_list):
    json = ts_list.to_json_dict(preserve_ro=True)
    print json

#saves data as CSV
def save_as_csv(data,output_dir):
    print ''

#saves data as JSON
def save_as_json(ts_list, output_dir):
    data = output_json(ts_list)
    metadata  = data['timeSeries'][0]['metadata']
    attributes = metadata['attributes']
    save_file =  output_dir + '/' + metadata['metricName'] + '.json'
    with open(save_file, 'w') as outfile:
        json.dump(data,outfile)

#saves data to specified location
def save_data(ts_list,location):
   print ''

#finds available metrics based on one or more search terms
def find_metrics(cm,search_terms):
    metrics =  cm.get_metric_schema()
    print ''
    print ''
    for metric in metrics:
        if all(term.lower() in metric.displayName.lower() for term in search_terms):
            print "Metric Name: " + metric.name
            print "Display Name: " + metric.displayName
            print "Description: " + metric.description
            print "Is Counter: " + str(metric.isCounter)
            print "Unit Numerator: " + metric.unitNumerator
            print "Unit Denominator: " + str(metric.unitDenominator)
            print "Aliases: " + str(metric.aliases)
            print "Sources: " + str(metric.sources)
            print "____________________________________________"
            print 

#collects metrics and executes output function based on output_format input.
def collect_metrics(cm,cluster_name,metrics,start_date,end_date,service_name,output_format,output_dir):
    metric_string = ','.join(metrics)
    select_string = 'SELECT ' + metric_string + ' WHERE clusterName = ' + '"'+ cluster_name +'"'
    if service_name!='None':
        select_string = select_string + ' AND serviceName = ' + '"'+ service_name + '"'
    result = cm.query_timeseries(select_string,start_date,end_date)
    ts_list = result[0]
    #We now have our raw metric data, fork off depending on output format
    if(output_format == 'JSON'):
        save_as_json(ts_list,output_dir)
    elif(output_format == 'CSV'):
        output_csv(ts_list,output_dir)
    else:
        print_data(ts_list)
