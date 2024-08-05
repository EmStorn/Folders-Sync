import os

def path_input_validation(user_input):
    """
    Function that checks if the path input by user exists.
    """
    try:
        path = user_input
        if os.path.exists(path):
            if os.path.isdir(path):
                return path
            else:
                print(f"The input path '{path}' exists but but does not point to a directory.")
                return None
        else:
            print(f"The inoout path '{path}' does not exist.")
    except Exception as e:
        print(f"An error occurred while validating the path input: {e}")
        return None

def sync_interval_validation(user_input):
    """
    Function that checks if the sync interval input by user is a number.
    """
    try:
        if user_input.isdigit() and int(user_input) > 0:
            return user_input
        else:
            print(f"Invalid sync interval input: '{user_input}' is not a positive integer.")
            return None
    except Exception as e:
        print(f"An error occurred while validating the sync time input: {e}")
        return None

def get_path_input(desired_folder):
    """
    Function that collects the path input by user. 
    In case it's not valid continue asking until receive a valid path.
    Expected argument is a string, with the name of the folder that will be used in input request.
    """
    while True:
        try:
            user_path_input = input(f"Input absolute path of the {desired_folder} folder: ")
            if path_input_validation(user_path_input):
                user_selected_path = user_path_input
                return user_selected_path
            else:
                print("Invalid path, please try again using a valid absolute path.")
        except Exception as e:
            print(f"An error occurred while processing the path input: {e}")

def get_sync_interval_input():
    """
    Function that collects the interval sync input by user in seconds. 
    In case it's not valid continue asking until receive a valid input.
    """
    while True:
        try:
            user_interval_input = input("Input desired sync interval time in seconds (using only digits): ")
            if sync_interval_validation(user_interval_input):
                user_selected_interval = int(user_interval_input)
                return user_selected_interval
            else:
                print("Invalid interval time, please try again using a valid interval.")    
        except Exception as e:
            print(f"An error occurred while processing the sync interval input: {e}")