"""Solution to the bonus task on slide 16: make turtle2 drive in a circle.

The driver from slide 13 with two changes:
    1. it publishes on /turtle2/cmd_vel
    2. it also sets angular.z, so the turtle turns while it drives

Spawn the second turtle first:
    ros2 service call /spawn turtlesim_msgs/srv/Spawn "{x: 2.0, y: 2.0}"

Run:
    ros2 run robotics_day2 circle

Radius of the circle = linear.x / angular.z = 1.0 m / 1.0 rad/s = 1 m
"""
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from geometry_msgs.msg import Twist


class Circle(Node):

    def __init__(self):
        super().__init__('circle')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.tick)

    def tick(self):
        msg = Twist()
        msg.linear.x = 1.0   # m/s
        msg.angular.z = 1.0  # rad/s
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Circle()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
