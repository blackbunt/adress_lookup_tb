# Import the required libraries

import yaml
import pyperclip
from geopy import distance, OpenCage
import time
import re
import os
from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError

def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as config_file:
        try:
            config = yaml.safe_load(config_file)
        except yaml.YAMLError as error:
            print(error)
            return None

    opencage_api_key = config.get('opencage_api', None)
    user_location = config.get('user_location', None)

    if opencage_api_key is None or user_location is None:
        print("Could not find necessary keys in the config file.")
        return None

    return opencage_api_key, user_location

# load config
api_key, user_loc = load_config()
if api_key and user_loc:
# Create an instance of the OpenCage geocoder
    geocoder = OpenCageGeocode(api_key)

def get_origin_coordinates(address):
    """Geokodierung der Ursprungsadresse
  :param address: Adresse des Ursprungs
  :return: Koordinaten des Ursprungs, formatierte Adresse des Ursprungs
  """
    # Geokodierung der Ursprungsadresse
    origin_location = geocoder.geocode(address)
    # print(origin_location)
    # Koordinaten des Ursprungs
    origin_coordinates = (origin_location[0]['geometry']['lat'], origin_location[0]['geometry']['lng'])
    formatted_target_address = origin_location[0]['formatted']
    return origin_coordinates, formatted_target_address


def get_destination_coordinates(address, origin_coordinates):
    """Geokodierung der Zieladresse, suche nach der Zieladresse mit Berücksichtigung der Nähe zum Ursprung
   :param origin_coordinates:
   :param address: Adresse des Ziels
   :return: Koordinaten des Ziels, formatierte Adresse des Ziels
   """
    # Suche nach der Zieladresse mit Berücksichtigung der Nähe zum Ursprung
    results = geocoder.geocode(address, proximity=origin_coordinates)
    formatted_target_address = results[0]['formatted']
    # print(formatted_target_address)
    # Extrahieren der Koordinaten des ersten Ergebnisses
    target_coordinates = (results[0]['geometry']['lat'], results[0]['geometry']['lng'])
    return target_coordinates, formatted_target_address


def clean_with_regex(address):
    """Clean the address using regex
  :param address: address to clean
  :return: street name, street number, postal code, city
  """
    # if germany is in the address, remove it
    if 'Germany' in address:
        address = address.replace('Germany', '')
        # remove trailing comma
        address = address[:-2]
    # find plz with regex
    plz = re.search(r'\d{5}', address).group()
    # Extract city using postal code as an anchor
    city = re.search(rf'{plz}\s+(.*)', address).group(1)
    # Extract street name
    street_name = re.search(r'(?:(.*),\s+)?([^0-9,]+)', address).group(2).strip()
    street_name_shorter = re.sub(r'\bStraße\b', 'Str.', street_name, flags=re.IGNORECASE)
    # Extract street number
    street_number = re.search(r'(\d+\w*)\b', address).group(1)
    return street_name_shorter, street_number, plz, city


def get_address(origin, destination):
    """
   Main function to gather the coordinates of the origin and the destination address
   search for the destination address in the vicinity of the origin address
   clean the address and order it to get the street name, street number, postal code and city
   get the map url of the destination address
   :param origin:
   :param destination:
   :return: list with street name, street number, postal code and city
   """
    if origin == destination:
        # end_address, address = get_destination_coordinates(destination, origin)
        address = clean_with_regex(destination)
        return address
    map_url = None
    try:
        start_coord, start_address = get_origin_coordinates(origin)
        end_coord, end_address = get_destination_coordinates(destination, start_coord)
        address = clean_with_regex(end_address)
        if end_address == start_address:
            raise InvalidInputError('Origin and destination address are identical')
        return address
    except (InvalidInputError, RateLimitExceededError, UnknownError) as e:
        print("Fehler beim Abrufen der Adresse:", e)
    except Exception as e:
        print("Ein unbekannter Fehler ist aufgetreten:")


def copy_to_clipboard(text):
    """Copy text to clipboard
    :param text: text to copy
    :return: None
    """
    pyperclip.copy(text)


def clear_console():
    os.system('cls')







if __name__ == '__main__':


    # print welcome message
    print("")
    print(" █████╗ ██████╗ ██████╗ ██████╗ ███████╗███████╗███████╗         █████╗ ██╗     ██╗  ██╗   ██╗")
    print("██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝        ██╔══██╗██║     ██║  ╚██╗ ██╔╝")
    print("███████║██║  ██║██║  ██║██████╔╝█████╗  ███████╗███████╗        ███████║██║     ██║   ╚████╔╝ ")
    print("██╔══██║██║  ██║██║  ██║██╔══██╗██╔══╝  ╚════██║╚════██║        ██╔══██║██║     ██║    ╚██╔╝  ")
    print("██║  ██║██████╔╝██████╔╝██║  ██║███████╗███████║███████║███████╗██║  ██║███████╗███████╗██║   ")
    print("╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝   ")
    print("\n\n                       schnelle, genaue adresssuche - nicht mehr.")
    # pause for 1.5 seconds
    time.sleep(1.5)
    # clear console
    clear_console()
    # get user input
    origin = user_loc
    destination = input("Adresse suchen: ")
    # get address
    address = get_address(origin, destination)
    street_name, street_number, plz, city = address
    # print(f'{street_name} {street_number}\n{plz} {city}')
    # print on first run
    clear_console()
    print('Willkommen bei AddressAlly!\n')
    print('Dieses Programm hilft Ihnen dabei, nach Adressen zu suchen und die Ergebnisse bequem zu kopieren.\n')
    print('Bitte folgen Sie den Anweisungen auf dem Bildschirm.\n')



    while True:
        try:
            clear_console()
            print(f'{street_name} {street_number}\n{plz} {city}\n\n')
            print("1. Adresse kopieren\n")
            print("2. Straße kopieren")
            print("3. PLZ Stadt kopieren\n")
            print("4. PLZ kopieren")
            print("5. Stadt kopieren\n")
            print("6. neue Eingabe\n")
            print("7. Programm beenden")
            auswahl = int(input("Auswahl: "))
            if auswahl == 1:
                copy_to_clipboard(f'{street_name} {street_number}\n{plz} {city}')
                print("Adresse kopiert!")
            elif auswahl == 2:
                copy_to_clipboard(f'{street_name} {street_number}')
                print("Straße kopiert!")
            elif auswahl == 3:
                copy_to_clipboard(f'{plz} {city}')
                print("PLZ Stadt kopiert!")
            elif auswahl == 4:
                copy_to_clipboard(f'{plz}')
                print("PLZ kopiert!")
            elif auswahl == 5:
                copy_to_clipboard(f'{city}')
                print("Stadt kopiert!")
            elif auswahl == 6:
                destination = input("Adresse suchen: ")
                address = get_address(origin, destination)
                street_name, street_number, plz, city = address
            elif auswahl == 7:
                exit(0)
                print("\n\n\n\n                    Danke für's Nutzen von AddressAlly! :)")
            else:
                print("Bitte eine Zahl zwischen 1 und 7 eingeben!")



        except ValueError:
            print("Bitte nur Zahlen eingeben!")
