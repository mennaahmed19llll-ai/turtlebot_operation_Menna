# turtlebot_operation_Menna

This project is a ROS 2 project for controlling a TurtleBot using LiDAR data and avoiding obstacles.

The project contains two packages:

- `obstacle_direction_controller`
- `obstacle_direction_interfaces`

The controller uses LiDAR data from `/scan` to detect obstacles and publishes movement commands to `/cmd_vel`.

The `/set_direction` service can also be used to change the robot's movement direction.

## Directions

The service accepts four directions:

- forward
- reverse
- left
- right

## Packages

### obstacle_direction_interfaces

This package contains the custom ROS 2 service:

`SetDirection.srv`

The request sends a direction:

```text
string direction
```

The service returns:

```text
bool success
string message
```

### obstacle_direction_controller

This package contains `direction_autopilot_node.py`.

The node:

- Receives LiDAR data from `/scan`
- Checks for nearby obstacles
- Chooses a movement direction
- Publishes movement commands to `/cmd_vel`
- Provides the `/set_direction` service
- Prints actions and direction changes in the terminal

## Setup

Go to the ROS 2 workspace:

```bash
cd ~/workspaces/ros2_ws
```

Build the packages:

```bash
colcon build --packages-select obstacle_direction_interfaces obstacle_direction_controller
```

Source the workspace:

```bash
source install/setup.bash
```

## Running the Node

Run the controller with:

```bash
ros2 run obstacle_direction_controller direction_autopilot
```

The node will start receiving LiDAR data and controlling the robot.

## Using the Service

The direction can be changed from another terminal.

For example, to move forward:

```bash
ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: 'forward'}"
```

Turn left:

```bash
ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: 'left'}"
```

Turn right:

```bash
ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: 'right'}"
```

Move backward:

```bash
ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: 'reverse'}"
```

## Useful ROS 2 Commands

Build the project:

```bash
colcon build --packages-select obstacle_direction_interfaces obstacle_direction_controller
```

This builds both packages.

Source the workspace:

```bash
source install/setup.bash
```

This makes the packages available in the current terminal.

Run the controller:

```bash
ros2 run obstacle_direction_controller direction_autopilot
```

Check the available services:

```bash
ros2 service list
```

Check the available topics:

```bash
ros2 topic list
```

View the LiDAR data:

```bash
ros2 topic echo /scan
```

View the movement commands:

```bash
ros2 topic echo /cmd_vel
```

## Testing

First, run the TurtleBot simulation.

Then run the controller:

```bash
ros2 run obstacle_direction_controller direction_autopilot
```

Open another terminal and call `/set_direction` with one of the four directions.

For example:

```bash
ros2 service call /set_direction obstacle_direction_interfaces/srv/SetDirection "{direction: 'left'}"
```

The robot should change its movement direction and the controller should print the change in the terminal.

The LiDAR data can also be tested by placing an obstacle near the robot. The controller detects the obstacle and changes the robot's movement.

## Expected Output

When the node starts:

```text
Direction autopilot started
```

When a service request changes the direction:

```text
Direction changed to left
```

When an obstacle is detected:

```text
Obstacle detected - turning left
```

A successful service call should also return a response similar to:

```text
success: true
message: "Direction changed to left"
```

## Project Structure

```text
turtlebot_operation_Menna/
├── obstacle_direction_controller/
│   ├── obstacle_direction_controller/
│   │   ├── __init__.py
│   │   └── direction_autopilot_node.py
│   ├── package.xml
│   ├── setup.py
│   ├── setup.cfg
│   ├── resource/
│   └── test/
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

For the demo, the TurtleBot simulation is run together with the controller node.

The robot uses the LiDAR data to detect obstacles and publishes movement commands to `/cmd_vel`. The `/set_direction` service can be called from another terminal to change the robot's direction while the program is running.
