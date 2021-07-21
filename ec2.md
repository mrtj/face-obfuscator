# Configuring Amazon EC2 instances to run face-obfuscator

## Create an EC2 instance

If you need help on how to create an Amazon EC2 instance and how to connect it with `ssh`, refer to [this guide](https://www.guru99.com/creating-amazon-ec2-instance.html)

### Instance type

It is highly recommended to use an EC2 instance with NVIDIA GPU to run `face-obfuscator`. Only one GPU will be used, so choose one from the following instance types:
 - `p2.xlarge`
 - `p3.2xlarge`
 - `g4dn.xlarge`

Optionally you can use also CPU-only instances, but the video processing will be much slower.

### Amazon Machine Image

If you use a GPU instance, choose [Amazon Linux 2 AMI with NVIDIA TESLA GPU Driver](https://aws.amazon.com/marketplace/pp/prodview-64e4rx3h733ru). If you use CPU-only instance, choose Amazon Linux 2 AMI.

### Storage

Ensure your root EBS volume has the size of at least 20 GBytes.

## Configure the instance

After the instance has launched, connect to it with ssh. We will need to install git, Docker, docker-compose and NVIDIA Container Toolkit on the instance.

### Install Git

```bash
$ sudo yum update -y
$ sudo yum install -y git
```

### Install Docker CE

```bash
$ sudo amazon-linux-extras install docker
$ sudo service docker start
$ sudo usermod -a -G docker ec2-user
$ sudo chkconfig docker on
```

Reboot the system:
```bash
$ sudo reboot
```

Reconnect to the instance with `ssh` and verify the installation:
```bash
$ docker run --rm hello-world
```

### Install docker-compose

```bash
$ sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose 
$ sudo chmod +x /usr/local/bin/docker-compose
```

Verify the installation:
```bash
$ docker-compose version
```

### Install NVIDIA Container Toolkit

```bash
$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | sudo tee /etc/yum.repos.d/nvidia-docker.repo
```

While installing NVIDIA Container Toolkit, temporary disable the yum repository `@amzn2-graphics` as it often contains only outdated version of the package.

```bash
$ sudo yum-config-manager --disable amzn2-graphics
$ sudo yum clean expire-cache
$ sudo yum install nvidia-docker2 -y
$ sudo yum-config-manager --enable amzn2-graphics
```

Restart the docker daemon and verify the installation:

```bash
$ sudo systemctl restart docker
$ docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```



For more info see the [NVIDIA Container Toolkit installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#id5).