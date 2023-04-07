# -*- coding: utf-8 -*-


class AWSConfigFileNotExistError(Exception):
    pass


class AWSCredentialsFileNotExistError(Exception):
    pass


class MalformedConfigFileError(Exception):
    pass


class ProfileNotFoundError(Exception):
    pass
