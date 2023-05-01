import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')
DATA_DIR = os.path.join(ROOT_DIR, 'data')

TRIPS_FILE = os.path.join(CONFIG_DIR, 'trips.csv')
RESULTS_FILE = os.path.join(DATA_DIR, 'results.csv')
LOG_FILE = os.path.join(DATA_DIR, 'log.txt')