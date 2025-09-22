FROM maven:latest
LABEL authors="gneg"

COPY scanity/pom.xml .
COPY scanity/src ./src

RUN mvn clean package -DskipTests

ENTRYPOINT ["java","-jar","./target/scanity-0.0.1-SNAPSHOT.jar"]