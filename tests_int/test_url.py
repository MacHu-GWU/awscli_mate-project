# -*- coding: utf-8 -*-

from awscli_mate.url import get_sign_in_url, get_switch_role_url

print(get_sign_in_url(profile="bmt_app_dev_us_east_1"))
print(get_switch_role_url(profile="bmt_app_dev_us_east_1_assume_role"))
