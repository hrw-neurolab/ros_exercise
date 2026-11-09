"""The mirror image of the driver: a subscriber node (Day 2, slide 13).

Prints every velocity command that arrives on the topic cmd_vel.

Run (while the driver is running):
    ros2 run robotics_day2 listener

Listen to the limited output instead:
    ros2 run robotics_day2 listener --ros-args -r cmd_vel:=act
"""
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from geometry_msgs.msg import Twist


class Listener(Node):

    def __init__(self):
        super().__init__('listener')
        # Same arguments as create_publisher, plus a callback for each message
        self.create_subscription(Twist, 'cmd_vel', self.on_msg, 10)

    def on_msg(self, msg):
        self.get_logger().info(
            f'linear.x = {msg.linear.x:.2f} m/s, angular.z = {msg.angular.z:.2f} rad/s')


def main(args=None):
    rclpy.init(args=args)
    node = Listener()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
