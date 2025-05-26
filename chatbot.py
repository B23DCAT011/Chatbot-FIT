# chatbot_logic.py
from db import get_all_subjects,get_teacher_by_name,get_sche_by_sub,get_material_by_sub,get_teacher_by_id,get_sub_info_by_name
from db import get_sub_info_by_id
def handle_chatbot_input(user_input):
    user_input = user_input.lower()

    greetings = ["xin chào", "chào", "hi", "hello", "hey"]
    for greet in greetings:
        if greet in user_input:
            return "👋 Chào bạn! Mình là trợ lý quản lý sinh viên. Bạn cần hỏi gì nào?"
    # Hỏi thông tin giáo viên theo tên
    if "giáo viên" in user_input and "id" not in user_input:
        name = user_input.split("giáo viên")[-1].strip()
        return get_teacher_by_name(name)

    # Hỏi thông tin giáo viên theo id
    elif "giáo viên" in user_input and "id" in user_input:
        id_part = user_input.split("id")[-1].strip()
        return get_teacher_by_id(id_part)

    # Hỏi thông tin môn học theo tên
    elif "thông tin môn" in user_input and "id" not in user_input:
        name = user_input.split("môn")[-1].strip()
        return get_sub_info_by_name(name)

    # Hỏi thông tin môn học theo id
    elif "thông tin môn" in user_input and "id" in user_input:
        sub_id = user_input.split("id")[-1].strip()
        return get_sub_info_by_id(sub_id)

    # Hỏi lịch thi theo tên môn
    elif "lịch thi" in user_input:
        name = user_input.split("thi")[-1].strip()
        return get_sche_by_sub(name)

    # Hỏi tài liệu môn học
    elif "tài liệu môn" in user_input:
        name = user_input.split("môn")[-1].strip()
        return get_material_by_sub(name)
    elif "tài liệu" in user_input:
        name = user_input.split("liệu")[-1].strip()
        return get_material_by_sub(name)


    # Hỏi danh sách tất cả môn học
    elif "danh sách môn học" in user_input or "các môn học" in user_input:
        return get_all_subjects()

    # Mặc định nếu không hiểu
    else:
        return "❓ Xin lỗi, tôi chưa hiểu yêu cầu của bạn. Bạn có thể hỏi về giáo viên, môn học, lịch thi hoặc tài liệu môn học."
