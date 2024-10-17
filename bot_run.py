from automation.booking import Booking

try:
    with Booking(teardown=False) as bot:
        bot.land_first_page()
        bot.change_currency('GBP')
        bot.refresh()
        bot.select_place_to_go('Jaipur')
        bot.select_dates(check_in_date='2022-09-27', check_out_date='2022-09-28')
        bot.select_guest_occupancy_detail()
        bot.select_adult_occupants(num_guest_adults=2)
        bot.select_child_occupants(num_guest_children=1, ages_guest_children=[15])
        bot.select_room_quantity(num_rooms=3)
        bot.click_search()
        bot.apply_filtration()
        bot.refresh()  # Giving bit a moment to grab sorted data(by price)
        bot.report_results()
except Exception as e:
    if 'in PATH' in str(e):
        print("There is a problem running this program from command line interface")
        print("""
              You are trying to run the bot from command line
              Please add to PATH your Selenium Drivers
              For 'Windows':
                set PATH=%PATH%;<path\to\your\selenium-driver-folder>
            For 'Linux':
            set PATH=$PATH:/path/to/your/selenium-driver-folder
            """)
    else:
        raise


    