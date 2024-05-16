# Selenium: automation of browser
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
from playsound import playsound
import random



# some other imports :-)
import os
import platform
import time
import random
import requests
import atexit
from pathlib import Path


from helpers.xpaths import *
from helpers.search import SearchHelper

class Session:
    delay = 7
    HOME_URL = "https://www.immobilienscout24.de"

    def __init__(self, headless=False, store_session=True, proxy=None, user_data=False):
        self.email = None
        self.may_send_email = False
        self.session_data = {
            "duration": 0,
            "new apartments": 0,
            "contacted": 0,
        }

        start_session = time.time()
        # Go further with the initialisation
        # Setting some options of the browser here below

        options = uc.ChromeOptions()

        # Create empty profile to avoid annoying Mac Popup
        if store_session:
            if not user_data:
            	user_data =  f"{Path().absolute()}/chrome_profile"
            if not os.path.isdir(user_data):
                os.mkdir(user_data)

            Path(f'{user_data}First Run').touch()
            options.add_argument('--profile-directory=Default')
            options.add_argument(f"--user-data-dir={user_data}")
            print(user_data)

        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        options.add_argument("--lang=en-GB")

        # Getting the chromedriver from cache or download it from internet
        print("Getting ChromeDriver ...")
        self.browser = uc.Chrome(options=options, executable_path='/usr/bin/chromedriver') #ChromeDriverManager().install(),
        # self.browser = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
        self.browser.set_window_size(1250, 750)

        # clear the console based on the operating system you're using
        os.system('cls' if os.name == 'nt' else 'clear')

        # Cool banner
        print('Starting...')
        time.sleep(1)

        self.started = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("Started session: {}\n\n".format(self.started))

    def navigate_to_home(self):
        print("Navigating to home...")
        self.browser.get(self.HOME_URL)
        time.sleep(2)

    def start_searching(self):
        print("Starting search...")
        search_helper = SearchHelper(self.browser)

        while True:
            new_offers = search_helper.get_new_offers()
            if (len(new_offers) > 0):
                self.alert()

            sleep_time = self.get_random_sleep()
            print(f"Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)

    # Actions of the session
    def login(self, email, password):
        print("Logging in with email...")
        print('Manual interference is required. Please login.')
        input('press ENTER to continue')

    def alert(self):
        print("\n\n\nAlerting...\n\n\n\n")
        # Path to your sound file (replace with your actual path)
        sound_file = "alert.mp3"

        # Play the sound
        playsound(sound_file)

        print("\n>>>>>>>>>\nAlert played\n<<<<<<<<<!")


    def get_random_sleep(self):
        return random.randint(40, 120)

    