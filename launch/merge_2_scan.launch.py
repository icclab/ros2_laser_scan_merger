#
#   created by: Michael Jonathan (mich1342)
#   github.com/mich1342
#   24/2/2022
#
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
import launch_ros.actions
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from nav2_common.launch import RewrittenYaml
from launch_ros.descriptions import ParameterFile

def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('ros2_laser_scan_merger'),
        'config',
        'params.yaml'
    )

    ld = LaunchDescription()

    namespace = LaunchConfiguration('namespace')

    ld.add_action(DeclareLaunchArgument(
        name='namespace',
        description='Namespace / Id of the robot',
        default_value='summit',
    ))

    configured_params = ParameterFile(
    RewrittenYaml(
        source_file=config,
        root_key=namespace,
        param_rewrites={},
        convert_types=True,
    ),
    allow_substs=True,
    )
    
    ld.add_action(launch_ros.actions.Node(
        package='ros2_laser_scan_merger',
        executable='ros2_laser_scan_merger',
        parameters=[configured_params],
        output='screen',
        respawn=True,
        respawn_delay=2,
    ))
    # TF2 for laser to map frame id, optional
    # launch_ros.actions.Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     name='static_transform_publisher',
    #     arguments=[
    #         '--x', '0', '--y', '0', '--z', '0',
    #         '--qx', '0', '--qy', '0', '--qz', '0', '--qw', '1',
    #         '--frame-id', 'map', '--child-frame-id', 'laser'
    #     ]
    # ),

    # Call pointcloud_to_laserscan package
    ld.add_action(launch_ros.actions.Node(
        name='pointcloud_to_laserscan',
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        parameters=[configured_params],
        remappings=[('/scan', 'scan'),], # make sure it gets namespaced
    ))

    return ld
    

