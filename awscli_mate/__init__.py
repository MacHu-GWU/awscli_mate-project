# -*- coding: utf-8 -*-

"""
AWS CLI improvement.
"""


from ._version import __version__

__short_description__ = "AWS CLI improvement."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .api import (
        AWSCliConfig,
    )
except ImportError as e:  # pragma: no cover
    print(e)

try:  # pragma: no cover
    from .cli import main
except ImportError:  # pragma: no cover

    def main():
        raise ImportError("Please do 'pip install fire' before using CLI!")
