# -*- coding: utf-8 -*-

from awscli_mate.awscli import AWSCliConfig
from awscli_mate.search import sort_profile_region_pairs


def test_sort_profile_region_pairs(awscli_config: AWSCliConfig):
    pairs = awscli_config.extract_profile_and_region_pairs()
    sorted_pairs = sort_profile_region_pairs(pairs, "p3")
    assert sorted_pairs[0][0] == "p3"
    sorted_pairs = sort_profile_region_pairs(pairs, "")
    assert sorted_pairs[0][0] == "p1"


if __name__ == "__main__":
    from awscli_mate.tests import run_cov_test

    run_cov_test(__file__, "awscli_mate.search", preview=False)
