# RIFT

![Docker](https://github.com/USCGA/rift/workflows/Docker/badge.svg?branch=master)

![banner](https://raw.githubusercontent.com/USCGA/rift/development/documentation/cover.png)

Backend for hub located at <https://uscgacyber.net>.

RIFT is a Python 3, Flask driven web application that uses MongoDB for storage. Basically, RIFT is a CTF hosting platform that is tailored to meet specific needs of competitive cyber teams. 

* CTFs: our team found value in allowing multiple users to be creators of their own CTFs. RIFT attempts to tackle some of issues with conventional CTF challenge hosting. By working with a Docker daemon, RIFT users can link their CTF challenge to a Docker image that will spin up when a player demands, assign ephemeral ports, and automatically update the challenge description with the services' ip & port. This way the challenge can still be attempted even if the challenge author isn't present or the challenge crashes. For challenges that only involve files: easy file-uploading for challenge authors.

* Writeups: writeups on challenges we encounter in live/online competitions are how we document techniques and share knowledge with other teams and new members. Wordpress felt tacky, so integrating a public writeup forum with access control felt right.

* Scoring: points are shared between CTFs hosted on RIFT, so each member of the team has a running point total for all team-generated content and a RIFT rank to sport. Moreover, completing writeups and creating challenges should also warrant points! Friendly competition is awesome for learning and engagement.

RIFT is currently crude and unfinished, but it's provided open source as a jump start to creating your own cyber team hub.

## Installation:

### Set up for Development

1. Create/Start a mongodb server:
Do this however you like but Docker keeps it clean.
```
mkdir ~/mongo_data
sudo docker run -d -p 27017:27017 -v ~/mongo_data:/data/db mongo
```

2. (Optional) Create virtualenv:
`python3 -m venv env`

3. (Optional) Activate virtualenv:
`source env/bin/activate`

4. Install Dependencies:
`pip install -r requirements.txt`

5. Run development server:
`./run_dev.sh`

5. RIFT should now be accessible at `http://localhost:5000`.

6. There is no default user or admin account, so you will need to create an account.

7. Using a tool of your choice, access the mongo database (default mongo credentials) and change your account priviliges to "Admin". You only have to do this once.

### Deploy

There is not a comprensive guide for deploying rift for use by your team. Your set-up experience will stray from the below guidance. You don't even need to use docker, but that happens to be how I keep RIFT portable for our team.

These tips presume you are familiar with [docker](https://www.docker.com/resources/what-container). There is a prebuilt docker image in the repository, but it is unlikely you will want to use it, considering it's themed entirely for use by USCGA Cyber.

1. Download the project. Use Flask's built-in development server. Make your changes.

2. Build the image.
While in the root of the project, build the image with: `sudo docker build -t rift .`

3. Start a mongo container.
This is your database. You need it or RIFT won't function. By default, RIFT will look for it on tcp:27017.
```
mkdir ~/mongo_data
sudo docker run -d -p 27017:27017 -v ~/mongo_data:/data/db mongo
```

4. Start RIFT container.
```
mkdir ~/uploads
sudo docker run -d -p 8000:8000 -v ~/uploads:/app/rift/uploads rift
```
5. RIFT should now be accessible at `http://localhost:8000`.

6. There is no default user or admin account, so you will need to create an account.

7. Using a tool of your choice, access the mongo database (default mongo credentials) and change your account priviliges to "Admin". You only have to do this once.

8. Use wsgi on a proper web-server to serve-up RIFT in a real production environment. Enable SSL.

If you use docker-compose, the below config starts both mongodb and rift. Note the flask 'image' parameter and modify accordingly.
```
version: '3'

services:
  flask:
    image: docker.pkg.github.com/uscga/rift/rift:latest
    restart: always
    ports:
     - "8000:8000"
    volumes:
     - ./uploads:/app/rift/uploads
  mongo:
    image: mongo
    restart: always
    volumes:
      - ./mongo_data:/data/db
    ports:
      - "27017:27017"
```

### Migrating and Backups

Persistent data is stored in `mongo_data` and `uploads`. Moving these folders or backing them up will suffice. Mount them as volumes when you start the Mongo and Rift containers.