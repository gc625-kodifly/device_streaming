from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gui',
            executable='nicegui_node',
            name='example_gui',
            output='screen',
        ),
        Node(
            package='lifecycle_py',
            executable='number_publisher',   # <- from console_scripts
            name='number_publisher',
            output='screen',
        ),
    ])
