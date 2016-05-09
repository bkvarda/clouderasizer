#Class for PPT plan. A PPT plan will auto generate a canned PPT based on a set of metrics that were pulled via a CollectionPlan
import os, metrics, collectionplan
from pptx import Presentation
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches
from collections import deque

#Create a metric slide
def create_metric_slide(prs,metric):
    #metric info
    metric_name = metric['timeSeries'][0]['metadata']['metricName'] 
   
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    for point in metric['timeSeries'][0]['data']:
        print point['timestamp']
    #title
    title = slide.shapes.title
    title.text = metric_name
    # define chart data ---------------------
    chart_data = ChartData()
    chart_data.categories = ['East', 'West', 'Midwest']
    chart_data.add_series('Series 1', (19.2, 21.4, 16.7))

    # add chart to slide --------------------
    x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4.5)
    slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data)
    return

#Create a title slide
def create_title_slide(prs):
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = "Hello, World!"
    subtitle.text = "python-pptx was here!"
    return 

#Create a presentation
def create_ppt(collection_zip,output_dir):
    #Unzip the collection
    collection_dir = collectionplan.unzip_collection(collection_zip,output_dir) 
    #Parse the collection
    collection = deque()
    
    for file in os.listdir(collection_dir):
        full_file_path = collection_dir + '/' + file
        collection.append(metrics.read_from_json(full_file_path))
    
    



    prs = Presentation()
    
    #create the title slide
    create_title_slide(prs)
    #create metric slide for each metric
    for metric in collection:
        create_metric_slide(prs,metric)    
    
    output_file = output_dir + '/' + 'test.pptx'
    prs.save(output_file)

