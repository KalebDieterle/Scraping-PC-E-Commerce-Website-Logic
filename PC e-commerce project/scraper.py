# A scraping program that scrapes many different websites in order to save data to a file.

# This scrapes (stores) information about different computer parts, for example : 

# Mouse - brand, model, price, length, width, height, weight, shape, connectivity, sensor, dpi, and polling rate.

# All of the functions that get the data work relatively similarly, they open the website needed for that data, and then browse through different pages, clicking buttons needed to get to the
# data, and wait for the information to fully load before saving the data.


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import classes

class SubCPU:
    def __init__(self, socket, clock_speed, core_count, thread_count):
        self.socket = socket
        self.clock_speed = clock_speed
        self.core_count = core_count
        self.thread_count = thread_count
    def __str__(self):
        return f"Socket: {self.socket}, clock speed: {self.clock_speed}, core count: {self.core_count}, thread count: {self.thread_count}"

# uncomment these in order to run the scraper in the background.

# chrome_options = Options()
# chrome_options.add_argument('--headless')  
# chrome_options.add_argument('--disable-gpu')
 
cService = webdriver.ChromeService(executable_path = 'C:/Users/kaleb/Documents/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service = cService)


cpu_data = []
gpu_data = []
motherboard_data = []
ram_data = []
hdd_data = []
ssd_data = []
psu_data = []
case_data = []
cooler_data = []
monitor_data = []
keyboard_data = []
mouse_data = []
headset_data = []

def greeting():
    options = {
        1 : getCPUData,
        2 : getGPUData,
        3 : getMotherboardData,
        4 : getRAMData,
        5 : getHardDriveData,
        6 : getSolidStateDriveData,
        7 : getPSUData,
        8 : getPCCaseData,
        9 : getCPUCoolerdata,
        10 : getKeyboardData,
        11 : getMouseData,
        12 : getMonitorData,
        13 : getHeadsetData
    }

    user_choices = ["CPU", "GPU", "Motherboard", "RAM", "Hard Drives", "SSD's", "Power Supply", "PC Cases", "Cooling Solutions", "Keyboard",
            "Mouse", "Monitor", "Headset"]
    
    picked = 'Null'

    while picked != 0:

        driver.get('https://www.google.com/')

        try: 
            print("What data would you like to scrape? Enter '0' to quit, or a number coorelating to an option to scrape that")
            for i, choice in enumerate(user_choices):
                print(f"{i+1} - {choice}")
            picked = input()
            picked = int(picked)

            if picked in options:
                options[picked]()
            elif picked == 0:
                import sys
                print("Exiting...")
                sys.exit()
            else:
                print("Invaid input, please enter an integer.")
        except Exception as e:
            print("Error: " + str(e))



def extract_price(driver):

        try:
            price_element = driver.find_element(By.CSS_SELECTOR, "span[itemprop='price']")
            return price_element.text.strip()
        except NoSuchElementException:
            return "N/A"

def getCPUData():

    print("Scraping CPU data...")

    website = 'https://www.pc-kombo.com/us/components'
    driver.get(website)
    def extract_price(driver):

        try:
            price_element = driver.find_element(By.CSS_SELECTOR, "span[itemprop='price']")
            return price_element.text.strip()
        except NoSuchElementException:
            return "N/A"

    all_matches_found = driver.find_element(by=By.XPATH, value="//a[@href='https://www.pc-kombo.com/us/components/cpus' and @class='btn btn-primary']")
    all_matches_found.click()

    def getSubtitleData():
        subtitle_info_list = []

        #splitting the subtitle into a list, we then store that data into variables

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='subtitle']")))
        subtitles = driver.find_elements(by=By.CSS_SELECTOR, value="div[class='subtitle']")

        for subtitle in subtitles:
            subtitle_text = subtitle.text
            subtitle_info = subtitle_text.split()
            
            #some subtitles vary in data structure, here we are compensating for that
            if len(subtitle_info) >= 11: 
                socket = subtitle_info[1]
                clock_speed = subtitle_info[3]
                core_count = subtitle_info[8]
                thread_count = subtitle_info[10]
                subtitle_info_list.append((socket, clock_speed, core_count, thread_count))
            else:
                socket = subtitle_info[1]
                clock_speed = subtitle_info[3]
                core_count = subtitle_info[5]
                thread_count = subtitle_info[7]
                subtitle_info_list.append((socket, clock_speed, core_count, thread_count))

        return subtitle_info_list

    try:


        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='product/cpu'")))
        cpu_links = driver.find_elements(by=By.CSS_SELECTOR, value="a[href*='product/cpu'")


        for link_index, link in enumerate(cpu_links):
            
            subtitle_data = getSubtitleData()
            sub_CPUs = []
            for data_tuple in subtitle_data:  # Iterate over each tuple in the list
                socket, clock_speed, core_count, thread_count = data_tuple
                subCPU = SubCPU(socket,clock_speed,core_count,thread_count)
                sub_CPUs.append(subCPU)

           
            link.click()
            driver.switch_to.window(driver.window_handles[1])

            try: 
            #wait for CPU details to load
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']")))
                
                cpu_name = driver.find_element(By.CSS_SELECTOR, "h1[itemprop='name']")
                name = cpu_name.text.strip()
                name = str(name)

                cpu_brand = driver.find_element(By.CSS_SELECTOR, "dd[itemprop='brand']")
                brand = cpu_brand.text.strip()
                brand = str(brand)

                price = extract_price(driver)
                
                price = str(price)

                cpu = classes.CPU(brand, name, price, sub_CPUs[link_index].socket, sub_CPUs[link_index].core_count, sub_CPUs[link_index].thread_count, sub_CPUs[link_index].clock_speed)
                cpu_data.append(cpu)

                with open("cpudata.txt", 'a') as file:
                    file.seek(0)
                    file.write(f'{brand},{name},{price},{sub_CPUs[link_index].socket},{sub_CPUs[link_index].core_count},{sub_CPUs[link_index].thread_count},{sub_CPUs[link_index].clock_speed}' + '\n')

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print("Error retrieving CPU details:", e)

            

        

        
                    
        print("Succesfully saved cpu data")
        driver.back()



        

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()


