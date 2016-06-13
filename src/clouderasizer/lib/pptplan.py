#Class for PPT plan. A PPT plan will auto generate a canned PPT based on a set of metrics that were pulled via a CollectionPlan
import os, metrics, collectionplan
from pptx import Presentation
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches
from pptx.util import Pt
from collections import deque

#Create a metric slide
def create_metric_slide(prs,metric):
    #metric info
    category =  metric['timeSeries'][0]['metadata']['attributes']['category']
    #determine if service
    if category == 'SERVICE':
        service_name = metric['timeSeries'][0]['metadata']['attributes']['serviceDisplayName']
    else:
        service_name = 'Cluster'

    metric_name = metric['timeSeries'][0]['metadata']['metricName']
    formatted_metric_name = ''
    #format the metric name and capitalize first letters
    metric_name_arr = metric_name.split("_")
    for word in metric_name_arr:
        formatted_metric_name += word.title() + " "
    
    metric_name = formatted_metric_name
         
    unit_type = metric['timeSeries'][0]['metadata']['unitNumerators'][0]
    numerator = metric['timeSeries'][0]['metadata']['unitNumerators'][0]
    denominators = metric['timeSeries'][0]['metadata']['unitDenominators']
    
    timestamps = deque()
    values = deque()
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    for point in metric['timeSeries'][0]['data']:
        formatted_timestamp = point['timestamp'].split("T")
        timestamps.append(formatted_timestamp[0])
        if unit_type == 'bytes':
            #value_in_mb = float(point['aggregateStatistics']['max'])/(1024*1024))
            value_in_gb = float(point['aggregateStatistics']['max'])/(1024*1024*1024)
            values.append(value_in_gb)
            numerator = 'gigabytes' 
        else:
            values.append(point['aggregateStatistics']['max'])
    
    #determine what our measurement (IE bytes/sec or just queries)
    if len(denominators) > 0:
        denominator = metric['timeSeries'][0]['metadata']['unitDenominators'][0]
        measurement = numerator + '/' + denominator
    else:
        denominator = 'None'
        measurement = numerator

    # change title and properties
    title = slide.shapes.title
    title.text = service_name + " " + metric_name
    title.text_frame.paragraphs[0].font.name = "calibri"
    title.text_frame.paragraphs[0].font.size = Pt(28)

    # define chart data ---------------------
    chart_data = ChartData()
    chart_data.categories = timestamps
    chart_series_title = measurement
    chart_data.add_series(chart_series_title, values)
    

    # add chart to slide --------------------
    x, y, cx, cy = Inches(0.5), Inches(1.4), Inches(9), Inches(6.0)
    chart =  slide.shapes.add_chart(XL_CHART_TYPE.LINE, x, y, cx, cy, chart_data)
    
    # sets chart plot to all be the same color (default in PPT is all different colors by category)
    plot = chart.chart.plots[0]
    plot.vary_by_categories = False

    # change axis properties
    category_axis = chart.chart.category_axis
    value_axis = chart.chart.value_axis

    # change axis font properties
    category_axis.tick_labels.font.name = "calibri"
    category_axis.tick_labels.font.size = Pt(11)
    value_axis.tick_labels.font.name = "calibri"
    value_axis.tick_labels.font.size = Pt(11)
   
    # change legend properties
    chart.chart.has_legend = True
    chart.chart.legend.include_in_layout = False
    chart.chart.legend.font.name = "calibri"
    chart.chart.legend.font.size = Pt(11)
    return

#Create a service slide
def create_service_slide():
    return

#Create a summary slide
def create_summary_slide():
    return

#Create a title slide
def create_title_slide(prs):
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = "Clouderasizer"
    subtitle.text = "Created by Brandon Kvarda"
    return 

#Parse pptplan
def parse_pptplan(pptplan):
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
    
    #Instantiate presentation
    prs = Presentation()
    
    #create the title slide
    create_title_slide(prs)
    #create metric slide for each metric
    for metric in collection:
        create_metric_slide(prs,metric)    
    
    #save output
    output_file = output_dir + '/' + 'test.pptx'
    prs.save(output_file)


