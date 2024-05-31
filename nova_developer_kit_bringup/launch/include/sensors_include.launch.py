# SPDX-FileCopyrightText: NVIDIA CORPORATION & AFFILIATES
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

from isaac_ros_launch_utils.all_types import *
import isaac_ros_launch_utils as lu


def generate_launch_description() -> LaunchDescription:
    args = lu.ArgumentContainer()
    args.add_arg('rosbag')
    args.add_arg('enabled_stereo_cameras')
    args.add_arg('type_negotiation_duration_s')
    args.add_arg('enable_human_segmentation', 'False')
    actions = args.get_launch_actions()

    # Sensor data from ROS 2 bag.
    actions.append(
        lu.include(
            'isaac_ros_data_replayer',
            'launch/include/data_replayer_include.launch.py',
            launch_arguments={
                'rosbag': args.rosbag,
                'replay_delay': args.type_negotiation_duration_s,
                'enable_3d_lidar': False,
                'enabled_stereo_cameras': args.enabled_stereo_cameras,
            },
            condition=IfCondition(lu.is_valid(args.rosbag)),
        ))

    # Sensor data from physical sensor drivers.
    actions.append(
        lu.include(
            'isaac_ros_perceptor_bringup',
            'launch/drivers/nova_sensor_drivers.launch.py',
            launch_arguments={
                'enable_3d_lidar': False,
                'enabled_2d_lidars': '',
                'enabled_stereo_cameras': args.enabled_stereo_cameras,
            },
            condition=UnlessCondition(lu.is_valid(args.rosbag)),
        ))
    actions.append(
        lu.include(
            'nova_developer_kit_description',
            'launch/nova_developer_kit_description.launch.py',
            condition=UnlessCondition(lu.is_valid(args.rosbag)),
        ))

    # Visualization.
    actions.append(
        lu.include(
            'isaac_ros_perceptor_bringup',
            'launch/tools/visualization.launch.py',
            launch_arguments={'enable_human_segmentation': args.enable_human_segmentation}))

    return LaunchDescription(actions)
