import os
import shutil
import filecmp

def compare_folders(source_folder, replica_folder):
    """
    Function that compare the content of two folder (taken as arguments) using filecmp library.
    It returns in order, items that are only existing in the source folder, 
    items that are only existing in replica folder and
    items that are existing in both source and replica folder, but have been updated based on
    file cmp comparison (metadata, modification time)
    """
    try:
        comparison = filecmp.dircmp(source_folder, replica_folder)

        source_folder_unique = set(comparison.left_only)
        replica_folder_unique = set(comparison.right_only)
        common_files_folders = set(comparison.common)

        items_to_update = set()

        for item in common_files_folders:
            path_source = os.path.join(source_folder, item)
            path_replica = os.path.join(replica_folder, item)
            if os.path.isfile(path_source) and os.path.isfile(path_replica):
                # Checks if files are different/update occured
                if not filecmp.cmp(path_source, path_replica, shallow=False):
                    items_to_update.add(item)
            # if the item is a directory will be added to the set, as it will be action recursively in Sync()
            elif os.path.isdir(path_source) and os.path.isdir(path_replica):
                items_to_update.add(item)

        return source_folder_unique, replica_folder_unique, items_to_update
    except Exception as e:
        print(f"An error occurred while comparing the folders: {e}")
        return set(), set(), set()

def copy_item(source_folder, replica_folder, file):
    """
    Function that copies an item from a folder to another.
    Arguments taken are paths of the two folders and the file to be handled.
    """
    try:
        item_to_be_copied = f"{source_folder}\{file}"
        item_to_bo_created = f"{replica_folder}\{file}"

        if os.path.isdir(item_to_be_copied):
            shutil.copytree(item_to_be_copied, item_to_bo_created)
        else: 
            shutil.copy2(item_to_be_copied, item_to_bo_created)
    except FileNotFoundError:
        print(f"The file or directory to be copied '{item_to_be_copied}' does not exist.")
    except PermissionError:
        print(f"You don't have permissions to copy '{item_to_be_copied}'.")
    except Exception as e:
        print(f"An error occurred while copying '{item_to_be_copied}': {e}")

def delete_item(folder, file):
    """
    Function that deletes an item from a folder.
    Arguments taken are path of the folders and the file to be handled.
    """
    try:
        item_to_be_deleted = f"{folder}\{file}"

        if os.path.isdir(item_to_be_deleted):
            shutil.rmtree(item_to_be_deleted)
        else:
            os.remove(item_to_be_deleted)
    except FileNotFoundError:
        print(f"The file or directory to be deleted '{item_to_be_deleted}' does not exist.")
    except PermissionError:
        print(f"You don't have permissions to copy '{item_to_be_deleted}'.")
    except Exception as e:
        print(f"An error occurred while deleting '{item_to_be_deleted}': {e}")

