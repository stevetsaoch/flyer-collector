# python
import re
from collections import deque
from datetime import datetime
from time import sleep

# selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# config
from config.config import Config

# driver
from driver.webdriver import Driver

# schema
from schema.task import FlyerTask, ProductTask


class OptimumFlyerCrawer:
    def __init__(self, task_queue: deque):
        self.store_name: str
        self.tab_title: str
        self.flyer_url: str
        self.flyer_title: str
        self._config: dict
        self.weekly_flyers: list = []
        self.task_queue = task_queue

        # init webdriver
        self.driver = Driver().driver()

    def init_config_and_attributes(self):
        config = Config().config
        config = config["stores"][f"{self.store_name}"]
        self.flyer_url = config["flyer_url"]
        self.tab_title = config["tab_title"]
        self.flyer_title = config["flyer_title"]
        self._config = config

    @property
    def config(self):
        return self._config

    def is_page_loaded(self):
        self.driver.get(self.flyer_url)
        # check is at flyer page
        try:
            WebDriverWait(self.driver, 120).until(
                EC.title_contains(f"{self.tab_title}")
            )
        except:
            raise

    def is_weekly_flyer_navigation_bar_loaded(self):
        # check flyer iframe is loaded
        try:
            WebDriverWait(self.driver, 120).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, "//iframe[@class='flippiframe navigationsframe']")
                )
            )
        except:
            self.driver.close()
            raise

    def get_all_weekly_flyers(self):
        # get weekly flyer, including current and preview flyers
        flyers = self.driver.find_elements(By.XPATH, "//flipp-filmstrip-pub")
        try:
            for flyer in flyers:
                header = self.driver.find_element(
                    By.XPATH,
                    f"//flipp-filmstrip-pub[@publication-id='{flyer.get_attribute('publication-id')}']//span[@class='flipp-filmstrip-pub-header']",
                ).text
                if re.search(rf"{self.flyer_title}", str(header)):
                    # get start time and end time
                    validity_dates = self.driver.find_element(
                        By.XPATH,
                        f"//flipp-filmstrip-pub[@publication-id='{flyer.get_attribute('publication-id')}']//flipp-validity-dates",
                    )

                    self.weekly_flyers.append(
                        FlyerTask(
                            store_name=self.store_name,
                            start_time=datetime.strptime(
                                str(validity_dates.get_attribute("start-date")),
                                "%Y-%m-%dT%H:%M:%S.%f%z",
                            ),
                            end_time=datetime.strptime(
                                str(validity_dates.get_attribute("end-date")),
                                "%Y-%m-%dT%H:%M:%S.%f%z",
                            ),
                            publication_id=str(flyer.get_attribute("publication-id")),
                        )
                    )

        except:
            self.driver.close()
            raise

    def get_pages_from_flyer(self):
        for flyer in self.weekly_flyers:
            pages = []
            publication_id = flyer.publication_id
            # click on navigationsframe to load page
            self.driver.execute_script(
                "arguments[0].click();",
                self.driver.find_element(
                    By.XPATH,
                    f"//flipp-filmstrip-pub[@publication-id='{publication_id}']//button",
                ),
            )
            self.driver.switch_to.default_content()
            # wait mainframe loaded and switch to it
            WebDriverWait(self.driver, 120).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, "//iframe[@class='flippiframe mainframe']")
                )
            )
            page_elements = self.driver.find_elements(By.XPATH, "//sfml-flyer-image")
            for page in page_elements:
                try:
                    pages.append(str(page.get_attribute("sfml-anchor-id")))
                except Exception as e:
                    continue
            flyer.pages = pages
            self.task_queue.append(flyer)

    def get_all_flyer_product_detail_url(self):
        for flyer in self.weekly_flyers:
            for page in flyer.pages:
                try:
                    products = self.driver.find_elements(
                        By.XPATH,
                        f"//sfml-flyer-image[@sfml-anchor-id='{page}']//div/button",
                    )
                    for product in products:
                        try:
                            # check whether button is a product
                            product.get_attribute("data-product-id")
                        except:
                            continue

                        # click image to get product detail url
                        try:
                            self.driver.execute_script("arguments[0].click();", product)
                            sleep(5)
                            self.driver.switch_to.default_content()
                            WebDriverWait(self.driver, 30).until(
                                EC.visibility_of_element_located(
                                    (
                                        By.XPATH,
                                        "//a[@class='product-details-link__link']",
                                    )
                                )
                            )
                            hrefs = self.driver.find_elements(
                                By.XPATH, "//a[@class='product-details-link__link']"
                            )
                            for href in hrefs:
                                try:
                                    product_url = href.get_attribute("href")
                                    product_task = ProductTask(
                                        store_name=self.store_name,
                                        publication_id=flyer.publication_id,
                                        url=product_url,
                                    )
                                    self.task_queue.append(product_task)
                                except:
                                    continue

                            WebDriverWait(self.driver, 10).until(
                                EC.frame_to_be_available_and_switch_to_it(
                                    (
                                        By.XPATH,
                                        "//iframe[@class='flippiframe mainframe']",
                                    )
                                )
                            )
                        except:
                            raise
                except:
                    self.driver.close()
                    raise

    def start(self):
        self.is_page_loaded()
        self.is_weekly_flyer_navigation_bar_loaded()
        self.get_all_weekly_flyers()
        self.get_pages_from_flyer()
        self.get_all_flyer_product_detail_url()
