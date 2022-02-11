# Simulation_ws

### Start Simulation 1
- ### called by spawn: trobot_gazebo worldlaunch.launch
- trobot_description spawn.launch
- ### need to make these one!
- ### called by other launch files: trobot_description rviz.launch

### Gmapping Simulation
- ### start sim
- trobot_motion_plan gmapping.launch
- controllers simple_py_only.launch 

### Move to point contoroller
- controllers simple_C.launch 
- ### This launches rviz and the waypoint controller

### Fire up lidar sensor for ros
