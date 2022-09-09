from flask import Flask,request
import sys
import pip
from flask.config import Config
from Restaurant.util.util import read_yaml_file,write_yaml_file
from Restaurant.logger import logging
from Restaurant.exception import RestaurantException
import os
import json
from Restaurant.config.configuration import Configuration
from Restaurant.pipeline.pipeline import Pipeline
from Restaurant.constants import CONFIG_DIR, ROOT_DIR,get_current_time_stamp
from Restaurant.entity.restaurant_prediction import RestaurantData,RestaurantPredictor
from flask import render_template,send_file,abort

ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "Restaurant"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,'model.yaml')
LOG_DIR = os.path.join(ROOT_DIR,LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR,PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR,SAVED_MODELS_DIR_NAME)

from Restaurant.logger import get_log_dataframe

RESTAURANT_DATA_KEY = "restaurant_data"
RATE_VALUE_KEY = "Rate"

app = Flask(__name__)

@app.route('/artifact',defaults={'req_path':'Restaurant'})
@app.route('/artifact/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs('Restaurant', exist_ok=True)
    #Joining the base and the requested path
    print(f"req_path:{req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    #Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    #Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path,"r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    #Show directory contents
    files = {os.path.join(abs_path,file_name): file_name for file_name in os.listdir(abs_path) if
                "artifact" in os.path.join(abs_path,file_name)}

    result = {
        "files":files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template("files.html",result=result)

@app.route('/',methods=['GET','POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)

@app.route('/train',methods=['GET','POST'])
def train():
    message= ""
    pipeline = Pipeline(config=Configuration(current_time_stamp=get_current_time_stamp()))
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress"
    context = {
        "experiment":pipeline.get_experiment_status().to_html(classes='table table-striped col-12'),
        "message":message}
    return render_template('train.html',context=context)


@app.route('/predict',methods= ['GET','POST'])
def predict():
    context={
        RESTAURANT_DATA_KEY:None,
        RATE_VALUE_KEY:None
    }

    if request.method == 'POST':
        online_order = str(request.form['online_order'])
        book_table = str(request.form['book_table'])
        votes = int(request.form['votes'])
        cuisines = int(request.form['cuisines'])
        approx_cost_fot_two_people = float(request.form['approx_cost(for two people)'])
        listed_in_type = str(request.form['listed_in(type)'])
        
        restaurant_data = RestaurantData(online_order=online_order,
                                        book_table=book_table,
                                        votes=votes,
                                        cuisines=cuisines,
                                        approx_cost_for_two_people=approx_cost_fot_two_people,
                                        listed_in_type=listed_in_type)
        restaurant_df = restaurant_data.get_restaurant_input_dataframe()
        restaurant_predictor = RestaurantPredictor(model_dir=MODEL_DIR)
        Rate_value = restaurant_predictor.predict(X=restaurant_df)
        context = {
            RESTAURANT_DATA_KEY:restaurant_data.get_restaurant_data_as_dict(),
            RATE_VALUE_KEY:Rate_value,
        }
        return render_template('predict.html',context=context)
    return render_template('predict.html',context=context)

@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models_files.html', result=result)

@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)

        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_model.html', result={"model_config": model_config})

    except  Exception as e:
        logging.exception(e)
        return str(e)


@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


if __name__ == '__main__':
    app.run()