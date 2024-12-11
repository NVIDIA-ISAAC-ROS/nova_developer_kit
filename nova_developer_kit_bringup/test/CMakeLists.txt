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

find_package(launch_testing_ament_cmake REQUIRED)

# Get the path to a dummy bag for use in the tests.
get_dummy_bag_path(DUMMY_BAG_PATH)

add_graph_startup_test(multi_cam_perceptor_dry_run
    launch/perceptor.launch.py
    TIMEOUT 60
    ARGS "mode:=rosbag rosbag:=${DUMMY_BAG_PATH} run_rviz:=False run_foxglove:=False"
)

add_graph_startup_test(single_cam_perceptor_dry_run
    launch/perceptor.launch.py
    TIMEOUT 60
    ARGS "mode:=rosbag rosbag:=${DUMMY_BAG_PATH} run_rviz:=False run_foxglove:=False stereo_camera_configuration:=front_configuration"
)

# Add installation of ESS models as a test fixture.
get_isaac_ros_asset_install_script_path(install_ess_models_script install_ess_models isaac_ros_ess_models_install)
ament_add_test(setup_ess_models
    COMMAND "${install_ess_models_script}"
    ENV "ISAAC_ROS_SKIP_ASSET_INSTALL="
    TIMEOUT 1200
    GENERATE_RESULT_FOR_RETURN_CODE_ZERO
)

# Register the setup ess models script as a pre-test requirement.
set_tests_properties(setup_ess_models PROPERTIES FIXTURES_SETUP pre_test)
set_tests_properties(multi_cam_perceptor_dry_run PROPERTIES FIXTURES_REQUIRED pre_test)
set_tests_properties(single_cam_perceptor_dry_run PROPERTIES FIXTURES_REQUIRED pre_test)
