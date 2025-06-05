import sqlite3
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel, QPushButton, QHBoxLayout
)
from add_transaction import AddTransactionForm  # Assuming add_transaction.py is in the same directory
from edit_transaction import EditTransactionForm
class TransactionViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaction Viewer")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        layout.addWidget(QLabel("All Transactions:"))
        layout.addWidget(self.table)
        self.setLayout(layout)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.load_data)
        add_entry_button = QPushButton("Add transaction")
        add_entry_button.clicked.connect(self.open_add_transaction_form)

        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.addWidget(add_entry_button)
        button_layout.addWidget(refresh_button)
        layout.addWidget(button_widget)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("budget.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        rows = cursor.fetchall()

        headers = [description[0] for description in cursor.description]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(headers) + 1)  # One for edit, one for delete
        self.table.setHorizontalHeaderLabels(headers + ["Edit / Delete"])

        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_index, col_index, item)
                
                # Create buttons
                edit_button = QPushButton("Edit")
                delete_button = QPushButton("Delete")

                # Capture transaction ID and row correctly
                transaction_id = row_data[0]
                edit_button.clicked.connect(lambda _, row=row_data: self.edit_transaction(row,id))
                delete_button.clicked.connect(lambda _, id=transaction_id: self.delete_transaction(id))

                # Create a widget to hold both buttons
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.addWidget(edit_button)
                action_layout.addWidget(delete_button)
                action_layout.setContentsMargins(0, 0, 0, 0)  # Remove spacing around buttons

                # Place the widget into the last column
                self.table.setCellWidget(row_index, len(row_data), action_widget)

        conn.close()  

    def delete_transaction(self,id):
        print("Deleting transaction ID:", id)
        conn = sqlite3.connect("budget.db")
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM transactions WHERE id = {id}")
        conn.commit()
        conn.close()
        self.load_data()
        
    def edit_transaction(self, row):
        print("Edit transaction:", row)
        # Here you would implement the logic to edit a transaction

    
    def open_add_transaction_form(self):
        form = AddTransactionForm()
        form.transaction_added.connect(self.add_transaction_to_db)
        form.exec()

    def add_transaction_to_db(self, data):
        conn = sqlite3.connect("budget.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (date, type, category, amount, note)
            VALUES (?, ?, ?, ?, ?)
        """, (data["date"], data["type"], data["category"], data["amount"], data["note"]))
        conn.commit()
        conn.close()
        self.load_data()

    def edit_transaction_in_db(self, data):
        conn = sqlite3.connect("budget.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE transactions
            SET date = ?, type = ?, category = ?, amount = ?, note = ?
            WHERE id = ?
        """, (data["date"], data["type"], data["category"], data["amount"], data["note"], data["id"]))
        conn.commit()
        conn.close()
        self.load_data()

    def edit_transaction(self, row_data, id):
        form = EditTransactionForm(row_data, self)
        form.transaction_edited.connect(self.edit_transaction_in_db, id)
        form.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = TransactionViewer()
    viewer.show()
    sys.exit(app.exec())