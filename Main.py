import os
import time
import logging
import modules.user_inputs as user_inputs, modules.files_actions as files_actions, modules.logging_config as logging_config

# User inputs collection
source_folder = user_inputs.get_path_input("source")
replica_folder = user_inputs.get_path_input("replica") 
sync_interval = user_inputs.get_sync_interval_input()
log_file_destination = user_inputs.get_path_input("log") 

# Logging config based on user input
logging_config.logging_configuration(log_file_destination)


def sync(source_folder, replica_folder):
    """
    Function that define the main logic of the script.
    It takes as args the folders that users selected as source and replica.
    In order, it compares the list of files and folder existing in the two folders.
    If a file is in source, but not in replica, it creates a copy in the replica folder.
    If a file is only in replica folder, it deletes it.
    Finally it checks for items that are common but have been updated, deleting the replica and
    creating a new copy. If the item is a folder, it runs again recursively, 
    to check and compare its content.
    Each action takes is logged, in log file and console.
    """
    try:

        source_unique, replica_unique, common_items = files_actions.compare_folders(source_folder, replica_folder)

        for item in source_unique:
            files_actions.copy_item(source_folder, replica_folder, item)
            logging_config.log_copy(source_folder, replica_folder, item)

        for item in replica_unique:
            logging_config.log_delete(replica_folder, item)
            files_actions.delete_item(replica_folder, item)

        for item in common_items:
            if os.path.isdir(os.path.join(source_folder, item)):
                new_source_folder = os.path.join(source_folder, item)
                new_replica_folder = os.path.join(replica_folder, item)
                sync(new_source_folder, new_replica_folder)
            else:
                # Delete and create a new copy of the file, for files that have been updated
                files_actions.delete_item(replica_folder, item)
                files_actions.copy_item(source_folder, replica_folder, item)
                logging_config.log_update(source_folder, replica_folder, item)
    except Exception as e:
                logging.error(f"An error occurred while syncing the folders: {e}")

if __name__ == "__main__":
    
    try:
        print("Press CTRL+C to stop the syncing in any moment.")
        while True:
            print("Sync beginning.")
            sync(source_folder, replica_folder)
            print("Sync completed.")
            time.sleep(sync_interval) 
    except KeyboardInterrupt:
        print("Sync process interrupted by user. Exiting.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
