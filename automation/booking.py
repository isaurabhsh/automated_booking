import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support import expected_conditions as EC

# from webdriver_manager.chrome import ChromeDriverManager

from automation.booking_filtration import BookingFiltration
import automation.constants as CONST
from automation.booking_report import BookingReport

from prettytable import PrettyTable


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=CONST.DRIVER_PATH, base_url=CONST.BASE_URL, teardown=False) -> None:
        self.debug = input("Debug Mode?")
        if self.debug: print(f"DEBUG : Executing Booking.__init__()")
        self.driver_path = driver_path
        self.base_url = base_url
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        if self.debug: print(f"DEBUG : =>\tself.driver_path:{self.driver_path}")
        if self.debug: print(f"DEBUG : =>\tself.teardown:{self.teardown}")
        options = webdriver.ChromeOptions()
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument('headless')
        # options.add_argument("--headless")
        # options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking,self).__init__(options=options)
        self.implicitly_wait(15) # wait 15 secs for "find_element" methods, but move to next method if first completes
        self.maximize_window() # maximize browser window
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.debug: print(f"DEBUG : Executing Booking.__exit__()")
        if self.debug: print(f"DEBUG : =>\tself.teardown:{self.teardown}")
        if self.teardown:
            self.quit()
            
    def land_first_page(self):
        if self.debug: print(f"DEBUG : Executing Booking.land_first_page()")
        if self.debug: print(f"DEBUG : =>\tself.base_url:{self.base_url}")
        self.get(url=self.base_url)
        
    def change_currency(self, currency='USD'):
        if self.debug: print(f"DEBUG : Executing Booking.change_currency()")
        # <button class ...... type="button" data-tooltip-text="Choose your currency">
        currency_element = self.find_element(by=By.CSS_SELECTOR,
                                             value='button[data-tooltip-text="Choose your currency"]')
        currency_element.click()
        

        # <a class ...... data-modal-header-async-url-param = "changed_currency=1&selected_currency=USD&top_currency=1"
        selected_currency_element = self.find_element(by=By.CSS_SELECTOR,
                                                      value=f'a[data-modal-header-async-url-param*="selected_currency={currency}"]')
        selected_currency_element.click()
        
    def select_place_to_go(self, place_to_go):
        if self.debug: print(f"DEBUG : Executing Booking.select_place_to_go()")
        # <input type="search" name="ss" id="ss" class="c-autocomplete__input sb-searchbox__input sb-destination__i....
        search_field = self.find_element(by=By.ID, value='ss')
        search_field.clear()  # Clearing pre-existing text value in the form field
        search_field.send_keys(place_to_go)
        first_result = self.find_element(by=By.CSS_SELECTOR, value='li[data-i="0"]')
        first_result.click()
        
    def select_dates(self, check_in_date, check_out_date):
        if self.debug: print(f"DEBUG : Executing Booking.select_dates()")
        check_in_date_element = self.find_element(by=By.CSS_SELECTOR, value=f'td[data-date="{check_in_date}"]')
        check_in_date_element.click()
        check_out_date_element = self.find_element(by=By.CSS_SELECTOR, value=f'td[data-date="{check_out_date}"]')
        check_out_date_element.click()
        
    def select_guest_occupancy_detail(self):
        if self.debug: print(f"DEBUG : Executing Booking.select_guest_occupancy_detail()")
        # < label id = "xp__guests__toggle" for ="xp__guests__input" class ="xp__input" data-group-toggle=""
        # role="button" aria-expanded="true" aria-controls="xp__guests__inputs-container" data-group-toggle-
        # shown="1" >
        select_guest_occupancy_form = self.find_element(by=By.ID, value='xp__guests__toggle')
        select_guest_occupancy_form.click()
        
    def select_adult_occupants(self, num_guest_adults=1):
        if self.debug: print(f"DEBUG : Executing Booking.select_adult_occupants()")
        # < label id = "xp__guests__toggle" for ="xp__guests__input" class ="xp__input" data-group-toggle="" ......
        # select_num_adults = self.find_element(by=By.ID, value='xp__guests__toggle')
        # select_num_adults.click()

        # < button class ="bui-button ........ type = "button" aria - label = "Decrease number of Adults"

        # < div class ="bui-stepper__wrapper sb-group__stepper-a11y" >
        #     < input style = "display: none" type = "number" class ="bui-stepper__input" data-bui-ref="input-" \
        #     stepper-field" id="group_adults" name="group_adults" min="1" max="30" value="2" data-group-adults-" \
        #     "count="" aria-valuenow="2" >" \
        #
        # < button class ="bui-button bui-button--secondary bui-stepper__subtract-button " data-bui-ref="input-" \
        # "stepper-subtract-button" type="button" aria-label="Decrease number of Adults" aria-describedby="group_" \
        # "adults_desc" >< span class ="bui-button__text" > − < / span >< / button >
        # < span class ="bui-stepper__display" data-bui-ref="input-stepper-value" aria-hidden="true" > 2 < / span >
        #
        # < button class ="bui-button bui-button--secondary bui-stepper__add-button " data-bui-ref="input-" \
        # "stepper-add-button" type="button" aria-label="Increase number of Adults" aria-describedby="group_" \
        # "adults_desc" >< span class ="bui-button__text" > + < / span >< / button >
        # < span class ="bui-u-sr-only" aria-live="assertive" id="group_adults_desc" > 2 Adults < / span >< / div >

        decrease_adult_button = self.find_element(by=By.CSS_SELECTOR,
                                                  value='button[aria-label="Decrease number of Adults"]')
        increase_adult_button = self.find_element(by=By.CSS_SELECTOR,
                                                  value='button[aria-label="Increase number of Adults"]')

        while True:
            curr_adults_element = self.find_element(by=By.ID, value='group_adults')
            num_curr_adults = curr_adults_element.get_attribute('value')

            if int(num_curr_adults)==int(num_guest_adults):
                break
            if int(num_curr_adults) < int(num_guest_adults):
                increase_adult_button.click()
            elif int(num_curr_adults) > int(num_guest_adults):
                decrease_adult_button.click()
    
    def select_child_occupants(self, num_guest_children=1, ages_guest_children=[1]):
        if self.debug: print(f"DEBUG : Executing Booking.select_child_occupants()")
        if num_guest_children != len(ages_guest_children):
            raise Exception("Number of children and count of their respective ages do not match")
        # < div class ="bui-stepper__wrapper sb-group__stepper-a11y" >
        #     < input style = "display: none" type = "number" class ="bui-stepper__input"
        #     data-bui-ref="input-stepper-field" id="group_children" name="group_children" min="0" max="10" value="0"
        #     data-group-children-count="" aria-valuenow="0" >
        #
        # < button class ="bui-button bui-button--secondary bui-stepper__subtract-button sb-group__stepper-button-dis" \
        #   "abled" data-bui-ref="input-stepper-subtract-button" type="button" aria-label="Decrease number of Children"
        #     aria-describedby="group_children_desc" disabled="true" >< span class ="bui-button__text" > − < / span >
        # < / button >
        #
        # < span class ="bui-stepper__display" data-bui-ref="input-stepper-value" aria-hidden="true" > 0 < / span >
        #
        # < button class ="bui-button bui-button--secondary bui-stepper__add-button "
        #     data-bui-ref="input-stepper-add-button" type="button" aria-label="Increase number of Children"
        #     aria-describedby="group_children_desc" > < span class ="bui-button__text" > + < / span >< / button >< span
        #     class ="bui-u-sr-only" aria-live="assertive" id="group_children_desc" > 0 Children < / span >< / div >

        decrease_children_button = self.find_element(by=By.CSS_SELECTOR,
                                                     value='button[aria-label="Decrease number of Children"]')
        increase_children_button = self.find_element(by=By.CSS_SELECTOR,
                                                     value='button[aria-label="Increase number of Children"]')
        guest_child_seq = 0
        while True:
            children_element = self.find_element(by=By.ID, value='group_children')
            num_curr_children = children_element.get_attribute('value')

            if int(num_curr_children)==int(num_guest_children):
                break
            if int(num_curr_children) < int(num_guest_children):
                increase_children_button.click()
                se = Select(self.find_element(by=By.CLASS_NAME, value=f'sb-group-field-has-error'))
                se.select_by_value(f"{ages_guest_children[guest_child_seq]}")
                guest_child_seq += 1
            elif int(num_curr_children) > int(num_guest_children):
                decrease_children_button.click()
    
    def select_room_quantity(self, num_rooms=1):
        if self.debug: print(f"DEBUG : Executing Booking.select_room_quantity()")
        # < div class ="bui-stepper__wrapper sb-group__stepper-a11y" >< input style = "display: none" type = "number"
        #     class ="bui-stepper__input" data-bui-ref="input-stepper-field" id="no_rooms" name="no_rooms"
        #     min="1" max="30" value="1" data-group-rooms-count="" >
        #
        # < button class ="bui-button bui-button--secondary bui-stepper__subtract-button sb-group__stepper-" \
        #     "button-disabled" data-bui-ref="input-stepper-subtract-button" type="button"
        #     aria-label="Decrease number of Rooms" aria-describedby="no_rooms_desc" >< span class ="bui-button" \
        #     "__text" > − < / span >< / button >
        # < span class ="bui-stepper__display" data-bui-ref="input-stepper-value" aria-hidden="true" > 1 < / span >
        #
        # < button class ="bui-button bui-button--secondary bui-stepper__add-button " data-bui-ref="input-" \
        #     "stepper-add-button" type="button" aria-label="Increase number of Rooms" aria-describedby="no_" \
        # "rooms_desc">< span class ="bui-button__text" > + < / span >< / button >< span class ="bui-u-sr-only"
        # aria-live="assertive" id="no_rooms_desc" > 1 Rooms < / span >< / div >
        
        decrease_rooms_button = self.find_element(by=By.CSS_SELECTOR,
                                                     value='button[aria-label="Decrease number of Rooms"]')
        increase_rooms_button = self.find_element(by=By.CSS_SELECTOR,
                                                     value='button[aria-label="Increase number of Rooms"]')
        
        while True:
            room_element = self.find_element(by=By.ID, value='no_rooms')
            num_curr_rooms = room_element.get_attribute('value')

            if int(num_curr_rooms)==int(num_rooms):
                break
            if int(num_curr_rooms) < int(num_rooms):
                increase_rooms_button.click()
            elif int(num_curr_rooms) > int(num_rooms):
                decrease_rooms_button.click()
                
    def click_search(self):
        if self.debug: print(f"DEBUG : Executing Booking.click_search()")
        search_button = self.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]')
        search_button.click()
        
    def apply_filtration(self):
        if self.debug: print(f"DEBUG : Executing Booking.apply_filtration()")
        filtration = BookingFiltration(self)
        filtration.apply_star_rating(4, 5, 2)
        filtration.sort_price()
        
    def report_results(self):
        if self.debug: print(f"DEBUG : Executing Booking.report_results()")
        # property_listings = self.find_element(by=By.CSS_SELECTOR, value='div[data-component="arp-properties-list"]'
        #                                       ).find_elements(by=By.CSS_SELECTOR, value='div[data-testid="property-card"]')
        # property_listings = self.find_element(by=By.ID, value='search_results_table'
        #                                       ).find_elements(by=By.CSS_SELECTOR, value='div[data-testid="property-card"]')
        hotel_boxes = self.find_element(by=By.ID, value='search_results_table')
        report = BookingReport(hotel_boxes, self.debug)
        hotel_search_result = report.pull_deal_boxes_attributes()
        
        result_table = PrettyTable(field_names=["Hotel Name", "Hotel Price", "Review Score", "Review Category"])
        result_table.add_rows(hotel_search_result)
        print(result_table)
        
