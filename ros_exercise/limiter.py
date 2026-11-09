"""A node that thinks (Day 2, slide 14).

Sense, Think, Act in its smallest form:
    /driver  --cmd_vel-->  /limiter  --act-->  /turtlesim

The limiter subscribes to cmd_vel, caps the forward speed at +/- LIMIT
and publishes the result on act.

Run:
    ros2 run robotics_day2 limiter

Let the output drive the turtle:
    ros2 run robotics_day2 limiter --ros-args -r act:=/turtle1/cmd_vel

See the thinking (set SPEED = 2.0 in driver.py first):
    ros2 topic echo /cmd_vel
    ros2 topic echo /act
"""
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from geometry_msgs.msg import Twist

LIMIT = 1.0  # m/s


class Limiter(Node):

    def __init__(self):
        super().__init__('limiter')
        self.create_subscription(Twist, 'cmd_vel', self.think, 10)
        self.pub = self.create_publisher(Twist, 'act', 10)

    def think(self, msg):
        x = msg.linear.x
        msg.linear.x = max(-LIMIT, min(x, LIMIT))
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Limiter()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
