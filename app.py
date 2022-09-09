from flask import Flask,request
import sys
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
    return render_template('predict.htm',context=context)


if __name__ == '__main__':
    app.run()