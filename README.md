# RIFT

![Docker](https://github.com/USCGA/rift/workflows/Docker/badge.svg?branch=master)

![banner](https://raw.githubusercontent.com/USCGA/rift/development/documentation/cover.png)

Backend for hub located at <https://uscgacyber.net>.

In development. Limited instructions.

### Setting up:

1. Create/Start mongodb docker container:
```
mkdir ~/data
sudo docker run -d -p 27017:27017 -v ~/data:/data/db mongo
```

2. (Optional) Create virtualenv:
`python3 -m venv env`

3. (Optional) Activate virtualenv:
`source env/bin/activate`

4. Install Dependencies:
`pip install -r requirements.txt`

5. Run development server:
`./run_dev.sh`
