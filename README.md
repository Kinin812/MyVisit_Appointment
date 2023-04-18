# MyVisit_Appointment - finding timeslots for writing in an instance



## Technology stack

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)


## Project description

Provides an opportunity to automatically sign up for visits to government agencies (for example, the Ministry of Internal Affairs).


## Running a project in dev mode

- Install and activate virtual environment

```bash
source /venv/bin/activated
```

- Install dependencies from requirements.txt

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- Create an .env file in the root of the project


- Fill in the secrets .env the telegram bot settings 

```python
API_TOKEN=5184539473:AAGJucddvdfdgnggqEHMTRLu5I6N8
CHAT_ID=468816489
```

- Make settings USERS_DATA, Person, DOC, MAX_DATA, TIMEOUT, INTERVAL in config.py


- Run command:
```bash
python parser.py
```

---

### Author
[Kinin812](https://github.com/Kinin812)
