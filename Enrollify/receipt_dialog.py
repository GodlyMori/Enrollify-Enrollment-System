# ============================================
# FIXED receipt_dialog.py
# Replace your existing receipt_dialog.py with this
# ============================================

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox, QScrollArea
)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import os


class ReceiptDialog(QDialog):
    """Professional payment receipt dialog - FIXED VERSION"""

    def __init__(self, payment_data, receipt_number, parent=None):
        super().__init__(parent)
        self.payment_data = payment_data
        self.receipt_number = receipt_number
        self.setWindowTitle("Payment Receipt")
        self.setMinimumSize(650, 850)  # Increased size
        self.setModal(True)
        self.setup_ui()

    def setup_ui(self):
        """Build the receipt UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scrollable content to prevent cutoff
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #F5F5F5; }")

        content = QFrame()
        content.setStyleSheet("background-color: #F5F5F5;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Receipt card
        self.receipt_card = self.create_receipt_card()
        content_layout.addWidget(self.receipt_card)

        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        print_btn = QPushButton("🖨️ Print Receipt")
        print_btn.setFixedHeight(50)
        print_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D9B84;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 600;
                padding: 0 25px;
            }
            QPushButton:hover {
                background-color: #35B499;
            }
        """)
        print_btn.clicked.connect(self.print_receipt)

        save_btn = QPushButton("💾 Save as PDF")
        save_btn.setFixedHeight(50)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2D9B84;
                border: 2px solid #2D9B84;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 600;
                padding: 0 25px;
            }
            QPushButton:hover {
                background-color: #F0FAF8;
            }
        """)
        save_btn.clicked.connect(self.save_as_pdf)

        close_btn = QPushButton("✓ Done")
        close_btn.setFixedHeight(50)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #F3F4F6;
                color: #111827;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 600;
                padding: 0 25px;
            }
            QPushButton:hover {
                background-color: #E5E7EB;
            }
        """)
        close_btn.clicked.connect(self.accept)

        buttons_layout.addWidget(print_btn, 1)
        buttons_layout.addWidget(save_btn, 1)
        buttons_layout.addStretch()
        buttons_layout.addWidget(close_btn, 1)

        content_layout.addLayout(buttons_layout)
        content_layout.addStretch()

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def create_receipt_card(self):
        """Create the main receipt card with improved layout"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #E5E7EB;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 40, 40, 40)  # Increased padding
        layout.setSpacing(25)  # Increased spacing

        # Header
        layout.addLayout(self.create_header())

        # Divider
        layout.addWidget(self.create_divider())

        # Receipt info
        layout.addLayout(self.create_receipt_info())

        # Divider
        layout.addWidget(self.create_divider())

        # Student info
        layout.addLayout(self.create_student_info())

        # Divider
        layout.addWidget(self.create_divider())

        # Payment breakdown
        layout.addLayout(self.create_payment_breakdown())

        # Divider
        layout.addWidget(self.create_divider())

        # Payment details
        layout.addLayout(self.create_payment_details())

        # Divider
        layout.addWidget(self.create_divider())

        # Footer
        layout.addLayout(self.create_footer())

        return card

    def create_header(self):
        """Create receipt header with logo"""
        header_layout = QVBoxLayout()
        header_layout.setSpacing(12)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo
        logo_label = QLabel()
        if os.path.exists('assets/enrollify_logo.png'):
            pixmap = QPixmap('assets/enrollify_logo.png').scaled(
                70, 70, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("✓")
            logo_label.setStyleSheet("""
                font-size: 50px;
                color: #2D9B84;
                background-color: #E8F4F2;
                border-radius: 35px;
                padding: 10px;
            """)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setFixedSize(70, 70)
        header_layout.addWidget(logo_label)

        # Title
        title = QLabel("PAYMENT RECEIPT")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 26px;
            font-weight: 700;
            color: #060C0B;
            letter-spacing: 1px;
        """)
        header_layout.addWidget(title)

        # School name
        school = QLabel("Enrollify Senior High School")
        school.setAlignment(Qt.AlignmentFlag.AlignCenter)
        school.setStyleSheet("""
            font-size: 15px;
            color: #6B7280;
            font-weight: 500;
        """)
        school.setWordWrap(True)
        header_layout.addWidget(school)

        return header_layout

    def create_receipt_info(self):
        """Receipt number and date"""
        info_layout = QVBoxLayout()
        info_layout.setSpacing(12)

        # Receipt number
        receipt_row = QHBoxLayout()
        receipt_label = QLabel("Receipt No:")
        receipt_label.setStyleSheet("font-size: 14px; color: #6B7280; font-weight: 500;")
        receipt_value = QLabel(f"#{self.receipt_number}")
        receipt_value.setStyleSheet("font-size: 14px; color: #111827; font-weight: 700;")
        receipt_row.addWidget(receipt_label)
        receipt_row.addStretch()
        receipt_row.addWidget(receipt_value)
        info_layout.addLayout(receipt_row)

        # Date
        date_row = QHBoxLayout()
        date_label = QLabel("Date:")
        date_label.setStyleSheet("font-size: 14px; color: #6B7280; font-weight: 500;")
        date_value = QLabel(QDateTime.currentDateTime().toString("MMMM dd, yyyy - hh:mm AP"))
        date_value.setStyleSheet("font-size: 14px; color: #111827; font-weight: 700;")
        date_value.setWordWrap(True)
        date_row.addWidget(date_label)
        date_row.addStretch()
        date_row.addWidget(date_value)
        info_layout.addLayout(date_row)

        # Status badge
        status_container = QHBoxLayout()
        status_container.addStretch()
        status_badge = QLabel("✓ PAID")
        status_badge.setStyleSheet("""
            background-color: #DCFCE7;
            color: #166534;
            font-size: 13px;
            font-weight: 700;
            padding: 8px 20px;
            border-radius: 20px;
        """)
        status_container.addWidget(status_badge)
        info_layout.addLayout(status_container)

        return info_layout

    def create_student_info(self):
        """Student information section"""
        section_layout = QVBoxLayout()
        section_layout.setSpacing(15)

        # Section title
        title = QLabel("STUDENT INFORMATION")
        title.setStyleSheet("""
            font-size: 13px;
            font-weight: 700;
            color: #6B7280;
            letter-spacing: 1px;
        """)
        section_layout.addWidget(title)

        student = self.payment_data.get('student_data', {})

        # Student details - with word wrap
        full_name = f"{student.get('firstname', '')} {student.get('middlename', '')} {student.get('lastname', '')}".strip()

        details = [
            ("Name", full_name),
            ("LRN", student.get('lrn', 'N/A')),
            ("Grade Level", student.get('grade', 'N/A')),
            ("Track", student.get('track', 'N/A')),
            ("Strand", student.get('strand', 'N/A'))
        ]

        for label, value in details:
            row = self.create_info_row(label, value)
            section_layout.addLayout(row)

        return section_layout

    def create_payment_breakdown(self):
        """Payment breakdown section"""
        section_layout = QVBoxLayout()
        section_layout.setSpacing(15)

        # Section title
        title = QLabel("PAYMENT BREAKDOWN")
        title.setStyleSheet("""
            font-size: 13px;
            font-weight: 700;
            color: #6B7280;
            letter-spacing: 1px;
        """)
        section_layout.addWidget(title)

        # Get fee breakdown with error handling
        try:
            from database_manager_mysql import get_database
            db = get_database()

            student = self.payment_data.get('student_data', {})
            track = student.get('track', 'Academic')
            strand = student.get('strand', '').strip() or None

            fees = db.get_tuition_fees(track, strand)
        except Exception as e:
            print(f"Error loading fees: {e}")
            # Fallback fees
            fees = {
                'enrollment_fee': 5000,
                'miscellaneous_fee': 4500,
                'tuition_fee': 15000,
                'special_fee': 2000,
                'total': 26500
            }

        # Fee items
        fee_items = [
            ("Enrollment Fee", fees['enrollment_fee']),
            ("Miscellaneous Fee", fees['miscellaneous_fee']),
            ("Tuition Fee", fees['tuition_fee']),
            ("Laboratory/Special Fee", fees['special_fee'])
        ]

        for label, amount in fee_items:
            row = self.create_fee_row(label, amount)
            section_layout.addLayout(row)

        # Subtotal
        section_layout.addWidget(self.create_divider())
        subtotal_row = self.create_fee_row("SUBTOTAL", fees['total'], bold=True)
        section_layout.addLayout(subtotal_row)

        # Total with highlight
        section_layout.addSpacing(10)
        total_container = QFrame()
        total_container.setStyleSheet("""
            background-color: #F9FAFB;
            border-radius: 8px;
            padding: 15px;
        """)
        total_layout = QHBoxLayout(total_container)
        total_layout.setContentsMargins(15, 10, 15, 10)

        total_label = QLabel("TOTAL AMOUNT PAID")
        total_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #111827;
        """)

        total_value = QLabel(f"₱{fees['total']:,.2f}")
        total_value.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #2D9B84;
        """)

        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(total_value)

        section_layout.addWidget(total_container)

        return section_layout

    def create_payment_details(self):
        """Payment method and details"""
        section_layout = QVBoxLayout()
        section_layout.setSpacing(15)

        # Section title
        title = QLabel("PAYMENT DETAILS")
        title.setStyleSheet("""
            font-size: 13px;
            font-weight: 700;
            color: #6B7280;
            letter-spacing: 1px;
        """)
        section_layout.addWidget(title)

        # Payment method
        method_name = self.get_payment_method_name(self.payment_data.get('payment_method', 'Unknown'))
        method_row = self.create_info_row("Payment Method", method_name)
        section_layout.addLayout(method_row)

        # Transaction ID (generated)
        transaction_id = f"TXN{self.receipt_number}"
        txn_row = self.create_info_row("Transaction ID", transaction_id)
        section_layout.addLayout(txn_row)

        return section_layout

    def create_footer(self):
        """Receipt footer"""
        footer_layout = QVBoxLayout()
        footer_layout.setSpacing(10)
        footer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Thank you message
        thank_you = QLabel("Thank you for your payment!")
        thank_you.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thank_you.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #2D9B84;
        """)
        footer_layout.addWidget(thank_you)

        # Note
        note = QLabel("This is an official receipt of payment.\nPlease keep this for your records.")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setStyleSheet("""
            font-size: 13px;
            color: #6B7280;
            line-height: 1.6;
        """)
        note.setWordWrap(True)
        footer_layout.addWidget(note)

        # School info
        school_info = QLabel("Enrollify SHS • enrollify@edu.ph • (02) 1234-5678")
        school_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        school_info.setStyleSheet("""
            font-size: 12px;
            color: #9CA3AF;
            margin-top: 10px;
        """)
        school_info.setWordWrap(True)
        footer_layout.addWidget(school_info)

        return footer_layout

    def create_info_row(self, label, value):
        """Create an info row with proper wrapping"""
        row = QHBoxLayout()
        row.setSpacing(10)

        lbl = QLabel(label + ":")
        lbl.setStyleSheet("font-size: 14px; color: #6B7280; font-weight: 500;")
        lbl.setMinimumWidth(120)

        val = QLabel(str(value))
        val.setStyleSheet("font-size: 14px; color: #111827; font-weight: 600;")
        val.setWordWrap(True)
        val.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(val)

        return row

    def create_fee_row(self, label, amount, bold=False):
        """Create a fee row with proper alignment"""
        row = QHBoxLayout()
        row.setSpacing(10)

        lbl = QLabel(label)
        if bold:
            lbl.setStyleSheet("font-size: 15px; color: #111827; font-weight: 700;")
        else:
            lbl.setStyleSheet("font-size: 14px; color: #374151; font-weight: 500;")

        val = QLabel(f"₱{amount:,.2f}")
        if bold:
            val.setStyleSheet("font-size: 15px; color: #111827; font-weight: 700;")
        else:
            val.setStyleSheet("font-size: 14px; color: #111827; font-weight: 600;")

        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(val)

        return row

    def create_divider(self):
        """Create a divider line"""
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #E5E7EB; max-height: 1px;")
        return divider

    def get_payment_method_name(self, method):
        """Get readable payment method name"""
        methods = {
            'card': 'Credit/Debit Card',
            'ewallet': 'E-Wallet (GCash/PayMaya)',
            'bank': 'Bank Transfer'
        }
        return methods.get(method, 'Unknown Payment Method')

    def print_receipt(self):
        """Print the receipt"""
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            dialog = QPrintDialog(printer, self)

            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                # Render the receipt card
                self.receipt_card.render(printer)
                QMessageBox.information(self, "Success", "Receipt printed successfully!")
        except Exception as e:
            QMessageBox.critical(
                self,
                "Print Error",
                f"Failed to print receipt:\n{str(e)}\n\nPlease try saving as PDF instead."
            )
            print(f"Print error: {e}")

    def save_as_pdf(self):
        """Save receipt as PDF"""
        try:
            from PyQt6.QtWidgets import QFileDialog

            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Receipt",
                f"Receipt_{self.receipt_number}.pdf",
                "PDF Files (*.pdf)"
            )

            if filename:
                if not filename.endswith('.pdf'):
                    filename += '.pdf'

                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                printer.setOutputFileName(filename)

                # Render the receipt card
                self.receipt_card.render(printer)

                QMessageBox.information(
                    self,
                    "Success",
                    f"Receipt saved successfully!\n\n{filename}"
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Save Error",
                f"Failed to save receipt:\n{str(e)}\n\nError details: {type(e).__name__}"
            )
            print(f"Save error: {e}")
            import traceback
            traceback.print_exc()