# A file containing many different classes in order to create objects from the data within the files.


class CustomerLogin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    def __str__(self):
        return f"Username: {self.username}, password: {self.password}"

# This is the super class that all of the other classes derive from.
class Componets:
    def __init__(self, brand, model, price):
        self.brand = brand
        self.model = model
        self.price = price
    def __str__(self):
        return f"Brand: {self.brand}, model: {self.model}, price: ${float(self.price):.2f}"
    
class CPU(Componets):
    def __init__(self, brand, model, price, socketType, coreCount, threads, clockSpeed):
        super().__init__(brand, model, price)
        self.socketType = socketType
        self.coreCount = coreCount
        self.clockSpeed = clockSpeed
        self.threads = threads
    def __str__(self):
        return super().__str__() + f", socket type: {self.socketType}, core count: {self.coreCount}, threads: {self.threads}, clock speed: {self.clockSpeed}GHz"
    
class GPU(Componets):
    def __init__(self, brand, model, price, memoryCapacity, wattage):
        super().__init__(brand, model, price)
        self.memoryCapacity = memoryCapacity
        self.wattage = wattage
    def __str__(self):
        return super().__str__() + f", memory capacity: {self.memoryCapacity}GB, wattage: {self.wattage}MHz"
    
class Motherboard(Componets):
    def __init__(self, brand, model, price, formFactor, chipset, socket):
        super().__init__(brand, model, price)
        self.formFactor = formFactor
        self.chipset = chipset
        self.socket = socket

    def __str__(self):
        return super().__str__() + f", form factor: {self.formFactor}, chipset: {self.chipset}, socket: {self.socket}"
    
class RAM(Componets):
    def __init__(self, brand, model, price, capacity, speed, noOfModules):
        super().__init__(brand, model, price)
        self.capacity = capacity
        self.speed = speed
        self.noOfModules = noOfModules
    def __str__(self):
        return super().__str__() + f", capacity: {self.capacity}GB, speed: {self.speed}, number of modules: {self.noOfModules}"

class HardDrive(Componets):
    def __init__(self, brand, model, price, capacity):
        super().__init__(brand, model, price)
        self.capacity = capacity
    def __str__(self):
        return super().__str__() + f", capacity: {self.capacity}TB"
    
class SolidStateDrive(Componets):
    def __init__(self, brand, model, price, capacity):
        super().__init__(brand, model, price)  
        self.capacity = capacity
    def __str__(self):
        return super().__str__() + f", capacity: {self.capacity}GB"

class PowerSupplyUnit(Componets):
    def __init__(self, brand, model, price, wattage, size):
        super().__init__(brand, model, price)
        self.wattage = wattage
        self.size = size
    def __str__(self):
        return super().__str__() + f", wattage: {self.wattage}W, size: {self.size}"

class ComputerCase(Componets):
    def __init__(self, brand, model, price, motherboard):
        super().__init__(brand, model, price)
        self.motherboard = motherboard
    def __str__(self):
        return super().__str__() + f", motherboard type: {self.motherboard}"

class CPUCooler(Componets):
    def __init__(self, brand, model, price):
        super().__init__(brand, model, price)
    def __str__(self):
        return super().__str__()

class Keyboard(Componets):
    def __init__(self, brand, model, price, rating, review_count):
        super().__init__(brand, model, price)
        self.rating = rating
        self.review_count = review_count
    def __str__(self):
        return super().__str__() + f", rating: {self.rating}, review count: {self.review_count}"

class Mouse(Componets):
    def __init__(self, brand, model, price, length, width, height, weight, shape, connectivity, sensor, dpi, polling_rate):
        super().__init__(brand, model, price)
        self.type = type
        self.length = length
        self.width = width
        self.height = height
        self.weight = weight
        self.shape = shape
        self.connectivity = connectivity
        self.sensor = sensor
        self.dpi = dpi
        self.polling_rate = polling_rate
    def __str__(self):
        return f"Brand: {self.brand}, Model: {self.model}, Price: {self.price}, Length: {self.length}mm, Width: {self.width}mm, Height: {self.height}mm, Weight: {self.weight} grams, Shape: {self.shape}, Connectivity: {self.connectivity}, Sensor: {self.sensor}, DPI: {self.dpi}, Polling Rate: {self.polling_rate}Hz"

class Monitor(Componets):
    def __init__(self, brand, model, price, resolution, refreshRate, size):
        super().__init__(brand, model, price)
        self.size = size
        self.resolution = resolution
        self.refreshRate = refreshRate
    def __str__(self):
        return super().__str__() + f", size: {self.size}in, resolution: {self.resolution}, refresh rate: {self.refreshRate}Hz"

class Headset(Componets):
    def __init__(self, brand, model, price, mic_type, connectivity):
        super().__init__(brand, model, price)
        self.mic_type = mic_type
        self.connectivity = connectivity
    def __str__(self):
        return super().__str__() + f", mic type: {self.mic_type}, connectivity: {self.connectivity}"