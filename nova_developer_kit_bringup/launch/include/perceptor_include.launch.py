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

# Camera config string is a subset of:
# - driver,rectify,resize,ess_full,ess_light,ess_skip_frames,cuvslam,nvblox
perceptor_configurations = {
    'front_configuration': {
        'front_stereo_camera': 'driver,rectify,resize,ess_full,cuvslam,nvblox',
        'back_stereo_camera': '',
        'left_stereo_camera': '',
        'right_stereo_camera': '',
    },
    'front_people_configuration': {
        'front_stereo_camera': 'driver,rectify,resize,ess_full,cuvslam,nvblox_people',
        'back_stereo_camera': '',
        'left_stereo_camera': '',
        'right_stereo_camera': '',
    },
    'front_left_right_configuration': {
        'front_stereo_camera': 'driver,rectify,resize,ess_full,cuvslam,nvblox',
        'back_stereo_camera': '',
        'left_stereo_camera': 'driver,rectify,resize,ess_light,ess_skip_frames,cuvslam,nvblox',
        'right_stereo_camera': 'driver,rectify,resize,ess_light,ess_skip_frames,cuvslam,nvblox',
    },
    'front_left_right_people_configuration': {
        'front_stereo_camera': 'driver,rectify,resize,ess_full,cuvslam,nvblox_people',
        'back_stereo_camera': '',
        'left_stereo_camera': 'driver,rectify,resize,ess_light,ess_skip_frames,cuvslam,nvblox',
        'right_stereo_camera': 'driver,rectify,resize,ess_light,ess_skip_frames,cuvslam,nvblox',
    },
}


def generate_launch_description() -> LaunchDescription:
    args = lu.ArgumentContainer()

    # String specifying the stereo camera configuration.
    args.add_arg('stereo_camera_configuration')

    perceptor_configuration = lu.get_dict_value(str(perceptor_configurations),
                                                args.stereo_camera_configuration)

    enabled_stereo_cameras_drivers = lu.get_keys_with_substring_in_value(
        perceptor_configuration, 'driver')
    enable_people_segmentation = lu.dict_values_contain_substring(perceptor_configuration,
                                                                  'nvblox_people')

    actions = args.get_launch_actions()
    actions.append(
        lu.include(
            'nova_developer_kit_bringup',
            'launch/include/hardware_abstraction_layer_include.launch.py',
            launch_arguments={
                'enabled_stereo_cameras': enabled_stereo_cameras_drivers,
                'enable_people_segmentation': enable_people_segmentation,
            },
        ))

    actions.append(
        lu.include(
            'isaac_ros_perceptor_bringup',
            'launch/perceptor_general.launch.py',
            launch_arguments={'perceptor_configuration': perceptor_configuration},
        ))

    return LaunchDescription(actions)
