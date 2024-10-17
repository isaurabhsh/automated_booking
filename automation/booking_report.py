from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class BookingReport:
    def __init__(self, boxes_section_element:WebElement, debug) -> None:
        self.debug = debug
        if self.debug: print(f"DEBUG : Executing BookingReport.__init__()")
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()
        if self.debug: print(f"DEBUG : =>\tlen(self.deal_boxes) : {len(self.deal_boxes)}")
        
    def pull_deal_boxes(self):
        if self.debug: print(f"DEBUG : Executing BookingReport.pull_deal_boxes()")
        return self.boxes_section_element.find_elements(by=By.CSS_SELECTOR, value='div[data-testid="property-card"]')
    
    def pull_deal_boxes_attributes(self):
        if self.debug: print(f"DEBUG : Executing BookingReport.pull_titles()")
        search_result = []
        for deal_box in self.deal_boxes:
            hotel_name = deal_box.find_element(by=By.CSS_SELECTOR, value='div[data-testid="title"]'
                                               ).get_attribute('innerHTML').strip()
            # print(f"hotel_name : {hotel_name}")
            hotel_price = deal_box.find_element(by=By.CSS_SELECTOR, value='div[data-testid="price-and-discounted-price"]'
                                                ).find_elements(by=By.TAG_NAME, value="span")[-1].get_attribute('innerHTML')
            # print(f"hotel_price : {hotel_price}")

            hotel_review_score = None
            hotel_review_category = None

            try:
                div_nodes = deal_box.find_element(by=By.CSS_SELECTOR, value='div[data-testid="review-score"]'
                                                  ).find_elements(by=By.TAG_NAME, value="div")
                div_node_values = [div.get_attribute('innerHTML') for div in div_nodes]
                hotel_review_score = div_node_values[0]
                review_count    = div_node_values[-1]
                review_category = div_node_values[2][:div_node_values[2].index('<')]
                review_category = "Just Alright" if review_category=="Review score" else review_category
                hotel_review_category = f"{review_category} with {review_count}"
                
            except Exception as e:
                hotel_review_score = "No Ratings"
            
            # print(f"hotel_score : {hotel_score}")
            search_result.append(
                [hotel_name, hotel_price, hotel_review_score, hotel_review_category]
            )
            
        return search_result
            
            