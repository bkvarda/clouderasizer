import logging, sys, argparse, time, datetime
from lib import metrics, config
from cm_api.api_client import ApiResource

#Connects to CM using provided (or configured) credentials and returns the Api object
def connect_cm(args):
    cm = ApiResource(args.cm_host, username=args.username, password=args.password)
    return cm

#Searches against available CM metrics bases on a series of terms
def do_search(args):
    cm = connect_cm(args)    
    metrics.find_metrics(cm,args.search)
    sys.exit(0)

#Collects metrics for one ore more metrics for the specified time period 
def do_collection(args):
    cm = connect_cm(args)    
    metrics.collect_metrics(cm,args.cluster_name,args.metrics,args.start_time,args.end_time,args.entity_name,args.save_as)
    sys.exit(0) 

def main():
    #Config and logging
    configuration = config.Config('configs/clouderasizer.conf')
    logfmt ='%(asctime)s - %(levelname)s - %(message)s'
    datefmt = '%m/%d/%Y %I:%M:%S'
    logging.basicConfig(filename=configuration.logging_dir+'/clouderasizer.log',level=logging.DEBUG,datefmt=datefmt,format=logfmt)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(logfmt))
    logging.getLogger('').addHandler(console)
    
    #Set defaults based on config file. These will be overriden by any command arguments, or if not specified will be the default arguments.
    cm_host = configuration.cloudera_manager_name
    username = configuration.cloudera_username
    password = configuration.cloudera_password
    cluster_name = configuration.cloudera_cluster_name
    current_time = datetime.datetime.fromtimestamp(time.time())
    last_year = datetime.datetime.fromtimestamp(time.time()-31536000)

    #CLI Argument Logic - Root parser
    parser = argparse.ArgumentParser(prog='clouderasizer.py')
    parser.add_argument('--username', default=username,
                        help='Name of an user with administrative access (defaults to %(default)s)')
    parser.add_argument('--password', default=password,
                        help='Password for the administrative user (defaults to %(default)s)')
    parser.add_argument('--cm_host', help="The hostname/ip of the Cloudera Manager server", default=cm_host)
    parser.add_argument('--cluster_name', help="The name of the cluster inside of CM",default=cluster_name)
    parser.add_argument('--config_file', help="Cluster configuration file (.ini)")
    
    subparsers = parser.add_subparsers()
   
    #metrics subparser    
    parser_metrics = subparsers.add_parser('metrics', help='Find and describe available metrics')
    parser_metrics.add_argument('--search', nargs='+', help='Find available metrics. Takes one or more words separated by spaces',default='None')
    parser_metrics.set_defaults(func=do_search)

    #collection subparser
    parser_collect=subparsers.add_parser('collect', help='Collect metrics')
    parser_collect.add_argument('--metrics', nargs='+',help='The names of the metrics to retrieve. Can be a space-separated list',required=True)
    parser_collect.add_argument('--start_time',help='The start time to collect from',default=last_year)
    parser_collect.add_argument('--end_time',help='The end time to collect until',default=current_time)
    parser_collect.add_argument('--entity_name',help='The service name or entity to collect the metrics for. By default it will grab at CLUSTER level',default='None')
    parser_collect.add_argument('--save_as',help='The format to save the metrics in - JSON, CSV, or NONE. Default is NONE',default='None')
    parser_collect.set_defaults(func=do_collection)
    
    #tsql subparser
    parser_tsql = subparsers.add_parser('tsql', help='Build a TSQL query for running your own API calls')

    args = parser.parse_args() 
    
    #call the function as determined by commands
    args.func(args) 
    
    print "Invalid options or syntax error"
    sys.exit(1)

 
main()
