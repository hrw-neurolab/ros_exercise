# Sourcing

When opening a new terminal ALWAYS source ROS:

```bash
source /opt/ros/$ros_version$/setup.bash
```

# Working Directory

Create a ROS working space e.g.:

```bash
mkdir ros_workspace
cd ros_workspace
```


# ROS Python package

To create a Python package with a template use:

```bash
ros2 pkg create --build-type ament_python my_package_name
```

# Virtual Environment

 Create virtual environment ***inside*** the new package (here: ros_exercise) with system dependencies:
 
```bash
python3 -m venv .venv --system-site-packages
```

# Copy Files

Copy the files into your new package folder like:

```
ros_exercise/                     # ament_python package (workspace root)
├── launch/                       # launch files
│   └── closed_loop.launch.py     # turtlesim + limiter + go_to_goal together
├── ros_exercise/                 # Python module — the nodes live here
│   ├── __init__.py
│   ├── driver.py                 # publisher: cmd_vel at 10 Hz, SPEED = 0.2
│   ├── listener.py               # subscriber
│   ├── circle.py                 # drives in a circle
│   ├── limiter.py                # clamps linear.x  → act
│   ├── limiter_angular.py        # clamps angular.z → act
│   ├── go_to_goal.py             # controller: pose → cmd_vel
│   └── py.typed                  # marks the package as typed (PEP 561)
├── resource/
│   └── ros_exercise              # empty marker file for the ament index
├── test/                         # ament linter tests
│   ├── test_copyright.py
│   ├── test_flake8.py
│   ├── test_mypy.py
│   ├── test_pep257.py
│   └── test_xmllint.py
├── package.xml                   # metadata + dependencies
├── setup.cfg                     # routes executables to lib/ros_exercise
└── setup.py                      # console_scripts + data_files (launch/)                     # console_scripts + data_files (launch/)
```

Add the entry points for the nodes in setup.py:

```python
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
```

# Build & Source

```bash
python3 -m colcon build
source install/setup.bash
```

# Run Node

```bash
ros2 run ros_exercise drive
```

```bash
ros2 run ros_exercise limiter
```

