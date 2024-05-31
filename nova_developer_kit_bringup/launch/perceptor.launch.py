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

# flake8: noqa: F403,F405
import isaac_ros_launch_utils as lu
from isaac_ros_launch_utils.all_types import *


def generate_launch_description() -> LaunchDescription:
    args = lu.ArgumentContainer()
    args.add_arg('mode', 'real_world', choices=['real_world', 'rosbag'], cli=True)
    args.add_arg('rosbag', 'None', cli=True)
    args.add_arg('enabled_fisheye_cameras', '', cli=True)
    args.add_arg('stereo_camera_configuration',
                 default='front_left_right_configuration',
                 choices=[
                     'front_configuration',
                     'front_people_configuration',
                     'front_left_right_configuration',
                     'front_left_right_people_configuration',
                 ],
                 cli=True)
    args.add_arg('use_foxglove_whitelist', True, cli=True)
    args.add_arg('type_negotiation_duration_s', lu.get_default_negotiation_time(), cli=True)

    is_real_world = lu.is_equal(args.mode, 'real_world')

    actions = args.get_launch_actions()
    actions.append(SetParameter('type_negotiation_duration_s', args.type_negotiation_duration_s))
    actions.append(SetParameter('use_sim_time', True, condition=UnlessCondition(is_real_world)))

    # Add the perceptor (note that this also includes the hardware abstraction layer for now).
    actions.append(
        lu.include('nova_developer_kit_bringup', 'launch/include/perceptor_include.launch.py'))

    actions.append(
        lu.include(
            'isaac_ros_perceptor_bringup',
            'launch/tools/visualization.launch.py',
            launch_arguments={'use_foxglove_whitelist': args.use_foxglove_whitelist},
        ))

    actions.append(lu.component_container('nova_container'))

    return LaunchDescription(actions)
