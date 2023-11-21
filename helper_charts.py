import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from datetime import datetime, timedelta,date
import numpy as np
from sys import getsizeof
import datetime
import math
from IPython.display import display, Markdown, HTML
from bokeh.io import output_file, show
from bokeh.plotting import figure, output_notebook
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, DataRange1d, LinearAxis, Range1d
from bokeh.models.tools import HoverTool
from bokeh.palettes import Category20, Viridis
from bokeh.core.properties import value
from bokeh.transform import factor_cmap, dodge
from bokeh.layouts import row
from bokeh.models import NumeralTickFormatter
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import layout, row, column, Spacer, widgetbox
from datetime import datetime
import scipy.stats as stats
import matplotlib.pyplot as plt
import base64
import ast
output_notebook(hide_banner = True)
pd.set_option('display.max_columns',500)
pd.set_option('display.max_rows',30)


class helper_charts():
    def __init__(self, width = 3, aspect_ratio = 2.75, label_font = '6pt'):
        self.width = width
        self.aspect_ratio = aspect_ratio
        self.label_font = label_font

    def width_adjust(self,new_val):
        self.width = new_val

    def width_default(self):
        self.width = 3

    def df_dl(self, df, title = 'Download', filename = 'Download'):
        csv = df.to_csv()
        b64 = base64.b64encode(csv.encode())
        payload = b64.decode()
        html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
        html = html.format(payload=payload, title=title, filename=filename)
        display(HTML(html))
        
        
    def step_calculator(self, col_list):
        tot = len(col_list)*6
        try:
            step = int((tot*2)/(len(col_list)-1))
        except:
            return [0]
        return [i/100 for i in range(-tot,tot + 1,step)]
    
    def parse_tuple(self, string):
        try:
            s = ast.literal_eval(str(string))
            if type(s) == tuple:
                return s
            return
        except:
            return
        
    def chart_setter(self, fig_name, df, col_list, layout = 'horizontal', hover_param = 'multiple'):
        hover = HoverTool()
        if hover_param == 'multiple':
            a = []
            for x in col_list:
                if 'date' in x.lower():
                    a.append("('" + x + "','@" + x + "{%Y-%m-%d}')")
                else:
                    a.append("('" + x + "','@" + x + "')")
            if 'date' in col_list[0].lower():
                hover.tooltips = list(self.parse_tuple(','.join(a)))
                hover.formatters = {'@' + col_list[0]:'datetime'}
            else:
                hover.tooltips = list(self.parse_tuple(','.join(a)))
        else:
            if 'date' in col_list[0].lower():
                hover.tooltips=[
                    ("" + col_list[0].title() + "", "@" + col_list[0] + "{%Y-%m-%d}"),
                   ('Metric', '$name'), #$name provides data from legend
                   ('Value', '@$name{0.00}')#@$name gives the value corresponding to the legend
        #             ("Value", "$y")
                ]
                hover.formatters = {'@' + col_list[0]:'datetime'}
            else:
                hover.tooltips=[
                    ("" + col_list[0].title() + "", "@" + col_list[0]),
                   ('Metric', '$name'), #$name provides data from legend
                   ('Value', '@$name{0.00}')#@$name gives the value corresponding to the legend
        #             ("Value", "$y")
                ]
    
        fig_name.add_tools(hover)
        
    ###################################################################################Chart Formats###################################################################################
    
        fig_name.sizing_mode = 'scale_width'
        fig_name.xaxis.major_label_orientation = math.pi/2
        fig_name.left[0].formatter.use_scientific = False
        #fig_name.y_range.start = 0
        
        if 'date' in col_list[0].lower():
            fig_name.xaxis.formatter=DatetimeTickFormatter(
                months=["%d %b %Y"],
                years=["%d %b %Y"],
            )            
    
    #################################################################################Legend Formatting###################################################################################
        
        if layout == 'horizontal':
            fig_name.legend.orientation = 'horizontal'
            fig_name.legend.click_policy = 'hide'
            fig_name.legend.location = 'center'
            fig_name.add_layout(fig_name.legend[0], 'below')
            fig_name.legend.label_text_font_size = self.label_font
            fig_name.aspect_ratio = self.aspect_ratio
            fig_name.y_range.range_padding = 0
        else:
            new_legend = fig_name.legend[0]
            fig_name.legend[0] = None
            fig_name.aspect_ratio = 1.75
            fig_name.add_layout(new_legend, 'right')
            fig_name.legend.label_text_font_size = '6pt'
            fig_name.legend.click_policy = 'hide'
            fig_name.y_range.range_padding = 0
            

    
    def line(self, df, x_col, y_col, title, y_col2 = '', layout = 'horizontal', hover_param = 'multiple'):
        color_cnt = 0
        self.width_default()
        ##################################################FIGURE FOR CHART##################################################
        
        if ('date' in x_col.lower() or df.loc[:,x_col].dtypes == 'int64'):
            p = figure(y_axis_label = 'Value' if type(y_col) == list else y_col.upper(), x_axis_label = x_col.upper(), title = title)
        else:
            p = figure(y_axis_label = 'Value' if type(y_col) == list else y_col.upper(), x_axis_label = x_col.upper(), title = title, x_range = df.loc[:,x_col])
        
        #########################################LOOP THROUGH ALL Y-PRIMARY COLUMNS#########################################
        
        for y_col_pos in y_col if type(y_col) == list else [y_col]:            
            p.line(x_col,
                    y = y_col_pos,
                    line_width =self.width,
                    source = df, 
                    line_color = Category20[20][color_cnt],
                    legend_label = y_col_pos.upper())
            color_cnt += 1
            
        #############################LOOP THROUGH ALL Y-SECONDARY COLUMNS(IF PROVIDED IN INPUT)#############################
        
        if y_col2 != '':
            
            display(Markdown("""#### Left Axis Columns: """ + ', '.join(y_col if type(y_col) == list else [y_col])))
            display(Markdown("""#### Right Axis Columns: """ + ', '.join(y_col2 if type(y_col2) == list else [y_col2])))
            
            color_cnt = 0
            
        ###################################################CALCULATE SECONDARY RANGES#######################################
        
            rng_start, rng_end = min(0,df.loc[:,y_col2].min().min()), \
            df.loc[:,y_col2].max().max() + 0.1 * df.loc[:,y_col2].max().max()
            
            p.extra_y_ranges = {"secondary_axis": Range1d(start=rng_start, end=rng_end)}
            p.add_layout(LinearAxis(y_range_name="secondary_axis"), 'right')
            
            for y_col2_pos in y_col if type(y_col2) == list else [y_col2]:
                p.line(x_col,
                    y = y_col2_pos,
                    line_width =self.width,
                    source = df, 
                    line_color = Category20[20][20 - color_cnt - 1],
                    y_range_name="secondary_axis",
                    legend_label = y_col2_pos.upper())
                color_cnt += 1
                
        if y_col2 == '':
            legend_cols = [x_col] + (y_col if type(y_col) == list else [y_col])
        else:
            legend_cols = [x_col] + (y_col if type(y_col) == list else [y_col]) + (y_col2 if type(y_col2) == list else [y_col2])

        ##########################################################CHART FORMAT##############################################
        
        rng_prim_start, rng_prim_end = min(0,df.loc[:,y_col].min().min()), \
            df.loc[:,y_col].max().max() + 0.1 * df.loc[:,y_col].max().max()
        
        self.chart_setter(p,df,legend_cols,layout,hover_param)
        
        p.y_range=Range1d(rng_prim_start, rng_prim_end)
        
        return p



    def vbar(self, df, x_col, y_col, title, y_col2 = '', layout = 'horizontal', hover_param = 'multiple'):
        color_cnt = 0
        dodge_cnt = 0
        ops_df = df.copy()
        ops_df.loc[:,x_col] = ops_df.loc[:,x_col].astype(str)
        self.width_adjust(0.1)
        
        if y_col2 == '':
            col_list = y_col if type(y_col) == list else [y_col]
        else:
            col_list = (y_col if type(y_col) == list else [y_col]) + (y_col2 if type(y_col2) == list else [y_col2])        
            
        ##################################################FIGURE FOR CHART##################################################
        
        p = figure(y_axis_label = 'Value' if type(y_col) == list else y_col.upper(), x_axis_label = x_col.upper(), title = title, x_range = ops_df.loc[:,x_col])
               
        dodge_pos = self.step_calculator(col_list)

        #########################################LOOP THROUGH ALL Y-PRIMARY COLUMNS#########################################
        
        for y_col_pos in y_col if type(y_col) == list else [y_col]:            
            p.vbar(x = dodge(x_col,dodge_pos[dodge_cnt] , range = p.x_range),
                    top = y_col_pos,
                    width = self.width,
                    source = ops_df, 
                    color = Category20[20][color_cnt],
                    legend = y_col_pos.upper())
            color_cnt += 1
            dodge_cnt += 1
            
        #############################LOOP THROUGH ALL Y-SECONDARY COLUMNS(IF PROVIDED IN INPUT)#############################
        
        if y_col2 != '':
            
            display(Markdown("""#### Left Axis Columns: """ + ', '.join(y_col if type(y_col) == list else [y_col])))
            display(Markdown("""#### Right Axis Columns: """ + ', '.join(y_col2 if type(y_col2) == list else [y_col2])))
            
            color_cnt = 0
            
        ###################################################CALCULATE SECONDARY RANGES#######################################
        
            rng_start, rng_end = min(0,ops_df.loc[:,y_col2].min().min()), \
            ops_df.loc[:,y_col2].max().max() + 0.1 * ops_df.loc[:,y_col2].max().max()
            
            p.extra_y_ranges = {"secondary_axis": Range1d(start=rng_start, end=rng_end)}
            p.add_layout(LinearAxis(y_range_name="secondary_axis"), 'right')
            
            for y_col2_pos in y_col if type(y_col2) == list else [y_col2]:
                p.vbar(x = dodge(x_col,dodge_pos[dodge_cnt] , range = p.x_range),
                        top = y_col2_pos,
                        width = self.width,
                        source = ops_df, 
                        color = Category20[20][20 - color_cnt - 1],
                        y_range_name="secondary_axis",
                        legend = y_col2_pos.upper())
                color_cnt += 1
                dodge_cnt += 1
            
                
        if y_col2 == '':
            legend_cols = [x_col] + (y_col if type(y_col) == list else [y_col])
        else:
            legend_cols = [x_col] + (y_col if type(y_col) == list else [y_col]) + (y_col2 if type(y_col2) == list else [y_col2])

        ##########################################################CHART FORMAT##############################################

        rng_prim_start, rng_prim_end = min(0,ops_df.loc[:,y_col].min().min()), \
            ops_df.loc[:,y_col].max().max() + 0.1 * ops_df.loc[:,y_col].max().max()
        
        self.chart_setter(p,ops_df,legend_cols,layout,hover_param)

        p.y_range=Range1d(rng_prim_start, rng_prim_end)
        
        return p















