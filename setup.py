import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'ros_exercise'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Makes the launch files findable by "ros2 launch ros_exercise ..."
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jonas Main PC',
    maintainer_email='jonas28st@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        # name used by "ros2 run" = module:function
        'driver = ros_exercise.driver:main',
        'listener = ros_exercise.listener:main',
        'circle = ros_exercise.circle:main',
        'limiter = ros_exercise.limiter:main',
        'limiter_angular = ros_exercise.limiter_angular:main',
        'go_to_goal = ros_exercise.go_to_goal:main',
        ],
    },
)
