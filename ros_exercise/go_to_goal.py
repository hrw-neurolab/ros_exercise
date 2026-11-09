"""Closing the loop: drive the turtle to a goal (discussion point on slide 14).

The limiter alone is not a control loop, because nothing is measured.
This node adds the feedback from day 1:

    Sense  subscribes to /turtle1/pose        where am I?
    Think  P controller, compares pose and goal how far off am I?
    Act    publishes a Twist on cmd_vel        move to reduce the error

The forward speed grows with the distance, so far away it asks for more
than 1 m/s. Put the limiter behind it and watch it cap the speed:

    ros2 run turtlesim turtlesim_node
    ros2 run robotics_day2 limiter --ros-args -r act:=/turtle1/cmd_vel
    ros2 run robotics_day2 go_to_goal

Or all three at once:
    ros2 launch robotics_day2 closed_loop.launch.py

Without the limiter (much faster at the start):
    ros2 run robotics_day2 go_to_goal --ros-args -r cmd_vel:=/turtle1/cmd_vel
"""
import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim_msgs.msg import Pose

GOAL_X = 8.0       # the turtlesim world is about 11 x 11, the turtle starts near 5.5, 5.5
GOAL_Y = 8.0
K_LINEAR = 1.0     # forward speed per metre of distance
K_ANGULAR = 4.0    # turning rate per radian of heading error
MAX_HEADING = 0.5  # rad, only drive forward when roughly facing the goal
TOLERANCE = 0.1    # m, close enough counts as reached


class GoToGoal(Node):

    def __init__(self):
        super().__init__('go_to_goal')
        self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.reached = False

    def on_pose(self, pose):
        # Sense: the error between where we are and where we want to be
        dx = GOAL_X - pose.x
        dy = GOAL_Y - pose.y
        distance = math.hypot(dx, dy)
        heading_error = math.atan2(dy, dx) - pose.theta
        # Wrap the angle to the range -pi .. +pi, so the turtle turns the short way
        heading_error = math.atan2(math.sin(heading_error), math.cos(heading_error))

        # Think: proportional control, the command grows with the error
        msg = Twist()
        if distance > TOLERANCE:
            self.reached = False
            msg.angular.z = K_ANGULAR * heading_error
            if abs(heading_error) < MAX_HEADING:
                msg.linear.x = K_LINEAR * distance
        elif not self.reached:
            self.reached = True
            self.get_logger().info(f'Goal reached at x = {pose.x:.2f}, y = {pose.y:.2f}')

        # Act: an empty Twist (all zeros) stops the turtle at the goal
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = GoToGoal()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
