import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel,
    QPushButton, QTextEdit, QMessageBox
)
from db import create_tables, insert_teacher, insert_subject, insert_exam_schedule
from chatbot import handle_chatbot_input
from chatbot_llama import get_answer

# ==== Cửa sổ Chat LLaMA ====
class LlamaChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 Chatbot LLaMA")
        self.setFixedSize(400, 600)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("🦙 Chat với LLaMA:"))

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Nhập câu hỏi...")
        layout.addWidget(self.chat_input)

        send_btn = QPushButton("Gửi")
        send_btn.clicked.connect(self.send_message)
        layout.addWidget(send_btn)

        self.setLayout(layout)

    def send_message(self):
        user_text = self.chat_input.text().strip()
        if user_text == "":
            return
        self.chat_display.append(f"🧑 Bạn: {user_text}")
        self.chat_input.clear()
        reply = get_answer(user_text)

        self.chat_display.append(f"🦙 LLaMA: {reply}")


# ==== Cửa sổ tìm kiếm ====
class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tìm kiếm thông tin")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("🔍 Nhập ID giáo viên hoặc ID môn học để tìm kiếm:"))

        self.teacher_input = QLineEdit()
        self.teacher_input.setPlaceholderText("ID giáo viên")
        layout.addWidget(self.teacher_input)

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("ID môn học")
        layout.addWidget(self.subject_input)

        self.search_result = QTextEdit()
        self.search_result.setReadOnly(True)
        layout.addWidget(self.search_result)

        search_btn = QPushButton("Tìm kiếm")
        search_btn.clicked.connect(self.search)
        layout.addWidget(search_btn)

        self.setLayout(layout)

    def search(self):
        from db import get_teacher_by_id, get_sub_info_by_id
        teacher_id = self.teacher_input.text().strip()
        subject_id = self.subject_input.text().strip()

        result_text = ""

        if teacher_id:
            teacher = get_teacher_by_id(teacher_id)
            if teacher:
                result_text += teacher
            else:
                result_text += f"❌ Không tìm thấy giáo viên với ID: {teacher_id}\n\n"

        if subject_id:
            subject = get_sub_info_by_id(subject_id)
            if subject:
                result_text += subject
            else:
                result_text += f"❌ Không tìm thấy môn học với ID: {subject_id}\n\n"

        if not teacher_id and not subject_id:
            result_text = "⚠️ Vui lòng nhập ít nhất một ID để tìm kiếm."

        self.search_result.setPlainText(result_text)

# ==== Giao diện chính ====
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatBot FIT")
        self.setFixedSize(400, 700)
        self.initUI()

    def initUI(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        # ==== Khung Chatbot ====
        layout.addWidget(QLabel("💬 Chatbot hỗ trợ:"))
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Nhập câu hỏi...")
        layout.addWidget(self.chat_input)

        send_button = QPushButton("Gửi")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        # ==== Nhập giáo viên ====
        layout.addWidget(QLabel("👨‍🏫 Thêm giáo viên:"))

        self.teacher_id = QLineEdit()
        self.teacher_id.setPlaceholderText("ID giáo viên")
        layout.addWidget(self.teacher_id)

        self.teacher_name = QLineEdit()
        self.teacher_name.setPlaceholderText("Tên giáo viên")
        layout.addWidget(self.teacher_name)

        self.teacher_email = QLineEdit()
        self.teacher_email.setPlaceholderText("Email giáo viên")
        layout.addWidget(self.teacher_email)

        add_teacher_btn = QPushButton("Thêm giáo viên")
        add_teacher_btn.clicked.connect(self.save_teacher)
        layout.addWidget(add_teacher_btn)

        # ==== Nhập môn học ====
        layout.addWidget(QLabel("📘 Thêm môn học:"))

        self.subject_id = QLineEdit()
        self.subject_id.setPlaceholderText("ID môn học")
        layout.addWidget(self.subject_id)

        self.subject_name = QLineEdit()
        self.subject_name.setPlaceholderText("Tên môn học")
        layout.addWidget(self.subject_name)

        self.subject_teacher = QLineEdit()
        self.subject_teacher.setPlaceholderText("id giáo viên")
        layout.addWidget(self.subject_teacher)

        self.subject_material = QLineEdit()
        self.subject_material.setPlaceholderText("Tài liệu môn học (không bắt buộc)")
        layout.addWidget(self.subject_material)

        add_subject_btn = QPushButton("Thêm môn học")
        add_subject_btn.clicked.connect(self.save_subject)
        layout.addWidget(add_subject_btn)

        # ==== Nhập lịch thi ====
        layout.addWidget(QLabel("📅 Thêm lịch thi:"))

        self.exam_subject_id = QLineEdit()
        self.exam_subject_id.setPlaceholderText("ID môn học")
        layout.addWidget(self.exam_subject_id)

        self.exam_date = QLineEdit()
        self.exam_date.setPlaceholderText("Ngày thi (VD: 2025-05-30)")
        layout.addWidget(self.exam_date)

        add_exam_btn = QPushButton("Thêm lịch thi")
        add_exam_btn.clicked.connect(self.save_exam)
        layout.addWidget(add_exam_btn)

        # ==== Nút mở cửa sổ tìm kiếm ====
        search_window_btn = QPushButton("🔎 Tìm kiếm thông tin")
        search_window_btn.clicked.connect(self.open_search_window)
        layout.addWidget(search_window_btn)

        # ==== Nút mở chat LLaMA ====
        llama_chat_btn = QPushButton("🦙 Chat với LLaMA")
        llama_chat_btn.clicked.connect(self.open_llama_chat)
        layout.addWidget(llama_chat_btn)

        central.setLayout(layout)

    def send_message(self):
        user_text = self.chat_input.text().strip()
        if user_text == "":
            return
        self.chat_display.append(f"🧑 Bạn: {user_text}")
        reply = handle_chatbot_input(user_text)
        self.chat_display.append(f"🤖 Chatbot: {reply}")
        self.chat_input.clear()
        if user_text == '.clear':
            self.chat_display.clear()

    def save_teacher(self):
        id = self.teacher_id.text()
        name = self.teacher_name.text()
        email = self.teacher_email.text()
        if id and name and email:
            insert_teacher(id, name, email)
            QMessageBox.information(self, "Thành công", "Đã thêm giáo viên.")
            self.teacher_id.clear()
            self.teacher_name.clear()
            self.teacher_email.clear()
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đủ thông tin giáo viên.")

    def save_subject(self):
        id = self.subject_id.text()
        name = self.subject_name.text()
        teacher = self.subject_teacher.text()
        material = self.subject_material.text()
        if id and name and teacher and material:
            insert_subject(id, name, teacher, material)
            QMessageBox.information(self, "Thành công", "Đã thêm môn học.")
            self.subject_id.clear()
            self.subject_name.clear()
            self.subject_teacher.clear()
            self.subject_material.clear()
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đủ thông tin.")

    def save_exam(self):
        subject_id = self.exam_subject_id.text()
        date = self.exam_date.text()
        if subject_id and date:
            insert_exam_schedule(subject_id, date)
            QMessageBox.information(self, "Thành công", "Đã thêm lịch thi.")
            self.exam_subject_id.clear()
            self.exam_date.clear()
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền ID môn và ngày thi.")

    def open_search_window(self):
        self.search_window = SearchWindow()
        self.search_window.show()

    def open_llama_chat(self):
        self.llama_chat_window = LlamaChatWindow()
        self.llama_chat_window.show()

# ==== Chạy chương trình ====
if __name__ == "__main__":
    create_tables()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