def getGPUData():
    print("Scraping GPU data...")

    website = 'https://www.pc-kombo.com/us/components'
    driver.get(website)

    def getSubtitleData():
        import re

        data = []
        gb_numbers = []
        w_numbers = []

        subtitles = driver.find_elements(By.CSS_SELECTOR, "div[class='subtitle']")
        for subtitle in subtitles:
            data.append(subtitle.text)
        
        pattern = r'(\d+)\s*(?:GB|W)'
        
        for line in data:
            matches = re.findall(pattern, line)
            if len(matches) >= 2:
                 gb_numbers.append(int(matches[0]))

                 w_numbers.append(int(matches[1]))

        return gb_numbers, w_numbers


    try:

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary[href='https://www.pc-kombo.com/us/components/gpus']")))
        element.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h5[class='name']")))    
        gpu_links = driver.find_elements(By.CSS_SELECTOR, "h5[class='name']")

        gpu_memories, gpu_wattages = getSubtitleData()

        for i, link in enumerate(gpu_links):

            link.click()
            driver.switch_to.window(driver.window_handles[1])

            gpu_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']")))
            name = gpu_name.text

            gpu_brand = driver.find_element(By.CSS_SELECTOR, "dd[itemprop='brand']")
            brand = gpu_brand.text

            price = extract_price(driver)
            

            memory = gpu_memories[i]
            wattage = gpu_wattages[i]

            gpu = classes.GPU(brand, name, price, memory, wattage)
            gpu_data.append(gpu)

            with open("gpudata.txt", 'a') as file:
                file.write(f"{brand},{name},{price},{memory},{wattage}" + '\n')




            driver.close()
            driver.switch_to.window(driver.window_handles[0])


    except Exception as e:
        print("Error: ",  e)
    finally:
        driver.quit()
        print("Data saved succesfully.")

