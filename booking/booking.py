from selenium.webdriver.common.by import By
import booking.constant as const
from selenium import webdriver
from booking.booking_filtration import Bookingfiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# sometimes it opens another verion of booking.com 
class Booking(webdriver.Chrome):
    def __init__(self, options, teardown=False):
        self.teardown = teardown
        super(Booking, self).__init__(options=options)
        self.set_window_position(2000, 0)
        self.implicitly_wait(10)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        try:
            currency_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
        except: 
            currency_element = self.find_element(By.CSS_SELECTOR,
                          'button[data-modal-aria-label="Select your currency"]'
                          )

        currency_element.click()
        try:
            selected_currency_element = self.find_elements(By.CSS_SELECTOR,
                                                      'div[class=" b284c0e8fc"]'
                                                      )
        except:
            selected_currency_element = self.find_elements(By.CSS_SELECTOR, 'div[class="bui-traveller-header__currency"]')
        for currencyElem in selected_currency_element:
            try:
                if currencyElem.get_attribute("innerHTML") == currency:
                    currencyElem.click()
            except:
                pass

    def select_place_to_go(self, place_go):
        try:
            search_field = self.find_element(By.ID, ":rh:")
        except:
            search_field = self.find_element(By.CLASS_NAME, "ada65db9b5")
        search_field.clear()
        search_field.send_keys(place_go)
        sleep(1)
        first_result = self.find_element(By.ID, 'autocomplete-result-0')
        first_result.click()

    def select_dates(self, check_in, check_out):
        check_in_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in}"]')
        check_in_element.click()

        check_out_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out}"]')
        check_out_element.click()

    def select_people(self, count=1):
        selection_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        selection_element.click()

        while True:
            decrease_adults_element = self.find_elements(By.CSS_SELECTOR, 'span[class="d71f792240"]')[1]
            decrease_adults_element.click()
            adults_value_element = self.find_element(By.CSS_SELECTOR, 'span[class="fb7047f72a"]')
            adults_value = adults_value_element.get_attribute("innerHTML")  # it gives me adults count
            print(adults_value)
            if int(adults_value) == 1:
                break 

        increase_button_element = self.find_element(By.CSS_SELECTOR, 'button[class="dba1b3bddf e99c25fd33 aabf155f9a f42ee7b31a a86bcdb87f e137a4dfeb d1821e6945"]')

        for _ in range(count - 1):
            increase_button_element.click()

    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

    def apply_filtration(self, rating: str):
        rating_list = rating.replace(" ", "").split(',')
        
        filtration = Bookingfiltration(driver=self)
        filtration.apply_star_rating(tuple(rating_list))
        filtration.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.find_element(
            By.CSS_SELECTOR, 'div[class="f9958fb57b"]'
        )

        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=['Hotel Name', 'Hotel Price', 'Hotel score']
        )
        table.add_rows(report.pull_deal_box_attribute())
        print(table)
