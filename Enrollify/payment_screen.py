# payment_screen.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QScrollArea, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QPainterPath
from database_manager_mysql import get_database
from receipt_dialog import ReceiptDialog
from PyQt6.QtCore import QDateTime
import os


class PaymentScreen(QWidget):
    logout_signal = pyqtSignal()
    back_signal = pyqtSignal()
    payment_completed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.student_data = {}
        self.selected_payment_method = None
        self.db = get_database()
        self.setStyleSheet("""
            QWidget {
                background-color: #F8FAFA;
            }
        """)
        self.setup_ui()

    def load_icon(self, icon_name):
        """Load icon from assets/icons/ with fallback to emoji"""
        path = f"assets/icons/{icon_name}"
        if os.path.exists(path):
            pixmap = QPixmap(path).scaled(
                40, 40,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            label = QLabel()
            label.setPixmap(pixmap)
            label.setStyleSheet("background: transparent; border: none;")
            return label
        else:
            # Fallback to emoji
            label = QLabel(icon_name)
            label.setStyleSheet("font-size: 40px; background: transparent; border: none;")
            return label

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setFixedHeight(100)
        header.setStyleSheet("background-color: white; border-bottom: none;")  # Removed border
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(60, 20, 60, 20)

        # Logo
        logo_label = QLabel()
        logo_label.setFixedSize(50, 50)
        self.create_checkmark_logo(logo_label)
        logo_title_layout = QHBoxLayout()
        logo_title_layout.setSpacing(15)
        logo_title_layout.addWidget(logo_label)

        # Title
        title_container = QVBoxLayout()
        title_container.setSpacing(2)
        title = QLabel("Enrollify")
        title.setStyleSheet("""
            color: #234940; 
            font-size: 26px; 
            font-weight: 700;
            border: none;
            background: transparent;
        """)
        subtitle = QLabel("Student Enrollment Portal")
        subtitle.setStyleSheet("""
            color: #6B7280; 
            font-size: 14px; 
            font-weight: 500;
            border: none;
            background: transparent;
        """)
        title_container.addWidget(title)
        title_container.addWidget(subtitle)
        logo_title_layout.addLayout(title_container)
        header_layout.addLayout(logo_title_layout)
        header_layout.addStretch()

        # Logout
        logout_btn = QPushButton("↪ Logout")
        logout_btn.setFixedSize(110, 40)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2D9B84;
                border: 2px solid #2D9B84;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover { 
                background-color: #F0FAF8;
            }
        """)
        logout_btn.clicked.connect(self.logout_signal.emit)
        header_layout.addWidget(logout_btn)
        main_layout.addWidget(header)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(60, 40, 60, 40)
        scroll_layout.setSpacing(30)

        # Page Title
        page_title_container = QWidget()
        page_title_container.setStyleSheet("background-color: #E8F5F3; border-radius: 12px; border: none;")
        page_title_layout = QHBoxLayout(page_title_container)
        page_title_layout.setContentsMargins(30, 25, 30, 25)
        page_title_layout.setSpacing(15)

        title_text_layout = QVBoxLayout()
        title_text_layout.setSpacing(5)
        page_title = QLabel("Complete Your Payment")
        page_title.setStyleSheet("""
            color: #234940; 
            font-size: 28px; 
            font-weight: 700;
            border: none;
            background: transparent;
        """)
        page_subtitle = QLabel("Finalize your SHS enrollment with secure payment")
        page_subtitle.setStyleSheet("""
            color: #6B7280; 
            font-size: 15px; 
            font-weight: 500;
            border: none;
            background: transparent;
        """)
        title_text_layout.addWidget(page_title)
        title_text_layout.addWidget(page_subtitle)
        page_title_layout.addLayout(title_text_layout)
        page_title_layout.addStretch()

        cancel_btn = QPushButton("✕  Cancel")
        cancel_btn.setFixedSize(120, 40)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #2D9B84;
                border: none;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton:hover { 
                color: #234940;
                text-decoration: underline;
            }
        """)
        cancel_btn.clicked.connect(self.back_signal.emit)
        page_title_layout.addWidget(cancel_btn)
        scroll_layout.addWidget(page_title_container)

        # Student Info Card
        student_info_card = self.create_student_info_card()
        scroll_layout.addWidget(student_info_card)

        # Payment Summary Card
        payment_summary_card = self.create_payment_summary_card()
        scroll_layout.addWidget(payment_summary_card)

        # Payment Method Card
        payment_method_card = self.create_payment_method_card()
        scroll_layout.addWidget(payment_method_card)

        # Action Buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(20)

        back_btn = QPushButton("←  Back")
        back_btn.setFixedHeight(55)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #6B7280;
                border: 2px solid #E5E7EB;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                padding: 0 30px;
                border: none;
            }
            QPushButton:hover { 
                background-color: #F9FAFB;
                border-color: #D1D5DB;
            }
        """)
        back_btn.clicked.connect(self.back_signal.emit)
        action_layout.addWidget(back_btn, 1)

        self.pay_btn = QPushButton("Pay ₱32,500")
        self.pay_btn.setFixedHeight(55)
        self.pay_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pay_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D9B84;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 700;
                padding: 0 40px;
            }
            QPushButton:hover { 
                background-color: #35B499;
            }
            QPushButton:disabled {
                background-color: #D1D5DB;
                color: #9CA3AF;
            }
        """)
        self.pay_btn.clicked.connect(self.process_payment)
        self.pay_btn.setEnabled(False)
        action_layout.addWidget(self.pay_btn, 2)
        scroll_layout.addLayout(action_layout)

        # Footer
        footer_label = QLabel("Your Gateway to Senior High Success")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet("""
            color: #9CA3AF; 
            font-size: 14px; 
            font-weight: 500; 
            padding: 20px;
            border: none;
            background: transparent;
        """)
        scroll_layout.addWidget(footer_label)
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

    def create_student_info_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: none;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(20)

        title = QLabel("Student Information")
        title.setStyleSheet("""
            color: #1F2937; 
            font-size: 20px; 
            font-weight: 700;
            border: none;
            background: transparent;
        """)
        card_layout.addWidget(title)

        info_grid = QHBoxLayout()
        info_grid.setSpacing(60)

        left_col = QVBoxLayout()
        left_col.setSpacing(15)
        self.name_label = self.create_info_row("Name:", "")
        self.grade_label = self.create_info_row("Grade Level:", "")
        self.strand_label = self.create_info_row("Strand:", "")
        left_col.addWidget(self.name_label)
        left_col.addWidget(self.grade_label)
        left_col.addWidget(self.strand_label)

        right_col = QVBoxLayout()
        right_col.setSpacing(15)
        self.lrn_label = self.create_info_row("LRN:", "")
        self.track_label = self.create_info_row("Track:", "")
        right_col.addWidget(self.lrn_label)
        right_col.addWidget(self.track_label)
        right_col.addStretch()

        info_grid.addLayout(left_col, 1)
        info_grid.addLayout(right_col, 1)
        card_layout.addLayout(info_grid)
        return card

    def create_info_row(self, label_text, value_text):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        label = QLabel(label_text)
        label.setStyleSheet("""
            color: #6B7280; 
            font-size: 14px; 
            font-weight: 500;
            border: none;
            background: transparent;
        """)
        label.setFixedWidth(100)

        value = QLabel(value_text)
        value.setStyleSheet("""
            color: #1F2937; 
            font-size: 14px; 
            font-weight: 600;
            border: none;
            background: transparent;
        """)
        value.setWordWrap(True)
        value.setObjectName("value_label")

        layout.addWidget(label)
        layout.addWidget(value, 1)
        return container

    def create_payment_summary_card(self):
        """Create payment summary card with dynamic fee labels"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: none;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(20)

        # Card title
        title = QLabel("Payment Summary")
        title.setStyleSheet("""
            color: #1F2937; 
            font-size: 20px; 
            font-weight: 700;
            border: none;
            background: transparent;
        """)
        card_layout.addWidget(title)

        # Fee items (store labels for dynamic update)
        self.enrollment_fee_label = self.create_fee_item(card_layout, "Enrollment Fee", "₱5,000")
        self.misc_fee_label = self.create_fee_item(card_layout, "Miscellaneous Fee", "₱4,500")
        self.tuition_fee_label = self.create_fee_item(card_layout, "Tuition Fee", "₱15,000")
        self.special_fee_label = self.create_fee_item(card_layout, "Laboratory/Special Fee", "₱2,000")

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #E5E7EB; max-height: 1px; border: none;")
        card_layout.addWidget(divider)

        # Total
        total_layout = QHBoxLayout()
        total_label = QLabel("Total Amount")
        total_label.setStyleSheet("""
            color: #1F2937; 
            font-size: 18px; 
            font-weight: 700;
            border: none;
            background: transparent;
        """)

        self.total_amount_label = QLabel("₱26,500")
        self.total_amount_label.setStyleSheet("""
            color: #2D9B84; 
            font-size: 24px; 
            font-weight: 700;
            border: none;
            background: transparent;
        """)

        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(self.total_amount_label)
        card_layout.addLayout(total_layout)

        return card

    def update_payment_summary(self):
        """Update payment summary based on student's track/strand"""
        if not self.student_data:
            return

        track = self.student_data.get('track', 'Academic')
        strand = self.student_data.get('strand', '').strip() or None

        fees = self.db.get_tuition_fees(track, strand)

        # Update fee items
        self.enrollment_fee_label.setText(f"₱{fees['enrollment_fee']:,.2f}")
        self.misc_fee_label.setText(f"₱{fees['miscellaneous_fee']:,.2f}")
        self.tuition_fee_label.setText(f"₱{fees['tuition_fee']:,.2f}")
        self.special_fee_label.setText(f"₱{fees['special_fee']:,.2f}")

        # Update total
        self.total_amount_label.setText(f"₱{fees['total']:,.2f}")
        self.pay_btn.setText(f"Pay ₱{fees['total']:,.0f}")
        self.payment_amount = fees['total']  # Store for payment processing

    def create_fee_item(self, parent_layout, label_text, amount_text):
        """Create a fee item row and return the amount QLabel for dynamic updates"""
        item_layout = QHBoxLayout()
        item_layout.setSpacing(10)

        label = QLabel(label_text)
        label.setStyleSheet("""
            color: #6B7280; 
            font-size: 15px; 
            font-weight: 500;
            border: none;
            background: transparent;
        """)

        amount = QLabel(amount_text)
        amount.setStyleSheet("""
            color: #1F2937; 
            font-size: 15px; 
            font-weight: 600;
            border: none;
            background: transparent;
        """)

        item_layout.addWidget(label)
        item_layout.addStretch()
        item_layout.addWidget(amount)

        parent_layout.addLayout(item_layout)

        return amount  # 👈 RETURN THE LABEL

    def create_payment_summary_card(self):
        """Create payment summary card with dynamic fee labels"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: none;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(20)

        title = QLabel("Payment Summary")
        title.setStyleSheet("""
            color: #1F2937; 
            font-size: 20px; 
            font-weight: 700;
            border: none;
            background: transparent;
        """)
        card_layout.addWidget(title)

        # ✅ Store references to amount labels
        self.enrollment_fee_label = self.create_fee_item(card_layout, "Enrollment Fee", "₱5,000")
        self.misc_fee_label = self.create_fee_item(card_layout, "Miscellaneous Fee", "₱4,500")
        self.tuition_fee_label = self.create_fee_item(card_layout, "Tuition Fee", "₱15,000")
        self.special_fee_label = self.create_fee_item(card_layout, "Laboratory/Special Fee", "₱2,000")

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #E5E7EB; max-height: 1px; border: none;")
        card_layout.addWidget(divider)

        # Total
        total_layout = QHBoxLayout()
        total_label = QLabel("Total Amount")
        total_label.setStyleSheet("""
            color: #1F2937; 
            font-size: 18px; 
            font-weight: 700;
            border: none;
            background: transparent;
        """)

        self.total_amount_label = QLabel("₱26,500")
        self.total_amount_label.setStyleSheet("""
            color: #2D9B84; 
            font-size: 24px; 
            font-weight: 700;
            border: none;
            background: transparent;
        """)

        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(self.total_amount_label)
        card_layout.addLayout(total_layout)

        return card

    def create_payment_method_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: none;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(25)

        title = QLabel("Select Payment Method")
        title.setStyleSheet("""
            color: #1F2937; 
            font-size: 20px; 
            font-weight: 700;
            border: none;
            background: transparent;
        """)
        card_layout.addWidget(title)

        methods_layout = QHBoxLayout()
        methods_layout.setSpacing(20)

        # Use load_icon() with image names
        self.card_btn = self.create_payment_method_button(self.load_icon("credit_card.png"), "Credit/Debit Card")
        self.card_btn.clicked.connect(lambda: self.select_payment_method("card"))
        methods_layout.addWidget(self.card_btn)

        self.ewallet_btn = self.create_payment_method_button(self.load_icon("ewallet.png"), "E-Wallet")
        self.ewallet_btn.clicked.connect(lambda: self.select_payment_method("ewallet"))
        methods_layout.addWidget(self.ewallet_btn)

        self.bank_btn = self.create_payment_method_button(self.load_icon("bank_transfer.png"), "Bank Transfer")
        self.bank_btn.clicked.connect(lambda: self.select_payment_method("bank"))
        methods_layout.addWidget(self.bank_btn)

        card_layout.addLayout(methods_layout)
        return card

    def create_payment_method_button(self, icon_widget, method_name):
        """Create button with icon widget (QLabel with image or emoji)"""
        btn = QPushButton()
        btn.setFixedHeight(120)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #E5E7EB;
                border-radius: 12px;
            }
            QPushButton:hover {
                border-color: #2D9B84;
                background-color: #F0FAF8;
            }
            QPushButton:checked {
                border-color: #2D9B84;
                background-color: #E8F5F3;
                border-width: 3px;
            }
        """)
        btn.setCheckable(True)

        btn_layout = QVBoxLayout(btn)
        btn_layout.setContentsMargins(20, 20, 20, 20)
        btn_layout.setSpacing(10)

        # Add icon widget (already has transparent background)
        btn_layout.addWidget(icon_widget)

        # Method name
        name_label = QLabel(method_name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet("""
            color: #1F2937; 
            font-size: 15px; 
            font-weight: 600;
            border: none;
            background: transparent;
        """)
        btn_layout.addWidget(name_label)
        return btn

    def select_payment_method(self, method):
        if method != "card":
            self.card_btn.setChecked(False)
        if method != "ewallet":
            self.ewallet_btn.setChecked(False)
        if method != "bank":
            self.bank_btn.setChecked(False)

        if method == "card":
            self.card_btn.setChecked(True)
        elif method == "ewallet":
            self.ewallet_btn.setChecked(True)
        elif method == "bank":
            self.bank_btn.setChecked(True)

        self.selected_payment_method = method
        self.pay_btn.setEnabled(True)

    def create_checkmark_logo(self, label):
        label.setText("")
        label.setStyleSheet("background-color: transparent; border: none;")

        if os.path.exists('assets/enrollify_logo.png'):
            pixmap = QPixmap('assets/enrollify_logo.png')
            if not pixmap.isNull():
                scaled = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)
                label.setPixmap(scaled)
                label.setFixedSize(scaled.size())
                return

        # Fallback checkmark
        self.logo_pixmap = QPixmap(50, 50)
        self.logo_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(self.logo_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#2D9B84"))
        painter.drawEllipse(3, 3, 44, 44)
        pen = QPen(QColor("#234940"))
        pen.setWidth(5)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        path = QPainterPath()
        path.moveTo(15, 25)
        path.lineTo(22, 32)
        path.lineTo(35, 15)
        painter.drawPath(path)
        painter.end()
        label.setPixmap(self.logo_pixmap)

    def set_student_data(self, data):
        """Set student data and update payment summary"""
        self.student_data = data

        # Update student info display
        full_name = f"{data.get('firstname', '')} {data.get('middlename', '')} {data.get('lastname', '')}".strip()
        self.update_info_value(self.name_label, full_name)
        self.update_info_value(self.lrn_label, data.get('lrn', ''))
        self.update_info_value(self.grade_label, data.get('grade', ''))
        self.update_info_value(self.track_label, data.get('track', ''))
        self.update_info_value(self.strand_label, data.get('strand', 'N/A'))

        # Update payment summary based on track/strand
        self.update_payment_summary()

    def update_info_value(self, container, new_value):
        value_label = container.findChild(QLabel, "value_label")
        if value_label:
            value_label.setText(new_value)

    def process_payment(self):
        """Process the payment with receipt generation"""
        if not self.selected_payment_method:
            QMessageBox.warning(self, "Payment Method Required",
                                "Please select a payment method to continue.")
            return

        # Use dynamic amount
        amount = getattr(self, 'payment_amount', 26500)

        payment_data = {
            'student_data': self.student_data,
            'payment_method': self.selected_payment_method,
            'amount': amount,
            'currency': 'PHP'
        }

        reply = QMessageBox.question(
            self, 'Confirm Payment',
            f'Confirm payment of ₱{amount:,.2f} via {self.get_payment_method_name()}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Generate receipt number
            import random
            receipt_number = f"{QDateTime.currentDateTime().toString('yyyyMMdd')}{random.randint(1000, 9999)}"

            # Show success message first
            QMessageBox.information(
                self, 'Payment Successful',
                f'✅ Payment of ₱{amount:,.2f} has been successfully processed!\n\n'
                f'Receipt No: #{receipt_number}\n'
                f'Student: {self.student_data.get("firstname", "")} {self.student_data.get("lastname", "")}\n\n'
                f'Your receipt will be displayed next.'
            )

            # Show receipt dialog
            receipt_dialog = ReceiptDialog(payment_data, receipt_number, self)
            receipt_dialog.exec()

            # Emit signal for main app
            self.payment_completed.emit(payment_data)

            # Reset payment selection
            self.reset_payment_selection()

    def get_payment_method_name(self):
        methods = {
            'card': 'Credit/Debit Card',
            'ewallet': 'E-Wallet',
            'bank': 'Bank Transfer'
        }
        return methods.get(self.selected_payment_method, 'Unknown')

    def reset_payment_selection(self):
        self.card_btn.setChecked(False)
        self.ewallet_btn.setChecked(False)
        self.bank_btn.setChecked(False)
        self.selected_payment_method = None
        self.pay_btn.setEnabled(False)