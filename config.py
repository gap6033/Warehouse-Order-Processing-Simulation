from datetime import datetime, timedelta


ORDER_TIME_MEAN_INTERVAL = 30  # Mean interval in seconds
ORDER_TIME_VARIANCE = 25

ORDER_GENERATION_START_TIME = datetime.strptime('08:00:00', '%H:%M:%S')
ORDER_GENERATION_END_TIME = ORDER_GENERATION_START_TIME + timedelta(hours=1)

ORDER_LOAD_MEAN = 6
ORDER_LOAD_VARIANCE = 9
MIN_ORDER_LOAD = 1
MAX_ORDER_LOAD = 45


WAREHOUSE_ROWS = 9
WAREHOUSE_COLS = 6
WAREHOUSE_SIZE = WAREHOUSE_ROWS * WAREHOUSE_COLS
STARTING_STATION_NUMBER = 1
PACKING_STATIONS = {7, 13, 19, 25, 31, 37, 43, 49}

PACKING_STATION_VALUE = 3
PACKING_TIME = 5

INITIAL_ROBOT_DISTANCE = 0

