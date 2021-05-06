###############################################
# Created by iiSeymour
# Changed by Mandeep Singh
# Changed date: 03/21/2019
# Licensce: free to use
#############################################

from flask import Flask, render_template
import altair as alt
import pandas as pd
import lapdata as ld

# load a simple dataset as a pandas DataFrame
from vega_datasets import data
cars = data.cars()

app = Flask(__name__)

##########################
# Flask routes
##########################
# render index.html home page
@app.route("/")
def home_page():
    return render_template("speed.html")

@app.route("/speed")
def speed_page():
    return render_template('speed.html')

@app.route("/inputs")
def inputs_page():
    return render_template('inputs.html')

#########################
### Altair Data Routes
#########################

# Creates graph for cars
@app.route("/data/cars")
def cars_demo():

    chart = alt.Chart(
        data=cars, height=700, width=700).mark_point().encode(
            x='Horsepower',
            y='Miles_per_Gallon',
            color='Origin',
        ).interactive()
    return chart.to_json()

@app.route("/data/speed")
def speed_graph():
    alt.renderers.enable('mimetype')
    alt.data_transformers.disable_max_rows()
    w, h = 1400, 250
    data = ld.getData()
    dfturns = ld.GetTurns()
    zoom = alt.selection_interval(bind='scales', encodings=['x'])
    cspeed = alt.Chart(data).mark_line().encode(x="LapDist", y=alt.Y('Speed', scale=alt.Scale(domain=[0, 300])), detail="Lap:O", color=alt.value("grey")).properties(width=w, height=h)
    cbest = alt.Chart(data[data["IsBestLap"] == True]).mark_line().encode(x="LapDist", y=alt.Y('Speed', scale=alt.Scale(domain=[0, 300])), color=alt.value("#ADFF2F")).properties(width=w, height=h)
    cturns = alt.Chart(dfturns).mark_rule().encode(x="LapDist").properties(width=w, height=h)
    ctext = alt.Chart(dfturns).mark_text(align="center", angle=90, dy=-7, dx=-100).encode(x="LapDist", text="Turn").properties(width=w, height=h)
    chart = cspeed + cbest + cturns + ctext
    chart = chart.add_selection(zoom)
    return chart.to_json()

@app.route("/data/inputs")
def inputs_graph():
    alt.renderers.enable('mimetype')
    alt.data_transformers.disable_max_rows()
    w, h = 1400, 250
    data = ld.getData()[["LapDist","Throttle","Brake","Lap"]]
    dfturns = ld.GetTurns()
    zoom = alt.selection_interval(bind='scales', encodings=['x'])
    throttle = alt.Chart(data).mark_line().encode(x='LapDist', y=alt.Y('Throttle', scale=alt.Scale(domain=[-0.2, 1.2])), color=alt.Color('Lap', scale=alt.Scale(scheme='blues'))).properties(width=w, height=h)
    brake = alt.Chart(data).mark_line().encode(x='LapDist', y=alt.Y('Brake', scale=alt.Scale(domain=[-0.2, 1.2])), color=alt.Color('Lap', scale=alt.Scale(scheme='reds'))).properties(width=w, height=h)
    cturns = alt.Chart(dfturns).mark_rule().encode(x="LapDist").properties(width=w, height=h)
    ctext = alt.Chart(dfturns).mark_text(align="center", angle=90, dy=-7, dx=-100).encode(x="LapDist", text="Turn").properties(width=w, height=h)
    brake = brake + cturns + ctext
    throttle = throttle + cturns + ctext
    chart = throttle.add_selection(zoom) & brake.add_selection(zoom) 
    chart = chart.resolve_scale(color='independent')
    return chart.to_json()

if __name__ == "__main__":
    app.run(debug=True)
