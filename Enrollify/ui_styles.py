"""
ENROLLIFY UI STYLE SYSTEM
Professional, consistent styling for all components
"""

from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor


class Colors:
    """✅ Standardized Color Palette"""

    # Primary Brand Colors
    PRIMARY = "#2D9B84"  # Main brand teal
    PRIMARY_HOVER = "#35B499"
    PRIMARY_LIGHT = "#E8F4F2"

    # Status Colors
    SUCCESS = "#10B981"  # Green
    WARNING = "#F59E0B"  # Orange
    DANGER = "#EF4444"  # Red
    INFO = "#0099FF"  # Blue

    # Neutrals
    DARK = "#060C0B"  # Main text
    GRAY_900 = "#111827"
    GRAY_700 = "#374151"
    GRAY_600 = "#4B5563"
    GRAY_500 = "#6B7280"  # Secondary text
    GRAY_400 = "#9CA3AF"
    GRAY_300 = "#D1D5DB"
    GRAY_200 = "#E5E7EB"  # Borders
    GRAY_100 = "#F3F4F6"
    GRAY_50 = "#F9FAFB"  # Light backgrounds
    WHITE = "#FFFFFF"

    # Background Colors
    BG_PRIMARY = "#FFFFFF"
    BG_SECONDARY = "#F8F9FA"
    BG_TERTIARY = "#F0F1F3"


class Spacing:
    """✅ Standardized Spacing System"""
    XS = 8
    SM = 16
    MD = 24
    LG = 32
    XL = 48
    XXL = 64


class Radius:
    """✅ Border Radius Standards"""
    SM = 6
    MD = 8
    LG = 12
    XL = 16
    FULL = 9999


class Shadows:
    """✅ Shadow Effects"""

    @staticmethod
    def card_shadow():
        """Standard card shadow"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 15))
        return shadow

    @staticmethod
    def elevated_shadow():
        """Elevated element shadow"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 25))
        return shadow


