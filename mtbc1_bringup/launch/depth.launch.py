# Revised by AR Lunan for MockTurtleBotC1 which uses Oak-D-Lite or -Pro Camera only
#
# Copyright (c) 2021 Juan Miguel Jimeno
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution, PythonExpression, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition, LaunchConfigurationEquals
from launch_ros.actions import Node


def generate_launch_description():
    
    oakd_sensors = ['oakd', 'oakdlite', 'oakdpro']
    to_oakd_vars = {
        "oakd": "OAK-D",
        "oakdlite": "OAK-D-LITE",
        "oakdpro": "OAK-D-PRO"
    }
    
    config = os.path.join(
        get_package_share_directory('mtbc1_bringup'), 'config', 'oakd_inertial.yaml'
    )
        
    return LaunchDescription([
            
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(PathJoinSubstitution(
                [FindPackageShare('depthai_examples'), 'launch', 'stereo_inertial.launch.py']
            )),

            launch_parameters=[config],

            condition=IfCondition(PythonExpression(['"', LaunchConfiguration('sensor'), '" in "', str(oakd_sensors), '"'])),
            launch_arguments={
                'camera_model': to_oakd_vars.get(LaunchConfiguration('sensor'), None),              
            }.items()   
        ),
    ])

