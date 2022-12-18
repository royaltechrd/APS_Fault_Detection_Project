import logging
import os
from datetime import datetime

#Log_File
LOG_FILE_NAME=f"{datetime.now().strftime('%m%d%Y_%H%m%s')}.log"

#Log_Dir
LOG_DIR=os.path.join(os.getcwd(),"logs")

#create folder if not available 
os.makedirs(LOG_DIR,exist_ok=True)

#LOG FILE PATH
LOG_FILE_PATH=os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s %(levelname)s %(message)s",
    level=logging.INFO
)
