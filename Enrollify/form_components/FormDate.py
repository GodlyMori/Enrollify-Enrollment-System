from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSpinBox
from PyQt6.QtCore import QDate
from datetime import datetime

class FormDate(QWidget):
    def __init__(self, label_text):
        super().__init__()
        self.setup_ui(label_text)

    def setup_ui(self, label_text):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.label = QLabel(label_text)
        self.label.setStyleSheet("""
            color: #374151;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 0.3px;
        """)
        layout.addWidget(self.label)

        # Date picker container
        date_container = QWidget()
        date_layout = QHBoxLayout(date_container)
        date_layout.setContentsMargins(0, 0, 0, 0)
        date_layout.setSpacing(16)

        # Month selector
        month_label = QLabel("Month")
        month_label.setStyleSheet("color: #9CA3AF; font-size: 12px; font-weight: 500;")
        self.month_combo = QComboBox()
        self.month_combo.addItems([
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        self.month_combo.setCurrentIndex(QDate.currentDate().month() - 1)
        self.month_combo.setMinimumHeight(50)
        self.month_combo.setStyleSheet("""
            QComboBox {
                background-color: #FFFFFF;
                border: none;
                border-bottom: 2px solid #E5E7EB;
                border-radius: 0px;
                padding: 12px 0px;
                padding-left: 4px;
                padding-right: 4px;
                font-size: 14px;
                color: #1F2937;
            }
            QComboBox:focus {
                border-bottom: 2px solid #2D9B84;
                background-color: #FAFBFC;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        # Day selector
        day_label = QLabel("Day")
        day_label.setStyleSheet("color: #9CA3AF; font-size: 12px; font-weight: 500;")
        self.day_spin = QSpinBox()
        self.day_spin.setMinimum(1)
        self.day_spin.setMaximum(31)
        self.day_spin.setValue(QDate.currentDate().day())
        self.day_spin.setMinimumHeight(50)
        self.day_spin.setStyleSheet("""
            QSpinBox {
                background-color: #FFFFFF;
                border: none;
                border-bottom: 2px solid #E5E7EB;
                border-radius: 0px;
                padding: 12px 0px;
                padding-left: 4px;
                padding-right: 4px;
                font-size: 14px;
                color: #1F2937;
            }
            QSpinBox:focus {
                border-bottom: 2px solid #2D9B84;
                background-color: #FAFBFC;
            }
        """)

        # Year selector
        year_label = QLabel("Year")
        year_label.setStyleSheet("color: #9CA3AF; font-size: 12px; font-weight: 500;")
        self.year_spin = QSpinBox()
        self.year_spin.setMinimum(1950)
        self.year_spin.setMaximum(QDate.currentDate().year())
        self.year_spin.setValue(QDate.currentDate().year() - 16)  # Default to ~16 years old
        self.year_spin.setMinimumHeight(50)
        self.year_spin.setStyleSheet("""
            QSpinBox {
                background-color: #FFFFFF;
                border: none;
                border-bottom: 2px solid #E5E7EB;
                border-radius: 0px;
                padding: 12px 0px;
                padding-left: 4px;
                padding-right: 4px;
                font-size: 14px;
                color: #1F2937;
            }
            QSpinBox:focus {
                border-bottom: 2px solid #2D9B84;
                background-color: #FAFBFC;
            }
        """)

        # Month column
        month_box = QVBoxLayout()
        month_box.setContentsMargins(0, 0, 0, 0)
        month_box.setSpacing(6)
        month_box.addWidget(month_label)
        month_box.addWidget(self.month_combo)

        # Day column
        day_box = QVBoxLayout()
        day_box.setContentsMargins(0, 0, 0, 0)
        day_box.setSpacing(6)
        day_box.addWidget(day_label)
        day_box.addWidget(self.day_spin)

        # Year column
        year_box = QVBoxLayout()
        year_box.setContentsMargins(0, 0, 0, 0)
        year_box.setSpacing(6)
        year_box.addWidget(year_label)
        year_box.addWidget(self.year_spin)

        date_layout.addLayout(month_box, 2)
        date_layout.addLayout(day_box, 1)
        date_layout.addLayout(year_box, 1)

        layout.addWidget(date_container)

        # Age display
        self.age_label = QLabel()
        self.age_label.setStyleSheet("color: #059669; font-size: 11px; font-weight: 500; margin-top: 4px;")
        layout.addWidget(self.age_label)

        # Connect changes to update age
        self.month_combo.currentIndexChanged.connect(self._update_age)
        self.day_spin.valueChanged.connect(self._update_age)
        self.year_spin.valueChanged.connect(self._update_age)

        self._update_age()

    def _update_age(self):
        """Update and display the calculated age"""
        try:
            month = self.month_combo.currentIndex() + 1
            day = self.day_spin.value()
            year = self.year_spin.value()

            birth_date = QDate(year, month, day)
            if birth_date.isValid():
                today = QDate.currentDate()
                age = today.year() - birth_date.year()
                if today.month() < birth_date.month() or (today.month() == birth_date.month() and today.day() < birth_date.day()):
                    age -= 1
                self.age_label.setText(f"Age: {age} years old")
            else:
                self.age_label.setText("")
        except:
            self.age_label.setText("")

    def value(self):
        """Return date in MM/dd/yyyy format"""
        month = self.month_combo.currentIndex() + 1
        day = self.day_spin.value()
        year = self.year_spin.value()
        return f"{month:02d}/{day:02d}/{year}"

    def setValue(self, date_str):
        """Set date from MM/dd/yyyy format"""
        try:
            if date_str and date_str.strip():
                parts = date_str.split('/')
                if len(parts) == 3:
                    month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
                    self.month_combo.setCurrentIndex(month - 1)
                    self.day_spin.setValue(day)
                    self.year_spin.setValue(year)
        except:
            pass

    def clear(self):
        """Reset to current date"""
        self.month_combo.setCurrentIndex(QDate.currentDate().month() - 1)
        self.day_spin.setValue(QDate.currentDate().day())
        self.year_spin.setValue(QDate.currentDate().year() - 16)

