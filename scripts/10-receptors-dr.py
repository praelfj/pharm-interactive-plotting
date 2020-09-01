"""
dose response interactive plot
"""
import numpy as np

from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, Label, Span
from bokeh.plotting import figure, output_file, show, ColumnDataSource

import pharmaplot.receptors as rec
from pharmaplot.config import html_output_dir


# generate bokeh plot using the following data
log_start = -9
log_end = -3
top = 100
bottom = 0
hillslope = 1
logec50 = -6

x_line = np.linspace(log_start, log_end, num=100)
y_line = rec.four_parameter_logistic_equation(x_line, top, bottom, hillslope, logec50)

x_points = np.linspace(log_start, log_end, num=16)
y_points = rec.four_parameter_logistic_equation(x_points, top, bottom, hillslope, logec50)

# set up source data and plot lines that will vary
line_source = ColumnDataSource(data=dict(x=x_line, y=y_line))
point_source = ColumnDataSource(data=dict(x=x_points, y=y_points))

plot = figure(y_range=(-5, 205), plot_width=600, plot_height=400,
              x_axis_label='log[agonist (M)]',
              y_axis_label='% Response',
              title='Dose Response Curve')

plot.line('x', 'y', source=line_source, line_width=3, line_alpha=0.6, color='black')
plot.circle('x', 'y', source=point_source, size=10, color='black')

# set up static line and annotations
plot.line(x_line, y_line, line_width=5, color='blue', line_alpha=0.3)
plot.circle(x_points, y_points, size=10, color='blue', line_alpha=0.3)

mytext = Label(x=-6.5, y=105, text='Top=100, Bottom=0, pEC50=6, Hill=1',
               text_color="blue", text_alpha=0.5)
plot.add_layout(mytext)

# add axes lines
vline = Span(location=0, dimension='height', line_color='black', line_width=1, line_alpha=0.3)
hline = Span(location=0, dimension='width', line_color='black', line_width=1, line_alpha=0.3)
plot.renderers.extend([vline, hline])

# set up java script callback function to make plot interactive
top_slider = Slider(start=0, end=200, value=100, step=5, title="Top Response (%)")
bottom_slider = Slider(start=0, end=200, value=0, step=5, title="Bottom Response (%)")
ec50_slider = Slider(start=3, end=8, value=6, step=0.1, title="pEC50")
hill_slider = Slider(start=0.1, end=4, value=1, step=0.1, title="Hill Coefficient")

callback = CustomJS(args=dict(LineSource=line_source,
                              PointSource=point_source,
                              top=top_slider,
                              bottom=bottom_slider,
                              ec50=ec50_slider,
                              hill=hill_slider),
                    code="""
    const LineData = LineSource.data;
    const PointData = PointSource.data;
    const TOP = top.value;
    const BOTTOM = bottom.value;
    const EC50 = ec50.value;
    const HILL = hill.value;
    const lx = LineData.x;
    const ly = LineData.y;
    const px = PointData.x;
    const py = PointData.y;

    // define function(s) for editing data
    function fpl(x, top, bottom, ec50, hillslope){
        return (bottom + ((top - bottom) / (1 + Math.pow(10, ((ec50 + x) * hillslope * -1)))));
    }

    // loop over data and edit
    for (var i = 0; i < lx.length; i++) {
        ly[i] = fpl(lx[i], TOP, BOTTOM, EC50, HILL);
    }

    for (var i = 0; i < px.length; i++) {
        py[i] = fpl(px[i], TOP, BOTTOM, EC50, HILL);
    }

    // emit changes
    LineSource.change.emit();
    PointSource.change.emit();
""")

# add sliders to plot and display
top_slider.js_on_change('value', callback)
bottom_slider.js_on_change('value', callback)
ec50_slider.js_on_change('value', callback)
hill_slider.js_on_change('value', callback)

layout = row(
    plot,
    column(top_slider, bottom_slider, ec50_slider, hill_slider),
)

output_file(html_output_dir + "10-receptors-dr.html",
            title="Dose Response")
show(layout)
