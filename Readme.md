Assumptions and Limitations:
- Simulating order processing in a warehouse.
- Warehouse is in the form of 2d matrix of size L * @
- There are 'x' pickup stations and y 'packing stations' all numbered between 1 to L * W (both inclusive)
- Stations are connected to their immediate adjacent station in all four directions - up, down, left and right directions
- The distance between two adjacent station is 1m
- Orders are generated randomly.
- Each order consists of items that are to be picked from pickup stations.
- The items of an order are all to be dropped them at one packing station.
- Warehouse has robots for picking up and drop items from an order for packing.
- The speed of the robot is 1m/s.
- Warehouse can process in two ways.
- Mode 1
    - A free Robot can pickup items in a generaetd order from all the pickup stations sequentially and then drop them at the packing station.
    - Only after completion of the packing the order can this robot be assigined a new order.
- Mode 2
    - A free robot can pick an item from a generated order and then drop it to the packing station.
    - Only after completion of the packing this item can this robot be assigined a new order.

- Robots per warehouse is equal to max(order size) among all the generated orders.
- There is no wait time assumed while picking item from "Storage Stations". Meaning two robots can pick item
from the same station at the same time.
- In mode1, a single order is handled by one robot.
- In mode2, a single item is handled by one robot.
- In mode 1, the packing station is assumed to be free the moment an "order" is packed. Meaning if an order was packed at
12:59:30, another robot can drop his order for packing at 12:59:30.
- In mode 2, the packing station is free the moment an "item" is packed.
- The robots speed and station distance is "1m/s" and "1m" respectively, for ease of calculation. If not one can create a
function that incorporates T = D/S formula to calculate the time.
- Since all the edges from a station are of equal distance, a simple bfs approach was used. In case they were unequal "Djikastra's
Algorithm" would be the better approach.
- To keep the process short, instead of adding realistic time.sleep() to simulate a realistically busy robot and a stationt, 
  the wait time was divided by 100.
- Date is assumed to be 1900-01-01 as which is the default date provided by the datetime module.

Functionalities:
- Docstrings have been added to the WarehouseDataBuilder Class to give an idea of the functionality.
- WarehouseDataBuilder - generates the data for the warehouse - Robots, stations, Orders, Warehouse Map
- WareHouseOne - This replicates mode1 process functionality
- WareHouseTwo - This replicates mode2 process functionality


Instructions for user:
- Extract the zip file contents onto a "Folder".
- Make sure you have python 3.10.7 (or similar compatible version) installed
- Bring your terminal to the extracted "Folder" and run:
    "pip install -r requirements.txt" 
    This is to install the numpy==1.25.2 package.
- All the variables have been configured via config.py file
- The program can be run from process.py file:
    - While terminal open in the extracted folder.
    - run "python process.py" command in the terminal
- The output would be three csv files:
    - "Process_report" - containing the time comparisons of two approaches
    - "Robot_Report_Mode_1" - containing distance moved by robot in mode 1
    - "Robot_Report_Mode_2" - containing distance moved by robot in mode 2
- Sample outputs have already been generated for the user. In case of a new run they would be overwritten.

