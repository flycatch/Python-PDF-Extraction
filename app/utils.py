import os
import time
# from apscheduler.schedulers.background import BackgroundScheduler

# scheduler = BackgroundScheduler()

UPLOAD_FOLDER = 'uploads'  # upload folder
AGE_LIMIT = 3600 # delete files older than 1 hr.
# RUNTIME = 900 # run periodic task every 15min

def delete_old_files(folder_path, age_limit=AGE_LIMIT):
    """
    Delete files that are older than `age_limit` seconds.

    :param folder_path: Path to the folder containing files.
    :param age_limit: Age limit in seconds.
    """
    try:
        current_time = time.time()
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            
            # Skip directories, only delete files
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getctime(file_path)  # File creation time

                # Delete only if file is older than 60 seconds
                if file_age > age_limit:
                    os.remove(file_path)
                    print(f"Deleted: {file_path} (Age: {file_age:.2f} seconds)")
    except Exception as e:
        print(f"Failed to delete files in folder {folder_path}: {str(e)}")

# def periodic_cleanup():
#     """Function to clean up files older than 1 minute."""
#     delete_old_files(UPLOAD_FOLDER)

# scheduler.add_job(periodic_cleanup, 'interval', seconds=RUNTIME)  # Runs every 10 seconds
# scheduler.start()

# if __name__ == "__main__":
#     try:
#         print("Scheduler started. Press Ctrl+C to stop.")
#         while True:
#             time.sleep(1)  # Keep the script running
#     except KeyboardInterrupt:
#         print("Stopping scheduler...")
#         scheduler.shutdown()




# import os
# # from .routes import UPLOAD_FOLDER
# from apscheduler.schedulers.background import BackgroundScheduler
# import time

# scheduler = BackgroundScheduler()

# def delete_files_in_folder(folder_path):
#     """Delete all files inside the given folder."""
#     try:
#         for file_name in os.listdir(folder_path):
#             file_path = os.path.join(folder_path, file_name)
#             if os.path.isfile(file_path):
#                 os.remove(file_path)
#         print(f"Deleted files in {folder_path}")
#     except Exception as e:
#         print(f"Failed to delete files in folder {folder_path}: {str(e)}")

# def periodic_cleanup():
#     """Function to clean up files every 10 seconds."""
#     delete_files_in_folder('uploads')

# scheduler.add_job(periodic_cleanup, 'interval', seconds=5)  # Runs every 10 seconds
# scheduler.start()

# if __name__ == "__main__":
#     try:
#         print("Scheduler started. Press Ctrl+C to stop.")
#         while True:
#             time.sleep(1)  # Keep the script running
#     except KeyboardInterrupt:
#         print("Stopping scheduler...")
#         scheduler.shutdown()


# def delete_files_in_folder(folder_path):
#     try:
#         for file_name in os.listdir(folder_path):
#             file_path = os.path.join(folder_path, file_name)
#             if os.path.isfile(file_path):
#                 os.remove(file_path)
#     except Exception as e:
#         print(f"Failed to delete files in folder {folder_path}: {str(e)}")


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