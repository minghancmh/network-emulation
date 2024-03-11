FROM kindest/node:v1.21.14

RUN apt update
RUN apt-get install netcat-openbsd

RUN echo "successfully installed..."

CMD [ "echo welcome" ]