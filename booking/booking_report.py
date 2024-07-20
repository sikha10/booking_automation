from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement


class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')

    def pull_deal_box_attribute(self):
        hotel_score = self.boxes_section_element.find_elements(By.CSS_SELECTOR, 'div[class="d0522b0cca fd44f541d8"]')
        collection = []
        for deal_box, hotel_sc in zip(self.deal_boxes, hotel_score):
            hotel_name = deal_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').get_attribute('innerHTML').strip()
            hotel_price = deal_box.find_element(
                By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').get_attribute('innerHTML').strip()
            hotels_scores = hotel_sc.get_attribute('innerHTML')
            collection.append([hotel_name, hotel_price, hotels_scores])

        return collection

