from datetime import timedelta, datetime
from collections import deque
import numpy as np
import random
import time
from threading import Lock
from models.models import Order, Robot, Item
from config import (ORDER_GENERATION_START_TIME, ORDER_GENERATION_END_TIME, ORDER_TIME_MEAN_INTERVAL, ORDER_TIME_VARIANCE,
                    MIN_ORDER_LOAD, MAX_ORDER_LOAD, ORDER_LOAD_MEAN, ORDER_LOAD_VARIANCE, PACKING_STATIONS, PACKING_STATION_VALUE,
                    STARTING_STATION_NUMBER, WAREHOUSE_SIZE, WAREHOUSE_ROWS, WAREHOUSE_COLS)

def generate_random_pickup_stations(first_station_number: int, warehouse_size: int, order_load: int, packaging_stations: int, starting_station: int) -> list:
    '''
    Generate Random PickUp stations for an Order of a given size
    '''
    pickup_stations = set()
    while len(pickup_stations) < order_load:
        station = random.randint(first_station_number, warehouse_size)
        if station in packaging_stations or station == starting_station:
            while station in packaging_stations or station == starting_station:
                station = random.randint(first_station_number, warehouse_size)
        pickup_stations.add(station)

    return sorted(pickup_stations)


def build_packing_station_deque():
    '''
    Build a Deque of Packing Station
    '''
    packing_stations = list(PACKING_STATIONS)
    dq = deque()
    curr_index = 0
    while curr_index < PACKING_STATION_VALUE:
        dq.append(packing_stations[curr_index])
        curr_index += 1
    return dq


