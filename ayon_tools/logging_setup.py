import logging
import os

format = (
    "%(levelname)-8s | %(asctime)s | %(module)-15s | line: %(lineno)-4d | %(message)s"
)

if os.getenv("DEBUG"):
    logging.basicConfig(level=logging.DEBUG, format=format)
else:
    logging.basicConfig(level=logging.INFO, format=format)
