import logging, sys, argparse, time, datetime
from lib import metrics, config, collectionplan, pptplan
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
def do_collect(args):
    cm = connect_cm(args)    
    metrics.collect_metrics(cm,args.cluster_name,args.metrics,args.start_time,args.end_time,args.entity_name,args.save_as,args.output_dir)
    sys.exit(0) 

def do_collectionplan(args):
    
    if(args.list):
        collectionplan.get_collectionplans(args.collectionplan_dir)
        sys.exit(0)
    elif(args.details):
        collectionplan.get_collectionplan(args.collectionplan_dir,args.details)
        sys.exit(0)
    elif(args.execute):
        cm = connect_cm(args)
        collectionplan.run_collectionplan(cm,args.cluster_name,args.collectionplan_dir,args.execute,args.output_dir,args.start_time,args.end_time)
        sys.exit(0)
    else:
        sys.exit(0)

def do_pptplan(args):
    
   if(args.generate):
       pptplan.create_ppt(args.generate,args.output_dir)
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
    collectionplan_dir = configuration.collectionplan_dir
    output_dir = configuration.output_dir

    #CLI Argument Logic - Root parser
    parser = argparse.ArgumentParser(prog='clouderasizer.py')
    parser.add_argument('--username', default=username,
                        help='Name of an user with administrative access (defaults to %(default)s)')
    parser.add_argument('--password', default=password,
                        help='Password for the administrative user (defaults to %(default)s)')
    parser.add_argument('--cm_host', help="The hostname/ip of the Cloudera Manager server", default=cm_host)
    parser.add_argument('--cluster_name', help="The name of the cluster inside of CM",default=cluster_name)
    parser.add_argument('--output_dir',help="The full path of the output directory", default=output_dir)
    parser.add_argument('--start_time',help='The start time to collect from',default=last_year)
    parser.add_argument('--end_time',help='The end time to collect until',default=current_time)
    subparsers = parser.add_subparsers()
   
    #metrics subparser    
    parser_metrics = subparsers.add_parser('metrics', help='Find and describe available metrics')
    parser_metrics.add_argument('--search', nargs='+', help='Find available metrics. Takes one or more words separated by spaces',default='None')
    parser_metrics.set_defaults(func=do_search)

    #collector subparser
    parser_collect=subparsers.add_parser('collect', help='Collect metrics')
    parser_collect.add_argument('--metrics', nargs='+',help='The names of the metrics to retrieve. Can be a space-separated list',required=True)
    parser_collect.add_argument('--entity_name',help='The service name or entity to collect the metrics for. By default it will grab at CLUSTER level',default='None')
    parser_collect.add_argument('--save_as',help='The format to save the metrics in - JSON, CSV, or NONE. Default is NONE',default='None')
    parser_collect.set_defaults(func=do_collect)
    
    #collectionplan subparser
    parser_collection=subparsers.add_parser('collectionplan', help='Execute a collection plan for collecting a defined series of metrics')
    parser_collection.add_argument('--execute',help='The name of the collection plan to execute')
    parser_collection.add_argument('--list',action='store_true',help='Shows list of collection plans')
    parser_collection.add_argument('--details',help='Shows details for a given collection plan')
    parser_collection.add_argument('--output_type',help='The type of output to produce - ZIP is the only current option',default='ZIP')
    parser_collection.add_argument('--output_path',help='The path to output to',default=configuration.output_dir)
    parser_collection.add_argument('--collectionplan_dir',help='The path where collectionplans are kept',default=collectionplan_dir)
    parser_collection.set_defaults(func=do_collectionplan)
   
    #pptplan subparser
    parser_pptplan = subparsers.add_parser('pptplan', help='Generate a PPT from a collection generated from collectionplan')
    parser_pptplan.add_argument('--generate', help='Generate a PPT from a collection. Takes a collection .zip as argument')
    parser_pptplan.set_defaults(func=do_pptplan)

    args = parser.parse_args() 
    
    #call the function as determined by commands
    args.func(args) 
    
    print "Invalid options or syntax error"
    sys.exit(1)

 
main()
