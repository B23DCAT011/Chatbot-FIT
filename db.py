import sqlite3

from main import cursor


def create_connection():
    conn = sqlite3.connect("student_management.db")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Bật hỗ trợ khóa ngoại trong SQLite (bắt buộc)
    cursor.execute("PRAGMA foreign_keys = ON")

    # Bảng giáo viên
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    # Bảng môn học
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            material TEXT,
            teacher_id TEXT NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
    """)

    # Bảng lịch thi
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exam_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
    """)

    conn.commit()
    conn.close()



def get_teacher_by_name(teacher_name):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Tìm giáo viên gần đúng theo tên
        cursor.execute("SELECT id, name, email FROM teachers WHERE name LIKE ?", ('%' + teacher_name + '%',))
        teacher = cursor.fetchone()

        if not teacher:
            return f"❌ Không tìm thấy giáo viên tên gần giống '{teacher_name}'."

        teacher_id = teacher[0]
        teacher_name = teacher[1]
        teacher_email = teacher[2]

        # Tìm các môn học giáo viên này dạy dựa trên id
        cursor.execute("SELECT id, name FROM subjects WHERE teacher_id = ?", (teacher_id,))
        subjects = cursor.fetchall()

        if not subjects:
            subject_info = "Chưa có môn học nào."
        else:
            subject_info = "\n".join([f"- {s[0]}: {s[1]}" for s in subjects])

        return f"""📘 Thông tin giáo viên:
👤 Họ tên: {teacher_name}
📧 Email: {teacher_email}
📚 Môn học đang dạy:
{subject_info}"""

    except sqlite3.Error as e:
        return f"Lỗi truy vấn cơ sở dữ liệu: {e}"
    finally:
        conn.close()
def get_teacher_by_id(id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Tìm giáo viên gần đúng theo tên
        cursor.execute("SELECT id, name, email FROM teachers WHERE id LIKE ?", ('%' + id+ '%',))
        teacher = cursor.fetchone()

        if not teacher:
            return f"❌ Không tìm thấy giáo viên có id {id}."

        teacher_id = teacher[0]
        teacher_name = teacher[1]
        teacher_email = teacher[2]

        # Tìm các môn học giáo viên này dạy dựa trên id
        cursor.execute("SELECT id, name FROM subjects WHERE teacher_id = ?", (teacher_id,))
        subjects = cursor.fetchall()

        if not subjects:
            subject_info = "Chưa có môn học nào."
        else:
            subject_info = "\n".join([f"- {s[0]}: {s[1]}" for s in subjects])

        return f"""📘 Thông tin giáo viên:
👤 Họ tên: {teacher_name}
📧 Email: {teacher_email}
📚 Môn học đang dạy:
{subject_info}"""

    except sqlite3.Error as e:
        return f"Lỗi truy vấn cơ sở dữ liệu: {e}"
    finally:
        conn.close()

def get_sche_by_sub(sub_name):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Tìm môn học theo tên
        cursor.execute("SELECT id FROM subjects WHERE name LIKE ?", ('%' + sub_name + '%',))
        sub = cursor.fetchone()

        if not sub:
            return f"Không tìm thấy môn học nào có tên chứa '{sub_name}'."

        sub_id = sub[0]

        # Tìm lịch thi dựa trên id môn học
        cursor.execute("SELECT exam_date FROM exam_schedule WHERE subject_id = ?", (sub_id,))
        schedule = cursor.fetchone()

        if not schedule:
            schedule_info = f"Môn '{sub_name}' hiện chưa có lịch thi."
        else:
            exam_date = schedule[0]
            schedule_info = f"Lịch thi môn '{sub_name}': {exam_date}."

    except sqlite3.Error as e:
        return f"Lỗi truy vấn cơ sở dữ liệu: {e}"

    finally:
        conn.close()

    return schedule_info
def get_material_by_sub(sub_name):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Tìm môn học theo tên
        cursor.execute("SELECT material FROM subjects WHERE name LIKE ?", ('%' + sub_name + '%',))
        link = cursor.fetchone()
        if not link:
            return f"Không tìm thấy môn học nào có tên '{sub_name}'."

        material_info = f'Tài liệu môn học nằm ở link sau: {link}'
    except sqlite3.Error as e:
        return f"Lỗi truy vấn cơ sở dữ liệu: {e}"

    finally:
        conn.close()

    return material_info

def get_sub_info_by_id(sub_id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Tìm giáo viên gần đúng theo tên
        cursor.execute("SELECT id, name, material,teacher_id FROM subjects WHERE id LIKE ?", ('%' + sub_id + '%',))
        sub = cursor.fetchone()

        if not sub:
            return f"❌ Không tìm thấy môn học id {sub_id}."

        sub_id = sub[0]
        sub_name = sub[1]
        material = sub[2]
        teacher_id = sub[3]

        return f"""📘 Thông tin môn học:
            ID:{sub_id}
            Tên môn học: {sub_name}
            Tài liệu: {material}
            ID giáo viên giảng dạy: {teacher_id}"""

    except sqlite3.Error as e:
        return f"Lỗi truy vấn cơ sở dữ liệu: {e}"
    finally:
        conn.close()
def get_sub_info_by_name(sub_name):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Tìm giáo viên gần đúng theo tên
        cursor.execute("SELECT id, name, material,teacher_id FROM subjects WHERE name LIKE ?", ('%' + sub_name + '%',))
        sub = cursor.fetchone()

        if not sub:
            return f"❌ Không tìm thấy môn học tên {sub_name}."

        sub_id = sub[0]
        sub_name = sub[1]
        material = sub[2]
        teacher_id = sub[3]

        return f"""📘 Thông tin môn học:
        ID:{sub_id}
        Tên môn học: {sub_name}
        Tài liệu: {material}
        ID giáo viên giảng dạy: {teacher_id}"""

    except sqlite3.Error as e:
        return f"Lỗi truy vấn cơ sở dữ liệu: {e}"
    finally:
        conn.close()
def get_all_subjects():
    conn = sqlite3.connect('student_management.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM subjects")
    subjects = cursor.fetchall()
    conn.close()

    if not subjects:
        return "Hiện tại chưa có môn học nào trong hệ thống."

    response = "📚 Các môn học trong kỳ này gồm:\n"
    for sub in subjects:
        response += f"🔹 {sub[0]} - {sub[1]}\n"
    return response.strip()


#Phần thêm thông tin
def insert_teacher(id, name, email):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teachers WHERE id = ?", (id,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("UPDATE teachers SET name = ?, email = ? WHERE id = ?", (name, email, id))
    else:
        cursor.execute("INSERT INTO teachers (id, name, email) VALUES (?, ?, ?)", (id, name, email))

    conn.commit()
    conn.close()
def insert_subject(id, name, teacher_id, material):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects WHERE id = ?", (id,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("UPDATE subjects SET name = ?, teacher_id = ?, material = ? WHERE id = ?",
                       (name, teacher_id, material, id))
    else:
        cursor.execute("INSERT INTO subjects (id, name, teacher_id, material) VALUES (?, ?, ?, ?)",
                       (id, name, teacher_id, material))

    conn.commit()
    conn.close()
def insert_exam_schedule(subject_id, exam_date):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM exam_schedule WHERE subject_id = ?", (subject_id,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("UPDATE exam_schedule SET exam_date = ? WHERE subject_id = ?", (exam_date, subject_id))
    else:
        cursor.execute("INSERT INTO exam_schedule (subject_id, exam_date) VALUES (?, ?)", (subject_id, exam_date))

    conn.commit()
    conn.close()

