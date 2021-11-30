from repository.basedb import BaseDB
from services.super_services import SuperServices
from services.user import UserServices
from bson.objectid import ObjectId


class QuestionServices(BaseDB, SuperServices):

    def __init__(self):
        self.collection = self.db["questions"]
        self.id_keys = ["_id", "published_by"]

    def __in(self, documents):
        [[document.update({key: ObjectId(value)}) for key, value in document.items(
        ) if key in self.id_keys] for document in documents]

        return documents

    def __out(self, documents):
        [document.update({"_id": str(document["_id"])})
         for document in documents]

        return documents

    def format_document(self, documents, input=True):
        documents = self.__in(documents) if input else self.__out(documents)

        return documents

    def lookup(self, documents):
        user_services = UserServices()

        [document.update({"published_by": user_services.find_by(
            filter={"_id": document["published_by"]})}) for document in documents]

        return documents

    def find_by(self, filter):
        filter = self.format_document([filter]).pop()

        document = self.collection.find_one(filter)
        document = self.lookup([document])
        document = self.format_document([document], input=False).pop()

        return document

    def find_all(self):
        documents = list(self.collection.find())
        documents = self.lookup(documents)

        for document in documents:
            del document["published_by"]["password"]

        documents = self.format_document(documents, input=False)
        return documents

    def save(self, question):
        question = self.format_document([question.dict()]).pop()
        self.collection.insert_one(question)
