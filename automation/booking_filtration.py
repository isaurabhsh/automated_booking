from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class BookingFiltration:
    def __init__(self, driver) -> None:
        self.driver = driver
        if self.driver.debug: print(f"DEBUG : Executing BookingFiltration.__init__()")
        if self.driver.debug: print(f"DEBUG : =>\tself.driver:{self.driver}")
        
    def apply_star_rating(self, *num_stars_range):
        if self.driver.debug: print(f"DEBUG : Executing BookingFiltration.apply_star_rating()")
        div_nodes = self.driver.find_element(by=By.CSS_SELECTOR, value='div[data-testid="filters-sidebar"]')
        star_rating_filter = div_nodes.find_element(by=By.CSS_SELECTOR, value='div[data-filters-group="class"]')
        star_ratings = star_rating_filter.find_elements(by=By.CSS_SELECTOR, value='*')
        for num_stars in num_stars_range:
            for star_class in star_ratings:
                if str(star_class.get_attribute('innerHTML')).strip()==f"{num_stars} stars":
                    star_class.click()
        
    def sort_price(self):
        if self.driver.debug: print(f"DEBUG : Executing BookingFiltration.sort_price()")
        try:
            sort_bar = self.driver.find_element(by=By.CSS_SELECTOR, value='div[data-sort-bar-container="sort-bar"]')
        except Exception as e:
            if self.driver.debug: print(f"DEBUG : =>\tSort Bar not found")
            sort_bar = None
        try:
            sort_dropdown = self.driver.find_element(by=By.CSS_SELECTOR, value='button[data-testid="sorters-dropdown-trigger"]')
        except Exception as e:
            if self.driver.debug: print(f"DEBUG : =>\tSort Dropdown not found")
            sort_dropdown = None

        price_sort_element = None
            
        if sort_bar:
            if self.driver.debug: print(f"DEBUG : =>\tSort Bar : Looking for - Price (lowest first) ")
            price_sort_element = self.driver.find_element(by=By.CSS_SELECTOR, value='li[data-id="price"]')
        elif sort_dropdown and not sort_bar:
            if self.driver.debug: print(f"DEBUG : =>\tClicking Sort Dropdown")
            sort_dropdown.click()
            
            try:
                if self.driver.debug: print(f"DEBUG : =>\tSort DropDown : Looking for - Price (lowest first) ")
                price_sort_element = self.driver.find_element(by=By.CSS_SELECTOR, value='button[data-id="price"]')
            except Exception as e:
                if self.driver.debug: print(f"DEBUG : =>\tSort DropDown : Not Found - Price (lowest first) ")
                price_sort_element = None
        else:
            if self.driver.debug: print("DEBUG : =>\tNeither result 'sort bar' not 'sort dropdown' fownd!!! ")
        
        if price_sort_element:
            if self.driver.debug: print(f"DEBUG : =>\tClicking - Price (lowest first) ")
            price_sort_element.click()
        
        