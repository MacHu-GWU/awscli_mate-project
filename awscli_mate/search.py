# -*- coding: utf-8 -*-

import typing as T

from .vendor.better_fuzzywuzzy import FuzzyMatcher

from .awscli import T_PROFILE_REGION_PAIR, AWSCliConfig


class ProfileRegionPairFuzzyMatcher(FuzzyMatcher[T_PROFILE_REGION_PAIR]):
    def get_name(self, item: T_PROFILE_REGION_PAIR) -> T.Optional[str]:
        return item[0]


def sort_profile_region_pairs(
    pairs: T.List[T_PROFILE_REGION_PAIR],
    query: str,
) -> T.List[T_PROFILE_REGION_PAIR]:
    """
    Sort the profile-region pairs by the query based on similarity

    :param pairs: a list of (profile, region) pairs
    :param query: the query used for similarity comparison

    :return: a list of (profile, region) pairs
    """
    if len(query):
        matcher = ProfileRegionPairFuzzyMatcher.from_items(pairs)
        return matcher.match(query, threshold=0, limit=99)
    else:
        return pairs


def get_sorted_profile_region_pairs(
    query: str,
) -> T.List[T_PROFILE_REGION_PAIR]:
    """
    Get profile-region pairs from ``~/.aws/config``, sorted by the query
    based on similarity

    :param query: the query used for similarity comparison

    :return: a list of (profile, region) pairs
    """
    pairs = AWSCliConfig().extract_profile_and_region_pairs()
    return sort_profile_region_pairs(pairs, query=query)
