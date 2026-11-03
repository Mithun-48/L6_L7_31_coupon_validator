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
# Tests for coupon_discount()
# ---------------------------------------------------------------------------
def test_coupon_discount_zero_cart_total():
    """Branch: cart_total <= 0 raises ValueError (boundary at 0)."""
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_coupon_discount_negative_cart_total():
    """Branch: cart_total <= 0 raises ValueError (strictly negative)."""
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", -50, True, "mon")


def test_welcome_coupon_existing_user():
    """Branch: WELCOME10 with is_new_user=False returns 0."""
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend_coupon_saturday_large_cart():
    """Branch: WEEKEND20 on 'sat' with cart_total >= 500 returns 20% discount."""
    assert coupon_discount("WEEKEND20", 600, False, "sat") == 120.0


def test_weekend_coupon_sunday_boundary_threshold():
    """Branch: WEEKEND20 on 'sun' with cart_total == 500 returns 20% discount."""
    assert coupon_discount("WEEKEND20", 500, False, "sun") == 100.0


def test_weekend_coupon_saturday_small_cart():
    """Branch: WEEKEND20 on 'sat' with cart_total < 500 returns flat 50."""
    assert coupon_discount("WEEKEND20", 400, False, "sat") == 50


def test_weekend_coupon_sunday_small_cart():
    """Branch: WEEKEND20 on 'sun' with cart_total < 500 returns flat 50 (boundary at 499)."""
    assert coupon_discount("WEEKEND20", 499, False, "sun") == 50


def test_weekend_coupon_weekday():
    """Branch: WEEKEND20 on a non-weekend day ('fri' / 'mon') returns 0."""
    assert coupon_discount("WEEKEND20", 600, False, "fri") == 0
    assert coupon_discount("WEEKEND20", 300, True, "wed") == 0


def test_flat100_coupon_above_threshold():
    """Branch: FLAT100 with cart_total > 300 returns flat 100."""
    assert coupon_discount("FLAT100", 301, False, "mon") == 100
    assert coupon_discount("FLAT100", 500, False, "tue") == 100


def test_flat100_coupon_at_or_below_threshold():
    """Branch: FLAT100 with cart_total <= 300 returns 0 (boundary at 300, and below)."""
    assert coupon_discount("FLAT100", 300, False, "mon") == 0
    assert coupon_discount("FLAT100", 150, False, "mon") == 0


def test_unknown_or_invalid_coupon():
    """Branch: Unknown coupon code falls through to default return 0."""
    assert coupon_discount("UNKNOWN_CODE", 500, True, "sat") == 0
    assert coupon_discount("", 200, False, "mon") == 0


# ---------------------------------------------------------------------------
# Tests for best_discount()
# ---------------------------------------------------------------------------
def test_best_discount_empty_codes():
    """Branch: Empty codes list returns 0 (loop not entered)."""
    assert best_discount([], 500, True, "sat") == 0


def test_best_discount_picks_highest_and_no_cap():
    """
    Branch: Multiple coupons tested where value > best updates best,
    and subsequent lower value does not update best.
    best <= cap returns best.
    """
    # FLAT100 gives 100, WELCOME10 gives 40 -> best is 100.
    # Cap = 400 * 0.4 = 160. Since 100 <= 160, returns 100.
    assert best_discount(["FLAT100", "WELCOME10"], 400, True, "mon") == 100


def test_best_discount_increasing_order():
    """Branch: Multiple coupons where value increases with each coupon."""
    # WELCOME10 gives 40, FLAT100 gives 100 -> best updates 0 -> 40 -> 100.
    # Cap = 500 * 0.4 = 200. Returns 100.
    assert best_discount(["WELCOME10", "FLAT100"], 500, True, "mon") == 100


def test_best_discount_all_zero():
    """Branch: All coupons return 0, best remains 0."""
    assert best_discount(["WELCOME10", "WEEKEND20"], 200, False, "mon") == 0


def test_best_discount_exceeds_cap():
    """
    Branch: best > cap returns cap.
    cart_total = 100, WEEKEND20 on 'sat' gives flat 50.
    Cap = 100 * 0.4 = 40. Since 50 > 40, returns 40.
    """
    assert best_discount(["WEEKEND20"], 100, False, "sat") == 40


# ---------------------------------------------------------------------------
# Tests for is_expired()
# ---------------------------------------------------------------------------
def test_is_expired_negative_days_valid():
    """Branch: days_valid <= 0 returns True (strictly negative validity)."""
    assert is_expired(10, 5, -2) is True


def test_is_expired_past_validity():
    """Branch: today - start > days_valid evaluates to True."""
    # 10 - 2 = 8 > 5 -> expired
    assert is_expired(10, 2, 5) is True


def test_is_expired_exact_validity_boundary():
    """Branch: today - start > days_valid evaluates to False (on boundary: today - start == days_valid)."""
    # 10 - 5 = 5, 5 > 5 is False -> still valid on the last day
    assert is_expired(10, 5, 5) is False


def test_is_expired_within_validity():
    """Branch: today - start > days_valid evaluates to False (well within validity)."""
    # 8 - 5 = 3 <= 5 -> not expired
    assert is_expired(8, 5, 5) is False
