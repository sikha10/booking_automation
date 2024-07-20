from booking.booking import Booking
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
with Booking(options=options) as bot:
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    bot.land_first_page()
    bot.change_currency(currency=input("currency: "))
    bot.select_place_to_go(input("where do you want to go: "))
    bot.select_dates(check_in=input("check in data: "), check_out=input("check out data: "))

    bot.select_people(int(input("how many people go: ")))
    bot.click_search()
    bot.apply_filtration(input("type hotels ratings: "))
    bot.refresh()
    bot.report_results()
