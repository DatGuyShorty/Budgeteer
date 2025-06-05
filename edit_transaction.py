from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QComboBox, QPushButton, QDateEdit
from PySide6.QtCore import QDate, Signal

class EditTransactionForm(QDialog):
    transaction_edited = Signal(dict)
    def __init__(self, transaction_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Transaction")
        self.transaction_id = transaction_data[0]  # ID from the DB

        layout = QVBoxLayout()
        form = QFormLayout()

        # Pre-fill data
        self.date_input = QDateEdit()
        self.date_input.setDisplayFormat("dd-MM-yyyy")
        qdate = QDate.fromString(transaction_data[1], "dd-MM-yyyy")
        self.date_input.setDate(qdate)

        self.type_input = QComboBox()
        self.type_input.addItems(["Income", "Expense"])
        self.type_input.setCurrentText(transaction_data[2].capitalize())

        self.category_input = QComboBox()
        self.category_input.addItems(["Food", "Bills", "Salary", "Entertainment", "Other"])
        self.category_input.setCurrentText(transaction_data[3])

        self.amount_input = QLineEdit(str(transaction_data[4]))
        self.note_input = QTextEdit(transaction_data[5])

        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.handle_submit)

        # Build layout
        form.addRow("Date:", self.date_input)
        form.addRow("Type:", self.type_input)
        form.addRow("Category:", self.category_input)
        form.addRow("Amount:", self.amount_input)
        form.addRow("Note:", self.note_input)

        layout.addLayout(form)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def handle_submit(self):
        transaction_data = {
            "date": self.date_input.date().toString("dd-MM-yyyy"),
            "type": self.type_input.currentText(),
            "category": self.category_input.currentText(),
            "amount": self.amount_input.text(),
            "note": self.note_input.toPlainText(),
            "id": self.transaction_id
        }

        self.transaction_edited.emit(transaction_data)  # Emit the signal
        self.close()
