from plone import api
from zope.i18nmessageid import MessageFactory

import urllib

#plotly stuff
import plotly 
from plotly.graph_objs import Bar, Scatter, Figure, Layout
from plotly.tools import FigureFactory as FF
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import cufflinks as cf
import json

from Products.statusmessages.interfaces import IStatusMessage

_ = MessageFactory('medialog.plotly')
 

def login(self):
    username = self.portal_registry['medialog.plotly.interfaces.IPlotlySettings.plotly_username']
    api_key  = self.portal_registry['medialog.plotly.interfaces.IPlotlySettings.plotly_api_key']
    plotly.tools.set_credentials_file(username=username, api_key=api_key)
    


def make_html(self, context):
    """let plottly make the graph
    generating the html from plotly"""
    
    #dont need login for offline
    #self.login()
    
    date = self.date.strftime("%Y%m%d")
    dtype = str(self.dtype)
    dybder = self.dybder
    figure_title = date + dtype
    trace=[]
    
    day_url = 'http://146.185.167.10/resampledday/%s/' %dtype
    #on its own line, in case of looping
    json_url = day_url + date + '.json'
    
    f = urllib.urlopen(json_url)   
    jsonfile=f.read()
    daydata=json.loads(jsonfile)
    df = pd.DataFrame(daydata)
    xaxis = df['ts']
    df.head()
    this_dive = pd.DataFrame(df['divedata'].values.tolist())
    
    #seven dives a day
    for i in range(1,this_dive.shape[1]):
        this_preassure = pd.DataFrame(this_dive[i-1].values.tolist())
        name=this_preassure['pressure(dBAR)'][0]
        
        #visible = "legendonly"
        visible = False
        if unicode(name) in dybder:
            visible = True 
             
        # Create a trace
        trace.append(go.Scatter(
                x = xaxis,
                y = this_preassure[dtype],
                name = name,
                visible = visible,
        ))
            
    layout = go.Layout(
        height=500,
        title = (figure_title)
    )
        
    fig = go.Figure(data=trace)
    self.plotly_html = plotly.offline.plot(fig, show_link=False, include_plotlyjs = False, output_type='div')
        
