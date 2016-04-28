from cm_api.api_client import ApiResource
from collections import deque

#returns a json data object
def output_json(ts_list):
    print ''

#returns a collection with CSV formatted rows
def output_csv(ts_list):
    for ts in ts_list.timeSeries:
        data = deque()
        header =  "timestamp" + "," + "min" + "," + "max" + "," +  str(ts.metadata.metricName) + "(" + str(ts.metadata.unitNumerators[0]) + ")"
        data.append(header)
        for point in ts.data:
            row = str(point.timestamp.isoformat()) + "," + str(point.aggregateStatistics.min) + "," + str(point.aggregateStatistics.max) + "," + str(point.value)
            data.append(row)
    return data

#prints collection rows out to console
def output_console(data):
    for row in data:
        print row
    

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
def collect_metrics(cm,cluster_name,metrics,start_date,end_date,service_name,output_format):
    metric_string = ','.join(metrics)
    select_string = 'SELECT ' + metric_string + ' WHERE clusterName = ' + '"'+ cluster_name +'"'
    if service_name!='None':
        select_string = select_string + ' AND serviceName = ' + '"'+ service_name + '"'
    result = cm.query_timeseries(select_string,start_date,end_date)
    ts_list = result[0]
    #We now have our raw metric data, fork off depending on output format
    if(output_format == 'JSON'):
        output_json(ts_list)
    elif(output_format == 'CSV'):
        output_csv(ts_list)
    else:
        output_console(output_csv(ts_list))
