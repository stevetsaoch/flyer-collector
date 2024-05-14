# python
from collections import deque

# selenium
from selenium.webdriver.support import expected_conditions as EC

#
from flyer_crawler.optimum_crawer import OptimumFlyerCrawer


class Superstore(OptimumFlyerCrawer):
    def __init__(self, task_queue: deque):
        super().__init__(task_queue)
        self.store_name = "superstore"
        self.init_config_and_attributes()
