# Lab 6: Code and Branch Coverage Analysis

## Student Details
- **Student Name:** Mithun Naik
- **SRN:** PES2UG24CS277
- **Course:** Software Engineering (UE24CS351A)
- **Repository (Fork):** [https://github.com/Mithun-48/L6_L7_31_coupon_validator](https://github.com/Mithun-48/L6_L7_31_coupon_validator)
- **Upstream Repository:** [https://github.com/SETAPESU26/L6_L7_31_coupon_validator](https://github.com/SETAPESU26/L6_L7_31_coupon_validator)
- **Branch:** `main`

---

## 1. Overview & Two-Commit Methodology
This lab analyzes the code and branch coverage of the `coupon_validator` module using `pytest` and `pytest-cov` (`coverage.py`).

The assignment is completed in **two distinct, verifiable commits**:
1. **Commit 1 (Code / Statement Coverage):** Focuses on executing all 32 executable lines of code in `coupon_validator.py`, achieving **100% statement coverage** with 13 tests.
2. **Commit 2 (Branch Coverage):** Extends the suite with 9 additional branch and boundary test cases (22 tests total) to evaluate all decision paths (True and False for every branch gate), achieving **100% branch coverage** (24/24 branches) alongside 100% statement coverage.

---

## 2. Coverage Metrics Comparison

| Metric | Baseline Starter | Commit 1 (Statement Coverage) | Commit 2 (Branch Coverage) | Overall Improvement |
|:---|:---:|:---:|:---:|:---:|
| **Total Tests** | 2 | 13 | **22** | **+20 tests** |
| **Statements Total** | 32 | 32 | **32** | — |
| **Statements Covered** | 9 | 32 | **32** | **+23** |
| **Statements Missed** | 23 | 0 | **0** | **-23** |
| **Statement Coverage %** | 28% | **100%** | **100%** | **+72%** |
| **Branch Decisions Total** | 24 | 24 | **24** | — |
| **Branch Decisions Covered** | 20 | 23 | **24** | **+4** |
| **Partial Branches Missed** | 4 | 1 | **0** | **-4** |
| **Total Coverage %** | **23%** | **98%** (1 partial branch) | **100%** (0 partial branches) | **+77%** |

---

## 3. Detailed Branch Analysis & Test Mapping

The `coupon_validator.py` module contains 3 primary functions. Every decision gate and boundary condition was analyzed and exercised across both commits:

### Function 1: `coupon_discount(code, cart_total, is_new_user, day)`

| Branch / Condition | Target Outcome | Stage | Test Function | Inputs / Condition | Expected Result |
|:---|:---|:---:|:---|:---|:---|
| `cart_total <= 0` | True (Boundary: 0) | Commit 1 | `test_coupon_discount_zero_cart_total` | `cart_total = 0` | Raises `ValueError("empty cart")` |
| `cart_total <= 0` | True (Negative) | Commit 2 | `test_coupon_discount_negative_cart_total` | `cart_total = -50` | Raises `ValueError("empty cart")` |
| `cart_total <= 0` | False | Commit 1 | Positive cart tests | `cart_total > 0` | Evaluates coupon code |
| `code == "WELCOME10"` | True (`is_new_user=True`) | Starter | `test_welcome_coupon_new_user` | `200`, `True`, `"mon"` | `20.0` (10% of 200) |
| `code == "WELCOME10"` | True (`is_new_user=False`) | Commit 1 | `test_welcome_coupon_existing_user` | `200`, `False`, `"mon"` | `0` |
| `code == "WELCOME10"` | False | Commit 1 | Other coupon tests | Other codes | Proceeds to next coupon |
| `code == "WEEKEND20"` | True (`day == "sat"`, `cart_total >= 500`) | Commit 1 | `test_weekend_coupon_saturday_large_cart` | `600`, `False`, `"sat"` | `120.0` (20% of 600) |
| `code == "WEEKEND20"` | True (`day == "sun"`, `cart_total == 500` boundary) | Commit 2 | `test_weekend_coupon_sunday_boundary_threshold` | `500`, `False`, `"sun"` | `100.0` (20% of 500) |
| `code == "WEEKEND20"` | True (`day == "sat"`, `cart_total < 500`) | Commit 1 | `test_weekend_coupon_saturday_small_cart` | `400`, `False`, `"sat"` | `50` (flat 50) |
| `code == "WEEKEND20"` | True (`day == "sun"`, `cart_total == 499` boundary) | Commit 2 | `test_weekend_coupon_sunday_small_cart` | `499`, `False`, `"sun"` | `50` (flat 50) |
| `code == "WEEKEND20"` | True (`day not in weekend`) | Commit 1 | `test_weekend_coupon_weekday` | `600`, `False`, `"fri"` / `"wed"` | `0` |
| `code == "WEEKEND20"` | False | Commit 1 | Other coupon tests | Other codes | Proceeds to next coupon |
| `code == "FLAT100"` | True (`cart_total > 300`) | Commit 1 | `test_flat100_coupon_above_threshold` | `301` / `500`, `"mon"` | `100` |
| `code == "FLAT100"` | True (`cart_total <= 300` boundary & below) | Commit 1 | `test_flat100_coupon_at_or_below_threshold` | `300` / `150`, `"mon"` | `0` |
| `code == "FLAT100"` | False | Commit 1 | Non-FLAT100 tests | Non-FLAT100 | Proceeds to fallback |
| Unrecognized coupon | Default fallthrough | Commit 1 | `test_unknown_or_invalid_coupon` | `"UNKNOWN"`, `""` | `0` |

### Function 2: `best_discount(codes, cart_total, is_new_user, day)`

| Branch / Condition | Target Outcome | Stage | Test Function | Inputs / Condition | Expected Result |
|:---|:---|:---:|:---|:---|:---|
| `for code in codes` | Empty list (loop bypassed) | Commit 2 | `test_best_discount_empty_codes` | `codes = []` | `0` |
| `value > best` | True (updates `best`) | Commit 1 | `test_best_discount_increasing_order` | `["WELCOME10", "FLAT100"]` | Updates `best` to `100` |
| `value > best` | False (does not update `best`) | Commit 2 | `test_best_discount_picks_highest_and_no_cap` | `["FLAT100", "WELCOME10"]` | `best` stays `100` |
| All discounts 0 | `best` remains 0 | Commit 2 | `test_best_discount_all_zero` | Ineligible coupons | `0` |
| `best > cap` (`cap = cart_total * 0.4`) | True (capped discount) | Commit 1 | `test_best_discount_exceeds_cap` | `["WEEKEND20"]`, `cart_total=100`, `"sat"` (best=50 > cap=40) | `40` |
| `best > cap` | False (within cap) | Commit 2 | `test_best_discount_picks_highest_and_no_cap` | `cart_total=400`, `best=100 <= cap=160` | `100` |

### Function 3: `is_expired(today, start, days_valid)`

| Branch / Condition | Target Outcome | Stage | Test Function | Inputs / Condition | Expected Result |
|:---|:---|:---:|:---|:---|:---|
| `days_valid <= 0` | True (`days_valid == 0`) | Starter | `test_zero_validity_expired` | `10, 5, 0` | `True` |
| `days_valid <= 0` | True (`days_valid < 0`) | Commit 2 | `test_is_expired_negative_days_valid` | `10, 5, -2` | `True` |
| `today - start > days_valid` | True (`today - start > days_valid`) | Commit 1 | `test_is_expired_past_validity` | `10, 2, 5` ($10-2 = 8 > 5$) | `True` (expired) |
| `today - start > days_valid` | False (Boundary: `today - start == days_valid`) | Commit 2 | `test_is_expired_exact_validity_boundary` | `10, 5, 5` ($10-5 = 5$, not $> 5$) | `False` (valid) |
| `today - start > days_valid` | False (Within validity: `today - start < days_valid`) | Commit 2 | `test_is_expired_within_validity` | `8, 5, 5` ($8-5 = 3 < 5$) | `False` (valid) |

---

## 4. Execution Commands

### Run Statement Coverage (Commit 1 Stage)
```bash
python -m pytest -v --cov=coupon_validator --cov-report=term-missing
```

### Run Full Statement and Branch Coverage (Commit 2 Stage)
```bash
python -m pytest -v --cov=coupon_validator --cov-branch --cov-report=term-missing --cov-report=html
```

---

## 5. Deliverables & Screenshots

### 1. Baseline Starter Coverage (23%)
![Initial Test Coverage](screenshots/01_initial_coverage.png)

### 2. Commit 1 Verification: Statement Code Coverage (100% Statements)
![Statement Coverage](screenshots/statement_coverage.png)

### 3. Commit 2 Verification: Final Branch Coverage (100% Statements, 100% Branches)
![Final Test Coverage](screenshots/02_final_coverage.png)

### 4. HTML Coverage Report Summary (100% Overall)
![HTML Coverage Report](screenshots/03_htmlcov_report.png)

### 5. Git Commit History & Remote Verification
![Git Verification](screenshots/04_git_verification.png)
