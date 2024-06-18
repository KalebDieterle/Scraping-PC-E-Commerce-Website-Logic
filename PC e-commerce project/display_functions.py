# A file containing different functions to display all of the different types of pc parts associated with the program.

# All functions will provide a line length, file name, the order of data extraction and object name that will be passed to the next function, in order to be able to re-use the same function to be 
# able to display all of these different parts.

import classes

# Determines with item_display() function to call depending on if this file is being called from main.py or moreOptions.py
def next_page(username, main, data):

    if main == True:

        from main import item_display

        page = item_display(username, data)

    else:

        from moreOptions import item_display

        page = item_display(username, data)

    return page

def displayCPUs(username, main):

    line_length = 7
    file_name = 'cpudata.txt'
    extraction = ('brand', 'model', 'price', 'socketType', 'coreCount', 'threads', 'clockSpeed')
    object = classes.CPU

    data = get_data(line_length, file_name, extraction, object)

    page = next_page(username, main, data)

    return page



def displayGPUs(username, main):

    line_length = 5
    file_name = 'gpudata.txt'
    extraction = ('brand', 'model', 'price', 'memoryCapacity', 'wattage')
    object = classes.GPU

    data = get_data(line_length, file_name, extraction, object)

    page = next_page(username, main, data)

    return page


def displayMotherboards(username, main):

    line_length = 5
    file_name = 'motherboarddata.txt'
    extraction = ('brand', 'model', 'price', 'memoryCapacity', 'wattage')
    object = classes.GPU

    data = get_data(line_length, file_name, extraction, object)

    page = next_page(username, main, data)

    return page


def displayRAM(username, main):

    line_length = 6
    file_name = 'ramdata.txt'
    extraction = ('brand', 'model', 'price', 'capacity', 'speed', 'noOfModules')
    object = classes.RAM

    data = get_data(line_length, file_name, extraction, object)

    page = next_page(username, main, data)

    return page

def displayHardDrives(username, main):

    line_length = 4
    file_name = 'harddrivedata.txt'
    extraction = ('brand', 'model', 'price', 'capacity')
    object = classes.HardDrive

    data = get_data(line_length, file_name, extraction, object)

    page = next_page(username, main, data)

    return page

def displaySSDs(username, main):

    line_length = 4
    file_name = 'ssddata.txt'
    extraction = ('brand', 'model', 'price', 'capacity')
    object = classes.SolidStateDrive

    data = get_data(line_length, file_name, extraction, object)

    page = next_page(username, main, data)

    return page

def displayPowerSupplies(username, main):

    line_length = 5
    file_name = 'psudata.txt'
    extraction = ('brand', 'model', 'price', 'size', 'wattage')
    object = classes.PowerSupplyUnit

    data = get_data(line_length, file_name, extraction, object)

    page = next_page(username, main, data)

    return page

def displayCases(username, main):

    line_length = 4
    file_name = 'casedata.txt'
    extraction = ('brand', 'model', 'price', 'motherboard')
    object = classes.ComputerCase

    data = get_data(line_length, file_name, extraction, object)

    page = next_page(username, main, data)

    return page

def displayCoolingSolutions(username, main):

    line_length = 3
    file_name = 'cpucoolerdata.txt'
    extraction = ('brand', 'model', 'price')
    object = classes.CPUCooler

    data = get_data(line_length, file_name, extraction, object)

    page = next_page(username, main, data)

    return page

def displayKeyboards(username, main):

    line_length = 5
    file_name = 'keyboarddata.txt'
    extraction = ('brand', 'model', 'price', 'rating', 'review_count')
    object = classes.Keyboard

    data = get_data(line_length, file_name, extraction, object)

    page = next_page(username, main, data)

    return page

def displayMice(username, main):
    
    line_length = 12
    file_name = 'mousedata.txt'
    extraction = ('brand', 'model', 'price', 'length', 'width', 'height', 'weight', 'shape', 'connectivity', 'sensor', 'dpi', 'polling_rate')
    object = classes.Mouse

    data = get_data(line_length, file_name, extraction, object)

    page = next_page(username, main, data)


def displayMonitors(username, main):

    line_length = 6
    file_name = 'monitordata.txt'
    extraction = ('brand', 'model', 'price', 'resolution', 'refreshRate', 'size')
    object = classes.Monitor

    data = get_data(line_length, file_name, extraction, object)

    page = next_page(username, main, data)

    return page

def displayHeadsets(username, main):

    line_length = 5
    file_name = 'headsetdata.txt'
    extraction = ('brand', 'model', 'price', 'mic_type', 'connectivity')
    object = classes.Headset

    data = get_data(line_length, file_name, extraction, object)
    
    page = next_page(username, main, data)

    return page


# This function is called from all of the previous display functions, it utilizes the information passed to it from the previous functions and loads the data from
# files, which it then create into objects.
def get_data(line_length, file_name, extraction, object):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
        data = []

        for line in lines:
            line = line.strip()
            if 'N/A' in line or 'None' in line or not line:
                continue

            parts = line.split(',')
            if len(parts) != line_length:
                continue

            # Check for empty parts within the line
            if any(part.strip() == '' for part in parts):
                continue

            try:
                data_dict = {field: value.strip() for field, value in zip(extraction, parts)}
                item = object(**data_dict)
                data.append(item)

            except ValueError as ve:
                print(f"ValueError: {ve} in line: {line}")
            except Exception as e:
                print(f"Error: {e} in line: {line}")

        return data

    except Exception as e:
        print("Error: " + str(e))
