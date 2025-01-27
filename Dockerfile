FROM ubuntu:latest
LABEL authors="jerry"

ENTRYPOINT ["top", "-b"]