"""Start the closed loop in one go: turtlesim, limiter and go_to_goal.

    /turtlesim --/turtle1/pose--> /go_to_goal --cmd_vel--> /limiter --act--> /turtlesim

Run:
    ros2 launch robotics_day2 closed_loop.launch.py
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='turtlesim'),
        Node(
            package='ros_exercise',
            executable='limiter',
            remappings=[('act', '/turtle1/cmd_vel')],
        ),
        Node(package='ros_exercise', executable='go_to_goal'),
    ])
