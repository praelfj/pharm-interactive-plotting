"""
basic Michaelis-Menten plot where Vmax and Km can be varied
"""
import os
import sys
import numpy as np

from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, Label
from bokeh.plotting import figure, output_file, show, ColumnDataSource

root_dir = os.path.join(os.getcwd(), '..')
sys.path.append(root_dir)

from pharmaplot import mm
from pharmaplot.config import html_output_dir

# generate fake data
x = np.logspace(-3, 2, num=500)
y = mm.michaelis_menten(x, 100, 10)

# generate bokeh plot using the above data

# set up source data and plot lines that will vary
source = ColumnDataSource(data=dict(x=x, y=y))

plot = figure(y_range=(0, 200), plot_width=600, plot_height=400,
              x_axis_label='substrate concentration (μM)',
              y_axis_label='initial velocity (μM/s)',
              title='Michaelis-Menten Kinetics')

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6, color='black')

# set up static line and annotations
plot.line(x, y, line_width=5, color='blue', line_alpha=0.3)

mytext = Label(x=50, y=70, text='Km = 10 (μM), Vmax = 100 (μM/s)',
               text_color="blue", text_alpha=0.5)
plot.add_layout(mytext)

# set up java script callback function to make plot interactive
vmax_slider = Slider(start=0.1, end=200, value=100, step=1, title="Vmax (μM/s)")
km_slider = Slider(start=1, end=100, value=10, step=1, title="Km (μM)")

callback = CustomJS(args=dict(source=source,
                              vmax=vmax_slider,
                              km=km_slider),
                    code="""
    const data = source.data;
    const VMAX = vmax.value;
    const KM = km.value;
    const x = data['x']
    const y = data['y']
    for (var i = 0; i < x.length; i++) {
        y[i] = (VMAX*x[i])/(KM+x[i]);
    }
    source.change.emit();
""")

# add sliders to plot and display
vmax_slider.js_on_change('value', callback)
km_slider.js_on_change('value', callback)

layout = row(
    plot,
    column(vmax_slider, km_slider),
)

output_file(html_output_dir + "01-mm-basic.html")
show(layout)
