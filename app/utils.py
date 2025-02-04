import os

def delete_files_in_folder(folder_path):
    try:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except Exception as e:
        print(f"Failed to delete files in folder {folder_path}: {str(e)}")


# def generate_unique_filename(trans_num, page_num, existing_files):
#     """
#     Generate a unique filename by appending a counter to avoid duplicates.

#     Args:
#         trans_num (str): The extracted transaction number.
#         page_num (int): The page number where it was found.
#         existing_files (set): A set to track generated filenames.

#     Returns:
#         str: A unique filename with a counter if necessary.
#     """
#     counter = 1
#     filename = f"{trans_num}_{page_num}.pdf"
    
#     while filename in existing_files:
#         filename = f"{trans_num}_{page_num}_{counter}.pdf"
#         counter += 1
    
#     existing_files.add(filename)
#     return filename