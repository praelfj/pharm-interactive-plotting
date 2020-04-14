"""
same as 01-mm-basic, except scatter plot point shave been added and axes have been changed to extend plots
"""
import numpy as np
from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, Label, Span
from bokeh.plotting import figure, output_file, show, ColumnDataSource

from pharmaplot import mm
from pharmaplot.config import html_output_dir

# create data for plot
log_start = -1
log_end = 3
vmax = 100
km = 10

x_line = np.logspace(log_start, log_end, num=100)
y_line = mm.michaelis_menten(x_line, vmax, km)

x_points = np.logspace(log_start, log_end, num=20)
y_points = mm.michaelis_menten(x_points, vmax, km)

# set up source data and plot lines that will vary
line_source = ColumnDataSource(data=dict(x=x_line, y=y_line))
point_source = ColumnDataSource(data=dict(x=x_points, y=y_points))

plot = figure(y_range=(-5, 200), x_range=(-5, 100), plot_width=600, plot_height=400,
              x_axis_label='[S]: substrate concentration (μM)',
              y_axis_label='initial velocity (μM/s)',
              title='Michaelis-Menten Kinetics')

plot.line('x', 'y', source=line_source, line_width=3, line_alpha=0.6, color='black')
plot.circle('x', 'y', source=point_source, size=10, color='black')

# set up static line and annotations
plot.line(x_line, y_line, line_width=5, color='blue', line_alpha=0.3)
plot.circle(x_points, y_points, size=10, color='blue', line_alpha=0.3)

mytext = Label(x=50, y=70, text='Km = 10 (μM), Vmax = 100 (μM/s)',
               text_color="blue", text_alpha=0.5)
plot.add_layout(mytext)

# add axes lines
vline = Span(location=0, dimension='height', line_color='black', line_width=1, line_alpha=0.3)
hline = Span(location=0, dimension='width', line_color='black', line_width=1, line_alpha=0.3)
plot.renderers.extend([vline, hline])

# set up java script callback function to make plot interactive
vmax_slider = Slider(start=0, end=200, value=100, step=1, title="Vmax (μM/s)")
km_slider = Slider(start=1, end=100, value=10, step=1, title="Km (μM)")

callback = CustomJS(args=dict(LineSource=line_source,
                              PointSource=point_source,
                              vmax=vmax_slider,
                              km=km_slider),
                    code="""
    const LineData = LineSource.data;
    const PointData = PointSource.data;
    const VMAX = vmax.value;
    const KM = km.value;
    const lx = LineData['x']
    const ly = LineData['y']
    const px = PointData['x']
    const py = PointData['y']
    for (var i = 0; i < lx.length; i++) {
        ly[i] = (VMAX*lx[i])/(KM+lx[i]);
    }
    LineSource.change.emit();
    for (var i = 0; i < px.length; i++) {
    py[i] = (VMAX*px[i])/(KM+px[i]);
    }
    PointSource.change.emit();
""")

# add sliders to plot and display
vmax_slider.js_on_change('value', callback)
km_slider.js_on_change('value', callback)

layout = row(
    plot,
    column(vmax_slider, km_slider),
)

output_file(html_output_dir + "01b-mm-scatter.html", title="Michaelis Menten Kinetics")
show(layout)
