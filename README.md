# Face Obfuscator

Face Obfuscator obfuscates human faces in a video.

## Installation

### AWS EC2

1. Create an EC2 instance with Amazon Linux 2 AMI. For GPU accelerated version, check out the [gpu branch](/mrtj/face-obfuscator/tree/gpu).
2. Launch the instance and login to it with ssh.
3. [Install docker and docker-compose](https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9) on the instance.
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
