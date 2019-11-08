"""
Model class for MyTardis API v1's StorageBoxResource.
"""
from ..utils import UnderscoreToCamelcase


class StorageBox():
    """
    Model class for MyTardis API v1's StorageBoxResource.
    """
    def __init__(self, storageBoxJson):
        self.json = storageBoxJson
        self.storageBoxId = None
        self.djangoStorageClass = None
        self.maxSize = None
        self.status = None
        self.name = None
        self.description = None
        self.masterBox = None
        self.options = []
        self.attributes = []
        if storageBoxJson is not None:
            for key in storageBoxJson:
                attr = UnderscoreToCamelcase(key)
                if attr == "id":
                    attr = "storageBoxId"
                if hasattr(self, attr):
                    self.__dict__[attr] = storageBoxJson[key]
            self.options = []
            for optionJson in storageBoxJson['options']:
                self.options.append(StorageBoxOption(optionJson=optionJson))
            self.attributes = []
            for attrJson in storageBoxJson['attributes']:
                self.attributes.append(StorageBoxAttribute(attrJson=attrJson))


class StorageBoxOption():
    """
    Model class for MyTardis API v1's StorageBoxOptionResource.
    """
    def __init__(self, optionJson):
        self.json = optionJson
        self.storageBoxOptionId = None
        self.key = None
        self.value = None
        if optionJson is not None:
            for key in optionJson:
                attr = UnderscoreToCamelcase(key)
                if attr == "id":
                    attr = "storageBoxOptionId"
                if hasattr(self, attr):
                    self.__dict__[attr] = optionJson[key]


class StorageBoxAttribute():
    """
    Model class for MyTardis API v1's StorageBoxAttributeResource.
    """
    def __init__(self, attrJson):
        self.json = attrJson
        self.storageBoxAttributeId = None
        self.key = None
        self.value = None
        if attrJson is not None:
            for key in attrJson:
                attr = UnderscoreToCamelcase(key)
                if attr == "id":
                    attr = "storageBoxAttributeId"
                if hasattr(self, attr):
                    self.__dict__[attr] = attrJson[key]
