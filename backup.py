import os
import time
import tarfile
import datetime
import logging
import sys 


# The destination folder where the logs are stored
dest_folder = "//192.168.0.3/public/Data/logs"

# The tar folder where the compressed logs will be saved
tar_folder = "//192.168.0.3/public/Data/logs/Archive"

# The log folder
BASE_DIR = '//192.168.0.3/public/Data/'
LOG_DIR = os.path.join(BASE_DIR, 'logs/')

# The number of seconds in 7 days
#seven_days = 7 * 24 * 60 * 60
seven_days =  1 * 60 * 60




# Get the current date and time
today = datetime.date.today().strftime("%Y%m%d")
currunttime = time.time()
current_datetime = datetime.datetime.now()
current_datetime_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

# Define the log file path with the current date and time
log_file_path = os.path.join(LOG_DIR, f"Achieve_log_{current_datetime_str}.log")

file_handler = logging.FileHandler(filename=log_file_path)
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
    handlers=handlers
    )
        
tar_file = f"logs_{today}.tar"

tar_path = os.path.join(tar_folder, tar_file)
with tarfile.open(tar_path, "w") as tar:

    # Loop through the files in the destination folder
    for file in os.listdir(dest_folder):
        file_path = os.path.join(dest_folder, file)

        # Check if the file is a log file and older than 7 days
        if file.endswith(".log") and (currunttime - os.path.getmtime(file_path)) > seven_days:
            try: 
                # Add the log file to the tar file
                tar.add(file_path, arcname=file)
                #Enable bottom line for debugging
                #print(f"Compressed {file} to {tar_file}")
                os.remove(file_path)
            except OSError:
                logging.info(file_path + ' is locked')
                continue

# Close the tar file
tar.close()

