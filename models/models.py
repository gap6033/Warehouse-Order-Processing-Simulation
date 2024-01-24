from collections import deque
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Item:
    '''
    Represents an Item received as part of an Order
    '''
    item_number: int
    process_end_time: datetime | bool = False

@dataclass
class Order:
    '''
    Represents the Order received for processing
    '''
    generated_time: datetime
    order_num: int
    item_list: set[Item]
    packing_station: int


@dataclass
class Robot:
    '''
    Represents the robot that would be taking Items of an Order from one station to other for processing
    '''
    robot_number: int
    curr_station: int
    distance_moved: int
    next_free_time: int

    @staticmethod
    def distance_to_reach_destination(start_station: int, destination_station: int, warehouse_map: dict) -> int:
        '''
        Calculate the distance covered to reach destination from start_station. Assumes it takes 1 unit of distance
        to reach from one station to the next connected station

        :param start_station (int): The station at which the Robot is
        :param destination_station (int): The station at which the Robot needs to reach
        :param warehouse_map (dict): Warehouse Map represented by Graph data structure

        Returns:
            Distance covered by Robot
        '''
        curr_dist = 0
        dq = deque()
        dq.append((curr_dist, start_station))
        visited = set()
        visited.add(start_station)
        while dq:
            curr_dist, popped_station = dq.popleft()
            for adj_station in warehouse_map[popped_station]:
                if adj_station == destination_station:
                    return curr_dist + 1
                if adj_station in visited:
                    continue
                dq.append((curr_dist + 1, adj_station))

                visited.add(adj_station)
                
        