class Styles:
    """✅ Complete Style Templates"""

    # ========================================================================
    # HEADERS
    # ========================================================================

    @staticmethod
    def header():
        """Standard header style"""
        return f"""
            QFrame {{
                background-color: {Colors.WHITE};
                border: none;
                border-bottom: 1px solid {Colors.GRAY_200};
            }}
        """

    # ========================================================================
    # NAVIGATION TABS
    # ========================================================================

    @staticmethod
    def nav_container():
        """Navigation container"""
        return f"""
            QFrame {{
                background-color: {Colors.WHITE};
                border: none;
                border-bottom: 1px solid {Colors.GRAY_200};
            }}
        """

    @staticmethod
    def nav_button_active():
        """Active navigation button"""
        return f"""
            QPushButton {{
                background-color: transparent;
                color: {Colors.DARK};
                border: none;
                border-bottom: 3px solid {Colors.PRIMARY};
                font-size: 16px;
                font-weight: 600;
                padding: 0 24px;
            }}
        """

    @staticmethod
    def nav_button_inactive():
        """Inactive navigation button"""
        return f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {Colors.GRAY_500};
                font-size: 15px;
                font-weight: 500;
                padding: 0 24px;
            }}
            QPushButton:hover {{
                background-color: {Colors.GRAY_50};
                color: {Colors.DARK};
            }}
        """

    # ========================================================================
    # BUTTONS
    # ========================================================================

    @staticmethod
    def button_primary():
        """Primary action button"""
        return f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: {Radius.MD}px;
                font-size: 15px;
                font-weight: 600;
                padding: 12px 24px;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: #1F7A66;
            }}
            QPushButton:disabled {{
                background-color: {Colors.GRAY_300};
                color: {Colors.GRAY_500};
            }}
        """

    @staticmethod
    def button_secondary():
        """Secondary action button"""
        return f"""
            QPushButton {{
                background-color: white;
                color: {Colors.PRIMARY};
                border: 2px solid {Colors.PRIMARY};
                border-radius: {Radius.MD}px;
                font-size: 15px;
                font-weight: 600;
                padding: 10px 24px;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY_LIGHT};
            }}
            QPushButton:pressed {{
                background-color: #D1EBE5;
            }}
        """

    @staticmethod
    def button_danger():
        """Danger/Delete button"""
        return f"""
            QPushButton {{
                background-color: {Colors.DANGER};
                color: white;
                border: none;
                border-radius: {Radius.MD}px;
                font-size: 15px;
                font-weight: 600;
                padding: 12px 24px;
            }}
            QPushButton:hover {{
                background-color: #DC2626;
            }}
            QPushButton:pressed {{
                background-color: #B91C1C;
            }}
        """

    # ========================================================================
    # CARDS
    # ========================================================================

    @staticmethod
    def card():
        """Standard card"""
        return f"""
            QFrame {{
                background-color: white;
                border: 1px solid {Colors.GRAY_200};
                border-radius: {Radius.LG}px;
            }}
            QFrame:hover {{
                border-color: {Colors.GRAY_300};
            }}
        """

    @staticmethod
    def card_elevated():
        """Card with shadow"""
        return f"""
            QFrame {{
                background-color: white;
                border: none;
                border-radius: {Radius.LG}px;
            }}
        """

    @staticmethod
    def card_stat(color):
        """Stat card with color accent"""
        return f"""
            QFrame {{
                background-color: white;
                border: 2px solid {color};
                border-radius: {Radius.LG}px;
                padding: {Spacing.MD}px;
            }}
            QFrame:hover {{
                border-color: {color};
                background-color: {Colors.GRAY_50};
            }}
        """

    # ========================================================================
    # INPUTS
    # ========================================================================

    @staticmethod
    def input():
        """Standard text input"""
        return f"""
            QLineEdit {{
                background-color: white;
                border: 2px solid {Colors.GRAY_200};
                border-radius: {Radius.MD}px;
                padding: 12px 16px;
                font-size: 14px;
                color: {Colors.DARK};
            }}
            QLineEdit:focus {{
                border-color: {Colors.PRIMARY};
                background-color: white;
            }}
            QLineEdit::placeholder {{
                color: {Colors.GRAY_400};
            }}
        """

    @staticmethod
    def combo():
        """Dropdown/Combobox"""
        return f"""
            QComboBox {{
                background-color: white;
                border: 2px solid {Colors.GRAY_200};
                border-radius: {Radius.MD}px;
                padding: 12px 16px;
                font-size: 14px;
                color: {Colors.DARK};
            }}
            QComboBox:focus {{
                border-color: {Colors.PRIMARY};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
        """

    # ========================================================================
    # TABLES
    # ========================================================================

    @staticmethod
    def table():
        """Standard table"""
        return f"""
            QTableWidget {{
                background-color: white;
                border: none;
                gridline-color: {Colors.GRAY_200};
                font-size: 14px;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {Colors.GRAY_200};
            }}
            QTableWidget::item:selected {{
                background-color: {Colors.PRIMARY_LIGHT};
                color: {Colors.DARK};
            }}
            QHeaderView::section {{
                background-color: {Colors.GRAY_100};
                color: {Colors.DARK};
                font-weight: 700;
                font-size: 14px;
                border: none;
                border-bottom: 2px solid {Colors.GRAY_300};
                padding: 12px;
            }}
        """

    # ========================================================================
    # SCROLLBARS
    # ========================================================================

    @staticmethod
    def scrollbar():
        """Standard scrollbar"""
        return f"""
            QScrollBar:vertical {{
                border: none;
                background: {Colors.GRAY_100};
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background: {Colors.GRAY_300};
                border-radius: 5px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {Colors.GRAY_400};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """

    # ========================================================================
    # TYPOGRAPHY
    # ========================================================================

    @staticmethod
    def heading_1():
        """H1 - Main page title"""
        return f"font-size: 32px; font-weight: 700; color: {Colors.DARK};"

    @staticmethod
    def heading_2():
        """H2 - Section title"""
        return f"font-size: 24px; font-weight: 700; color: {Colors.DARK};"

    @staticmethod
    def heading_3():
        """H3 - Subsection title"""
        return f"font-size: 20px; font-weight: 600; color: {Colors.DARK};"

    @staticmethod
    def body_text():
        """Body text"""
        return f"font-size: 14px; color: {Colors.GRAY_700};"

    @staticmethod
    def subtitle():
        """Subtitle/Secondary text"""
        return f"font-size: 14px; color: {Colors.GRAY_500};"

    @staticmethod
    def caption():
        """Small caption text"""
        return f"font-size: 12px; color: {Colors.GRAY_500};"


# ============================================================================
# USAGE EXAMPLES
# ============================================================================
if __name__ == '__main__':
    print("=" * 60)
    print("ENROLLIFY UI STYLE SYSTEM")
    print("=" * 60)
    print("\n✅ Colors:")
    print(f"  Primary: {Colors.PRIMARY}")
    print(f"  Success: {Colors.SUCCESS}")
    print(f"  Warning: {Colors.WARNING}")
    print(f"  Danger: {Colors.DANGER}")

    print("\n✅ Spacing:")
    print(f"  Small: {Spacing.SM}px")
    print(f"  Medium: {Spacing.MD}px")
    print(f"  Large: {Spacing.LG}px")

    print("\n✅ Usage:")
    print("  from ui_styles import Colors, Styles")
    print('  button.setStyleSheet(Styles.button_primary())')
    print('  card.setStyleSheet(Styles.card())')
    print("=" * 60)