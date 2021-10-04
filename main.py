import pandas as pd
import numpy as np
import bokeh

from bokeh.layouts import column, gridplot
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, StringFormatter

# Process the data from the CDSS file
cf_data = pd.read_excel('cf_cc_dash/CFDashboardData.xlsx',header=1)

# FIlter out for Contra Costa County
contra_costa_data = cf_data.query('County == "Contra Costa"')

# Keep only the columns I'm interested in
Calfresh_households = contra_costa_data[['County','Month',
'Date','Calendar Year','Federal Fiscal Year',
'State Fiscal Year','CalFresh Households','CalFresh Persons',
'All Public Assistance Households','All Non-Assistance Households']]

# Set the ColumnDataSource as the dataframe

source = ColumnDataSource(Calfresh_households)

# Create the table, and add alignment for the numerical values using
# the formatter from the Bokeh api.
columns = [
        TableColumn(field="Month", title="Month"),
        TableColumn(field="Calendar Year", title="Calendar Year",
                formatter=StringFormatter(text_align="right")),
        TableColumn(field="CalFresh Households", title="CalFresh Households",
                formatter=NumberFormatter(text_align="right")),
        TableColumn(field="CalFresh Persons", title="CalFresh Persons",
                formatter=NumberFormatter(text_align="right")),
    ]


# Set up the table variable for the dashboard
full_table = DataTable(source=source, columns=columns, height=280,
                      index_position=None, name="table",
                      sizing_mode='stretch_both',
                      selectable=False)
# Customize tool tip
TOOLTIPS = """
<div class="plot-tooltip">
    <div>
        <h5>@{Calendar Year}</h5>
    </div>
    <div>
        Month: @Month
    </div>
    <div>
        Persons: @{CalFresh Persons}{0,000}
    </div>
</div>
"""
# Create the first chart using the number of people on CalFresh
chart = figure(x_axis_type="datetime" , plot_height=250, title="CalFresh persons since 2014",
           toolbar_location=None, tools="xpan", tooltips=TOOLTIPS,
           name="chart")
chart.xgrid.grid_line_color = None
chart.y_range.start = 0
chart.line('Date','CalFresh Persons', source=source)
# Customize the tooltip to match above
Household_tooltips = """
<div class="plot-tooltip">
    <div>
        <h5>@{Calendar Year}</h5>
    </div>
    <div>
        Month: @Month @{Calendar Year}
    </div>
    <div>
        Households: @{CalFresh Households}{0,000}
    </div>
</div>
"""
# Create a chart with the number of households
hh_chart = figure(x_axis_type="datetime" ,plot_height=250, title="CalFresh households since 2014",
           toolbar_location=None, tools="xpan", tooltips=Household_tooltips,
           name="hh_chart")
hh_chart.xgrid.grid_line_color = None
hh_chart.y_range.start = 0
hh_chart.line('Date','CalFresh Households', source=source)

# Add this to the main file.

curdoc().add_root(hh_chart)
curdoc().add_root(chart)
curdoc().add_root(full_table)
