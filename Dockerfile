FROM ubuntu:latest
LABEL authors="thuan"

ENTRYPOINT ["top", "-b"]