def getMotherboardData():

    print("Scraping Motherboard data...")
    import re

    website = 'https://www.pc-kombo.com/us/components'
    driver.get(website)

    def extract_info(line):
            
        pattern = r'(e-?atx|\w+).*Socket\s+(\d+).*Chipset\s+(\w+)'

        match = re.search(pattern, line, re.IGNORECASE)


        if match:
                form_factor = match.group(1)
                socket_number = match.group(2)
                chipset = match.group(3)
                return form_factor, socket_number, chipset
        else:
            return None, None, None

    def getSubtitleData(driver):
        data = []
        form_factors = []
        socket_numbers = []
        chipsets = []

        subtitles = driver.find_elements(By.CSS_SELECTOR, "div[class='subtitle']")
        for subtitle in subtitles:
            data.append(subtitle.text)

        for line in data:
            first_word, socket_number, chipset = extract_info(line)
            form_factors.append(first_word)
            socket_numbers.append(socket_number)
            chipsets.append(chipset)


        return form_factors, socket_numbers, chipsets



    try:

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary[href='https://www.pc-kombo.com/us/components/motherboards']")))
        element.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h5[class='name']")))    
        gpu_links = driver.find_elements(By.CSS_SELECTOR, "h5[class='name']")

        form_factors, socket_numbers, chipsets = getSubtitleData(driver)

        for i, link in enumerate(gpu_links):

            link.click()
            driver.switch_to.window(driver.window_handles[1])

            ram_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']")))
            name = ram_name.text

            ram_brand = driver.find_element(By.CSS_SELECTOR, "dd[itemprop='brand']")
            brand = ram_brand.text

            price = extract_price(driver)
            
            form_factor = form_factors[i]
            socket_number = socket_numbers[i]
            chipset = chipsets[i]

            motherboard = classes.Motherboard(brand, name, price, form_factor, socket_number, chipset)
            motherboard_data.append(motherboard)

            with open("motherboarddata.txt", 'a') as file:
                file.write(f"{brand},{name},{price},{form_factor},{socket_number},{chipset}" + '\n')




            driver.close()
            driver.switch_to.window(driver.window_handles[0])


    except Exception as e:
        print("Error: ",  e)
    finally:
        driver.quit()
        print("Data saved succesfully.")


def getRAMData():
    print("Scraping RAM data...")

    website = 'https://www.pc-kombo.com/us/components'
    driver.get(website)

    def getSubtitleData():
        import re

        data = []
        gb_numbers = []
        speeds = []
        kit_numbers = []

        pattern = r'(\d+)\s*GB\s*(DDR\d+)-(\d+)\s*Kit\s*of\s*(\d+)'

        subtitles = driver.find_elements(By.CSS_SELECTOR, "div[class='subtitle']")
        for subtitle in subtitles:
            data.append(subtitle.text)

        for line in data:
            matches = re.match(pattern, line)
            if matches:
                gb_numbers.append(int(matches.group(1)))
                speeds.append(matches.group(2) + '-' + matches.group(3))
                kit_numbers.append(int(matches.group(4)))

        return gb_numbers, speeds, kit_numbers
        


    try:

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary[href='https://www.pc-kombo.com/us/components/rams']")))
        element.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h5[class='name']")))    
        gpu_links = driver.find_elements(By.CSS_SELECTOR, "h5[class='name']")

        ram_capacities, ram_speeds, ram_modulesCounts = getSubtitleData()

        for i, link in enumerate(gpu_links):

            link.click()
            driver.switch_to.window(driver.window_handles[1])

            ram_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']")))
            name = ram_name.text

            ram_brand = driver.find_element(By.CSS_SELECTOR, "dd[itemprop='brand']")
            brand = ram_brand.text

            price = extract_price(driver)
            
            capacity = ram_capacities[i]
            speed = ram_speeds[i]
            moduleCount = ram_modulesCounts[i]

            ram = classes.RAM(brand, name, price, capacity, speed, moduleCount)
            ram_data.append(ram)

            with open("ramdata.txt", 'a') as file:
                file.write(f"{brand},{name},{price},{capacity},{speed},{moduleCount}" + '\n')




            driver.close()
            driver.switch_to.window(driver.window_handles[0])


    except Exception as e:
        print("Error: ",  e)
    finally:
        driver.quit()
        print("Data saved succesfully.")

