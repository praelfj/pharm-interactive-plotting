"""
single plot with specific binding + hill coefficient
"""
import numpy as np

from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, Label, Span
from bokeh.plotting import figure, output_file, show, ColumnDataSource

import pharmaplot.receptors as rec
from pharmaplot.config import html_output_dir

## generate bokeh plot using the following data
log_start = -9
log_end = -3
bmax = 100
kd = 1e-6
hill = 1

x_line = np.logspace(log_start, log_end, num=100)
x_log_line = np.log10(x_line)
y_line = rec.specific_binding_hill(x_line, bmax, kd, hill)

x_points = np.logspace(log_start, log_end, num=16)
x_log_points = np.log10(x_points)
y_points = rec.specific_binding_hill(x_points, bmax, kd, hill)

# set up source data and plot lines that will vary
line_source = ColumnDataSource(data=dict(x=x_line, y=y_line, x_log=x_log_line))
point_source = ColumnDataSource(data=dict(x=x_points, y=y_points, x_log=x_log_points))

plot = figure(x_range=(-9.1, -2.9), y_range=(-10, 210), plot_width=600, plot_height=400,
              x_axis_label='log[compound (M)]',
              y_axis_label='Specific Binding',
              title='Specific Binding')

plot.line('x_log', 'y', source=line_source, line_width=3, line_alpha=0.6, color='black')
plot.circle('x_log', 'y', source=point_source, size=10, color='black')

# set up static line and annotations
plot.line(x_log_line, y_line, line_width=5, color='blue', line_alpha=0.3)
plot.circle(x_log_points, y_points, size=10, color='blue', line_alpha=0.3)

mytext = Label(x=-5.2, y=110, text='log(Kd) = -6, Bmax = 100',
               text_color="blue", text_alpha=0.5)
plot.add_layout(mytext)

# add axes lines
vline = Span(location=0, dimension='height', line_color='black', line_width=1, line_alpha=0.3)
hline = Span(location=0, dimension='width', line_color='black', line_width=1, line_alpha=0.3)
plot.renderers.extend([vline, hline])

# set up java script callback function to make plot interactive
bmax_slider = Slider(start=0, end=200, value=100, step=10, title="Bmax")
pkd_slider = Slider(start=-8, end=-3, value=-6, step=0.1, title="log[Kd (M)]")
hill_slider = Slider(start=0.1, end=4, value=1, step=0.1, title="Hill Coefficient]")

callback = CustomJS(args=dict(LineSource=line_source,
                              PointSource=point_source,
                              bmax=bmax_slider,
                              kd=pkd_slider,
                              hill=hill_slider),
                    code="""
    const LineData = LineSource.data;
    const PointData = PointSource.data;
    const BMAX = bmax.value;
    const KD = Math.pow(10, kd.value);
    const HILL = hill.value;
    const lx = LineData.x;
    const ly = LineData.y;
    const px = PointData.x;
    const py = PointData.y;

    // define function(s) for editing data
    function sb(x, BMAX, KD, HILL){
        return (Math.pow(x, HILL)*BMAX)/(Math.pow(x, HILL)+ Math.pow(KD, HILL));
    }

    // loop over data and edit
    for (var i = 0; i < lx.length; i++) {
        ly[i] = sb(lx[i], BMAX, KD, HILL);
    }

    for (var i = 0; i < px.length; i++) {
    py[i] = sb(px[i], BMAX, KD, HILL);
    }

    // emit changes
    LineSource.change.emit();
    PointSource.change.emit();
""")

# add sliders to plot and display
bmax_slider.js_on_change('value', callback)
pkd_slider.js_on_change('value', callback)
hill_slider.js_on_change('value', callback)

layout = row(
    plot,
    column(bmax_slider, pkd_slider, hill_slider),
)

output_file(html_output_dir + "08-receptors-sb-hill.html",
            title="Saturation Binding Curve with Cooperativity")
show(layout)