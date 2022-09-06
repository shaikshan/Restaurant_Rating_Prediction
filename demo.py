from Restaurant.exception import RestaurantException
from Restaurant.logger import logging
from Restaurant.pipeline.pipeline import Pipeline
import os,sys
from Restaurant.config.configuration import Configuration

def main():
    try:
        config_path = os.path.join("config","config.yaml")
        pipe = Pipeline(Configuration(config_file_path=config_path))
        pipe.start()
        logging.info("main function execution completed.")
    except Exception as e:
        logging.info(f"{e}")
        print(e)



if __name__=='__main__':
    main()