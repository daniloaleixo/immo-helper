
import time
import json
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException

class SearchHelper:
    delay = 7

    start_urls = [
      "https://www.immobilienscout24.de/Suche/shape/wohnung-mieten?shape=cWhqX0l9ZXVwQXZKcUdkRXtLZEZnbkByQGNyQWBOa3BAaUB5QW5Xc0JmZEFtVEpzQGdUY21DbVp1a0Fja0BmS3duQHZ6QW1PakB1R25CeWhAZ2xBd0hnQntAbEJkQHtMdkp5YEB7Q3lZb1d9TGNZbWJAb2dAZ1FxU2ZCfVFiV2VEYldWdmZAa0NlQWtackBzUWRJfVFsVGltQXhnQ2ViQGR6QXNBflRmQ25NblNoUnxgQG5NaFBiQXJPaUN4Vm1NZFVvVHpmQG15QGhNY15_QE5uRWJAfk54Um5KbENnRXBMfUFkX0B6U3BzQGJIZkNoT19HfFN3WHRbcVViSm5gRHxBekRgbkBiVw..&numberofrooms=2.0-&price=700.0-1600.0&livingspace=40.0-70.0&exclusioncriteria=swapflat&pricetype=calculatedtotalrent&sorting=2",
    ]

    def __init__(self, browser):
        self.browser = browser

    # Function needs to get the current offers on the page and compare to the ones that I have saved already
    def get_new_offers(self):
      last_offers = self.get_last_offers()
      current_offers = self.get_all_offers_available()

      new_offers = self.compare_offers(last_offers, current_offers)
      self.save_new_offers(new_offers)
      print(f">>>>>> Found {len(new_offers)} new offers")

      self.save_current_offers(current_offers)
      
      return new_offers

    def get_all_offers_available(self):
      offers = []
      
      for url in self.start_urls:
        self.browser.get(url)
        time.sleep(5)

        try:
          print("Getting current offers...")

          xpath = "//div[@class='result-list-entry__data']"
          WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                  (By.XPATH, xpath)))
          child_elements = self.browser.find_elements(By.XPATH, xpath)
          
          for child in child_elements:
            try:
              element = child.find_element(By.XPATH, ".//a")
              offer = {
                "title": element.find_element(By.XPATH, ".//h2").text,
                "link": element.get_attribute("href")
              }
              offers.append(offer)
            except:
              print("Element not found", child.text)

          print(f"Found {len(offers)} current offers")
            

        except TimeoutException:
          self._exit_by_time_out()
      
      return offers 

    def get_last_offers(self):
      with open("last_offers.json", "r") as f:
        return json.load(f)
    
    def _exit_by_time_out(self):
      print("Loading an element took too much time!. Please check your internet connection.")
      print("Alternatively, you can add a sleep or higher the delay class variable.")
      exit(1)

    def compare_offers(self, last_offers, current_offers):
      new_offers = [offer for offer in current_offers if offer not in last_offers]
      return new_offers

    def save_current_offers(self, offers):
      with open("last_offers.json", "w") as f:
        json.dump(offers, f)
    
    def save_new_offers(self, offers):
      # Get current date and hour (adjust format as needed)
      now = datetime.now().strftime("%Y-%m-%d_%H-%M")  # Year-Month-Day_Hour-Minute

      # Create filename with timestamp
      filename = f"new_offers_{now}.json"

      with open(filename, "w") as f:
        json.dump(offers, f)