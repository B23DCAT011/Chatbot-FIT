# 🎓 Chatbot Hỗ Trợ Sinh Viên Học Tập

Một chatbot AI hỗ trợ sinh viên tra cứu thông tin học tập như điểm số, môn học, lịch học,... qua giao diện đồ họa PyQt6. Ứng dụng sử dụng mô hình ngôn ngữ LLaMA kết hợp với cơ sở dữ liệu SQLite để xử lý câu hỏi và truy xuất dữ liệu.

## 🚀 Tính Năng

- 💬 Giao tiếp tự nhiên với chatbot AI
- 📚 Tra cứu điểm số, môn học, lịch học và thông tin sinh viên
- 🧠 Tích hợp mô hình LLaMA để hiểu ngôn ngữ tự nhiên
- 🖥️ Giao diện đồ họa thân thiện với PyQt6
- 🗃️ Lưu trữ dữ liệu bằng cơ sở dữ liệu SQLite

## 🛠️ Công Nghệ Sử Dụng

- [x] Python 3.10+
- [x] PyQt6
- [x] SQLite
- [x] vinallama-7b-chat_q5_0
- [x] LangChain

## 🗂️ Cấu Trúc Dự Án
ChatBot_FIT/

│

├── assets/ # Hình ảnh, icon, hoặc tệp giao diện

├── data/ # Dữ liệu gốc hoặc tệp dữ liệu cần xử lý

├── vector_db/ # Thư mục xử lý dữ liệu vector cho LLM

│ └── preparevectordb.py # Tạo vector db từ dữ liệu gốc ở data

│
├── chatbot.py # Chatbot cơ bản

├── chatbot_llama.py # Chatbot dùng mô hình LLaMA

├── db.py # Quản lý kết nối và thao tác với SQLite

├── main.py # Điểm khởi chạy ứng dụng (PyQt6)

├── QT.py # Tệp tạo giao diện người dùng (PyQt6)

├── Test.py # Tệp test thử chatbot hoặc giao diện

├── student_management.db # Cơ sở dữ liệu SQLite chính

├── README.md # Tệp mô tả dự án

## ⚙️ Cài Đặt

### 1. Clone project
```bash
git clone https://github.com/B23DCAT011/Chatbot-FIT.git
cd Chatbot-FIT

python -m venv venv
source venv/bin/activate  # Hoặc venv\Scripts\activate nếu dùng Windows

python QT.py
```
## TM
https://docs.google.com/document/d/1UUTHQFXbq8wJ96SXdcqQ9kB1ISYCAuKcUjUEb1qdiNo/edit?tab=t.0