FROM adoptopenjdk:8-jdk-hotspot

WORKDIR /usr/src/app

COPY ./build/libs/santa-boj-0.0.1-SNAPSHOT.jar .

ENTRYPOINT ["java","-jar","santa-boj-0.0.1-SNAPSHOT.jar"]

EXPOSE 8888