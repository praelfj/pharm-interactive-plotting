"""
creates interactive html with dual saturation binding and scatchard transformation plots
"""
import numpy as np

from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, Label, Span
from bokeh.plotting import figure, output_file, show, ColumnDataSource

import pharmaplot.receptors as rec
from pharmaplot.config import html_output_dir

# -------------------------------------------------
# set common parameters to both plots
# -------------------------------------------------
# set plot parameters
pw = 500
ph = 400

# set shared data values
log_start = -9
log_end = -3
bmax = 100
kd = 1e-6

x_line = np.logspace(log_start, log_end, num=100)
x_log_line = np.log10(x_line)
y_line = rec.specific_binding(x_line, bmax, kd)

x_points = np.logspace(log_start, log_end, num=16)
x_log_points = np.log10(x_points)
y_points = rec.specific_binding(x_points, bmax, kd)

b_l, bf_l = rec.scatchard(x_line, bmax, kd)
b_p, bf_p = rec.scatchard(x_points, bmax, kd)

# -------------------------------------------------
# make specific binding plot
# -------------------------------------------------
# set up source data and plot lines that will vary
line_source = ColumnDataSource(data=dict(x=x_line, y=y_line, x_log=x_log_line,
                                         b=b_l, bf=bf_l))
point_source = ColumnDataSource(data=dict(x=x_points, y=y_points, x_log=x_log_points,
                                          b=b_p, bf=bf_p))

sb_plot = figure(plot_width=pw, plot_height=ph,
                 x_axis_label='log[Free Compound (M)]',
                 y_axis_label='Specific Binding',
                 title='Specific Binding')

sb_plot.line('x_log', 'y', source=line_source, line_width=3, line_alpha=0.6, color='black')
sb_plot.circle('x_log', 'y', source=point_source, size=10, color='black')

# set up static line and annotations
sb_plot.line(x_log_line, y_line, line_width=5, color='blue', line_alpha=0.3)
sb_plot.circle(x_log_points, y_points, size=10, color='blue', line_alpha=0.3)

mytext = Label(x=-6, y=20, text='log(Kd) = -6, Bmax = 100',
               text_color="blue", text_alpha=0.5)
sb_plot.add_layout(mytext)

# add axes lines
vline = Span(location=0, dimension='height', line_color='black', line_width=1, line_alpha=0.3)
hline = Span(location=0, dimension='width', line_color='black', line_width=1, line_alpha=0.3)
sb_plot.renderers.extend([vline, hline])

# -------------------------------------------------
# make scatchard transformation plot
# -------------------------------------------------
sc_plot = figure(plot_width=pw, plot_height=ph,
                 x_axis_label='Specific Binding',
                 y_axis_label='Specific Binding/Free Lignad',
                 title='Scatchard Transformation')

sc_plot.line('b', 'bf', source=line_source, line_width=3, line_alpha=0.6, color='black')
sc_plot.circle('b', 'bf', source=point_source, size=10, color='black')

# set up static line and annotations
sc_plot.line(b_l, bf_l, line_width=5, color='blue', line_alpha=0.3)
sc_plot.circle(b_p, bf_p, size=10, color='blue', line_alpha=0.3)

mytext = Label(x=50, y=6e7, text='log(Kd) = -6, Bmax = 100',
               text_color="blue", text_alpha=0.5)
sc_plot.add_layout(mytext)

# add axes lines
vline = Span(location=0, dimension='height', line_color='black', line_width=1, line_alpha=0.3)
hline = Span(location=0, dimension='width', line_color='black', line_width=1, line_alpha=0.3)
sc_plot.renderers.extend([vline, hline])

# -------------------------------------------------
# make plot interactive
# -------------------------------------------------
# set up java script callback function to make plot interactive
bmax_slider = Slider(start=0, end=200, value=100, step=10, title="Bmax")
pkd_slider = Slider(start=-8, end=-3, value=-6, step=0.1, title="log[Kd (M)]")

callback = CustomJS(args=dict(LineSource=line_source,
                              PointSource=point_source,
                              bmax=bmax_slider,
                              kd=pkd_slider),
                    code="""
    const LineData = LineSource.data;
    const PointData = PointSource.data;
    const BMAX = bmax.value;
    const KD = Math.pow(10, kd.value);
    const lx = LineData.x;
    const ly = LineData.y;
    const lb = LineData.b;
    const lbf = LineData.bf;
    const px = PointData.x;
    const py = PointData.y;
    const pb = PointData.b;
    const pbf = PointData.bf;

    // define function(s) for editing data
    function sb(x, BMAX, KD){
        return (x*BMAX)/(x+KD);
    }

    function sc(x, BMAX, KD){
        return sb(x, BMAX, KD)/x;
    }

    // loop over data and edit
    for (var i = 0; i < lx.length; i++) {
        ly[i] = sb(lx[i], BMAX, KD);
        lb[i] = sb(lx[i], BMAX, KD);
        lbf[i] = sc(lx[i], BMAX, KD);
    }

    for (var i = 0; i < px.length; i++) {
        py[i] = sb(px[i], BMAX, KD);
        pb[i] = sb(px[i], BMAX, KD);
        pbf[i] = sc(px[i], BMAX, KD);
    }

    // emit changes
    LineSource.change.emit();
    PointSource.change.emit();
""")

# add sliders to plot and display
bmax_slider.js_on_change('value', callback)
pkd_slider.js_on_change('value', callback)

# -------------------------------------------------
# set layout and display
# -------------------------------------------------
layout = row(
    sb_plot,
    sc_plot,
    column(bmax_slider, pkd_slider),
)

output_file(html_output_dir + "07-receptors-sb-sc-dual.html",
            title="Dual Saturation Binding and Scatchard Plot")
show(layout)
