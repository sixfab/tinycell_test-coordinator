import os

TEMP_PATH = os.path.expanduser("~") + "/.tinycell_test-coordinator"

if not os.path.exists(TEMP_PATH):
    os.mkdir(TEMP_PATH)


