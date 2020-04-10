from utils.config import *
from utils.settings import *
import os

STAGING = os.environ["STAGING"]

if STAGING == "True":
    config = StagingConfig()
else:
    config = ProductionConfig()

# print(f"[DEBUG] Config being used is: {config.__class__.__name__}")
