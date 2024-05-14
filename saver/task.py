# python
from collections import deque
from time import sleep

# pymongo
from pymongo.collection import Collection

# database
from database.mongo import mongo_client

# schema
from schema.task import Task


class TaskSaver:
    def __init__(self, task_queue: deque):
        self.mongo_client = mongo_client
        self.collection_name = "tasks"
        self.task_queue: deque = task_queue

    def _get_collection(self, database_name: str, collection_name: str) -> Collection:
        database = self.mongo_client[database_name]
        collection = database[collection_name]
        return collection

    def check_is_task_exist(self, task: Task):
        result = None
        collection = self._get_collection(
            task.task.store_name, f"{self.collection_name}"
        )
        if task.task.type == "flyer":
            result = collection.find_one(
                {
                    "$and": [
                        {"task.store_name": task.task.store_name},
                        {"task.publication_id": task.task.publication_id},
                    ]
                }
            )
        elif task.task.type == "product":
            result = collection.find_one(
                {
                    "$and": [
                        {"task.store_name": task.task.store_name},
                        {"task.publication_id": task.task.publication_id},
                        {"task.url": task.task.url},
                    ]
                }
            )
        return result

    def start(self):
        while True:
            try:
                task = self.task_queue.pop()
                task = Task(task=task)
                # check weather task is existed
                if self.check_is_task_exist(task):
                    raise Exception("Task is existed")
                else:
                    collection = self._get_collection(
                        task.task.store_name, f"{self.collection_name}"
                    )
                    collection.insert_one(task.model_dump())
            except Exception as e:
                sleep(2)
                continue
