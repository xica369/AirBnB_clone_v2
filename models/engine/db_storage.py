#!/usr/bin/python3
"""This is the file DBStorage class for AirBnB"""
import json
import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

type_class = [User, State, City, Amenity, Place, Review]


class DBStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __engine = None
    __session = None

    def __init__(self):
        """method constructor of objects DBStorage
        Return:
            Nothing
        """

        s = 'mysql+mysqldb://{}:{}@{}/{}'.format(os.environ["HBNB_MYSQL_USER"],
                                                 os.environ["HBNB_MYSQL_PWD"],
                                                 os.environ["HBNB_MYSQL_HOST"],
                                                 os.environ["HBNB_MYSQL_DB"])
        self.__engine = create_engine(s, pool_pre_ping=True)

        try:
            if os.environ["HBNB_ENV"] == "test":
                Base.metadata.drop_all(bind=self.__engine)
        except KeyError:
            pass

    def all(self, cls=None):
        """that returns the list of objects of one type of class
        Return:
            returns a dictionary objects
        """
        objects_list = []
        dict_objects = {}

        if cls:
            objects_list = self.__session.query(eval(cls)).all()
        else:
            for name_class in type_class:
                objects_list.extend = self.__session.query(eval(name_class)).all()

        for obj in objects_list:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            dict_objects[key] = obj

        return dict_objects

    def new(self, obj):
        """add the object to the current database session
        Args:
            obj: given object
        """
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None
        Return:
            Nothing
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database and create the current database
        session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.close()
