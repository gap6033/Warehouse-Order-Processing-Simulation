from warehouse_one import WarehouseOne
from warehouse_two import WarehouseTwo
import csv
from models.models import Order, Item

class Process:
    def __init__(self):
        self.mode1 = WarehouseOne()
        self.mode2 = WarehouseTwo()
        self.process_report1 = None
        self.process_report2 = None

    def execute(self):
        self.process_report1 = self.mode1.activate_robots()
        self.process_report2 = self.mode2.activate_robots()
        self.generate_process_comparison_report()

    def generate_process_comparison_report(self):
        order_count = len(self.process_report1)
        with open('Process_report.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Order Number', 'Pickup Node', 'Packing Station', 'Order Generated Time', 'Completed Mode 1', 'Completed Mode 2'])
            for i in range(1, order_count + 1):
                order: Order = self.process_report1[i]
                item: Item
                for item in order.item_list:
                    row = [i, item.item_number, order.packing_station, order.generated_time, item.process_end_time, self.get_report_two_item_data(i, item.item_number)]
                    writer.writerow(row)
                    

    def get_report_two_item_data(self, order_num, item_number):
        item: Item
        for item in self.process_report2[order_num].item_list:
            if item.item_number == item_number:
                return item.process_end_time
            

        
if __name__ == '__main__':
    process = Process()
    process.execute()
