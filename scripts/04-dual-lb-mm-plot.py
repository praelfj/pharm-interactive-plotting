"""
script generating an interactive plot with both classical Micahelis-Menten kinetics and  plot with Linweaver-Burk
kinetics on a side-by-side, interactive visualization
"""
# import libraries
import numpy as np

from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, Label, Span
from bokeh.plotting import figure, output_file, show, ColumnDataSource

from pharmaplot import mm
from pharmaplot.config import html_output_dir

# -------------------------------------------------
# create baseline michaelis-menten plot
# -------------------------------------------------
# set plot parameters
pw = 500
ph = 400

# set data values
log_start = -2
log_end = 3
vmax = 10
km = 1

# -------------------------------------------------
# create baseline michaelis-menten plot
# -------------------------------------------------
# set up starting values
x_line = np.logspace(log_start, log_end, num=100)
y_line = mm.michaelis_menten(x_line, vmax, km)

x_points = np.logspace(log_start, log_end, num=20)
y_points = mm.michaelis_menten(x_points, vmax, km)

# set up source data and plot lines that will vary
mm_line_source = ColumnDataSource(data=dict(x=x_line, y=y_line))
mm_point_source = ColumnDataSource(data=dict(x=x_points, y=y_points))

mm_plot = figure(y_range=(-0.5, 20), x_range=(-0.5, 10), plot_width=pw, plot_height=ph,
                 x_axis_label='[S]: substrate concentration (μM)',
                 y_axis_label='initial velocity (μM/s)',
                 title='Michaelis-Menten Kinetics')

mm_plot.line('x', 'y', source=mm_line_source, line_width=3, line_alpha=0.6, color='black')
mm_plot.circle('x', 'y', source=mm_point_source, size=10, color='black')

# set up static line and annotations
mm_plot.line(x_line, y_line, line_width=5, color='blue', line_alpha=0.3)
mm_plot.circle(x_points, y_points, size=10, color='blue', line_alpha=0.3)

mytext = Label(x=3.8, y=10, text='Km = 1 (μM), Vmax = 10 (μM/s)',
               text_color="blue", text_alpha=0.5)
mm_plot.add_layout(mytext)

# add axes lines
vline = Span(location=0, dimension='height', line_color='black', line_width=1, line_alpha=0.3)
hline = Span(location=0, dimension='width', line_color='black', line_width=1, line_alpha=0.3)
mm_plot.renderers.extend([vline, hline])

# -------------------------------------------------
# create baseline lineweaver-burk plot
# -------------------------------------------------
x_line = np.linspace(-3, np.max(x_points))
y_line = mm.lineweaver_burk(x_line, vmax, km)

x_points = 1 / np.geomspace(0.1, 10, num=8)
y_points = mm.lineweaver_burk(x_points, vmax, km)

# set up source data and plot lines that will vary
lb_line_source = ColumnDataSource(data=dict(x=x_line, y=y_line))
lb_point_source = ColumnDataSource(data=dict(x=x_points, y=y_points))

lb_plot = figure(y_range=(-0.05, 0.8), x_range=(-1.5, 4), plot_width=pw, plot_height=ph,
                 x_axis_label='1/[S]: substrate concentration (1/μM)',
                 y_axis_label='1/initial velocity (s/μM)',
                 title='Lineweaver-Burk Kinetics')

lb_plot.line('x', 'y', source=lb_line_source, line_width=3, line_alpha=0.6, color='black')
lb_plot.circle('x', 'y', source=lb_point_source, size=10, color='black')

# add axes lines
vline = Span(location=0, dimension='height', line_color='black', line_width=1, line_alpha=0.3)
hline = Span(location=0, dimension='width', line_color='black', line_width=1, line_alpha=0.3)
lb_plot.renderers.extend([vline, hline])

# set up static line and annotations
lb_plot.line(x_line, y_line, line_width=5, color='blue', line_alpha=0.3)
lb_plot.circle(x_points, y_points, size=10, color='blue', line_alpha=0.3)

mytext = Label(x=-0.1, y=0.4, text='Km = 1 (μM), Vmax = 10 (μM/s)',
               text_color="blue", text_alpha=0.5)
lb_plot.add_layout(mytext)

# -------------------------------------------------
# make plot interactive
# -------------------------------------------------
# set up java script callback function to make plot interactive
vmax_slider = Slider(start=1, end=20, value=10, step=0.1, title="Vmax (μM/s)")
km_slider = Slider(start=0.1, end=10, value=1, step=0.1, title="Km (μM)")

callback = CustomJS(args=dict(mmLineSource=mm_line_source,
                              mmPointSource=mm_point_source,
                              lbLineSource=lb_line_source,
                              lbPointSource=lb_point_source,
                              vmax=vmax_slider,
                              km=km_slider),
                    code="""
    const mmLineData = mmLineSource.data;
    const mmPointData = mmPointSource.data;
    const lbLineData = lbLineSource.data;
    const lbPointData = lbPointSource.data;
    const VMAX = vmax.value;
    const KM = km.value;
    const mmlx = mmLineData['x'];
    const mmly = mmLineData['y'];
    const mmpx = mmPointData['x'];
    const mmpy = mmPointData['y'];
    const lblx = lbLineData['x'];
    const lbly = lbLineData['y'];
    const lbpx = lbPointData['x'];
    const lbpy = lbPointData['y'];
    
    // define functions for plotting data
    function mm(x, VMAX, KM){
        return (VMAX*x)/(KM+x);
    }
    
    function lb(x, VMAX, KM){
        return ((KM/VMAX)*x) + (1/VMAX);
    }
    
    // loop over data to edit
    for (var i = 0; i < mmlx.length; i++) {
        mmly[i] = mm(mmlx[i], VMAX, KM);
    }
    for (var i = 0; i < mmpx.length; i++) {
        mmpy[i] = mm(mmpx[i], VMAX, KM);
    }
    for (var i = 0; i < lblx.length; i++) {
        lbly[i] = lb(lblx[i], VMAX, KM);
    }
    for (var i = 0; i < lbpx.length; i++) {
        lbpy[i] = lb(lbpx[i], VMAX, KM);
    }
    
    // change data sources
    mmLineSource.change.emit();
    mmPointSource.change.emit();
    lbLineSource.change.emit();
    lbPointSource.change.emit();
""")

# add sliders to plot and display
vmax_slider.js_on_change('value', callback)
km_slider.js_on_change('value', callback)

# -------------------------------------------------
# create baseline michaelis-menten plot
# -------------------------------------------------
layout = row(
    mm_plot,
    lb_plot,
    column(vmax_slider, km_slider),
)

output_file(html_output_dir + "04-dual-lb-mm-plot.html", title="Michaelis-Menten Kinetics")
show(layout)
