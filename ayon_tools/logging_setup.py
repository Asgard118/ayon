import logging
import os

if os.getenv("DEBUG"):
    logging.basicConfig(level=logging.DEBUG)
