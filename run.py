from booking.booking import Booking

with Booking() as bot:
    bot.land_first_page()
    bot.change_currency(currency=input("currency: "))
    bot.select_place_to_go(input("where do you want to go: "))
    bot.select_dates(check_in=input("check in data: "), check_out=input("check out data: "))

    bot.select_people(int(input("how many people go: ")))
    bot.click_search()
    bot.apply_filtration()
    bot.refresh()
    bot.report_results()