class WarehouseDataBuilder:
    def __init__(self):
        self.warehouse_matrix = self.build_matrix()
        self.warehouse_map = self.build_warehouse_map()
        self.packing_stations = set()
        self.packing_station_locks = {}
        self.build_packing_station_data()
        self.add_locks_to_packing_station()
    
    @staticmethod
    def build_matrix():
        '''
        Build a 2d matrix representing warehouse of size WAREHOUSE_ROWS * WAREHOUSE_COLS defined in config.py
        Each cell of the matrix represents a station. The matrix is numbered row wise from left to right. The station 
        numbers are 1-indexed and are identified using the number alloted to them.
        '''
        warehouse = []
        station_number = 1
        for i in range(WAREHOUSE_ROWS):
            station = []
            warehouse.append(station)
            for _ in range(WAREHOUSE_COLS):
                warehouse[i].append(station_number)
                station_number += 1
        return warehouse
    
    def build_warehouse_map(self):
        '''
        Build a graph with connected edges between stations
        '''
        adj_list = {}
        for r in range(WAREHOUSE_ROWS):
            for c in range(WAREHOUSE_COLS):
                curr_station = self.warehouse_matrix[r][c]
                if curr_station not in adj_list:
                    adj_list[curr_station] = set()
                directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
                for x, y in directions:
                    adj_row = r + y
                    adj_col = c + x
                    if adj_row < 0 or adj_row == WAREHOUSE_ROWS or adj_col < 0 or adj_col == WAREHOUSE_COLS:
                        continue
                    adj_station = self.warehouse_matrix[adj_row][adj_col]
                    adj_list[curr_station].add(adj_station)
                    if adj_station not in adj_list:
                        adj_list[adj_station] = set()
                    adj_list[adj_station].add(curr_station)

        return adj_list

    
    @staticmethod
    def generate_random_order_start_time():
        '''
        Generate Order with random order times following the mean time interval and time variance
        restriction as configured via config.py
        '''
        random_times = []
        current_time = ORDER_GENERATION_START_TIME

        while current_time < ORDER_GENERATION_END_TIME:
            random_seconds = max(0, int(random.gauss(ORDER_TIME_MEAN_INTERVAL, ORDER_TIME_VARIANCE ** 0.5)))
            current_time += timedelta(seconds=random_seconds)
            random_times.append(current_time)
        random_times.sort()
        return random_times
    
    @staticmethod
    def generate_random_order_loads(total_orders: int):
        '''
        Generate random order loads following load variance and load mean restriction for all randomly generated
        orders

        :param total_orders (int): The total generated orders
        '''
        # Generate normally distributed numbers with mean=0 and std=1
        normal_values = np.random.normal(0, 1, total_orders)

        # Scale and shift the normal values to have the desired mean and std
        scaled_values = normal_values * (ORDER_LOAD_VARIANCE ** 0.5) + ORDER_LOAD_MEAN

        # Clip the values to fit within the specified range
        clipped_values = np.clip(scaled_values, MIN_ORDER_LOAD, MAX_ORDER_LOAD)

        # Round the values to integers
        rounded_integers = np.round(clipped_values).astype(int)

        return rounded_integers
    
    @staticmethod
    def build_pickup_stations_list(order_loads: list[int]):
        '''
        Add pickup stations to all the generated order loads
        
        :param order_loads (list[int]): Order sizes for all the randomly generated orders
        '''
        pickup_station_list = []
        for i in range(len(order_loads)):
            curr_order_load = order_loads[i]
            pickup_station_list.append(generate_random_pickup_stations(STARTING_STATION_NUMBER, WAREHOUSE_SIZE, curr_order_load, PACKING_STATIONS, STARTING_STATION_NUMBER))
        return pickup_station_list
    
    @staticmethod
    def build_orders(order_generated_times: list[datetime], pickup_stations_list: list[int]):
        '''
        Build Order Data for all the generated order start time
        '''
        packing_stations_deque = build_packing_station_deque()
        orders = []
        order_num = len(order_generated_times)
        for i in range(len(order_generated_times) - 1, -1, -1):
            order_generated_time = order_generated_times[i]
            item_list = []
            for station in pickup_stations_list[i]:
                item_list.append(Item(station))
            packing_station = packing_stations_deque.popleft()
            orders.append(Order(order_generated_time, order_num, item_list, packing_station))
            order_num -= 1
            packing_stations_deque.append(packing_station)
        return orders
    
    @staticmethod
    def build_robot_availability_data(robot_count: int, curr_station: int, distance_moved: int) -> list[Robot]:
        '''
        Generate Robot Objects for all the robots at the warehouse

        :param robot_count: Number of robots in warehouse
        :param curr_station: Station at which the robot is docked
        :param distance moved: Distance Moved by robot.
        '''
        curr_robot = 1
        robot_data = []
        while curr_robot <= robot_count:
            robot_data.append(Robot(curr_robot, curr_station, distance_moved, ORDER_GENERATION_START_TIME))
            curr_robot += 1
        return robot_data
    
    def build_packing_station_data(self):
        '''
        Add packing station number pair to the initalized "self.packing_stations".
        '''
        for station in PACKING_STATIONS:
            self.packing_stations.add(station)
    
    def add_locks_to_packing_station(self):
        '''
        Add packing station number and thread.locks as key-value pair to the initialized self.packing_station_locks
        This is to avoid race conditions when two robots bring item to a station simultaneously, when the station is
        free.
        '''
        for station in PACKING_STATIONS:
            self.packing_station_locks[station] = Lock()
            
    def book_packing_station(self, packing_station_number: int):
        '''
        Aquire Packing Station for packing item brought over by a robot

        :param packaging_station_number (int): The current packaging station
        '''
        start_time = time.time()
        with self.packing_station_locks[packing_station_number]:
            while packing_station_number not in self.packing_stations:
                continue
            self.packing_stations.remove(packing_station_number)
        end_time = time.time()
        wait_time = end_time - start_time
        return wait_time
            
    def free_packing_station(self, packing_station_number: int):
        '''
        Release Packing Station after it has finished packing for other robots to bring items

        :param packaging_station_number (int): The current packaging station
        '''
        self.packing_stations.add(packing_station_number)
        
    ORDER_GENERATED_TIMES = generate_random_order_start_time()
    ORDER_LOADS = generate_random_order_loads(len(ORDER_GENERATED_TIMES))
    PICKUP_STATIONS_LIST = build_pickup_stations_list(ORDER_LOADS)
    ORDERS = build_orders(ORDER_GENERATED_TIMES, PICKUP_STATIONS_LIST)

