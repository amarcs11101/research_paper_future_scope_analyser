import logging
import os
from datetime import datetime
 
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
today = datetime.now().strftime("%Y-%m-%d")
log_file_path = os.path.join(log_dir, f"{today}.log")
 
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()   
    ]
) 
