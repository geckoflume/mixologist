# Mixologist

Cocktail machine project for Ambiant Intelligence class @ Instituto Superior Técnico, Lisbon, Portugal.

More information: [https://fenix.tecnico.ulisboa.pt/disciplinas/AI514/2019-2020/2-semestre](https://fenix.tecnico.ulisboa.pt/disciplinas/AI514/2019-2020/2-semestre)

*Group 10*

## Features

## TODO
- Add HTTPS layer
- Add security/auth
- Add stop button
- Add edit/delete ingredients and recipes

## Specifications

### Database specification

![Database relationship diagram](database.png "Database relationship diagram")

## Prerequisites

- Python 3
- flask, pymysql, flask-socketio, pyserial
- MySQL/MariaDB

## How to build

Replace db settings in Database.py.
```
sudo apt install python3 python3-pip python3-dev python3-setuptools mariadb-server mariadb-client
pip install --user pipenv
pipenv install
```
Optional:
```
sudo apt install apache2 php php-json php-mbstring php-zip php-gd php-xml php-curl php-mysql

```

## Valuable resources:

- https://sweetcode.io/flask-python-3-mysql/
- https://www.diffordsguide.com/encyclopedia/1045/cocktails/top-100-most-frequently-appearing-cocktail-ingredients
- https://linuxhint.com/install_phpmyadmin_debian_10/