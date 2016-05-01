#Object to hold configuration
import  os, json, metrics, datetime
class CollectionPlan:
    def __init__(self,collectionplan):
        self.plan = json.load(collection)

#Creates collection directory
def create_collection_dir(root_output_dir,plan_name):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    folder_path = root_output_dir + '/' + plan_name + '_' + current_time
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

#Generates a list of collectionplans that reside in a directory
def get_collectionplans(dir):
    plans = os.listdir(dir)
    print 'Collection Plans'
    print '________________'
    for plan in plans:
        print plan

#Prints details of a collection plan
def get_collectionplan(dir,plan_name):
    plan_file= dir + '/' + plan_name
    with open(plan_file) as file:
        plan = json.load(file)
        file.close()
        print 'Metric Name  |  Service Name | Start Date | End Date | Save As |' 
        print '----------------------------------------------------------------'
        for metric in plan:
            print metric['metric_name'] + ' | '+ metric['service_name'] + ' | '+ metric['start_time'] + ' | '+ metric['end_time'] + ' | '+ metric['output_as'] + ' | '

#Parses collection plan and returns JSON representation of the plan
def parse_collectionplan(dir,plan_name):
    plan_file = dir + '/' + plan_name
    with open(plan_file) as file:
        plan = json.load(file)
        file.close()
        return plan

#Executes a collectionplan
def run_collectionplan(cm,cluster_name,collection_plan_dir,plan_name,root_output_dir,start_time,end_time):
    collection_dir = create_collection_dir(root_output_dir,plan_name)
    plan = parse_collectionplan(collection_plan_dir,plan_name)
    out_fmt = 'JSON'
    for metric in plan:
        metric_list = list()
        metric_list.append(metric['metric_name'])
        data = metrics.collect_metrics(cm,cluster_name,metric_list,start_time,end_time,metric['service_name'],metric['output_as'],collection_dir)
        out_fmt = metric['output_as']

        

