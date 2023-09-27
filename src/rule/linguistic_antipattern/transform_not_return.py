from src.common.enum import IdentifierType
from src.common.error_handler import ErrorSeverity, handle_error
from src.common.util_parsing import is_test_method
from src.model.issue import Issue
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern

# Impacted identifier: All
# Impacted identifier: Method
from src.nlp import term_list


class TransformNotReturn(LinguisticAntipattern):

    ID = 'B.5'
    ISSUE_CATEGORY = 'Transform method does not return'
    ISSUE_DESCRIPTION = 'The name of a method suggests the transformation of an object but there is no return value.'

    def __init__(self):
        super.__init__()

    #Override
    def __process_identifier(self, identifier):
        # AntiPattern: The name starts with or inner term contains transformation term and return type is void
        try:
            if not is_test_method(self.__project, self.__entity, identifier):
                inner_terms = [x.lower() for x in identifier.name_terms[1:-1]]
                if (identifier.name_terms[0].lower() in term_list.get_transform_terms_staring(self.__project) or
                    any(item in inner_terms for item in term_list.get_transform_terms_inner(self.__project))) \
                        and identifier.return_type == 'void':
                    issue = Issue(self, identifier)
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('B.5', error_message, ErrorSeverity.Error, False, e)
