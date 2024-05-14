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


class OptimumProductCrawer:
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

    def is_product_detail_loaded(self):
        # check is at flyer page
        try:
            WebDriverWait(self.driver, 120).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        f"//div[@data-track-product-component='product-details']",
                    )
                )
            )
        except:
            raise

    def detail_into_a_string(self):
        pass

    def is_meat(self):
        pass
