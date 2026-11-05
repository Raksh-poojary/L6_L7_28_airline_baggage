
import pytest

from airline_baggage import (
    baggage_fee,
    carry_on_ok,
    check_in_status
)


# --------------------------------------------------
# 1. BAGGAGE FEE TESTS
# --------------------------------------------------

def test_invalid_cabin():
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee("first", 20, "domestic", False)


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", -5, "domestic", False)


def test_member_economy_allowance():
    # Economy allowance = 15 + 10 for members
    assert baggage_fee("economy", 25, "domestic", True) == 0


def test_business_member_no_extra_allowance():
    # Business members do not receive the additional 10 kg
    assert baggage_fee("business", 41, "domestic", True) == 20


def test_within_allowance():
    assert baggage_fee("economy", 10, "domestic", False) == 0


def test_domestic_excess_fee():
    # Excess = 30 - 15 = 15; fee = 15 * 20
    assert baggage_fee("economy", 30, "domestic", False) == 300


def test_international_excess_fee():
    # Excess = 30 - 15 = 15; fee = 15 * 45
    assert baggage_fee("economy", 30, "international", False) == 675


def test_domestic_excess_above_20():
    # Excess = 40 - 15 = 25; doubled rate = 40
    assert baggage_fee("economy", 40, "domestic", False) == 1000


def test_international_excess_above_20():
    # Excess = 40 - 15 = 25
    # Doubled rate = 90; international surcharge = 10
    assert baggage_fee("economy", 40, "international", False) == 2500


# --------------------------------------------------
# 2. CARRY-ON TESTS
# --------------------------------------------------

def test_infant_with_two_items():
    assert carry_on_ok(10, 2, True) is True


def test_infant_with_more_than_two_items():
    assert carry_on_ok(10, 3, True) is False


def test_non_infant_within_weight_and_item_limit():
    assert carry_on_ok(7, 1, False) is True


def test_non_infant_over_weight_limit():
    assert carry_on_ok(8, 1, False) is False


def test_non_infant_multiple_items():
    assert carry_on_ok(5, 2, False) is False


# --------------------------------------------------
# 3. CHECK-IN STATUS TESTS
# --------------------------------------------------

def test_checkin_open_with_baggage():
    assert check_in_status(60, True, False) == "open"


def test_checkin_late_with_baggage():
    assert check_in_status(50, True, False) == "late"


def test_checkin_closed_with_baggage():
    assert check_in_status(40, True, False) == "closed"


def test_checkin_open_without_baggage():
    assert check_in_status(45, False, False) == "open"


def test_checkin_late_without_baggage():
    assert check_in_status(35, False, False) == "late"


def test_checkin_closed_without_baggage():
    assert check_in_status(20, False, False) == "closed"


def test_checkin_open_international():
    assert check_in_status(120, True, True) == "open"


def test_checkin_late_international():
    assert check_in_status(110, True, True) == "late"


def test_checkin_closed_international():
    assert check_in_status(90, True, True) == "closed"
