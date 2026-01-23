#!/usr/bin/env bash
set -e

source /opt/ros/humble/setup.bash

if [ -f "$HOME/ros2_ws/install/setup.bash" ]; then
  source "$HOME/ros2_ws/install/setup.bash"
fi

exec "$@"
