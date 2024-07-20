from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

class Bookingfiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, star_values):
        # Old Logic
        # star_filtration_box = self.driver.find_element(By.CSS_SELECTOR, 'div[data-filters-group="class"]')
        # star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, 'div[class="e2585683de be323bc46b d8d16787ba e08ac371bf df30cb1b27"]')

        # for star_value in star_values:
        #     for star_element in star_child_elements:
        #         if str(star_element.find_element(By.CSS_SELECTOR, 'div[class="adc8292e09 ea1e323a59 a3c80e4a68 fbe4119cc7 c9dfcc67e5"]').get_attribute('innerHTML')).strip(' ') == f'{star_value}':
        #             star_element.click()

        # New Logic
        for star_value in star_values:
            retry_count = 3  # Number of retries
            while retry_count > 0:
                try:
                    star_child_element = self.driver.find_element(By.CSS_SELECTOR, f'div[data-filters-item="class:class={star_value}"]')
                    print(star_child_element)
                    sleep(1)
                    star_child_element.click()
                    break  # Exit the loop if click is successful
                except StaleElementReferenceException:
                    retry_count -= 1
                    sleep(1)  # Wait before retrying
                    print(f"Retrying... ({3 - retry_count}/3)")
                except NoSuchElementException:
                    print(f"Star rating element for {star_value} not found.")
                    break  # Exit the loop if the element is not found

    def sort_price_lowest_first(self):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, 'li[data-id="price"]')
            element.click()

        except:
            print("first method did not work")

        try:
            top_element = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
            top_element.click()
            element = self.driver.find_element(By.CSS_SELECTOR, 'button[data-id="price"]')
            element.click()

        except:
            print("second method did not work")
