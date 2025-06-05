from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QPushButton, QComboBox, QDateEdit
)
from PySide6.QtCore import QDate, Signal


class AddTransactionForm(QDialog):
    transaction_added = Signal(dict)  # Signal to emit data

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Transaction")
        self.setMinimumSize(300, 300)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("dd-MM-yyyy")

        self.type_input = QComboBox()
        self.type_input.addItems(["Income", "Expense"])

        self.category_input = QComboBox()
        self.category_input.addItems(["Food", "Bills", "Salary", "Entertainment", "Other"])

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")

        self.note_input = QTextEdit()
        self.note_input.setPlaceholderText("Add a note...")

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.handle_submit)

        form_layout.addRow("Date:", self.date_input)
        form_layout.addRow("Type:", self.type_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Amount:", self.amount_input)
        form_layout.addRow("Note:", self.note_input)

        layout.addLayout(form_layout)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

    def handle_submit(self):
        transaction_data = {
            "date": self.date_input.date().toString("dd-MM-yyyy"),
            "type": self.type_input.currentText(),
            "category": self.category_input.currentText(),
            "amount": self.amount_input.text(),
            "note": self.note_input.toPlainText()
        }

        self.transaction_added.emit(transaction_data)  # Emit the signal
        self.close()