def getHardDriveData():
    print("Scraping Hard Drive data...")
    
    website = 'https://www.pc-kombo.com/us/components'
    driver.get(website)
    def getSubtitleData():
        import re

        storage_sizes = []

        subtitles = driver.find_elements(By.CSS_SELECTOR, "div[class='subtitle']")
        for subtitle in subtitles:
            line = subtitle.text.strip()
            match = re.search(r'(\d+)\s*TB', line)
            if match:
                storage_sizes.append(match.group(1))

        return storage_sizes

        


    try:

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary[href='https://www.pc-kombo.com/us/components/hdds']")))
        element.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h5[class='name']")))    
        hdd_links = driver.find_elements(By.CSS_SELECTOR, "h5[class='name']")

        storage_sizes = getSubtitleData()

        for i, link in enumerate(hdd_links):

            link.click()
            driver.switch_to.window(driver.window_handles[1])

            hdd_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']")))
            name = hdd_name.text

            hdd_brand = driver.find_element(By.CSS_SELECTOR, "dd[itemprop='brand']")
            brand = hdd_brand.text

            price = extract_price(driver)
            
            storage_size = storage_sizes[i]

            hdd = classes.HardDrive(brand, name, price, storage_size)
            hdd_data.append(hdd)

            with open("harddrivedata.txt", 'a') as file:
                file.write(f"{brand},{name},{price},{storage_size}" + '\n')




            driver.close()
            driver.switch_to.window(driver.window_handles[0])


    except Exception as e:
        print("Error: ",  e)
    finally:
        driver.quit()
        print("Data saved succesfully.")

def getSolidStateDriveData():
    print("Scraping SSD data...")

    website = 'https://www.pc-kombo.com/us/components'
    driver.get(website)
    def getSubtitleData():
        import re

        storage_sizes = []

        subtitles = driver.find_elements(By.CSS_SELECTOR, "div[class='subtitle']")
        for subtitle in subtitles:
            line = subtitle.text.strip()
            match = re.search(r'(\d+)\s*GB', line)
            if match:
                storage_sizes.append(match.group(1))

        return storage_sizes

        


    try:

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary[href='https://www.pc-kombo.com/us/components/ssds']")))
        element.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h5[class='name']")))    
        ssd_links = driver.find_elements(By.CSS_SELECTOR, "h5[class='name']")

        storage_sizes = getSubtitleData()

        for i, link in enumerate(ssd_links):

            link.click()
            driver.switch_to.window(driver.window_handles[1])

            ssd_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']")))
            name = ssd_name.text

            ssd_brand = driver.find_element(By.CSS_SELECTOR, "dd[itemprop='brand']")
            brand = ssd_brand.text

            price = extract_price(driver)
            
            storage_size = storage_sizes[i]

            ssd = classes.SolidStateDrive(brand, name, price, storage_size)
            ssd_data.append(ssd)

            with open("ssddata.txt", 'a') as file:
                file.write(f"{brand},{name},{price},{storage_size}" + '\n')




            driver.close()
            driver.switch_to.window(driver.window_handles[0])


    except Exception as e:
        print("Error: ",  e)
    finally:
        driver.quit()
        print("Data saved succesfully.")

def getPSUData():
    print("Scraping PSU data...")

    website = 'https://www.pc-kombo.com/us/components'
    driver.get(website)
    def getSubtitleData():
        import re

        psu_sizes = []
        psu_wattages = []

        subtitles = driver.find_elements(By.CSS_SELECTOR, "div[class='subtitle']")
        for subtitle in subtitles:
            line = subtitle.text.strip()
            match = re.search(r'(\w+)\s+(\d+)W', line)
            if match:
                psu_sizes.append(match.group(1))
                psu_wattages.append(match.group(2))


        return psu_sizes, psu_wattages

        


    try:

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary[href='https://www.pc-kombo.com/us/components/psus']")))
        element.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h5[class='name']")))    
        psu_links = driver.find_elements(By.CSS_SELECTOR, "h5[class='name']")

        psu_sizes, psu_wattages = getSubtitleData()

        for i, link in enumerate(psu_links):

            link.click()
            driver.switch_to.window(driver.window_handles[1])

            psu_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']")))
            name = psu_name.text

            psu_brand = driver.find_element(By.CSS_SELECTOR, "dd[itemprop='brand']")
            brand = psu_brand.text

            price = extract_price(driver)
            
            psu_size = psu_sizes[i]
            psu_wattage = psu_wattages[i]

            psu = classes.PowerSupplyUnit(brand, name, price, psu_size, psu_wattage)
            psu_data.append(psu)

            with open("psudata.txt", 'a') as file:
                file.write(f"{brand},{name},{price},{psu_size},{psu_wattage}" + '\n')




            driver.close()
            driver.switch_to.window(driver.window_handles[0])


    except Exception as e:
        print("Error: ",  e)
    finally:
        driver.quit()
        print("Data saved succesfully.")

