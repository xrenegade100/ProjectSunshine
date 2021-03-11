from datetime import datetime

from model.identifier_type import IdentifierType
from model.issue import Issue


class SetReturns:

    def __init__(self):
        self.__entity = None
        self.__id = 'A.3'
        self.__issues = []
        self.__issue_category = '\'Set\' method returns'
        self.__issue_description = 'A set method having a return type different than \'void\'.'

    def __process_identifier(self, identifier):

        if identifier.name_terms[0].lower() == 'set':
            if identifier.return_type != 'void':
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.Method
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.analysis_datetime = datetime.now()
                self.__issues.append(issue)

    def analyze(self, entity):
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues