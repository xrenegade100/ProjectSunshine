from datetime import datetime

from app.common.enum import IdentifierType
from app.common.error_handler import handle_error, ErrorSeverity
from app.common.util_parsing import get_all_return_statements
from app.model.issue import Issue
from app.nlp import term_list


class GetNoReturn:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'B.3'
        self.__issues = []
        self.__issue_category = '\'Get\' method does not return'
        self.__issue_description = 'The name suggests that the method returns something (e.g., name starts with \'get\' or \'return\').'

    def __process_identifier(self, identifier):
        # AntiPattern: The name starts with a get term, but there are no return statements
        try:
            if identifier.name_terms[0].lower() in term_list.get_get_terms(self.__project):
                return_statements = get_all_return_statements(identifier.source)

                if len(return_statements) == 0:
                    issue = Issue()
                    issue.file_path = self.__entity.path
                    issue.identifier = identifier.get_fully_qualified_name()
                    issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                    issue.category = self.__issue_category
                    issue.details = self.__issue_description
                    issue.id = self.__id
                    issue.analysis_datetime = datetime.now()
                    issue.file_type = self.__entity.file_type
                    issue.line_number = identifier.line_number
                    issue.column_number = identifier.column_number
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('B.3', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
