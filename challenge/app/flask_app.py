import os

from flask import Flask, request, render_template, jsonify
from challenge.pipeline.prediction_utilities import predict_with_minimum_mae_model, calculate_n_most_similar_diamonds

app = Flask("Diamond APP", template_folder='template')

@app.get("/")
def index():
    return render_template('index.html')

# /api/predict?carat=1.0&cut=Ideal&color=E&clarity=VVS1&depth=61.5&table=55&x=6.5&y=6.5&z=4.0
@app.get("/api/predict/")
def predict():
    carat = request.args.get('carat')
    cut = request.args.get('cut')
    color = request.args.get('color')
    clarity = request.args.get('clarity')
    depth = request.args.get('depth')
    table = request.args.get('table')
    x = request.args.get('x')
    y = request.args.get('y')
    z = request.args.get('z')

    params = {
        'carat': carat,
        'cut': cut,
        'color': color,
        'clarity': clarity,
        'depth': depth,
        'table': table,
        'x': x,
        'y': y,
        'z': z
    }
    return jsonify({"message": "Price predicted successfully", "data": predict_with_minimum_mae_model(params)})

# /api/similarities?n=3&cut=Premium&color=E&clarity=SI1&carat=0.25
@app.get("/api/similarities/")
def similarities():
    n = request.args.get('n')
    cut = request.args.get('cut')
    color = request.args.get('color')
    clarity = request.args.get('clarity')
    carat = request.args.get('carat')

    cat_data = {
        'cut': cut,
        'color': color,
        'clarity': clarity,
    }
    return jsonify({"message": "Similar diamonds found", "data": calculate_n_most_similar_diamonds(n, carat, cat_data)})


if __name__ == '__main__':
    app.run()
