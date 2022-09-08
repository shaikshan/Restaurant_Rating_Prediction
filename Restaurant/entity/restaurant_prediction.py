from unicodedata import category
from Restaurant.exception import RestaurantException
from Restaurant.util.util import *
import os,sys
import pandas as pd


class RestaurantData:
    def __init__(self,
                    online_order:str,
                    book_table:str,
                    votes:int,
                    cuisines:int,
                    approx_cost_for_two_people:float,
                    listed_in_type:str,
                    Rate:float):
        try:
            self.online_order = online_order
            self.book_table = book_table
            self.votes = votes
            self.cuisines = cuisines
            self.approx_cost_for_two_people = approx_cost_for_two_people
            self.listed_in_type = listed_in_type
            self.Rate = Rate
        except Exception as e:
            raise RestaurantException(e,sys) from e
    
    def get_restaurant_input_dataframe(self):
        try:
            restaurant_input_dict = self.get_restaurant_data_as_dict()
            return pd.DataFrame(restaurant_input_dict)
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def get_restaurant_data_as_dict(self):
        try:
            input_data = {
                "online_order":[self.online_order],
                "book_table":[self.book_table],
                "votes":[self.votes],
                "cuisines":[self.cuisines],
                "approx_cost(for two people)":[self.approx_cost_for_two_people],
                "listed_in(type)":[self.listed_in_type]
                }
            return input_data
        except Exception as e:
            raise RestaurantException(e,sys) from e


class RestaurantPredictor:
    def __init__(self,model_dir:str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def get_latest_best_model_path(self):
        try:
            folder_name = list(map(int,os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir,f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir,file_name)
            return latest_model_path
        except Exception as e:
            raise RestaurantException(e,sys) from e

    def predict(self,X):
        try:
            model_path = self.get_latest_best_model_path()
            model = load_object(file_path=model_path)
            Rate = model.predict(X)
            return Rate
        except Exception as e:
            raise RestaurantException(e,sys) from e
        
