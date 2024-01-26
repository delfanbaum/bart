# project exceptions
class NotInProjectException(Exception):
    pass

class MissingProjectRootException(Exception):
    pass

class ProjectDirExistsException(Exception):
    pass


# document exceptions
class ProjectFileExistsException(Exception):
    pass

class DocumentLevelException(Exception):
    pass
