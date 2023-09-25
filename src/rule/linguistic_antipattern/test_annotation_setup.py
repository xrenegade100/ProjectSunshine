from datetime import datetime

from typing_extensions import override
from src.common.enum import FileType, IdentifierType, LanguageType
from src.common.error_handler import ErrorSeverity, handle_error
from src.model.issue import Issue
from linguistic_antipattern import LinguisticAntipattern

# Impacted File: Test
# Impacted identifier: Method


class TestAnnotationSetup(LinguisticAntipattern):

    ID = 'X.1'
    ISSUE_CATEGORY = '\'Before\' annotation not in use'
    ISSUE_DESCRIPTION = 'Utilize the \'Before\' annotation for setup methods'

    def __init__(self):
        super.__init__()
        self.__junit = None

    def __get_junit_version(self):
        pass

    @override
    def __process_identifier(self, identifier):
        if self.__entity.language == LanguageType.Java and self.__junit is not None:
            if self.__junit >= 4:
                try:
                    if len(identifier.name_terms) == 1 and \
                            identifier.name_terms[0].lower() == 'setup' and \
                            'Before' not in identifier.annotations:
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
                    handle_error('X.1', error_message, ErrorSeverity.Error, False, e)

    @override
    def analyze(self, project, entity):
        if entity.file_type == FileType.Test:
            self.__project = project
            self.__junit = project.junit_version
            self.__entity = entity
            for class_item in self.__entity.classes:
                for method_item in class_item.methods:
                    self.__process_identifier(method_item)

        return self.__issues