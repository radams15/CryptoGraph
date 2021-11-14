FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3-pip python3-gi python3-gi-cairo libgtk-3-0 xauth gobject-introspection gir1.2-gtk-3.0 zlib1g-dev light-themes
RUN apt-get install -y libjpeg-dev
RUN pip3 install cryptocompare matplotlib pyinstaller
