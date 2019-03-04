from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import re, time, math, unittest

GRID_URL = 'http://localhost:4444/wd/hub'

class AutoSearchPage:
    # default element locators and constants
    registration_date_element = "//*[contains(text(),'Erstzul')]"
    year_selector = 'yearRange.min'
    sort_price = 'sort'
    get_price_all_vehicle_data_element = "//div[@data-qa-selector='price']"
    total_result_count = "//div[@data-qa-selector='results-amount']"
    total_results_per_page_count = "//select[@name='pageSize']/option[1]"
    get_vehicle_year = "//a[@data-qa-selector='ad']/ul/li[1]"

    # constructor
    def __init__(self, driver):
        print('initialising the driver object ...')
        self.driver = driver

    # method to filter by first registrations and highest price

    def find(self, search_year, sort_by):
        src = self.driver.find_element(By.XPATH, self.registration_date_element);
        type(src)
        src.click()
        # src1=driver.find_element_by_xpath("//*[contains(text(),'belie')]")
        search_year_select = Select(self.driver.find_element(By.NAME, self.year_selector))
        search_year_select.select_by_visible_text(search_year)
        sort_by_select = Select(self.driver.find_element(By.NAME, self.sort_price))
        sort_by_select.select_by_visible_text(sort_by)
        time.sleep(4)

    # method to get the price of all vehicles in an array

    def get_price_of_all_vehicles(self):
        # get_price_vehicle = self.driver.find_element(By.XPATH, self.get_price_all_vehicle_data_element);
        vehicle_prices = []
        price_elements = self.driver.find_elements(By.XPATH, self.get_price_all_vehicle_data_element)
        for price_element in price_elements:
            vehicle_price_array = re.findall(r'\d+', price_element.text)
            actual_price = int(vehicle_price_array[0] + vehicle_price_array[1])
            vehicle_prices.append(actual_price)
        return vehicle_prices

    def get_total_pages(self):
        count_result_vehicles = self.driver.find_element(By.XPATH, self.total_result_count)
        count_per_page_result = self.driver.find_element(By.XPATH, self.total_results_per_page_count)
        total_vehicle = int(re.findall(r'\d+', count_result_vehicles.text)[0])
        return math.ceil(total_vehicle / int(count_per_page_result.text))

    def get_year_of_all_vehicles(self):
        vehicle_year = []
        year_elements = self.driver.find_elements(By.XPATH, self.get_vehicle_year)
        for i in year_elements:
            vehicle_year_array = re.findall(r'\d+', i.text)
            actual_year = int(vehicle_year_array[1])
            vehicle_year.append(actual_year)
        return vehicle_year

    def close_page(self):
        self.driver.quit();


## The test cases for the module
class VehiclesTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(desired_capabilities=DesiredCapabilities.CHROME, command_executor=GRID_URL)
        self.driver.set_page_load_timeout(20)
        self.driver.get('https://www.autohero.com/de/search/')
        self.auto_search_page = AutoSearchPage(self.driver)
        self.auto_search_page.find('2015', 'Höchster Preis')

    def get_page_url_for(self, page_number):
        if page_number == 1:
            return self.driver.current_url
        else:
            return 'https://www.autohero.com/de/search/?page=' + str(page_number) + '&sort=PRICE_DESC&&yearMin=2015'


    def test_page_sort_order(self):
        price_array_main = []
        for i in range(1, self.auto_search_page.get_total_pages() + 1):
            page_url = self.get_page_url_for(i)
            self.driver.get(page_url)
            vehicle_prices = self.auto_search_page.get_price_of_all_vehicles()
            years_array = self.auto_search_page.get_year_of_all_vehicles()
            sorted_array = sorted(vehicle_prices, reverse=True)
            # check if the price is sorted correctly in that page
            assert vehicle_prices == sorted_array, "The prices are not correctly in page number " + str(i);
            # compare with the values in all the pages
            price_array_main.append(vehicle_prices)
            sort_main_array=sorted(price_array_main,reverse=True)
            assert price_array_main==sort_main_array, "The prices are not sorted correctly in order , The problematic page is " + str(i)
            # Check to see if the vehicles are greater than 2015
            # Taken from SO https://stackoverflow.com/questions/20229822/check-if-all-values-in-list-are-greater-than-a-certain-number
            # Not sure about generators
            assert all(i >= 2015 for i in years_array), 'There are vehicles with year less than 2015'

    def tearDown(self):
        self.auto_search_page.close_page()



if __name__ == '__main__':
    unittest.main()

