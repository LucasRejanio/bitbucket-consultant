import logging
import os
import json


def file_actions(actions_type, file_path, data=None, context=None):
    if actions_type == "create" or actions_type == "update" or actions_type == "sync" and data != None:
        try:
            with open(f'{file_path}', 'w') as f:
                json.dump(data, f, indent=2)

                if context == None:
                    logging.info(f"{actions_type.title()} file '{file_path}'.")
                else:
                    logging.info(f"{actions_type.title()} '{file_path}' with {context} data.")
        except:
            logging.error(f"Error to {actions_type.title()} file '{file_path}'")

    elif actions_type == "delete":
        try:
            os.remove(f"{file_path}")
            logging.info(f"File '{file_path}' was deleted.")
        except:
            logging.info(f"File '{file_path}' does not exist to delete.")

    elif actions_type == "open":
        try:
            with open(f'{file_path}', "r") as f:
                file_uploaded = json.load(f)
            return file_uploaded
        except:
            logging.error(f"Error to open '{file_path}'")
