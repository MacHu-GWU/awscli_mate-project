
.. .. image:: https://readthedocs.org/projects/awscli_mate/badge/?version=latest
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


.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://awscli_mate.readthedocs.io/index.html

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://awscli_mate.readthedocs.io/py-modindex.html

.. .. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
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
It is very common that you wants to set a profile as the default when using a tools that doesn't support explicit ``--profile ...`` argument. ``awscli_mate`` provides a command to do this for you. It will update your ``.aws/config`` and ``.aws/credentials`` file and set the ``default`` profile to the one you specified.

Example:

.. code-block:: python

    awscli_mate set_profile_as_default --profile=your_profile


One Click MFA auth
------------------------------------------------------------------------------
Based on this `AWS re:Post How do I use an MFA token to authenticate access to my AWS resources through the AWS CLI? <https://repost.aws/knowledge-center/authenticate-mfa-cli>`_, you have to run ``aws sts get-session-token ...`` command to get some token, and manually copy and paste them to either environment variable or ``.aws/credentials`` file. This is a bit tedious. ``awscli_mate`` provides a one-click command to do this for you. Basically, it will use a base profile to get the token, let's say it is ``your_profile``, and automatically create / update a new profile called ``your_profile_mfa`` in your ``.aws/config`` and ``.aws/credentials`` file. So you can keep using the ``your_profile_mfa`` in your application.

Example:

.. code-block:: python

    awscli_mate mfa_auth --profile=your_profile --mfa_code=123456 --hours=12 --overwrite_default=True

Note that this command also automatically set the MFA profile as default profile. If you don't want to set the ``your_profile_mfa`` as default profile automatically, you can just remove the ``--overwrite_default`` part.


Use ``awscli_mate`` as a Python Library
------------------------------------------------------------------------------
See `example <./example.ipynb>`_.


Use ``awscli_mate`` as a Interactive CLI
------------------------------------------------------------------------------
**Set named AWS Profile as default**

.. image:: https://github.com/MacHu-GWU/awscli_mate-project/assets/6800411/c031a52a-2b4e-4dde-85f1-ab558aa1644f

**Do MFA Authentication**

.. image:: https://github.com/MacHu-GWU/awscli_mate-project/assets/6800411/5cc9ddef-18a5-4d76-942f-4be1e97601aa

**Keyboard shortcuts**:

- hit Ctrl + E or UP to move item selection up.
- hit Ctrl + R to scroll item selection up.
- hit Ctrl + D or DOWN to move item selection up.
- hit Ctrl + F to scroll item selection up.
- hit Ctrl + H or LEFT to move query input cursor to the left (this won't work on Windows).
- hit Ctrl + L or RIGHT to move query input cursor to the right.
- hit Ctrl + G to move query input cursor to the previous word.
- hit Ctrl + K to move query input cursor to the next word.
- hit Ctrl + X to clear the query input.
- hit Tab to auto-complete.
- hit BACKSPACE to delete query input backward.
- hit DELETE to delete query input forward.
- hit Enter to run it.


.. _install:

Install
------------------------------------------------------------------------------

``awscli_mate`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install awscli_mate

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade awscli_mate
