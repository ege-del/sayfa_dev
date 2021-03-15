"""
adds each cronjob specificed in the config.py file
refer to config.py to add new cronjobs
"""
import pathlib
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '../'))
import config

aug_paths = list(map(lambda x : x.format(os.path.abspath('..')) , config.CRONJOBS))
open(config.CRONJOB_PATH,'w+').writelines(aug_paths)
