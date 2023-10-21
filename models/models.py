from collections import deque
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Item:
    item_number: int
    process_end_time: datetime | bool = False

@dataclass
class Order:
    generated_time: datetime
    order_num: int
    item_list: set[Item]
    packing_station: int


@dataclass
class Robot:
    robot_number: int
    curr_station: int
    distance_moved: int
    next_free_time: int

    @staticmethod
    def time_to_reach_destination(start_station: int, destination_station: int, warehouse_map: dict) -> int:
        curr_time = 0
        dq = deque()
        dq.append((curr_time, start_station))
        visited = set()
        visited.add(start_station)
        while dq:
            curr_time, popped_station = dq.popleft()
            for adj_station in warehouse_map[popped_station]:
                if adj_station == destination_station:
                    return curr_time + 1
                if adj_station in visited:
                    continue
                dq.append((curr_time + 1, adj_station))

                visited.add(adj_station)
                
        

