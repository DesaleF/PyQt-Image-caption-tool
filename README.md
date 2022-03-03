# PyQt-Image-Caption
This codebase contains a pyqt application to create image captioning dataset to train image captioning models.

# Docker Image
## build image
```shell
docker build --no-cache -t desalef/pyqt-caption-dataset .
```
## run container
```shell
xhost +
docker run --rm -it \
	-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
  --ipc=host --volume="$HOME/.Xauthority:/root/.Xauthority:rw" \
  --userns=host \
  --net=host \
  desalef/pyqt-caption-dataset:latest /bin/bash
```

## run main.py inside the container
```shell
python3 src/main.py
```

# Note:
To caption images inside the folder you need to mount the folder into the docker container when you run the container. simply add ```" -v path/to/images:/usr/app \ "``` after ```" --net=host \ "``` on run command provided above.

## TODO:
* export captions into different dataset format
* Undo and Redo changes
* Enter for save and load next image

# Sample Screenshot
![Screenshot_1](assets/sample_screenshot.png?raw=true "App Screenshot")

# Dirctory Structure
```shell
├── assets
│   ├── arrow-left.png
│   ├── arrow-right.png
│   └── ...
├── docker
│   ├── build.sh
│   └── run-docker.sh
├── src
│   ├── __init__.py
│   ├── actions.py
│   └── main.py
├── utils
│   ├── __init__.py
│   └── utils.py
├── Dockerfile
├── __init__.py
├── LICENSE
├── main.ui
└── README.md

```
