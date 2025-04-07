FROM ubuntu:latest
LABEL authors="karim"

ENTRYPOINT ["top", "-b"]