
.. image:: https://readthedocs.org/projects/awscli_mate/badge/?version=latest
    :target: https://awscli_mate.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/awscli_mate-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/awscli_mate-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/awscli_mate-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/awscli_mate-project

.. image:: https://img.shields.io/pypi/v/awscli_mate.svg
    :target: https://pypi.python.org/pypi/awscli_mate

.. image:: https://img.shields.io/pypi/l/awscli_mate.svg
    :target: https://pypi.python.org/pypi/awscli_mate

.. image:: https://img.shields.io/pypi/pyversions/awscli_mate.svg
    :target: https://pypi.python.org/pypi/awscli_mate

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/awscli_mate-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://awscli_mate.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://awscli_mate.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
    :target: https://awscli_mate.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/awscli_mate-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/awscli_mate-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/awscli_mate-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/awscli_mate#files


Welcome to ``awscli_mate`` Documentation
==============================================================================
``awscli_mate`` improves the original AWS CLI.

Make sure you have done::

    pip install awscli_mate
    pip install boto3
    pip install fire


Set AWS Profile as Default
------------------------------------------------------------------------------
Example:

.. code-block:: python

    awscli_mate set_profile_as_default --profile=your_profile


One Click MFA auth
------------------------------------------------------------------------------
Example:

.. code-block:: python

    awscli_mate mfa_auth --profile=your_profile --mfa_code=123456 --hours=12 --overwrite_default=True

Note that this command also automatically set the MFA profile as default profile.


.. _install:

Install
------------------------------------------------------------------------------

``awscli_mate`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install awscli_mate

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade awscli_mate