def getPCCaseData():
    print("Scraping PC case data...")

    website = 'https://www.pc-kombo.com/us/components'
    driver.get(website)
    def getSubtitleData():
        import re

        case_motherboards = []

        subtitles = driver.find_elements(By.CSS_SELECTOR, "div[class='subtitle']")
        for subtitle in subtitles:
            line = subtitle.text.strip()
            
            case_motherboards.append(line)

        return case_motherboards

        


    try:

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary[href='https://www.pc-kombo.com/us/components/cases']")))
        element.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h5[class='name']")))    
        case_links = driver.find_elements(By.CSS_SELECTOR, "h5[class='name']")

        case_motherboards = getSubtitleData()

        for i, link in enumerate(case_links):

            link.click()
            driver.switch_to.window(driver.window_handles[1])

            case_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']")))
            name = case_name.text

            case_brand = driver.find_element(By.CSS_SELECTOR, "dd[itemprop='brand']")
            brand = case_brand.text

            price = extract_price(driver)
            
            case_motherboard = case_motherboards[i]

            case = classes.ComputerCase(brand, name, price, case_motherboard)
            case_data.append(case)

            with open("casedata.txt", 'a') as file:
                file.write(f"{brand},{name},{price},{case_motherboard}" + '\n')




            driver.close()
            driver.switch_to.window(driver.window_handles[0])


    except Exception as e:
        print("Error: ",  e)
    finally:
        driver.quit()
        print("Data saved succesfully.")

def getCPUCoolerdata():
    print("Scraping CPU Cooler data...")

    website = 'https://www.pc-kombo.com/us/components'
    driver.get(website)

    try:

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary[href='https://www.pc-kombo.com/us/components/cpucoolers']")))
        element.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h5[class='name']")))    
        case_links = driver.find_elements(By.CSS_SELECTOR, "h5[class='name']")

  

        for i, link in enumerate(case_links):

            link.click()
            driver.switch_to.window(driver.window_handles[1])

            cooler_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']")))
            name = cooler_name.text

            cooler_brand = driver.find_element(By.CSS_SELECTOR, "dd[itemprop='brand']")
            brand = cooler_brand.text

            price = extract_price(driver)
            
           

            cooler = classes.CPUCooler(brand, name, price)
            cooler_data.append(cooler)

            with open("cpucoolerdata.txt", 'a') as file:
                file.write(f"{brand},{name},{price}" + '\n')




            driver.close()
            driver.switch_to.window(driver.window_handles[0])


    except Exception as e:
        print("Error: ",  e)
    finally:
        driver.quit()
        print("Data saved succesfully.")

