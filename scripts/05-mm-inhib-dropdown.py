"""
interactive standard Michaelis-Menten plots with a dropdown menu to select inhibition type

combination of competitive, noncompetitive, and uncompetitive on the same plot
"""
# import libraries
import numpy as np

from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, Label, Span, Select
from bokeh.plotting import figure, output_file, show, ColumnDataSource

from pharmaplot import mm
from pharmaplot.config import html_output_dir

# generate data for plotting
log_start = -1
log_end = 4

vmax = 100
km = 5
ki = 1
conc_i = 0

x_line = np.logspace(log_start, log_end, num=100)
y_line = mm.mm_competitive(x_line, vmax=vmax, km=km, ki=ki, conc_i=conc_i)

x_points = np.logspace(log_start, log_end, num=20)
y_points = mm.mm_competitive(x_points, vmax=vmax, km=km, ki=ki, conc_i=conc_i)

# set up source data and plot lines that will vary
line_source = ColumnDataSource(data=dict(x=x_line, y=y_line))
point_source = ColumnDataSource(data=dict(x=x_points, y=y_points))

plot = figure(y_range=(-5, 120), x_range=(-5, 100), plot_width=600, plot_height=400,
              x_axis_label='[S]: substrate concentration (μM)',
              y_axis_label='initial velocity (μM/s)',
              title='Michaelis-Menten Kinetics with Inhibition')

plot.line('x', 'y', source=line_source, line_width=3, line_alpha=0.6, color='black')
plot.circle('x', 'y', source=point_source, size=10, color='black')

# set up static line and annotations
plot.line(x_line, y_line, line_width=5, color='blue', line_alpha=0.3)
plot.circle(x_points, y_points, size=10, color='blue', line_alpha=0.3)

mytext = Label(x=10, y=87, text='[I] = 0 (μM)',
               text_color="blue", text_alpha=0.5)
plot.add_layout(mytext)

# add axes lines
vline = Span(location=0, dimension='height', line_color='black', line_width=1, line_alpha=0.3)
hline = Span(location=0, dimension='width', line_color='black', line_width=1, line_alpha=0.3)
plot.renderers.extend([vline, hline])

# set up java script callback function and widgets to make plot interactive
ci_slider = Slider(start=0, end=100, value=0, step=1, title="[I] (μM)")
ki_slider = Slider(start=1, end=100, value=50, step=1, title="Ki (μM)")
inhib_select = Select(title="Inhibition Type:", value="competitive",
                      options=["competitive", "noncompetitive", "uncompetitive"])

callback = CustomJS(args=dict(LineSource=line_source,
                              PointSource=point_source,
                              ci=ci_slider,
                              ki=ki_slider,
                              vmax=vmax,
                              km=km,
                              inhibType=inhib_select),
                    code="""
    const LineData = LineSource.data;
    const PointData = PointSource.data;
    const VMAX = vmax;
    const KM = km;
    const CI = ci.value;
    const KI = ki.value;
    const lx = LineData['x'];
    const ly = LineData['y'];
    const px = PointData['x'];
    const py = PointData['y'];
    const it = inhibType.value;

    function competitive(x, VMAX, KM, CI, KI){
        return (VMAX*x)/((KM*(1+(CI/KI))+x));
    }
    function noncompetitive(x, VMAX, KM, CI, KI){
        return (VMAX*x)/((KM*(1+(CI/KI)))+(x*(1+(CI/KI))));
    }
    function uncompetitive(x, VMAX, KM, CI, KI){
        return (VMAX*x)/(KM+(x*(1+(CI/KI))));
    }
    for (var i = 0; i < lx.length; i++) {
        if (it == "competitive"){
            ly[i] = competitive(lx[i], VMAX, KM, CI, KI);
            py[i] = competitive(px[i], VMAX, KM, CI, KI);
        } else if (it == "noncompetitive"){
            ly[i] = noncompetitive(lx[i], VMAX, KM, CI, KI);
            py[i] = noncompetitive(px[i], VMAX, KM, CI, KI);
        } else if (it == "uncompetitive"){
            ly[i] = uncompetitive(lx[i], VMAX, KM, CI, KI);
            py[i] = uncompetitive(px[i], VMAX, KM, CI, KI);      
        }
    }

    LineSource.change.emit();
    PointSource.change.emit();
    // (VMAX*lx[i])/((KM*(1+(CI/KI)))+(lx[i]*(1+(CI/KI)))) noncompetitive
    // (VMAX*lx[i])/(KM+(lx[i]*(1+(CI/KI)))) uncompetitive
""")

# add sliders to plot and display
ci_slider.js_on_change('value', callback)
ki_slider.js_on_change('value', callback)
inhib_select.js_on_change('value', callback)

layout = row(
    plot,
    column(ci_slider, ki_slider, inhib_select),
)

output_file(html_output_dir + "05-mm-inhib-dropdown.html",
            title="Michaelis-Menten Kinetics with Inhibition")
show(layout)
