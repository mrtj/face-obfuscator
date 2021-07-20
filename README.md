# Face Obfuscator

Face Obfuscator obfuscates human faces in a video.

## Installation

### AWS EC2

1. Create an EC2 instance with [Amazon Linux 2 AMI with NVIDIA TESLA GPU Driver](https://aws.amazon.com/marketplace/pp/prodview-64e4rx3h733ru). The implementation in this branch uses NVIDIA GPUs for faster face detection, so choose an accelerated instance type (currently P2, P3, P4 or G4dn instances).
2. Launch the instance and login to it with ssh.
3. [Install docker and docker-compose](https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9) on the instance.
4. If you did not choose an Amazon Machine Image (AMI) with NVIDIA TESLA GPU Driver preinstalled, install manually the [NVIDIA driver](https://github.com/NVIDIA/nvidia-docker/wiki/Frequently-Asked-Questions#how-do-i-install-the-nvidia-driver) on the host OS. For more info, see also the [AWS documentation on NVIDIA drivers](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html#preinstalled-nvidia-driver)
5. Install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker) on the host OS.
4. Clone this repo on the instance:
```bash
$ git clone https://github.com/mrtj/face-obfuscator.git
```

## Running

1. Place the input video(s) in the `input` folder:
```bash
$ cd face-obfuscator
$ cp path/to/my_input_video.mp4 input/my_input_video.mp4
```
2. Run the application with `docker-compose`. The first time you execute this command, docker will build the application image. This can take some time. Successive executions will be faster.
```bash
$ docker-compose up --build
```
3. The application will try to open each video files in the `input` folder, blur the faces on each frame of the video, and save the blurred video to the `output` folder.
