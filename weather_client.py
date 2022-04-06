# weather_client.py
import socket
import configparser

#set up config parser
config = configparser.ConfigParser()
config.read('config.ini')

# get IP address and port
host = config['NETWORK']['ip']       
port = int(config['NETWORK']['port_number']) 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
stillRunning = True
print("\n~~~~Welcome to the Weather Widget!~~~~\n\tAvailable commands:\nTEMP\tMAX\tMIN\tPRESSURE\nHUMIDITY\tDESCRIPTION\tEXIT")

while stillRunning:
    data=input("\nPlease enter a command followed by a city: ")
    if data:
        first_entry=str(data.split()[0].casefold())
        if data.casefold() == "EXIT".casefold():
            s.send(data.encode()) #send EXIT message
            print("See you again soon!\n")
            stillRunning=False
        elif first_entry != "TEMP".casefold() and first_entry != "MAX".casefold() and first_entry != "MIN".casefold() and first_entry != "PRESSURE".casefold() and first_entry != "HUMIDITY".casefold() and first_entry != "DESCRIPTION".casefold():
            #invalid command
            print("Invalid command: " + data.split()[0])
            print("Valid commands are: \nTEMP\nMAX\nMIN\nPRESSURE\nHUMIDITY\nDESCRIPTION\nEXIT")
        elif len(data.split()) !=2:
            #wrong format
            if len(data.split()) < 2:
                #missing args
                if first_entry == "TEMP".casefold() or first_entry == "MAX".casefold() or first_entry == "MIN".casefold() or first_entry == "PRESSURE".casefold() or first_entry == "HUMIDITY".casefold():
                    #missing city name
                    print("Missing element: "+data.split()[0] + "\n\tusage: " + data.split()[0] + " <cityname>")
                else:
                    #missing command
                    print("Missing element: <command>\n\tusage: <command> <cityname>")
            elif len(data.split()) > 2:
                #too many args
                print("Invalid entry. Proper format: <command> <cityname>")
        else:
            s.send(data.encode()) #send data
            #separate command and city name
            split_data=data.split()
            command=split_data[0]
            city_name=split_data[1]
            #server does work on data, sends back a string
            raw_data = s.recv(1024).decode()
            if raw_data == "City not found":
                print(raw_data)
            else:
                print("\n*-*-*-*-*-*Weather for "+city_name+"*-*-*-*-*-*")
                if command.casefold()=="TEMP".casefold():
                    print("\tCurrent temp: " + raw_data + "°F")
                elif command.casefold()=="MAX".casefold():
                    print("\tMax temp: " + raw_data + "°F")
                elif command.casefold()=="MIN".casefold():
                    print("\tMin temp: " + raw_data + "°F")
                elif command.casefold()=="PRESSURE".casefold():
                    print("\tPressure: " + raw_data + " hPa")
                elif command.casefold()=="HUMIDITY".casefold():
                    print("\tHumidity: " + raw_data + "%")
                elif command.casefold()=="DESCRIPTION".casefold():
                        print("\tDescription: " + raw_data)
s.close()

