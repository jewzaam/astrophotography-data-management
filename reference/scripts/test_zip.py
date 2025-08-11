"""
Goal is to verify I can open a zip file containing image files and extract image headers.
"""

# my imports
import common

ZIP_DIR="test_data/"
ZIP_FILENAME="test_data/accept.zip"

output = common.get_filenames([ZIP_DIR], recursive=True, zips=True)

print(output)
