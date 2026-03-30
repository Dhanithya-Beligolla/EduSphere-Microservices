"""
Pagination helpers.
"""

import math


def calc_skip(page: int, page_size: int) -> int:
    """Calculate MongoDB skip value from page number."""
    return (page - 1) * page_size


def calc_total_pages(total_count: int, page_size: int) -> int:
    """Calculate total number of pages."""
    if total_count == 0:
        return 0
    return math.ceil(total_count / page_size)
