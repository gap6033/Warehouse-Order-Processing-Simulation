Instructions for user:
- Extract the zip file contents onto a "Folder".
- Make sure you have python 3.10.7 (or similar compatible version) installed
- Bring your terminal to the extracted "Folder" and run:
    "pip install -r requirements.txt" 
    This is to install the numpy==1.25.2 package.
-All the variables have been configured via config.py file
- The program can be run from process.py file:
    - While terminal open in the extracted folder.
    - run "python process.py" command in the terminal
-The output would be three csv files:
    - "Process_report" - containing the time comparisons of two approaches
    -"Robot_Report_Mode_1" - containing distance moved by robot in mode 1
    -"Robot_Report_Mode_2" - containing distance moved by robot in mode 2
-Sample outputs have already been generated for the user. In case of a new run they would be overwritten.

Assumptions and Limitations:
-There is no wait time assumed while picking item from "Storage Stations". Meaning two robots can pick item
from the same station at the same time.
-In mode1, a single order is handled by one robot.
-In mode2, a single item is handled by one robot.
-In mode 1, the packing station is assumed to be free the moment an "order" is packed. Meaning if an order was packed at
12:59:30, another robot can drop his order for packing at 12:59:30.
-In mode 2, the packing station is free the moment an "item" is packed.
-The robots speed and station distance is "1m/s" and "1m" respectively, for ease of calculation. If not one can create a
function that incorporates T = D/S formula to calculate the time.
-Since all the edges from a station are of equal distance, a simple bfs approach was used. In case they were unequal, "Djikastra's
Algorithm" would be the better approach.
-To keep the process short, instead of adding realistic time.sleep() to simulate a realistically busy robot and a stationt, 
the wait time was divided by 100.
-Date is assumed to be 1900-01-01 as which is the default date provided by the datetime module.

Functionalities:
-Docstrings have been added to the WarehouseDataBuilder Class to give an idea of the functionality.
-WarehouseDataBuilder - generates the data for the warehouse - Robots, stations, Orders, Warehouse Map
-WareHouseOne - This replicates mode1 process functionality
-WareHouseTwo - This replicates mode2 process functionality
