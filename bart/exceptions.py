# project exceptions
class NotInProjectException(Exception):
    pass

class MissingProjectRootException(Exception):
    pass

class ProjectDirExistsException(Exception):
    pass

class ReorderingException(Exception):
    pass


# document exceptions
class ProjectFileExistsException(Exception):
    pass

class DocumentLevelException(Exception):
    pass

class MarkupNotAllowedException(Exception):
    pass
