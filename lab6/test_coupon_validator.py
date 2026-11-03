import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


# ---------------------------------------------------------------------------
# Starter Test Cases
# ---------------------------------------------------------------------------
def test_welcome_coupon_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_zero_validity_expired():
    assert is_expired(10, 5, 0) is True


# ---------------------------------------------------------------------------
# Statement Coverage Tests for coupon_discount()
# ---------------------------------------------------------------------------
def test_coupon_discount_zero_cart_total():
    """Executes Line 3: raise ValueError('empty cart')."""
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_welcome_coupon_existing_user():
    """Executes Line 7: return 0 for WELCOME10 existing user."""
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend_coupon_saturday_large_cart():
    """Executes Line 11: return cart_total * 0.20."""
    assert coupon_discount("WEEKEND20", 600, False, "sat") == 120.0


def test_weekend_coupon_saturday_small_cart():
    """Executes Line 12: return 50."""
    assert coupon_discount("WEEKEND20", 400, False, "sat") == 50


def test_weekend_coupon_weekday():
    """Executes Line 13: return 0."""
    assert coupon_discount("WEEKEND20", 600, False, "fri") == 0


def test_flat100_coupon_above_threshold():
    """Executes Line 16: return 100."""
    assert coupon_discount("FLAT100", 301, False, "mon") == 100


def test_flat100_coupon_at_or_below_threshold():
    """Executes Line 17: return 0."""
    assert coupon_discount("FLAT100", 300, False, "mon") == 0


def test_unknown_or_invalid_coupon():
    """Executes Line 18: return 0 (fallback)."""
    assert coupon_discount("UNKNOWN_CODE", 500, True, "sat") == 0


# ---------------------------------------------------------------------------
# Statement Coverage Tests for best_discount()
# ---------------------------------------------------------------------------
def test_best_discount_increasing_order():
    """Executes Lines 22-26 (loop, update best) and Line 30 (return best)."""
    assert best_discount(["WELCOME10", "FLAT100"], 500, True, "mon") == 100


def test_best_discount_exceeds_cap():
    """Executes Line 29: return cap."""
    assert best_discount(["WEEKEND20"], 100, False, "sat") == 40


# ---------------------------------------------------------------------------
# Statement Coverage Tests for is_expired()
# ---------------------------------------------------------------------------
def test_is_expired_past_validity():
    """Executes Line 36: return today - start > days_valid (evaluates to True)."""
    assert is_expired(10, 2, 5) is True
