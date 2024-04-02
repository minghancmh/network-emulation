FROM kindest/node:v1.21.14

WORKDIR /usr/src

RUN apt update && apt-get install netcat-openbsd

COPY send_hello.sh .
COPY welcome.sh .

RUN chmod +x send_hello.sh
RUN chmod +x welcome.sh

# can put the actions that we want to run in the ./welcome.sh script
ENTRYPOINT ["/usr/local/bin/entrypoint", "./welcome.sh"]





