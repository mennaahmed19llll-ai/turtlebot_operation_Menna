import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

from obstacle_direction_interfaces.srv import SetDirection


class DirectionAutopilot(Node):

    def __init__(self):
        super().__init__('direction_autopilot')

        # Publisher for robot movement
        self.publisher_ = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Subscriber for LiDAR data
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Service used to override the current direction
        self.service = self.create_service(
            SetDirection,
            '/set_direction',
            self.set_direction_callback
        )

        # Default movement state
        self.current_direction = 'forward'

        self.get_logger().info(
            'Direction autopilot started'
        )

    def set_direction_callback(self, request, response):
        valid_directions = [
            'forward',
            'reverse',
            'left',
            'right'
        ]

        direction = request.direction.lower()

        if direction in valid_directions:
            self.current_direction = direction

            response.success = True
            response.message = (
                f'Direction changed to {direction}'
            )

            self.get_logger().info(
                response.message
            )

        else:
            response.success = False
            response.message = (
                'Invalid direction. Use forward, reverse, left, or right.'
            )

            self.get_logger().warn(
                response.message
            )

        return response

    def scan_callback(self, msg):
        # Remove invalid LiDAR readings
        valid_ranges = [
            distance
            for distance in msg.ranges
            if distance > 0.0
        ]

        if not valid_ranges:
            return

        # Find the closest obstacle
        closest_distance = min(valid_ranges)

        # If an obstacle is too close, turn left
        if closest_distance < 0.5:
            self.current_direction = 'left'

            self.get_logger().info(
                'Obstacle detected - turning left'
            )

        self.publish_movement()

    def publish_movement(self):
        msg = Twist()

        if self.current_direction == 'forward':
            msg.linear.x = 0.2
            msg.angular.z = 0.0

        elif self.current_direction == 'reverse':
            msg.linear.x = -0.2
            msg.angular.z = 0.0

        elif self.current_direction == 'left':
            msg.linear.x = 0.0
            msg.angular.z = 0.5

        elif self.current_direction == 'right':
            msg.linear.x = 0.0
            msg.angular.z = -0.5

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = DirectionAutopilot()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main() 
