import sys
import os

dir_path = os.path.abspath(os.path.dirname(__file__))
if dir_path not in sys.path:
    sys.path.insert(0, dir_path)


__all__ = [
    'syncopation',
    'basic_functions',
    'music_objects',
    'parameter_setter',
    'rhythm_parser',
    'readmidi',
    # models
    'KTH',
    'LHL',
    'PRS',
    'SG',
    'TMC',
    'TOB',
    'WNBD',
]
