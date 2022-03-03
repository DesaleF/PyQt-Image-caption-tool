FROM ubuntu:20.04

LABEL maintainer="DesaleF <desale.df@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive

# # Add user
# RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# Install Python 3, PyQt5
RUN apt-get update && apt-get install -y python3-pyqt5

# copy the files into the docker
WORKDIR /usr/app
COPY assets assets
COPY utils utils
COPY src src
COPY __init__.py __init__.py
COPY main.ui main.ui
ENV PYTHONPATH=/usr/app/:$PYTHONPATH

CMD [ "python3", "src/main.py" ]

