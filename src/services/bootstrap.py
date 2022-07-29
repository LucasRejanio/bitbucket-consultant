import logging
import os


def create_data_dir():
    logging.info("Function create_data_dir called.")

    logging.info('Creating data dir.')
    current_dir = os.getcwd()
    data_path = os.path.join(current_dir, "data")
    try:
        os.mkdir(data_path)
        logging.info("Created data folder!")
    except FileExistsError:
        logging.info("Dir data already exists.")
