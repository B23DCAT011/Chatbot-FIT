import sqlite3

# Kết nối đến database
conn = sqlite3.connect('student_management.db')
cursor = conn.cursor()

# Lấy dữ liệu từ bảng teachers
cursor.execute("SELECT * FROM teachers")
giao_vien = cursor.fetchall()

# Lấy dữ liệu từ bảng subjects
cursor.execute("SELECT * FROM subjects")
mon_hoc = cursor.fetchall()

# Lấy dữ liệu từ bảng exam_schedule
cursor.execute("SELECT * FROM exam_schedule")
lich_thi = cursor.fetchall()

conn.close()

# ==== CHUẨN HÓA DỮ LIỆU ====

# Tạo ánh xạ ID giáo viên -> tên
gv_dict = {str(gv[0]): gv[1] for gv in giao_vien}  # ID có thể là int

# In ra danh sách giáo viên
print("Danh sách Giáo viên\n")
for gv in giao_vien:
    print(f"ID: {gv[0]} - Tên: {gv[1]} - Email: {gv[2]}")
print()

# In ra danh sách môn học
print("Danh sách Môn học\n")
for mh in mon_hoc:
    ma_mh, ten_mh, tailieu, id_gv = mh
    ten_gv = gv_dict.get(str(id_gv), "Không rõ")
    print(f"Môn học có mã {ma_mh}, tên là \"{ten_mh}\", tài liệu: {tailieu}, được giảng dạy bởi giáo viên {ten_gv}.")
print()

# Tạo ánh xạ mã môn -> tên môn
mh_dict = {mh[0]: mh[1] for mh in mon_hoc}

# In ra lịch thi
print("Lịch thi\n")
for lt in lich_thi:
    _, ma_mh, ngay_thi = lt
    ten_mh = mh_dict.get(ma_mh, "Không rõ")
    print(f"Môn \"{ten_mh}\" (mã {ma_mh}) sẽ thi vào ngày {ngay_thi}.")