def getMonitorData():
    print("Scraping monitor data...")

    website = 'https://www.pc-kombo.com/us/components'
    driver.get(website)

    def getSubtitleData():
        import re

        monitor_sizes = []
        monitor_resolutions = []
        monitor_refreshrates =[]

        subtitles = driver.find_elements(By.CSS_SELECTOR, "div[class='subtitle']")
        for subtitle in subtitles:
            line = subtitle.text.strip()
            match = re.search(r'(\d+\s*x\s*\d+)\s+(\d+)\s*Hz\s+(\d+(\.\d+)?)', line)
            if match:
                monitor_sizes.append(match.group(1))
                monitor_resolutions.append(match.group(2))
                monitor_refreshrates.append(match.group(3))


        return monitor_sizes, monitor_resolutions, monitor_refreshrates

    try:

        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn.btn-primary[href='https://www.pc-kombo.com/us/components/displays']")))
        element.click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h5[class='name']")))    
        monitor_links = driver.find_elements(By.CSS_SELECTOR, "h5[class='name']")

        monitor_sizes, monitor_resolutions, monitor_refreshrates = getSubtitleData()

  

        for i, link in enumerate(monitor_links):

            link.click()
            driver.switch_to.window(driver.window_handles[1])

            cooler_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']")))
            name = cooler_name.text

            cooler_brand = driver.find_element(By.CSS_SELECTOR, "dd[itemprop='brand']")
            brand = cooler_brand.text

            price = extract_price(driver)

            monitor_size = monitor_sizes[i]
            monitor_resolution = monitor_resolutions[i]
            monitor_refreshrate = monitor_refreshrates[i]
            
           

            monitor = classes.Monitor(brand, name, price, monitor_size, monitor_resolution, monitor_refreshrate)
            monitor_data.append(monitor)

            with open("monitordata.txt", 'a') as file:
                file.write(f"{brand},{name},{price},{monitor_size},{monitor_resolution},{monitor_refreshrate}" + '\n')




            driver.close()
            driver.switch_to.window(driver.window_handles[0])


    except Exception as e:
        print("Error: ",  e)
    finally:
        driver.quit()
        print("Data saved succesfully.")

j = 2
def getKeyboardData():
    from selenium.webdriver.common.keys import Keys


    try:
        global j
        website = 'https://mechanicalkeyboards.com/collections/mechanical-keyboards'
        driver.get(website)

        while j <= 28:
        

            keyboards_element = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="product-grid"]/li[1]/div/div[2]/div/h3/a')))

            keyboard_links = driver.find_elements(By.CSS_SELECTOR, 'a[class="full-unstyled-link"]')

            i = 0

            for keyboard in keyboard_links:
                if i < 2:
                    i += 1
                    continue
                else:
                    keyboard.send_keys(Keys.CONTROL + Keys.RETURN)

                    driver.switch_to.window(driver.window_handles[-1])

                    brand_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ProductInfo-template--22168607654188__main"]/div[1]/span[1]/span')))
                    brand = brand_element.text

                    name_element = driver.find_element(By.CSS_SELECTOR, 'h1[class="product__title h2"]')
                    name = name_element.text

                    price = driver.find_element(By.XPATH, '//*[@id="price-template--22168607654188__main"]/div[1]/dl/div[1]/dd/span')
                    price = price.text[1:]

                    try:

                        rating_element = driver.find_element(By.CSS_SELECTOR, 'span[class="jdgm-rev-widg__summary-average"]')
                        rating = rating_element.text

                        reviews_element = driver.find_element(By.CSS_SELECTOR, 'div[class="jdgm-rev-widg__summary-text"]')
                        review_count = reviews_element.text

                    except:

                        rating = "N/A"
                        review_count = "N/A"

                    print(f"{brand},{name},{price},{rating},{review_count}")
                    with open('keyboarddata.txt', 'a') as file:
                        file.write(f"{brand},{name},{price},{rating},{review_count}\n")

                    keyboard = classes.Keyboard(brand,name,price,rating,review_count)
                    keyboard_data.append(keyboard)

                    driver.close()

                    driver.switch_to.window(driver.window_handles[0])

                    i +=1

                    if i == 27:

                        button_link = driver.find_element(By.CSS_SELECTOR, f"a[href='/collections/mechanical-keyboards?page={j}']")
                        button_link.click()

                        j += 1
                        
                        



    except Exception as e:
        print("An error occurred:", e)

    finally:
        print("Successful")
        driver.quit()

def get_price(index):
    buttons = driver.find_elements(By.CSS_SELECTOR, 'button.v-btn--icon')
    button = buttons[index]
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    driver.execute_script("arguments[0].click();", button)

    retailers = driver.find_elements(By.CSS_SELECTOR, 'a.v-btn--density-default.v-btn--size-x-large')

    for retailer in retailers:
        if 'Amazon' in retailer.text:
            driver.execute_script("arguments[0].scrollIntoView(true);", retailer)
            driver.execute_script("arguments[0].click();", retailer)
            driver.switch_to.window(driver.window_handles[1])

            try:
                wholeprice_element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.a-price-whole')))
                fractionprice_element = driver.find_element(By.CSS_SELECTOR, 'span.a-price-fraction')
                
                if wholeprice_element:
                    price = f'{wholeprice_element.text}.{fractionprice_element.text}'
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    return price
            except NoSuchElementException:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                break
            
    return 'N/A'


