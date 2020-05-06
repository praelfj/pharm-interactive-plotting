// lwb inhibitor troubleshooting
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