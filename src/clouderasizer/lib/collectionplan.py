#Object to hold configuration
import  os, json, metrics, datetime, logging, zipfile, shutil
class CollectionPlan:
    def __init__(self,collectionplan):
        self.plan = json.load(collection)

#Creates collection directory
def create_collection_dir(root_output_dir,plan_name):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    folder_path = root_output_dir + '/' + plan_name + '_' + current_time
    if not os.path.exists(folder_path):
        logging.info("Creating collection directory " + folder_path)
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
        print 'Metric Name  |  Service Name | Save As |' 
        print '----------------------------------------------------------------'
        for metric in plan:
            print metric['metric_name'] + ' | '+ metric['service_name'] + ' | '+  metric['output_as'] + ' | '

#Parses collection plan and returns JSON representation of the plan
def parse_collectionplan(dir,plan_name):
    plan_file = dir + '/' + plan_name
    with open(plan_file) as file:
        plan = json.load(file)
        file.close()
        return plan

def zip_collectionplan(collection_output_folder, root_output_dir):
    zip_file = root_output_dir + '/' + os.path.basename(os.path.normpath(collection_output_folder)) + '.zip'
    with zipfile.ZipFile(zip_file,'w',zipfile.ZIP_DEFLATED) as myzip:
        for root, dirs, files in os.walk(collection_output_folder):
            for file in files:
                logging.info("Adding file " + file + " to zip " + zip_file)
                arcname = os.path.basename(os.path.normpath(collection_output_folder)) + '/' + file
                myzip.write(os.path.join(root,file),arcname=arcname)
        shutil.rmtree(root)
        logging.info("Cleaning up " + root)
    myzip.close()
    #get rid of the original files

#Unzips the collection and returns the path to the collection
def unzip_collection(collection_zip,output_dir):
    zip_file = collection_zip
    path = ''
    with zipfile.ZipFile(zip_file,'r',zipfile.ZIP_DEFLATED) as myzip:
        file_list = myzip.namelist()
        path = output_dir + '/' + os.path.dirname(file_list[0])   
        myzip.extractall(path=output_dir)	
    myzip.close() 
    
    return path

#Executes a collectionplan
def run_collectionplan(cm,cluster_name,collection_plan_dir,plan_name,root_output_dir,start_time,end_time):
    logging.info("Executing collectionplan " + plan_name)
    collection_dir = create_collection_dir(root_output_dir,plan_name)
    plan = parse_collectionplan(collection_plan_dir,plan_name)
    out_fmt = 'JSON'
    for metric in plan:
        metric_list = list()
        metric_list.append(metric['metric_name'])
        data = metrics.collect_metrics(cm,cluster_name,metric_list,start_time,end_time,metric['service_name'],metric['query_type'],metric['output_as'],collection_dir)
        out_fmt = metric['output_as']
    zip_collectionplan(collection_dir,root_output_dir)

    
        

