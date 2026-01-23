FROM ros:humble-ros-base

ARG USERNAME=kodifly
ARG USER_UID=1000
ARG USER_GID=1000

SHELL ["/bin/bash", "-c"]

# Create user
RUN groupadd --gid ${USER_GID} ${USERNAME} \
 && useradd  --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME} \
 && apt-get update \
 && apt-get install -y sudo \
 && echo ${USERNAME} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USERNAME} \
 && chmod 0440 /etc/sudoers.d/${USERNAME}

# Dev deps (add whatever you need here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-colcon-common-extensions \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir nicegui

USER ${USERNAME}
WORKDIR /home/${USERNAME}

COPY docker/ros_entrypoint.sh /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