def getMouseData():
    
    def remove_numbers():
        with open('mousedata.txt', 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            file.truncate()

            for line in lines:
                modified_line = line[1:]  
                file.write(modified_line)

    website = 'https://www.eloshapes.com/mouse/database'
    driver.get(website)

    page_number = 1
    max_pages = 27

    while page_number <= max_pages:
        try:
            rows = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.v-data-table__tr')))

            #itterate through rows in order to scrape data from each, opening up the amazon link if it is available to retrieve price.
            for i, row in enumerate(rows):
                row_split = row.text.split()
                if len(row_split) < 12: 
                    continue 
                
                columns = row.find_elements(By.CSS_SELECTOR, 'td.v-data-table__td')

                name = columns[2].text.strip()

                name_split = name.split()
                brand = name_split[0]

                price = get_price(i)
                length = columns[3].text.strip()
                width = columns[4].text.strip()
                height = columns[5].text.strip()
                weight = columns[6].text.strip()
                shape = columns[7].text.strip()
                connectivity = columns[8].text.strip()
                sensor = columns[9].text.strip()
                dpi = columns[10].text.strip()
                polling_rate = columns[11].text.strip()

                mouse = classes.Mouse(brand, name, price, length, width, height, weight, shape, connectivity, sensor, dpi, polling_rate)
                print(mouse)
                mouse_data.append(mouse)
                
                with open('mousedata.txt', 'a') as file:
                    file.write(f"{brand},{name},{price},{length},{width},{height},{weight},{shape},{connectivity},{sensor},{dpi},{polling_rate}\n")

            #move to next page if there is one
            try:
                next_button = driver.find_element(By.XPATH, '//*[@id="__nuxt"]/div/main/div/div[2]/div[2]/div[3]/nav/ul/li[contains(@class, "next")]/button')
                driver.execute_script("arguments[0].click();", next_button)
                page_number += 1
                print(f"Navigating to page {page_number}...")
            except NoSuchElementException:
                print("No more pages to navigate.")
                break

        except Exception as e:
            print(f"An error occurred on page {page_number}: {e}")

        finally:
            print(f"Page {page_number} processing complete")
            
    driver.quit()
    print("All pages processed, driver quit successfully")

def getHeadsetData():
    website = 'https://www.balticdata.lv/en/spelu-zona/austinas-spelem'
    driver.get(website)
    expand_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[product-page-count="96"]')))
    driver.execute_script("arguments[0].click();", expand_list)
    page_number = 1

    while page_number < 4:

        try:

            productList_elements = driver.find_elements(By.CSS_SELECTOR, 'span[class="Title"]')
            product_cards = driver.find_elements(By.CSS_SELECTOR, 'div[class="EBI4ProductObjectPlate"]')
            xpath_selector = '//img[contains(@src, "ProductBrand")]'
            image_elements = driver.find_elements(By.XPATH, xpath_selector)
            
            for i, product in enumerate(productList_elements):
                product_card = product_cards[i]

                brand = image_elements[i].get_attribute('title')
                name = product.text

                euro_price = product_card.find_element(By.CLASS_NAME, 'EBI4ProductObjectPlatePriceSale').text
                euro_price = euro_price.replace(' €', '').strip()
                price = float(euro_price) * 1.09
                price = round(price, 2)

                get_productdata = product_card.find_elements(By.CSS_SELECTOR, 'span[class="ParamValue"]')
                mic_type = get_productdata[4].text
                connectivity = get_productdata[0].text


                headset = classes.Headset(brand, price, name, mic_type, connectivity)
                print(headset)
                with open('headsetdata.txt', 'a') as file:
                    file.write(f'{brand},{name},{price},{mic_type},{connectivity}\n')
            

            next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="ProductPageContainer2"]/div/a[{page_number+1}]')))
            driver.execute_script('arguments[0].click();', next_button)
            page_number += 1


            print("********************\nTransfering to next page\n********************")
            time.sleep(3)


        except Exception as e:
            print('Error: ' + str(e))

    print("Successfully saved data.")

greeting()