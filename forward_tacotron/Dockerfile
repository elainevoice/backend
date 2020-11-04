# Get Python version 3.7.4
FROM python:3.7.4

# Apparently opencv-python has an issue 
# Got to install these libraries
RUN apt-get update
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6'  -y

# Get espeak
RUN apt-get -y install espeak

# Install GIT 
RUN apt-get -y install git-all

# retrieve forward tacotron
RUN git clone https://github.com/as-ideas/ForwardTacotron /root/ForwardTacotron

# Install Packages
RUN pip install -r /root/ForwardTacotron/requirements.txt

# CUDA
RUN apt-get update && apt-get install -y build-essential
RUN apt-get --purge remove -y nvidia*

ADD ./Downloads/nvidia_installers /tmp/nvidia                             > Get the install files you used to install CUDA and the NVIDIA drivers on your host
RUN /tmp/nvidia/NVIDIA-Linux-x86_64-331.62.run -s -N --no-kernel-module   > Install the driver.
RUN rm -rf /tmp/selfgz7                                                   > For some reason the driver installer left temp files when used during a docker build (i don't have any explanation why) and the CUDA installer will fail if there still there so we delete them.
RUN /tmp/nvidia/cuda-linux64-rel-6.0.37-18176142.run -noprompt            > CUDA driver installer.
RUN /tmp/nvidia/cuda-samples-linux-6.0.37-18176142.run -noprompt -cudaprefix=/usr/local/cuda-6.0   > CUDA samples comment if you don't want them.
RUN export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64         > Add CUDA library into your PATH
RUN touch /etc/ld.so.conf.d/cuda.conf                                     > Update the ld.so.conf.d directory
RUN rm -rf /temp/*  > Delete installer files.

# Set Working Directory
WORKDIR /root/ForwardTacotron