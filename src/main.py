from dataclasses import dataclass
import os, time, threading
import keyboard
from ObjectManager import *
from Cursor import Cursor
from parser import *
#from GameObjects import *
from publisher import *
import paho.mqtt.client as mqtt
from ANSIEscapeSequences import ESC

DEBUG = True
PLAYER = 1

def game_loop():
    cursor = Cursor()
    cursor.reprint_whole_map(ObjectManager(), same_position=False)
    
    while True:
        cursor.print_changes(ObjectManager())
        for obj in ObjectManager().objectsDict:
            ObjectManager().objectsDict[obj].update()
        ObjectManager().update()
        time.sleep(0.01)


def on_press(key):
    try:
        match key.name:
            case "w":
                ObjectManager().move_object(PLAYER, 0, -1)
            case "s":
                ObjectManager().move_object(PLAYER, 0, 1)
            case "a":
                ObjectManager().move_object(PLAYER, -1, 0)
            case "d":
                ObjectManager().move_object(PLAYER, 1, 0)
            case "f":
                place_or_throw_object(PLAYER, RollingBomb)
                #if DEBUG == False:
                #    publisher(str(PLAYER) + "f", PLAYER, "throw")
            case "r":
                place_or_throw_object(PLAYER, Mine)
                if DEBUG == False:
                    publisher(str(PLAYER) + "r", PLAYER, "throw")
            case "c":
                place_or_throw_object(PLAYER, Wall)
                if DEBUG == False:
                    publisher(str(PLAYER) + "c", PLAYER, "throw")
            case "l":
                cursor.reprint_whole_map(ObjectManager())
    except AttributeError:
        print('special key {0} pressed'.format(key))
        if '{0}'.format(key) == 'Key.enter':
            print(ESC.visible_cursor())
            os._exit(0)

    if not DEBUG:
            # place for publisher function call
            publisher(str(ObjectManager().objectsDict[PLAYER].x)+ ',' +str(ObjectManager().objectsDict[PLAYER].y) + ',' + str(ObjectManager().objectsDict[PLAYER].id) + ';', PLAYER)


def on_release(key):
    # print('{0} released'.format(key)) 
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def keyboard_loop():
    # Collect events until released
    keyboard.on_press(on_press)
    keyboard.wait()
        
def get_ip_address(interface):
    try:
        ni.ifaddresses(interface) # type: ignore
        ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr'] # type: ignore
        return ip
    except Exception:
        return '127.0.0.1'

def subscriber():
    # Logging aktivieren für detaillierte Debug-Informationen
    #logging.basicConfig(level=logging.DEBUG)

    # Client initialisieren
    subscriber = "subscriber" + str(PLAYER)
    client = mqtt.Client(client_id=subscriber, protocol=mqtt.MQTTv311)
    client.enable_logger()

    # Broker-Adresse und Port
    broker_address = "192.168.2.23" 
    port = 1883  # Standard-MQTT-Port

    # callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # try to connect
    try:
        client.connect(broker_address, port=port, keepalive=60)
    except Exception as e:
        print(f"failed connection attemp: {e}, Debug Mode activ")
        exit()
        
    # loop
    client.loop_forever()





def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Subscriber verbunden")
        client.subscribe("update")  # subscribtion for specific subject#
        client.subscribe("map")
        client.subscribe("throw")
    else:
        print(f"Subscriber Verbindung fehlgeschlagen mit Code {rc}")

def message_parser(message):
    """enables bigger maps due to parsing coords > 10"""
    result = []
    acc = ""
    
    for string in message:
        if string != "," and string != ";":
            acc += string
        if string == "," or string == ";":
            result.append(int(acc))
            acc = ""

    return result

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    topic = msg.topic
    
    match topic:
        case "update":
            array = message_parser(message)
            x, y, id = array[0], array[1], array[2]
            ObjectManager().move_object(id, x - ObjectManager().objectsDict[id].x, y - ObjectManager().objectsDict[id].y)
        case "throw":
            if int(message[0]) != PLAYER:
                if message[1] == "f":
                    place_or_throw_object(int(message[0]), RollingBomb)
                if message[1] == "r":
                    place_or_throw_object(int(message[0]), Mine)
                if message[1] == "c":
                    place_or_throw_object(int(message[0]), Wall)
        case "map":
            if message == "0" and PLAYER == 1:
                publisher(str(len(str(ObjectManager().world_size))) + str(ObjectManager().world_size) + ObjectManager().world_as_string, PLAYER, "map")
            if message != "0" and PLAYER != 1:
                i = int(message[0]) # first string is len
                ObjectManager().world.coord = map_as_coord(message[(i + 1):], ObjectManager().world.x)
                look_for_objects(ObjectManager())
                ObjectManager().map_shared = True


def start_game():
    print(ESC.invisible_cursor(), end="\r")
    cursor = Cursor()
    
    if DEBUG is False:
        if PLAYER == 1:
            ObjectManager().world.coord = map_parser("map.txt")
            look_for_objects(ObjectManager()) # loads players if placed on map.txt

            # saves map as string to share it to player
            ObjectManager().world_as_string = map_as_string("map.txt")

            t1 = threading.Thread(target=subscriber)
            t1.start()
        else:
            # other players waiting in loop until they recieve the map
            t1 = threading.Thread(target=subscriber)
            t1.start()
            counter = 0
            while(ObjectManager().map_shared == False):
                publisher("0", PLAYER, "map")
                time.sleep(0.1)
                print(f"\r waiting for map {bin(counter)}", end="\r")
                counter += 1
                
            
    else:
        ObjectManager().world.coord = map_parser("src/map.txt")
        look_for_objects(ObjectManager()) # loads players if placed on map.txt
        print(ObjectManager().objectsDict, "1")

    # multithreading start
    t2 = threading.Thread(target=game_loop)
    t3 = threading.Thread(target=keyboard_loop)
    
    t2.start()
    t3.start()

    
if __name__ == "__main__":
    """The old way to start a game"""
    start_game()