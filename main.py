# python
from time import sleep
from collections import deque
from threading import Thread

# flyer crawler
from flyer_crawler.superstore import Superstore

# task saver
from saver.task import TaskSaver

task_queue = deque([])
task_saver = TaskSaver(task_queue)
superstore = Superstore(task_queue)

thread_2 = Thread(target=superstore.start)
thread_2.daemon = True
thread_2.start()

thread_1 = Thread(target=task_saver.start)
thread_1.daemon = True
thread_1.start()

while True:
    sleep(1)
