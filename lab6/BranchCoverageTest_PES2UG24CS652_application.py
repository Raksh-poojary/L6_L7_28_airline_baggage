
import pytest

from airline_baggage import (
    baggage_fee,
    carry_on_ok,
    check_in_status
)


# --------------------------------------------------
# BAGGAGE FEE — BRANCH TESTS
# --------------------------------------------------

def test_member_non_business():
    assert baggage_fee("economy", 25, "domestic", True) == 0


def test_non_member():
    assert baggage_fee("economy", 20, "domestic", False) == 100


def test_business_member():
    assert baggage_fee("business", 45, "domestic", True) == 100


def test_business_non_member():
    assert baggage_fee("business", 45, "domestic", False) == 100


def test_excess_exactly_20():
    # Economy allowance 15; excess exactly 20
    assert baggage_fee("economy", 35, "domestic", False) == 400


def test_excess_greater_than_20_domestic():
    assert baggage_fee("economy", 36, "domestic", False) == 840


def test_excess_greater_than_20_international():
    assert baggage_fee("economy", 36, "international", False) == 2100


def test_small_international_excess():
    assert baggage_fee("economy", 20, "international", False) == 225

def test_invalid_cabin():
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee("first", 20, "domestic", False)

def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", -5, "domestic", False)

# --------------------------------------------------
# CARRY-ON — BRANCH TESTS
# --------------------------------------------------

def test_infant_allowed():
    assert carry_on_ok(10, 2, True) is True


def test_infant_not_allowed():
    assert carry_on_ok(10, 3, True) is False


def test_non_infant_weight_exactly_7():
    assert carry_on_ok(7, 1, False) is True


def test_non_infant_weight_above_7():
    assert carry_on_ok(7.1, 1, False) is False


def test_non_infant_items_exactly_one():
    assert carry_on_ok(5, 1, False) is True


def test_non_infant_items_above_one():
    assert carry_on_ok(5, 2, False) is False


# --------------------------------------------------
# CHECK-IN — BRANCH TESTS
# --------------------------------------------------

def test_domestic_with_baggage_at_cutoff():
    assert check_in_status(60, True, False) == "open"


def test_domestic_with_baggage_late_boundary():
    assert check_in_status(45, True, False) == "late"


def test_domestic_with_baggage_closed():
    assert check_in_status(44, True, False) == "closed"


def test_domestic_without_baggage_at_cutoff():
    assert check_in_status(45, False, False) == "open"


def test_domestic_without_baggage_late_boundary():
    assert check_in_status(30, False, False) == "late"


def test_domestic_without_baggage_closed():
    assert check_in_status(29, False, False) == "closed"


def test_international_with_baggage():
    assert check_in_status(120, True, True) == "open"


def test_international_without_baggage():
    assert check_in_status(105, False, True) == "open"


def test_international_late():
    assert check_in_status(110, True, True) == "late"


def test_international_closed():
    assert check_in_status(90, True, True) == "closed"
