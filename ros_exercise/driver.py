"""Your first publisher node (Day 2, slide 13).

Publishes a velocity command on the topic cmd_vel ten times per second.

Run:
    ros2 run robotics_day2 driver

Drive the turtle directly (no limiter in between):
    ros2 run robotics_day2 driver --ros-args -r cmd_vel:=/turtle1/cmd_vel
"""
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from geometry_msgs.msg import Twist

SPEED = 0.2  # m/s forward. Set it to 2.0 to see the limiter at work (slide 14).


class Driver(Node):

    def __init__(self):
        super().__init__('driver')
        # Message type, topic name, queue size
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        # Call self.tick every 0.1 s, i.e. ten times per second
        self.timer = self.create_timer(0.1, self.tick)

    def tick(self):
        msg = Twist()
        msg.linear.x = SPEED
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Driver()
    try:
        rclpy.spin(node)  # keeps the node alive and runs its callbacks
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
