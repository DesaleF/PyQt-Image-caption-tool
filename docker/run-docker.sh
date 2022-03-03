# !/bin/bash
xhost +
docker run --rm -it \
	-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
  --ipc=host --volume="$HOME/.Xauthority:/root/.Xauthority:rw" \
  --userns=host \
  --net=host \
  desalef/pyqt-caption-dataset:latest /bin/bash
  # --device /dev/snd \