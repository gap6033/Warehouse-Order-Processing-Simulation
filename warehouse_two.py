
import copy
import csv
from datetime import timedelta
from queue import Queue
import time
import threading

from models.models import Order, Robot, Item
from warehouse_data_builder import WarehouseDataBuilder
from config import STARTING_STATION_NUMBER, INITIAL_ROBOT_DISTANCE, PACKING_TIME

class WarehouseTwo(WarehouseDataBuilder):
    def __init__(self):
        super().__init__()
        self.item_queue = Queue()
        self.generated_orders: list = copy.deepcopy(WarehouseDataBuilder.ORDERS)
        self.robots = self.build_robot_availability_data(max(self.ORDER_LOADS), STARTING_STATION_NUMBER, INITIAL_ROBOT_DISTANCE)
        self.item_queue_lock = threading.Lock()
        self.process_report = {}

    def add_item_to_queue(self):
        prev_order = None
        while self.generated_orders:
            curr_order: Order = self.generated_orders.pop()
            self.process_report[curr_order.order_num] = curr_order
            if prev_order:
                wait_time: timedelta = curr_order.generated_time - prev_order.generated_time
                time.sleep(wait_time.total_seconds()/100)
            for item in curr_order.item_list:
                self.item_queue.put((item, curr_order.generated_time, curr_order.packing_station))
            prev_order = curr_order

    def process_item(self, robot: Robot):
        while not self.item_queue.empty() or self.generated_orders:
            process_item = False
            with self.item_queue_lock:
                if not self.item_queue.empty():
                    item, item_generated_time , item_packing_station = self.item_queue.get()
                    process_item = True
            if process_item:
                item_process_start_time = max(robot.next_free_time, item_generated_time)
                self.process_current_item(item_process_start_time, item_packing_station, item, robot)
            
        
    def process_current_item(self, item_process_start_time, item_packing_station, item: Item, robot: Robot):
        pickup_station_number = item.item_number
        time_to_pick_items = robot.time_to_reach_destination(robot.curr_station, pickup_station_number, self.warehouse_map)
        robot.curr_station = pickup_station_number
        
        time_to_drop_to_packing_station = robot.time_to_reach_destination(robot.curr_station, item_packing_station, self.warehouse_map)
        item_drop_time = item_process_start_time + timedelta(seconds=time_to_pick_items + time_to_drop_to_packing_station)
        robot.distance_moved += time_to_pick_items + time_to_drop_to_packing_station
        robot.curr_station = item_packing_station
        
        time.sleep((time_to_pick_items + time_to_drop_to_packing_station)/100)

        packing_station_wait_time = self.book_packing_station(item_packing_station) * 100
        
        packing_time = PACKING_TIME
        time.sleep(packing_time/100)

        self.free_packing_station(item_packing_station)

        item_process_end_time = item_drop_time + timedelta(seconds=packing_time + (packing_station_wait_time))
        print('Robot:', robot.robot_number, '\n', 'Robot Station:', robot.curr_station, '\n', 'Item Number:', item, '\n', 'Packing Station:', item_packing_station, '\n', 'Item Process Start Time:', item_process_start_time, '\n', 'Item Process End Time:', item_process_end_time, '\n')
        robot.next_free_time = item_process_end_time
        item.process_end_time = item_process_end_time

    def generate_robot_report(self):
        with open('Robot_Report_Mode_2.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Robot Number', 'Distance Travelled in metres'])
            robot: Robot
            for robot in self.robots:
                writer.writerow([robot.robot_number, robot.distance_moved])

    def activate_robots(self):
        robot_threads = [threading.Thread(target=self.process_item, args=(robot,)) for robot in self.robots]

        # Start the robot threads
        for thread in robot_threads:
            thread.start()
        
        self.add_item_to_queue()

        for thread in robot_threads:
            thread.join()
        
        self.generate_robot_report()

        return self.process_report
    


