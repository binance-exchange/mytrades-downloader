import glob
import os

def scan_files(destination_dir, file_format=None):
  if file_format:
    return [os.path.basename(x) for x in glob.glob("{}*.{}".format(destination_dir, file_format))]
  return [os.path.basename(x) for x in glob.glob("{}*".format(destination_dir))]
