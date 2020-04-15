import os
from .config import *
from .settings import *


# Set default config to ProductionConfig unless STAGING environment
# is set to true on Linux `export STAGING=True` or Windows Powershell
# `$Env:STAGING="True"`. Using os.environ directly will throw errors
# if not set.
STAGING = os.getenv("STAGING") or "False"

if STAGING == "True":
    config = StagingConfig()
else:
    config = ProductionConfig()

# print(f"[DEBUG] Config being used is: {config.__class__.__name__}")
