.. _release_history:

Release and Version History
==============================================================================


Backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.3.2 (2023-04-12)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- add return value to :meth:`awscli_mate.awscli.AWSCliConfig.set_profile_as_default`.
- add return value to :meth:`awscli_mate.awscli.AWSCliConfig.mfa_auth`.

**Miscellaneous**

- add an example jupyter notebook


0.3.1 (2023-04-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``SectionTypeEnum``, ``ConfigKeyEnum``, ``CredentialKeyEnum`` to public API.

**Minor Improvements**

- use automic write to write config / credentials file

**Miscellaneous**

- add lots of unit test for edge cases.
- reach 100% coverage test.
- add more doc string.



0.2.1 (2023-04-05)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``awscli_mate`` CLI interface.


0.1.1 (2023-04-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add :class:`awscli_mate.awscli.AWSCliConfig` to public API. It provides awscli enhancement utilities.
- add :meth:`awscli_mate.awscli.AWSCliConfig.set_profile_as_default`.
- add :meth:`awscli_mate.awscli.AWSCliConfig.mfa_auth`.

**Miscellaneous**

- First release
