from selenium.webdriver.common.by import By
import booking.constant as const
from selenium import webdriver
from booking.booking_filtration import Bookingfiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"D:\selenium chromedriver\chromedriver.exe", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        super(Booking, self).__init__()
        self.implicitly_wait(10)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        currency_element = self.find_element(By.CSS_SELECTOR,
                          'button[data-tooltip-text="Choose your currency"]'
                          )
        currency_element.click()
        selected_currency_element = self.find_element(By.CSS_SELECTOR,
                                                      f'a[data-modal-header-async-url-param="changed_currency=1&selected_currency={currency}&top_currency=1"]'
                                                      )
        selected_currency_element.click()

    def select_place_to_go(self, place_go):
        search_field = self.find_element(By.ID, "ss")
        search_field.clear()
        search_field.send_keys(place_go)

        first_result = self.find_element(By.CSS_SELECTOR, 'li[data-i="0"]')
        first_result.click()

    def select_dates(self, check_in, check_out):
        check_in_element = self.find_element(By.CSS_SELECTOR, f'td[data-date="{check_in}"]')
        check_in_element.click()

        check_out_element = self.find_element(By.CSS_SELECTOR, f'td[data-date="{check_out}"]')
        check_out_element.click()

    def select_people(self, count=1):
        selection_element = self.find_element(By.ID, "xp__guests__toggle")
        selection_element.click()

        while True:
            decrease_adults_element = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]')
            decrease_adults_element.click()

            adults_value_element = self.find_element(By.ID, "group_adults")
            adults_value = adults_value_element.get_attribute('value')  # it gives me adults count
            if int(adults_value) == 1:
                break
        increase_button_element = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]')

        for _ in range(count - 1):
            increase_button_element.click()

    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

    def apply_filtration(self):
        filtration = Bookingfiltration(driver=self)
        filtration.apply_star_rating(4, 5)
        filtration.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.find_element(
            By.ID, "search_results_table"
        )

        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=['Hotel Name', 'Hotel Price', 'Hotel score']
        )
        table.add_rows(report.pull_deal_box_attribute())
        print(table)
