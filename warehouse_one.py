
import copy
import csv
from datetime import timedelta
from queue import Queue
import time
import threading

from models.models import Order, Robot, Item
from warehouse_data_builder import WarehouseDataBuilder
from config import STARTING_STATION_NUMBER, INITIAL_ROBOT_DISTANCE, PACKING_TIME

class WarehouseOne(WarehouseDataBuilder):
    def __init__(self):
        super().__init__()
        self.order_queue = Queue()
        self.generated_orders = copy.deepcopy(WarehouseDataBuilder.ORDERS)
        self.robots = self.build_robot_availability_data(max(self.ORDER_LOADS), STARTING_STATION_NUMBER, INITIAL_ROBOT_DISTANCE)
        self.total_orders = len(self.generated_orders)
        self.order_queue_lock = threading.Lock()
        self.process_report = {}

    def add_order_to_queue(self):
        '''
        Adds order from the generated orders to a queue for the robot to pick
        '''
        prev_order = None
        while self.generated_orders:
            curr_order: Order = self.generated_orders.pop()
            if prev_order:
                wait_time: timedelta = curr_order.generated_time - prev_order.generated_time
                time.sleep(wait_time.total_seconds()/100)
            self.order_queue.put(curr_order)
            self.process_report[curr_order.order_num] = curr_order
            prev_order = curr_order

    def process_order(self, robot: Robot):
        '''
        Robot Picks order from queue and processes it
        '''
        while self.generated_orders or not self.order_queue.empty():
            order: Order
            process_order = False
            with self.order_queue_lock:
                if not self.order_queue.empty():
                    order = self.order_queue.get()
                    process_order = True
            if process_order:
                order_process_start_time = max(robot.next_free_time, order.generated_time)
                self.process_current_order(order_process_start_time, order, robot)

        
    def process_current_order(self, order_process_start_time, order: Order, robot: Robot):
        pickup_stations = order.item_list
        time_to_pick_items = 0
        item: Item
        for item in pickup_stations:
            pickup_station_number = item.item_number
            time_to_pick_items += robot.time_to_reach_destination(robot.curr_station, pickup_station_number, self.warehouse_map)
            robot.curr_station = pickup_station_number
        packing_station = order.packing_station
        time_to_drop_to_packing_station = robot.time_to_reach_destination(robot.curr_station, packing_station, self.warehouse_map)
        order_drop_time = order_process_start_time + timedelta(seconds=time_to_pick_items + time_to_drop_to_packing_station)
        robot.distance_moved += time_to_pick_items + time_to_drop_to_packing_station
        robot.curr_station = packing_station
        time.sleep((time_to_pick_items + time_to_drop_to_packing_station)/100)

        packing_station_number = order.packing_station
        packing_station_wait_time = self.book_packing_station(packing_station_number) * 100
        
        packing_time = len(order.item_list) * PACKING_TIME
        time.sleep(packing_time/100)
        self.free_packing_station(packing_station_number)

        order_process_end_time = order_drop_time + timedelta(seconds=packing_time + (packing_station_wait_time))
        print(robot.robot_number, threading.current_thread().name,'Robot:', robot.robot_number, '\n', 'Order Number', order.order_num, 'Order Process Start Time:', order_process_start_time, '\n', 'Order Process End Time:', order_process_end_time, '\n')
        robot.next_free_time = order_process_end_time
        
        for station in pickup_stations:
            station.process_end_time = order_process_end_time

    def generate_robot_report(self):
        with open('Robot_Report_Mode_1.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Robot Number', 'Distance Travelled in metres'])
            robot: Robot
            for robot in self.robots:
                writer.writerow([robot.robot_number, robot.distance_moved])

    def activate_robots(self):
        robot_threads = [threading.Thread(target=self.process_order, args=(robot,)) for robot in self.robots]

        # Start the robot threads
        for thread in robot_threads:
            thread.start()
        
        self.add_order_to_queue()

        for thread in robot_threads:
            thread.join()
        
        self.generate_robot_report()

        return self.process_report
    
        
