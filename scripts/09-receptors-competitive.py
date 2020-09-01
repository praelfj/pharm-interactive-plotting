"""
competitive radioligand binding curve interactive plot
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
nonspecific = 0
total = 100
pIC50 = 6
nH = 1

x_line = np.linspace(log_start, log_end, num=100)
y_line = rec.competitive_binding(x_line, nonspecific, total, pIC50, nH)

x_points = np.linspace(log_start, log_end, num=16)
y_points = rec.competitive_binding(x_points, nonspecific, total, pIC50, nH)

# set up source data and plot lines that will vary
line_source = ColumnDataSource(data=dict(x=x_line, y=y_line))
point_source = ColumnDataSource(data=dict(x=x_points, y=y_points))

plot = figure(y_range=(-10, 115), plot_width=600, plot_height=400,
              x_axis_label='log[competitor (M)]',
              y_axis_label='% Specific Binding of Radioligand',
              title='Competitive Inhibition')

plot.line('x', 'y', source=line_source, line_width=3, line_alpha=0.6, color='black')
plot.circle('x', 'y', source=point_source, size=10, color='black')

# set up static line and annotations
plot.line(x_line, y_line, line_width=5, color='blue', line_alpha=0.3)
plot.circle(x_points, y_points, size=10, color='blue', line_alpha=0.3)

mytext = Label(x=-7, y=105, text='pIC50 = 6, Hill Coefficient = 1',
               text_color="blue", text_alpha=0.5)
plot.add_layout(mytext)

# add axes lines
vline = Span(location=0, dimension='height', line_color='black', line_width=1, line_alpha=0.3)
hline = Span(location=0, dimension='width', line_color='black', line_width=1, line_alpha=0.3)
plot.renderers.extend([vline, hline])

# set up java script callback function to make plot interactive
pIC50_slider = Slider(start=3, end=8, value=6, step=0.1, title="pIC50")
hill_slider = Slider(start=0.1, end=4, value=1, step=0.1, title="Hill Coefficient")

callback = CustomJS(args=dict(LineSource=line_source,
                              PointSource=point_source,
                              pic50=pIC50_slider,
                              hill=hill_slider),
                    code="""
    const LineData = LineSource.data;
    const PointData = PointSource.data;
    const PIC50 = pic50.value;
    const HILL = hill.value;
    const lx = LineData.x;
    const ly = LineData.y;
    const px = PointData.x;
    const py = PointData.y;
    const TOTAL = 100;
    const NONSPECIFIC = 0;

    // define function(s) for editing data
    function competitive(x, nonspecific, total, pIC50, nH){
        return (nonspecific + (total - nonspecific)/(1 + Math.pow(10, nH*(pIC50 + x))));
    }

    // loop over data and edit
    for (var i = 0; i < lx.length; i++) {
        ly[i] = competitive(lx[i], NONSPECIFIC, TOTAL, PIC50, HILL);
    }

    for (var i = 0; i < px.length; i++) {
    py[i] = competitive(px[i], NONSPECIFIC, TOTAL, PIC50, HILL);
    }

    // emit changes
    LineSource.change.emit();
    PointSource.change.emit();
""")

# add sliders to plot and display
pIC50_slider.js_on_change('value', callback)
hill_slider.js_on_change('value', callback)

layout = row(
    plot,
    column(pIC50_slider, hill_slider),
)

output_file(html_output_dir + "09-receptors-competitive.html",
            title="Competitive Inhibition")
show(layout)
