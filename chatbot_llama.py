# -*- coding: utf-8 -*-
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS

# Cấu hình đường dẫn
model_file = "C:/Users/Admin/Desktop/RAG_demo/models/vinallama-7b-chat_q5_0.gguf"
embedding_file = "C:/Users/Admin/Desktop/RAG_demo/models/all-MiniLM-L6-v2-f16.gguf"
vt_db_path = "vector_db/db_faiss"

# Prompt mẫu
template = """
Bạn là một trợ lý thông minh. Trả lời ngắn gọn, chính xác, dễ hiểu, và chỉ dùng thông tin trong phần {context} ở trên. 
Không suy đoán. Không lan man. Nếu câu hỏi là yêu cầu, hãy phản hồi lịch sự nhưng dứt khoát. Nếu người dùng chỉ cần xác nhận, hãy trả lời gọn và tự nhiên như: "Đã rõ!", "OK, tôi hiểu.", hoặc "Tôi sẽ thực hiện điều đó.".
Câu hỏi: {question}
"""
# Biến toàn cục
llm_chain = None

# Chỉ tạo prompt template một lần
def create_prompt(tmp):
    return PromptTemplate(template=tmp, input_variables=["context", "question"])

# Chỉ tạo QA chain khi cần
def init_llm_chain():
    global llm_chain
    print("🧠 Loading model and vector DB...")
    db = read_from_db()
    llm = load_model(model_file)
    prompt = create_prompt(template)
    llm_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={'prompt': prompt},
    )
    print("✅ LLM chain is ready.")

def load_model(model_file):
    return CTransformers(
        model=model_file,
        model_type="llama",
        max_new_tokens=256,
        temperature=0.01,
    )

def read_from_db():
    embedding = GPT4AllEmbeddings(model_file=embedding_file)
    db = FAISS.load_local(vt_db_path, embedding, allow_dangerous_deserialization=True)
    return db

def get_answer(question):
    init_llm_chain()
    result = llm_chain.invoke({"query": question})
    return result["result"]
