.. _release_history:

Release and Version History
==============================================================================


Backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.1.2 (2024-01-21)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- ``python-Levenshtein`` is no longer mandatory dependencies.
- removed ``atomicwrites`` since it is not maintained anymore.
- add ``pathlib_mate`` as dependency to provide atomic write support.
- add color syntax highlight in CLI.


1.1.1 (2024-01-12)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add the following public API:
    - ``awscli_mate.api.T_PROFILE_REGION_PAIR``
    - ``awscli_mate.api.ProfileRegionPairFuzzyMatcher``
    - ``awscli_mate.api.sort_profile_region_pairs``
    - ``awscli_mate.api.get_sorted_profile_region_pairs``

**Minor Improvements**

- Refactor the UI module to make it more succinct and readable.


1.0.2 (2023-11-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Also display the aws account, alias, region information after "set default profile".
- Also display the aws account, alias, region information after "mfa auth".


1.0.1 (2023-10-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First API stable release.
- Release ``1.X.Y``.
- CLI features:
    - cli command ``awscli_mate``
    - set a profile as default
    - do MFA authentication using a base profile
- UI:
    - cli command ``awscli_mate_ui``
    - set a profile as default
    - do MFA authentication using a base profile
    - open sign in url in browser using a AWS profile
    - open switch role url in browser using a AWS profile
- Public API:
    - The import pattern now is ``import awscli_mate.api as awscli_mate``.
    - ``awscli_mate.api.__version__``
    - ``awscli_mate.api.strip_comment``
    - ``awscli_mate.api.AWSCliConfig``
    - ``awscli_mate.api.SectionTypeEnum``
    - ``awscli_mate.api.ConfigKeyEnum``
    - ``awscli_mate.api.CredentialKeyEnum``
    - ``awscli_mate.api.get_account_alias``
    - ``awscli_mate.api.get_sign_in_url``
    - ``awscli_mate.api.get_switch_role_url``

**Miscellaneous**

- Start using the ``zelfred`` package for the interactive UI.


0.4.1 (2023-10-12)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add the interactive CLI UI.


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
