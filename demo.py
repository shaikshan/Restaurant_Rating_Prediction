from Restaurant.exception import RestaurantException
from Restaurant.logger import logging
from Restaurant.pipeline.pipeline import Pipeline
import os,sys
from Restaurant.config.configuration import Configuration

def main():
    try:
        pipe = Pipeline()
        pipe.run_pipeline()
    except Exception as e:
        logging.info(f"{e}")
        print(e)



if __name__=='__main__':
    main()