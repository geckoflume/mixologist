# Mixologist

Cocktail machine project for Ambient Intelligence class @ Instituto Superior Técnico, Lisbon, Portugal.

Report: [Mixologist_AI_Project_Report_Group10.pdf](Mixologist_AI_Project_Report_Group10.pdf)

More information: [https://fenix.tecnico.ulisboa.pt/disciplinas/AI514/2019-2020/2-semestre](https://fenix.tecnico.ulisboa.pt/disciplinas/AI514/2019-2020/2-semestre)

*Group 10*

## Features
- Cup filling up to a specified weight/liquid quantity
- Beverage pouring only if a cup is present and if the cup has the needed capacity
- Cocktail making only if the quantities of the required ingredients are available
- Alerts on empty bottles / full glass
- Storage, management of recipes in a database
- Google Assistant voice control (recipe search)
- Notifications on status update
- Computation of the number of cocktails that it is possible to make with the current bottles

## Enhancements
- Add authentication

## Specifications
This application is written in Python 3, built around the Flask framework for routing.  
Data is stored in a MySQL database and can be updated using HTTP REST methods.

### Database specification
![Database relationship diagram](database.png "Database relationship diagram")

## Prerequisites
### Hardware
- Orange Pi PC or other GPIO-capable board
- 4 peristaltic pumps
- 4 relay module to drive the pumps
- An Arduino
- 5 load cells modules
- 5 HX711 ADC modules

### Software
- Arduino IDE
- Python 3
- Python dependencies (flask, pymysql, flask-socketio, pyA20, spidev, pyserial, requests, pyopenssl - can be installed with the [Pipfile](Pipfile), please read [How to build](#how-to-build))
- MySQL/MariaDB server
- IFTTT account

## How to build
### Wiring / Hardware
Default pin connections are the following:

#### Relay board
| Relay input | Orange Pi PC pin |
|-------------|------------------|
| 1           | PA10             |
| 2           | PA9              |
| 3           | PA8              |
| 4           | PA7              |

#### HX711 modules
| HX711 #  | HX711 pin       | Arduino pin |
|----------|-----------------|-------------|
| 1        | DOUT <br/>SCK   | 4 <br/>5    |
| 2        | DOUT <br/>SCK   | 6 <br/>7    |
| 3        | DOUT <br/>SCK   | 8 <br/>9    |
| 4        | DOUT <br/>SCK   | 10 <br/>11  |
| 5        | DOUT <br/>SCK   | 12 <br/>13  |

### Software
#### Arduino
Upload the [arduino/calibration/calibration.ino](arduino/calibration/calibration.ino) sketch to your Arduino and note down the calibration value for each load cell in the provided Serial assistant.  
Edit the [arduino/json_read_5x/json_read_5x.ino](arduino/json_read_5x/json_read_5x.ino) sketch:
```C
float calibrationValue_b1 = -420.00; // calibration value load cell 1          !!!
float calibrationValue_b2 = -418.53; // calibration value load cell 2
float calibrationValue_g = -951.84;  // calibration value load cell 3
float calibrationValue_b3 = -420.80; // calibration value load cell 4
float calibrationValue_b4 = -416.38; // calibration value load cell 5
```
And update the values for each load cell.  
Upload this sketch to your Arduino and connect it to your Orange Pi.

#### IFTTT (enable Google Assistant and notifications)
Create an IFTTT account on [https://ifttt.com/](https://ifttt.com/), then enable the [Google Assistant service](https://ifttt.com/google_assistant) and the [Webhooks service](https://ifttt.com/maker_webhooks).  
Once done, note down your API key, and create two applets:
![IFTTT applets](ifttt.png "IFTTT applets")

#### MySQL database
Load the [init.sql](init.sql) file to populate your database and note down your connection settings.

#### Orange Pi
Replace database, Arduino, WS2812 and IFTTT connection settings in [webapp/config.ini](webapp/config.ini).  
If needed, replace the relay GPIO pins in [webapp/Pump.py](webapp/Pump.py). 
```
sudo apt install python3 python3-pip python3-dev python3-setuptools mariadb-server mariadb-client libffi-dev
pip install --user pipenv
git clone https://github.com/geckoflume/mixologist.git
cd mixologist
pipenv install
python3 webapp/app.py
```
The webserver is now started on https://ORANGE_PI_IP:5000/.