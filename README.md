# Flask and Docker example

This is the sample python3, MongoDB CRUD app. Each part is deployed on separate Docker containers. The Nginx and uWSGI used as a web and app servers respectivly. 

The complete app stack as below.

1. Python3 and Flask
2. JWT Authentication
3. Mongodb
4. Docker and Docker Compose
5. Nginx and uWSGI

# Prerequisites
Install Docker and  Docker Compose.

# Steps to run
1. Git pull
2. Run

```
$ docker-compose up --build
```