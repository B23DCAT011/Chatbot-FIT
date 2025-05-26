from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
import shutil
import os
import re

def clean_text(text):
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)    # Ghép dòng bị ngắt sai
    text = re.sub(r"\n\s*\n", "\n", text)           # Xoá dòng trống
    text = re.sub(r"\s+", " ", text)                # Xoá khoảng trắng thừa
    return text.strip()

def reset_faiss_db(path):
    if os.path.exists(path):
        shutil.rmtree(path)  # Xóa toàn bộ dữ liệu FAISS cũ
        print(f"Đã xóa dữ liệu cũ tại {path}")

#biến
data_path = "data"  # Thư mục chứa các file PDF
vt_db_path = "vector_db/db_faiss"  # Đường dẫn lưu trữ DB FAISS

def create_db_from_text():
    raw ="""Nhằm đáp ứng nhu cầu và thị hiếu của khách hàng về việc sở hữu số tài khoản đẹp, dễ nhớ, giúp tiết kiệm thời gian, mang đến sự thuận lợi trong giao dịch. Ngân hàng Sài Gòn – Hà Nội (SHB) tiếp tục cho ra mắt tài khoản số đẹp 9 số và 12 số với nhiều ưu đãi hấp dẫn.
    Cụ thể, đối với tài khoản số đẹp 9 số, SHB miễn phí mở tài khoản số đẹp trị giá 880.000đ; giảm tới 80% phí mở tài khoản số đẹp trị giá từ 1,1 triệu đồng; phí mở tài khoản số đẹp siêu VIP chỉ còn 5,5 triệu đồng.
    Đối với tài khoản số đẹp 12 số, SHB miễn 100% phí mở tài khoản số đẹp, khách hàng có thể lựa chọn tối đa toàn bộ dãy số của tài khoản. Đây là một trong những điểm ưu việt của tài khoản số đẹp SHB so với thị trường. Ngoài ra, khách hàng có thể lựa chọn số tài khoản trùng số điện thoại, ngày sinh, ngày đặc biệt, hoặc số phong thủy mang lại tài lộc cho khách hàng trong quá trình sử dụng.
    Hiện nay, SHB đang cung cấp đến khách hàng 3 loại tài khoản số đẹp: 9 số, 10 số và 12 số. Cùng với sự tiện lợi khi giao dịch online mọi lúc mọi nơi qua dịch vụ Ngân hàng số, hạn chế rủi ro khi sử dụng tiền mặt, khách hàng còn được miễn phí chuyển khoản qua mobile App SHB, miễn phí quản lý và số dư tối thiểu khi sử dụng tài khoản số đẹp của SHB.
    Ngoài kênh giao dịch tại quầy, khách hàng cũng dễ dàng mở tài khoản số đẹp trên ứng dụng SHB Mobile mà không cần hồ sơ thủ tục phức tạp.
    Hướng mục tiêu trở thành ngân hàng số 1 về hiệu quả tại Việt Nam, ngân hàng bán lẻ hiện đại nhất và là ngân hàng số được yêu thích nhất tại Việt Nam, SHB sẽ tiếp tục nghiên cứu và cho ra mắt nhiều sản phẩm dịch vụ số ưu việt cùngchương trình ưu đãi hấp dẫn, mang đến cho khách hàng lợi ích và trải nghiệm tuyệt vời nhất.
    Để biết thêm thông tin về chương trình, Quý khách vui lòng liên hệ các điểm giao dịch của SHB trên toàn quốc hoặc Hotline *6688"""
    #tách văn bản
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=450,
        chunk_overlap=50,
        length_function=len
    )
    chunks = text_splitter.split_text(raw)

    embedding = GPT4AllEmbeddings(model_file="C:/Users/Admin/Desktop/RAG_demo/models/all-MiniLM-L6-v2-f16.gguf")  # Kiểm tra đường dẫn chính xác tới mô hình

    db = FAISS.from_texts(texts=chunks, embedding=embedding)
    db.save_local(vt_db_path)
    return db


def create_db_from_files():
    # Khai bao loader de quet toan bo thu muc dataa
    loader = DirectoryLoader(data_path, glob="*.pdf", loader_cls = PyPDFLoader)
    documents = loader.load()

    for doc in documents:
        doc.page_content = clean_text(doc.page_content)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    # Embeding
    embedding_model = GPT4AllEmbeddings(model_file="C:/Users/Admin/Desktop/RAG_demo/models/all-MiniLM-L6-v2-f16.gguf")
    db = FAISS.from_documents(chunks, embedding_model)
    db.save_local(vt_db_path)
    return db

print("1")
db = create_db_from_files()  # Chạy hàm tạo DB từ văn bản
print("debug")
