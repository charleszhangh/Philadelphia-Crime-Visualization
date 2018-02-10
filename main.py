"""
Created January 6th, 2018
Program: Visualizes various countries' music preferences for acousticness, danceability, energy, and valence.
@author: Charles Zhang
"""

from bokeh.io import curdoc
import datetime
import pandas as pd
import math
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column, widgetbox, row
from bokeh.models import CustomJS, ColumnDataSource, HoverTool, Range1d, Tool
from bokeh.models.glyphs import ImageURL
import numpy as np
from bokeh.models.widgets import Slider, Div, Select, RangeSlider, MultiSelect, DataTable, TableColumn, TextInput, DateRangeSlider, Paragraph, DatePicker
from bokeh.models.annotations import Title
from os.path import join, dirname
from bokeh.core.properties import field

url = "Philadelphia-Crime-Visualization/static/2006_all.png"
N = 1
desc = Div(text=open(join(dirname(__file__), 'description.html')).read(), width=400)
# source = ColumnDataSource(dict(
#     url = [url]
# ))

def get_dataset(src):
    new_dict = dict(url = [src])
    return ColumnDataSource(data=new_dict)
source = get_dataset(url)
def make_plot():

    xdr = Range1d(start=0, end=1100)
    ydr = Range1d(start=0, end=750)
    p = figure(
        title=None, x_range=xdr, y_range=ydr, plot_width=1100, plot_height=750,
        h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location=None)

    #p = figure(x_range=(0,1000), y_range=(0,1000))
    image1 = ImageURL(url="url", x=0, y=0, w=900, h=750, anchor="bottom_left")
    p.add_glyph(source, image1)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    #p.image_url(url=['crime20.png'], x=0, y=1,w=750, h=650)
    #p.add_glyph(image1)
    return p

#event handlers below makes changes to Slider values
def update_data(attrname, old, new):
    crime = crime_select.value
    year = year_slider.value
    str_crime = ""

    if (crime == "All"):
        str_crime = "all"
    elif (crime == "Aggravated Assault or Homicide"):
        str_crime = "homicide"
    elif (crime == "Driving Under The Influence"):
        str_crime = "driving"
    elif (crime == "Drug Or Narcotics Use"):
        str_crime = "drug"
    elif (crime == "Fraud"):
        str_crime = "fraud"
    elif (crime == "Sex Offenses"):
        str_crime = "sex"
    elif (crime == "Theft"):
        str_crime = "theft"
    elif (crime == "Vandalism"):
        str_crime = "vandalism"
    elif (crime == "Robbery"):
        str_crime = "robbery"
    elif (crime == "Other Assaults"):
        str_crime = "otherassaults"
    elif (crime == "All Other Offenses"):
        str_crime = "otheroffenses"

    new_url = "Philadelphia-Crime-Visualization/static/" + str(year) + "_" + str_crime + ".png"
    #print(new_url)
    new_source = get_dataset(new_url)
    source.data.update(new_source.data)

# creates Sliders and Selectors
year_slider = Slider(start=2006, end=2017, value=2006, step=1, title="Year")


crime_select = Select(title="Crime:", value = "All", options=["All","Aggravated Assault or Homicide",
                                                              "Driving Under The Influence","Drug Or Narcotics Use",
                                                              "Fraud","Sex Offenses","Theft","Vandalism","Robbery",
                                                              "Other Assaults","All Other Offenses"])

plot = make_plot()

for w in [year_slider]:
    w.on_change('value', update_data)

for w in [crime_select]:
    w.on_change('value', update_data)

info = column(desc,year_slider,crime_select)

page = row(info, plot)
curdoc().add_root(page)
curdoc().title = "Philadelphia Crime Map"