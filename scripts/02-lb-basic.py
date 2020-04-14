"""
script for generating a linewevaer-burk interactive plot
"""
import numpy as np
from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, Label, Span
from bokeh.plotting import figure, output_file, show, ColumnDataSource

from pharmaplot import mm
from pharmaplot.config import html_output_dir


# make data for the plot
vmax = 10
km = 1

x_points = 1 / np.geomspace(0.1, 10, num=8)
y_points = mm.lineweaver_burk(x_points, vmax, km)

x_line = np.linspace(-3, np.max(x_points))
y_line = mm.lineweaver_burk(x_line, vmax, km)

# set up source data and plot lines that will vary
line_source = ColumnDataSource(data=dict(x=x_line, y=y_line))
point_source = ColumnDataSource(data=dict(x=x_points, y=y_points))

plot = figure(y_range=(-0.05, 0.8), x_range=(-1.5, 4), plot_width=600, plot_height=400,
              x_axis_label='1/[S]: substrate concentration (1/μM)',
              y_axis_label='1/initial velocity (s/μM)',
              title='Lineweaver-Burk Kinetics')

plot.line('x', 'y', source=line_source, line_width=3, line_alpha=0.6, color='black')
plot.circle('x', 'y', source=point_source, size=10, color='black')

# add axes lines
vline = Span(location=0, dimension='height', line_color='black', line_width=1, line_alpha=0.3)
hline = Span(location=0, dimension='width', line_color='black', line_width=1, line_alpha=0.3)
plot.renderers.extend([vline, hline])

# set up static line and annotations
plot.line(x_line, y_line, line_width=5, color='blue', line_alpha=0.3)
plot.circle(x_points, y_points, size=10, color='blue', line_alpha=0.3)

mytext = Label(x=0.3, y=0.4, text='Km = 1 (μM), Vmax = 10 (μM/s)',
               text_color="blue", text_alpha=0.5)
plot.add_layout(mytext)

# set up java script callback function to make plot interactive
vmax_slider = Slider(start=3, end=50, value=10, step=1, title="Vmax (μM/s)")
km_slider = Slider(start=0.1, end=4, value=1, step=0.1, title="Km (μM)")

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
        ly[i] = ((KM/VMAX)*lx[i]) + (1/VMAX);
    }
    LineSource.change.emit();
    for (var i = 0; i < px.length; i++) {
    py[i] = ((KM/VMAX)*px[i]) + (1/VMAX);
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

output_file(html_output_dir + "02-lb-basic.html", title="Lineweaver-Burk Plot")
show(layout)
