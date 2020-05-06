"""
interactive plots for lineweaver-burk kinetics, with an inhibitor dropdown menu
"""
import numpy as np

from bokeh.layouts import row, column
from bokeh.models import CustomJS, Slider, Label, Span, Select
from bokeh.plotting import figure, output_file, show, ColumnDataSource

from pharmaplot import mm
from pharmaplot.config import html_output_dir

# generate data for plotting
log_start = -2
log_end = 1
vmax = 10
km = 1

ki = 1
conc_i = 0

x_points = 1 / np.logspace(log_start, log_end, num=12)
y_points = mm.lwb_competitive(x_points, vmax=vmax, km=km, ki=ki, conc_i=conc_i)

x_line = np.linspace(-3 / km, np.max(x_points), num=5)
y_line = mm.lwb_competitive(x_line, vmax=vmax, km=km, ki=ki, conc_i=conc_i)

# set up source data and plot lines that will vary
line_source = ColumnDataSource(data=dict(x=x_line, y=y_line))
point_source = ColumnDataSource(data=dict(x=x_points, y=y_points))

plot = figure(y_range=(-0.05, 0.8), x_range=(-1.5, 4), plot_width=600, plot_height=400,
              x_axis_label='1/[S]: substrate concentration (1/μM)',
              y_axis_label='1/initial velocity (s/μM)',
              title='Lineweaver-Burk Kinetics with Inhibition')

plot.line('x', 'y', source=line_source, line_width=3, line_alpha=0.6, color='black')
plot.circle('x', 'y', source=point_source, size=10, color='black')

# set up static line and annotations
plot.line(x_line, y_line, line_width=5, color='blue', line_alpha=0.3)
plot.circle(x_points, y_points, size=10, color='blue', line_alpha=0.3)

mytext = Label(x=2, y=0.2, text='[I] = 0 (μM)',
               text_color="blue", text_alpha=0.5)
plot.add_layout(mytext)

# add axes lines
vline = Span(location=0, dimension='height', line_color='black', line_width=1, line_alpha=0.3)
hline = Span(location=0, dimension='width', line_color='black', line_width=1, line_alpha=0.3)
plot.renderers.extend([vline, hline])

# set up java script callback function and widgets to make plot interactive
ci_slider = Slider(start=0, end=100, value=0, step=1, title="[I] (μM)")
ki_slider = Slider(start=15, end=100, value=50, step=1, title="Ki (μM)")
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

    // define functions for editing data
    function competitive(x, VMAX, KM, CI, KI){
        return ((KM*(1+(CI/KI)))/VMAX)*x+(1/VMAX);
    }
    function noncompetitive(x, VMAX, KM, CI, KI){
        return (KM/VMAX)*((1+(CI/KI))* x)+((1+(CI/KI))/VMAX);
    }
    function uncompetitive(x, VMAX, KM, CI, KI){
        return (KM/VMAX)*x +((1+(CI/KI))/VMAX);
    }

    // loop over line data and point data to edit
    for (var i = 0; i < lx.length; i++) {
        if (it == "competitive"){
            ly[i] = competitive(lx[i], VMAX, KM, CI, KI);
        } else if (it == "noncompetitive"){
            ly[i] = noncompetitive(lx[i], VMAX, KM, CI, KI);
        } else if (it == "uncompetitive"){
            ly[i] = uncompetitive(lx[i], VMAX, KM, CI, KI);
        }
    }

    for (var i = 0; i < px.length; i++) {
        if (it == "competitive"){
            py[i] = competitive(px[i], VMAX, KM, CI, KI);
        } else if (it == "noncompetitive"){
            py[i] = noncompetitive(px[i], VMAX, KM, CI, KI);
        } else if (it == "uncompetitive"){
            py[i] = uncompetitive(px[i], VMAX, KM, CI, KI);      
        }
    }

    // emit changes
    LineSource.change.emit();
    PointSource.change.emit();
""")

# add sliders to plot and display
ci_slider.js_on_change('value', callback)
ki_slider.js_on_change('value', callback)
inhib_select.js_on_change('value', callback)

layout = row(
    plot,
    column(ci_slider, ki_slider, inhib_select),
)

output_file(html_output_dir + "06-lb-inhib-dropdown.html",
            title="Lineweaver-Burk Kinetics with Inhibition")
show(layout)


