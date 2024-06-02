import sys
import os

dir_path = os.path.abspath(os.path.dirname(__file__))
if dir_path not in sys.path:
    sys.path.insert(0, dir_path)

