################################################################################
# CMake
################################################################################
cmake_minimum_required(VERSION 2.8.3)
project(zetabank_msgs)
################################################################################
# Packages
################################################################################
find_package(catkin REQUIRED COMPONENTS
  message_generation
  std_msgs
  sensor_msgs
  std_srvs
)

################################################################################
# Declare ROS messages, services and actions
################################################################################
add_message_files(
  FILES
  CommInfo.msg
  SensorState.msg
  VersionInfo.msg
  PanoramaImg.msg
  Waypoint.msg
  WaypointList.msg
  Trajectory.msg
  TrajectoryList.msg
  NavigationControl.msg
  NavigationControlStatus.msg
  SaveWaypoint.msg
  BreakTurn.msg
  BatteryInformationMsgs.msg
)

add_service_files(
  DIRECTORY srv
  FILES
  CmdInfo.srv
  TakePanorama.srv
  SetFollowState.srv
  TurnSrv.srv
  TurnQuaternionSrv.srv
)


generate_messages(
  DEPENDENCIES
  std_msgs
  sensor_msgs
)

################################################################################
# Declare ROS dynamic reconfigure parameters
################################################################################

################################################################################
# Catkin specific configuration
################################################################################
catkin_package(
  CATKIN_DEPENDS std_msgs sensor_msgs std_srvs message_runtime
)

################################################################################
# Build
################################################################################

################################################################################
# Install
################################################################################

################################################################################
# Test
################################################################################
