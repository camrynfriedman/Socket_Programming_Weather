# weather_server.py
import socket
import requests
import json  # required for OpenWeatherMap API
import logging
import configparser
from datetime import date, datetime

''' Commands:
    - TEMP -> gets the current temp
    - MAX -> gets max temp
    - MIN -> gets min temp
    - PRESSURE -> gets pressure
    - HUMIDITY -> gets humidity
    - DECSRIPTION -> gets description
    - EXIT -> exits
'''
#set up log
logging.basicConfig(filename='server.log', filemode='w', format='%(asctime)s  %(levelname)s %(message)s', datefmt='%a %b %d %H:%M:%S %Y', level='INFO')
logging.info('Application started. Log created.')

#set up config parser
config = configparser.ConfigParser()
config.read('config.ini')

# get IP address and port
host = config['NETWORK']['ip']       
port = int(config['NETWORK']['port_number'])      
# open socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  # bind to address and port
s.listen(1)  # listen for connection
conn, addr = s.accept()  # when client sends connection, accept it
now = datetime.now()
dt_string = now.strftime("%a %b %d %H:%M:%S %Y")
print(dt_string + ' weather_server starting on port ' + str(port)) #change this
stillRunning = True
while stillRunning:
    data = conn.recv(1024).decode()  # receive command from client
    logging.info("REQUEST \'%s\' received.", data)
    if data:
        if data.casefold() == "EXIT".casefold():
            stillRunning = False
        else:
            #separate command and city name
            split_data=data.split()
            command=split_data[0]
            city_name=split_data[1]
            #access API for city
            api_key = config['API']['api_key']
            base_url = config['API']['base_url']
            complete_url = base_url + "appid=" + api_key + \
                "&q=" + city_name + "&units=imperial"
            response = requests.get(complete_url)
            x = response.json()
            # do something with the client command data
            ##COMMAND = TEMP##
            if command.casefold() == "TEMP".casefold():
                if x["cod"] == 200:
                    y = x["main"] # store the value of "main" key in variable y
                    raw_data=str(y["temp"]) # store TEMP value as string
                else:
                    raw_data = "City not found"
            ##COMMAND = MAX##
            elif command.casefold() == "MAX".casefold():
                if x["cod"] == 200:
                    y = x["main"] # store the value of "main" key in variable y
                    raw_data=str(y["temp_max"]) # store MAX value as string
                else:
                    raw_data = "City not found"
            ##COMMAND = MIN##
            elif command.casefold() == "MIN".casefold():
                if x["cod"] == 200:
                    y = x["main"] # store the value of "main" key in variable y
                    raw_data=str(y["temp_min"]) # store MIN value as string
                else:
                    raw_data = "City not found"
            ##COMMAND = PRESSURE##
            elif command.casefold() == "PRESSURE".casefold():
                if x["cod"] == 200:
                    y = x["main"] # store the value of "main" key in variable y
                    raw_data=str(y["pressure"]) # store PRESSURE value as string
                else:
                    raw_data = "City not found"
             ##COMMAND = HUMIDITY##
            elif command.casefold() == "HUMIDITY".casefold():
                if x["cod"] == 200:
                    y = x["main"] # store the value of "main" key in variable y
                    raw_data=str(y["humidity"]) # store HUMIDITY value as string
                else:
                    raw_data = "City not found"
             ##COMMAND = DESCRIPTION##
            elif command.casefold() == "DESCRIPTION".casefold():
                if x["cod"] == 200:
                    y = x["weather"] # store the value of "weather" key in variable y
                    raw_data=str(y[0]["description"]) # store DESCRIPTION key value as string
                else:
                    raw_data = "City not found"
            conn.send(raw_data.encode()) #send data to client
            logging.info("RESPONSE \'%s\' sent",raw_data)
                
logging.info('Application terminated.')               
print('\nReceived: ' + data)
print("Closing connection...")
conn.close()
