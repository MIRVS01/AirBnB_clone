#!/usr/bin/python3
"""
Contains the FileStorage class model


"""
import json
from json import JSONEncoder, JSONDecoder
import os

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review


class FileStorage:
    """
    serializes instances to a JSON file and
    deserializes JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary __objects
        """
        return self.__objects

    def new(self, obj):
        """
        sets in __objects the `obj` with key <obj class name>.id
        """
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj
        # -> I think this structure is incorrect
        # self.__objects.update({"{}.{}".format(obj.__class__.__name__,
        #                                              obj.id): obj})

    def save(self):
        """
        Serialize __objects to the JSON file
        """
        with open(self.__file_path, mode="w") as f:
            dict_storage = {}
            for k, v in self.__objects.items():
                dict_storage[k] = v.to_dict()
            json.dump(dict_storage, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects
        -> Only IF it exists!
        """
        # try:
        #     with open(self.__file_path, encoding="utf-8") as f:
        #         for obj in json.load(f).values():
        #             self.new(eval(obj["__class__"])(**obj))
        # except FileNotFoundError:
        #     pass
        if os.path.isfile(self.__file_path):
            file_lines = []
            with open(self.__file_path, mode='r') as file:
                file_lines = file.readlines()
            file_txt = ''.join(file_lines) if len(file_lines) > 0 else '{}'
            json_objs = JSONDecoder().decode(file_txt)
            base_model_objs = dict()
            classes = self.model_classes
            for key, value in json_objs.items():
                cls_name = value['__class__']
                if cls_name in classes.keys():
                    base_model_objs[key] = classes[cls_name](**value)
            self.__objects = base_model_objs
