from services.super_services import SuperServices
from repository.basedb import BaseDB
from bson.objectid import ObjectId


class UserServices(BaseDB, SuperServices):

    def __init__(self):
        self.collection = self.db["users"]
        self.id_keys = ["_id"]

    def check_password(self, user, password):
        return True if user["password"] == password else False

    def format_document(self, documents, input=True):
        convert = ObjectId if input else str

        [[document.update({key: convert(value)}) for key,
          value in document.items() if key in self.id_keys] for document in documents]
        return documents

    def lookup(self, documents):
        return documents

    def find_by(self, filter):
        filter = self.format_document([filter]).pop()
        document = self.collection.find_one(filter)

        document = self.format_document([document], input=False).pop()
        return document

    def find_all(self):
        pass

    def save(self, document):
        self.collection.insert_one(document.dict())
