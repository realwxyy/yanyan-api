from concurrent_log_handler import ConcurrentRotatingFileHandler
import logging
import os

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logfile = os.path.abspath("mylogfile.log")
time_rotating_file_handler = ConcurrentRotatingFileHandler(logfile, "a", 5*1024*1024, 30)
time_rotating_file_handler.setLevel(logging.INFO)
time_rotating_file_handler.setFormatter(formatter)
logger.addHandler(time_rotating_file_handler)
# 输出到控制台的log
sh = logging.StreamHandler()
sh.setLevel(level=logging.INFO)
sh.setFormatter(formatter)
logger.addHandler(sh)