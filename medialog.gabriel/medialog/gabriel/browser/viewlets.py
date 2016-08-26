#plone stuff
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#from plone import api
from zope.i18nmessageid import MessageFactory

import urllib

#plotly stuff
import plotly 
from plotly.graph_objs import Bar, Scatter, Figure, Layout,  Surface
from plotly.tools import FigureFactory as FF
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

import json
import datetime 

class PlotView(ViewletBase):
    """ plot something """

    @property
    def plotly_html(self):
        """return the html generated from plotly"""

        context = self.context
        
        if not context.plotly_html:
            self.make_plot()
        
        return context.plotly_html
        
        
        
class GraphView(ViewletBase):
    """ return graph for current day """
    
    def yesterday(self):
        return datetime.date.today() - datetime.timedelta(1)
    
    def graph(self):
        """return the html generated from plotly"""
        
        context = self.context        
        #today we will show yesterdays graph
        yesterday = datetime.date.today() - datetime.timedelta(1)
        
        if context.dato != yesterday:  
            dtype = context.dtype
            trace = []
       
            date = yesterday.strftime("%Y%m%d")
            day_url = 'http://146.185.167.10/resampledday/%s/' %dtype
            #on its own line, in case of looping
            json_url = day_url + date + '.json'
            f = urllib.urlopen(json_url)   
            jsonfile=f.read()
            daydata=json.loads(jsonfile)
            df = pd.DataFrame(daydata)
            xaxis = df['ts'].replace(to_replace=':00:00 GMT', value='', regex=True)
            df.head()
            this_dive = pd.DataFrame(df['divedata'].values.tolist())
    
            #seven dives a day, usually
            for i in range(1,this_dive.shape[1]):
                this_preassure = pd.DataFrame(this_dive[i-1].values.tolist())
                name=str(this_preassure['pressure(dBAR)'][0])
                graphname = name + ' dBar '
        
                # Create a trace
                trace.append(go.Scatter(
                            x = xaxis,
                            y = this_preassure[dtype],
                            name = graphname,
                ))
            
            layout = go.Layout(
                height=1000,
                width=1200,
                autosize=True,
                xaxis=dict(
                title='Tidspunkt',
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                ),
                yaxis=dict(
                    title='Verdi',
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                )
            )
    
            fig = go.Figure(data=trace)
            plotly_html = plotly.offline.plot(fig, show_link=False, include_plotlyjs = False, output_type='div')

            #and now the 3D graph
            z = []
        
            #construct the 3d z
            for i in range(0,len(df)):
                this_z = pd.DataFrame(df['divedata'][i]).sort_values('pressure(dBAR)', ascending=True)
                z.append(this_z[dtype])
                #.values.tolist())

            data = [
                go.Surface(
                z=  z,
                x= pd.DataFrame(df['divedata'][0])['pressure(dBAR)'].sort_values(),
                y = df['ts']
                )
            ]

            layout = go.Layout(
                autosize=True,
                scene=dict(
                    xaxis=dict(
                        title="Dybde"
                    ),
                    yaxis=dict(
                        title="Tid"
                    )
                ),
                width=900,
                height=1000,
                margin=dict(
                    l=5,
                    r=5,
                    b=5,
                    t=9
                )
            )

            fig = go.Figure(data=data, layout=layout)
            plotly_html += plotly.offline.plot(fig, show_link=False, include_plotlyjs = False, output_type='div')
            context.plotly_html = plotly_html
            context.dato = yesterday
        
        return context.plotly_html
        
        