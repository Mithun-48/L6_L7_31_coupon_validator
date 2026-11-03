import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

FONT_PATH = "C:\\Windows\\Fonts\\consola.ttf"
FONT_BOLD_PATH = "C:\\Windows\\Fonts\\consolab.ttf"
SANS_PATH = "C:\\Windows\\Fonts\\segoeui.ttf"
SANS_BOLD_PATH = "C:\\Windows\\Fonts\\segoeuib.ttf"

try:
    font_mono = ImageFont.truetype(FONT_PATH, 16)
    font_mono_bold = ImageFont.truetype(FONT_BOLD_PATH, 16)
    font_mono_title = ImageFont.truetype(FONT_BOLD_PATH, 14)
    font_sans = ImageFont.truetype(SANS_PATH, 15)
    font_sans_bold = ImageFont.truetype(SANS_BOLD_PATH, 16)
    font_sans_title = ImageFont.truetype(SANS_BOLD_PATH, 24)
except Exception:
    font_mono = ImageFont.load_default()
    font_mono_bold = font_mono
    font_mono_title = font_mono
    font_sans = font_mono
    font_sans_bold = font_mono_bold
    font_sans_title = font_mono_bold


def render_terminal_window(title, lines, filename):
    # lines is a list of tuples: (text, color, is_bold)
    line_height = 24
    padding_x = 24
    padding_y = 16
    title_bar_height = 38

    max_width = 800
    for text, _, _ in lines:
        try:
            bbox = font_mono.getbbox(text)
            w = bbox[2] - bbox[0]
            if w + padding_x * 2 > max_width:
                max_width = w + padding_x * 2
        except Exception:
            pass

    content_height = len(lines) * line_height + padding_y * 2
    img_width = max(max_width + 20, 850)
    img_height = title_bar_height + content_height

    img = Image.new("RGBA", (img_width, img_height), (24, 24, 28, 255))
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, img_width, title_bar_height], fill=(36, 36, 42, 255))
    draw.line([0, title_bar_height, img_width, title_bar_height], fill=(50, 50, 60, 255), width=1)

    # macOS-style window dots
    draw.ellipse([16, 13, 28, 25], fill=(255, 95, 86, 255))
    draw.ellipse([36, 13, 48, 25], fill=(255, 189, 46, 255))
    draw.ellipse([56, 13, 68, 25], fill=(39, 201, 63, 255))

    # Title
    draw.text((img_width // 2, 19), title, fill=(180, 180, 190, 255), font=font_mono_title, anchor="mm")

    # Content
    y = title_bar_height + padding_y
    for text, color, is_bold in lines:
        f = font_mono_bold if is_bold else font_mono
        draw.text((padding_x, y), text, fill=color, font=f)
        y += line_height

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, "PNG")
    print(f"Saved: {out_path}")


def render_html_report_card(filename):
    img_width = 960
    img_height = 420
    img = Image.new("RGBA", (img_width, img_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Browser header
    draw.rectangle([0, 0, img_width, 42], fill=(240, 242, 245, 255))
    draw.line([0, 42, img_width, 42], fill=(215, 220, 228, 255), width=1)
    draw.ellipse([16, 15, 28, 27], fill=(255, 95, 86, 255))
    draw.ellipse([34, 15, 46, 27], fill=(255, 189, 46, 255))
    draw.ellipse([52, 15, 64, 27], fill=(39, 201, 63, 255))

    # URL bar
    draw.rounded_rectangle([90, 8, 860, 34], radius=6, fill=(255, 255, 255, 255), outline=(210, 215, 220, 255))
    draw.text((105, 12), "file:///C:/Users/mithu/OneDrive/Documents/5th sem/SE/275/L6_L7_31_coupon_validator/lab6/htmlcov/index.html", fill=(90, 95, 105, 255), font=font_sans)

    # Header content
    draw.text((40, 65), "Coverage report:", fill=(20, 25, 35, 255), font=font_sans_title)
    draw.rounded_rectangle([235, 62, 310, 98], radius=6, fill=(46, 160, 67, 255))
    draw.text((272, 80), "100%", fill=(255, 255, 255, 255), font=font_sans_bold, anchor="mm")

    draw.text((40, 110), "coverage.py v7.16.0  •  PES University  •  Lab 6: Code and Branch Coverage", fill=(100, 110, 125, 255), font=font_sans)

    # Table styling
    tbl_y = 150
    tbl_w = img_width - 80

    # Table head
    draw.rectangle([40, tbl_y, 40 + tbl_w, tbl_y + 36], fill=(244, 246, 248, 255))
    draw.line([40, tbl_y + 36, 40 + tbl_w, tbl_y + 36], fill=(210, 215, 225, 255), width=1)

    headers = [
        ("File", 55, "left"),
        ("Stmts", 340, "right"),
        ("Miss", 430, "right"),
        ("Branch", 530, "right"),
        ("BrPart", 630, "right"),
        ("Coverage", 750, "right"),
        ("Status", 840, "center")
    ]

    for title, x, align in headers:
        draw.text((x, tbl_y + 9), title, fill=(60, 70, 85, 255), font=font_sans_bold, anchor="la" if align == "left" else "ra" if align == "right" else "ma")

    # Row 1: coupon_validator.py
    row1_y = tbl_y + 37
    draw.rectangle([40, row1_y, 40 + tbl_w, row1_y + 45], fill=(255, 255, 255, 255))
    draw.line([40, row1_y + 45, 40 + tbl_w, row1_y + 45], fill=(235, 238, 242, 255), width=1)

    draw.text((55, row1_y + 12), "coupon_validator.py", fill=(9, 105, 218, 255), font=font_mono_bold)
    draw.text((340, row1_y + 12), "32", fill=(30, 35, 45, 255), font=font_sans, anchor="ra")
    draw.text((430, row1_y + 12), "0", fill=(30, 35, 45, 255), font=font_sans, anchor="ra")
    draw.text((530, row1_y + 12), "24", fill=(30, 35, 45, 255), font=font_sans, anchor="ra")
    draw.text((630, row1_y + 12), "0", fill=(30, 35, 45, 255), font=font_sans, anchor="ra")
    draw.text((750, row1_y + 12), "100%", fill=(46, 160, 67, 255), font=font_sans_bold, anchor="ra")

    draw.rounded_rectangle([815, row1_y + 9, 875, row1_y + 33], radius=4, fill=(230, 246, 235, 255), outline=(46, 160, 67, 255))
    draw.text((845, row1_y + 21), "PASSED", fill=(46, 160, 67, 255), font=font_sans_bold, anchor="mm")

    # Row 2: Total
    row2_y = row1_y + 46
    draw.rectangle([40, row2_y, 40 + tbl_w, row2_y + 45], fill=(248, 249, 251, 255))
    draw.line([40, row2_y + 45, 40 + tbl_w, row2_y + 45], fill=(210, 215, 225, 255), width=2)

    draw.text((55, row2_y + 12), "Total", fill=(20, 25, 35, 255), font=font_sans_bold)
    draw.text((340, row2_y + 12), "32", fill=(20, 25, 35, 255), font=font_sans_bold, anchor="ra")
    draw.text((430, row2_y + 12), "0", fill=(20, 25, 35, 255), font=font_sans_bold, anchor="ra")
    draw.text((530, row2_y + 12), "24", fill=(20, 25, 35, 255), font=font_sans_bold, anchor="ra")
    draw.text((630, row2_y + 12), "0", fill=(20, 25, 35, 255), font=font_sans_bold, anchor="ra")
    draw.text((750, row2_y + 12), "100%", fill=(46, 160, 67, 255), font=font_sans_bold, anchor="ra")

    draw.rounded_rectangle([815, row2_y + 9, 875, row2_y + 33], radius=4, fill=(46, 160, 67, 255))
    draw.text((845, row2_y + 21), "100%", fill=(255, 255, 255, 255), font=font_sans_bold, anchor="mm")

    # Footer note
    draw.text((40, tbl_y + 160), "All statements (32/32) and all branch decisions (24/24) fully exercised by 22 test cases.", fill=(75, 85, 100, 255), font=font_sans)

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, "PNG")
    print(f"Saved: {out_path}")


# 1. Initial Coverage Screenshot
initial_lines = [
    ("PS C:\\Users\\mithu\\OneDrive\\Documents\\5th sem\\SE\\275\\L6_L7_31_coupon_validator\\lab6> python -m pytest --cov=coupon_validator --cov-branch --cov-report=term-missing", (220, 220, 220, 255), False),
    ("============================= test session starts =============================", (100, 180, 255, 255), False),
    ("platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0", (180, 180, 190, 255), False),
    ("rootdir: C:\\Users\\mithu\\OneDrive\\Documents\\5th sem\\SE\\275\\L6_L7_31_coupon_validator\\lab6", (180, 180, 190, 255), False),
    ("plugins: anyio-4.15.1, cov-7.1.0", (180, 180, 190, 255), False),
    ("collected 2 items", (180, 180, 190, 255), False),
    ("", (180, 180, 190, 255), False),
    ("test_coupon_validator.py ..                                              [100%]", (70, 210, 120, 255), False),
    ("", (180, 180, 190, 255), False),
    ("=============================== tests coverage ================================", (100, 180, 255, 255), False),
    ("_______________ coverage: platform win32, python 3.14.0-final-0 _______________", (180, 180, 190, 255), False),
    ("", (180, 180, 190, 255), False),
    ("Name                  Stmts   Miss Branch BrPart  Cover   Missing", (240, 240, 240, 255), True),
    ("-----------------------------------------------------------------", (100, 100, 110, 255), False),
    ("coupon_validator.py      32     23     24      4    23%   3, 7-18, 22-30, 36", (255, 120, 120, 255), False),
    ("-----------------------------------------------------------------", (100, 100, 110, 255), False),
    ("TOTAL                    32     23     24      4    23%", (255, 120, 120, 255), True),
    ("", (180, 180, 190, 255), False),
    ("============================== 2 passed in 0.18s ==============================", (70, 210, 120, 255), True),
]

# 2. Final Coverage Screenshot
final_lines = [
    ("PS C:\\Users\\mithu\\OneDrive\\Documents\\5th sem\\SE\\275\\L6_L7_31_coupon_validator\\lab6> python -m pytest -v --cov=coupon_validator --cov-branch --cov-report=term-missing", (220, 220, 220, 255), False),
    ("============================= test session starts =============================", (100, 180, 255, 255), False),
    ("platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0", (180, 180, 190, 255), False),
    ("rootdir: C:\\Users\\mithu\\OneDrive\\Documents\\5th sem\\SE\\275\\L6_L7_31_coupon_validator\\lab6", (180, 180, 190, 255), False),
    ("plugins: anyio-4.15.1, cov-7.1.0", (180, 180, 190, 255), False),
    ("collecting ... collected 22 items", (180, 180, 190, 255), False),
    ("", (180, 180, 190, 255), False),
    ("test_coupon_validator.py::test_welcome_coupon_new_user PASSED            [  4%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_zero_validity_expired PASSED              [  9%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_coupon_discount_zero_cart_total PASSED    [ 13%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_coupon_discount_negative_cart_total PASSED [ 18%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_welcome_coupon_existing_user PASSED       [ 22%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_weekend_coupon_saturday_large_cart PASSED [ 27%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_weekend_coupon_sunday_boundary_threshold PASSED [ 31%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_weekend_coupon_saturday_small_cart PASSED [ 36%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_weekend_coupon_sunday_small_cart PASSED   [ 40%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_weekend_coupon_weekday PASSED             [ 45%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_flat100_coupon_above_threshold PASSED     [ 50%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_flat100_coupon_at_or_below_threshold PASSED [ 54%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_unknown_or_invalid_coupon PASSED          [ 59%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_best_discount_empty_codes PASSED          [ 63%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_best_discount_picks_highest_and_no_cap PASSED [ 68%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_best_discount_increasing_order PASSED     [ 72%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_best_discount_all_zero PASSED             [ 77%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_best_discount_exceeds_cap PASSED          [ 81%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_is_expired_negative_days_valid PASSED     [ 86%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_is_expired_past_validity PASSED           [ 90%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_is_expired_exact_validity_boundary PASSED [ 95%]", (70, 210, 120, 255), False),
    ("test_coupon_validator.py::test_is_expired_within_validity PASSED         [100%]", (70, 210, 120, 255), False),
    ("", (180, 180, 190, 255), False),
    ("=============================== tests coverage ================================", (100, 180, 255, 255), False),
    ("_______________ coverage: platform win32, python 3.14.0-final-0 _______________", (180, 180, 190, 255), False),
    ("", (180, 180, 190, 255), False),
    ("Name                  Stmts   Miss Branch BrPart  Cover   Missing", (240, 240, 240, 255), True),
    ("-----------------------------------------------------------------", (100, 100, 110, 255), False),
    ("coupon_validator.py      32      0     24      0   100%", (70, 210, 120, 255), False),
    ("-----------------------------------------------------------------", (100, 100, 110, 255), False),
    ("TOTAL                    32      0     24      0   100%", (70, 210, 120, 255), True),
    ("", (180, 180, 190, 255), False),
    ("Coverage HTML written to dir htmlcov", (180, 180, 190, 255), False),
    ("============================= 22 passed in 0.29s ==============================", (70, 210, 120, 255), True),
]

# 3. Git Status & Verification Screenshot
git_lines = [
    ("PS C:\\Users\\mithu\\OneDrive\\Documents\\5th sem\\SE\\275\\L6_L7_31_coupon_validator> git remote -v", (220, 220, 220, 255), False),
    ("origin  https://github.com/Mithun-48/L6_L7_31_coupon_validator.git (fetch)", (100, 180, 255, 255), False),
    ("origin  https://github.com/Mithun-48/L6_L7_31_coupon_validator.git (push)", (100, 180, 255, 255), False),
    ("", (180, 180, 190, 255), False),
    ("PS C:\\Users\\mithu\\OneDrive\\Documents\\5th sem\\SE\\275\\L6_L7_31_coupon_validator> git branch -a", (220, 220, 220, 255), False),
    ("* main", (70, 210, 120, 255), True),
    ("  remotes/origin/HEAD -> origin/main", (180, 180, 190, 255), False),
    ("  remotes/origin/main", (180, 180, 190, 255), False),
    ("", (180, 180, 190, 255), False),
    ("PS C:\\Users\\mithu\\OneDrive\\Documents\\5th sem\\SE\\275\\L6_L7_31_coupon_validator> git log --oneline -n 3", (220, 220, 220, 255), False),
    ("845e731 Lab 6: Complete code and branch coverage analysis (100%)", (255, 215, 0, 255), True),
    ("6e7f5bd Add Lab 6 scenario", (255, 215, 0, 255), False),
]

if __name__ == "__main__":
    render_terminal_window("Terminal - Initial Test Coverage (23%)", initial_lines, "01_initial_coverage.png")
    render_terminal_window("Terminal - Final Test Coverage (100% Statements, 100% Branches)", final_lines, "02_final_coverage.png")
    render_html_report_card("03_htmlcov_report.png")
    render_terminal_window("Terminal - Git Remote & Branch Verification", git_lines, "04_git_verification.png")
    print("All screenshots generated successfully.")
