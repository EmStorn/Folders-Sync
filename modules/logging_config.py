import logging
import os
import modules.files_actions as files_actions
from datetime import datetime

def logging_configuration(log_folder):
    """
    Function that creates the configuration of the logging system.
    Takes timestamp to name the log file with strating time of the process.
    Path of the file is an expected argument.
    """
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file = f"Log_{timestamp}.log"
        log_file_path = os.path.join(log_folder, log_file)
        
        # Create logger, level INFO as custome messages will be INFO
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        # Create file handler for logging to a file
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.INFO)
        
        # Create console handler for logging to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create a formatter and set it for both handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    except Exception as e:
        print(f"An error occurred during logging configuration: {e}")

def log_copy(source_folder, replica_folder, item):
    """
    Functions that logs the copying of items.
    Items are always copied from source folder to replica folder.
    """
    try:
        if os.path.isdir(os.path.join(source_folder, item)):
            new_folder_path = os.path.join(source_folder, item)
            new_replica_folder_path = os.path.join(replica_folder, item)
            logging.info(f"Folder {item} newly created in {source_folder}")
            logging.info(f"Folder {item} copied from {source_folder} to {replica_folder}")
            new_folder_items = files_actions.get_items_in_folder(new_folder_path)
            for sub_item in new_folder_items:
                log_copy(new_folder_path, new_replica_folder_path, sub_item)
        else:
            logging.info(f"{item} newly created in {source_folder}")
            logging.info(f"{item} copied from {source_folder} to {replica_folder}")
    except Exception as e:
        logging.error(f"An error occurred while logging the copy of '{item}': {e}")

def log_delete(replica_folder, item):
    """
    Functions that logs the deletion of items.
    Items are always deleted from replica folder only.
    """
    try:
        if os.path.isdir(os.path.join(replica_folder, item)):
            replica_subfolder_path = os.path.join(replica_folder, item)
            replica_subfolder_items = files_actions.get_items_in_folder(replica_subfolder_path)
            logging.info(f"Folder {item} deleted from {replica_folder}")
            for sub_item in replica_subfolder_items:
                log_delete(replica_subfolder_path, sub_item)
        else:
            logging.info(f"{item} deleted from {replica_folder}")
    except Exception as e:
        logging.error(f"An error occurred while logging the deletion of '{item}': {e}")

def log_update(source_folder, replica_folder, item):
    """
    Functions that logs the update (delete and new copy creatin) of items.
    Items are always copied from source folder to replica folder.
    """
    try:
        if os.path.isdir(os.path.join(source_folder, item)):
            new_folder_path = os.path.join(source_folder, item)
            new_replica_folder_path = os.path.join(replica_folder, item)
            new_folder_items = files_actions.get_items_in_folder(new_folder_path)
            for sub_item in new_folder_items:
                log_copy(new_folder_path, new_replica_folder_path, sub_item)
        else:
            logging.info(f"{item} updated in {replica_folder}")
    except Exception as e:
        logging.error(f"An error occurred while logging the copy of '{item}': {e}")