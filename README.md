# turtlebot_operation_Menna
# TurtleBot Operation

This project uses ROS 2 to control a TurtleBot and avoid obstacles using LiDAR data.

There are two packages in the project:

- obstacle_direction_controller
- obstacle_direction_interfaces

The controller reads the LiDAR data from `/scan` and sends movement commands through `/cmd_vel`. A custom service called `/set_direction` is also used to change the direction of the robot.

## Directions

The available directions are:

- forward
- reverse
- left
- right

## Setup

Build the packages:

```bash
cd ~/workspaces/ros2_ws
colcon build --packages-select obstacle_direction_interfaces obstacle_direction_controller
source install/setup.bash
```

Run the controller:

```bash
ros2 run obstacle_direction_controller direction_autopilot
```

## Set Direction

The `/set_direction` service can be called from another terminal.

For example:

```bash
ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: 'left'}"
```

The direction can be changed to `forward`, `reverse`, `left`, or `right`.

## Testing

Some useful commands for testing are:

```bash
ros2 service list
ros2 topic list
ros2 topic echo /scan
ros2 topic echo /cmd_vel
```

`ros2 topic echo /scan` shows the LiDAR readings and `ros2 topic echo /cmd_vel` shows the movement commands being sent to the robot.

When the service is called successfully, an output similar to this should appear:

```text
success: true
message: "Direction changed to left"
```

If an obstacle is detected near the robot, the controller changes its movement to avoid it.

## Project Structure

```text
turtlebot_operation_Menna/
├── obstacle_direction_controller/
│   ├── obstacle_direction_controller/
│   │   ├── __init__.py
│   │   └── direction_autopilot_node.py
│   ├── package.xml
│   ├── setup.py
│   └── setup.cfg
│
├── obstacle_direction_interfaces/
│   ├── srv/
│   │   └── SetDirection.srv
│   ├── CMakeLists.txt
│   └── package.xml
│
└── README.md
```

## Demo

For the demo, the TurtleBot simulation and the controller are run together. The robot uses the LiDAR readings to detect obstacles, and the `/set_direction` service can be used to change its direction.
