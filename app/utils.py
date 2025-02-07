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
