
from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from typing import List, Optional

# ===== 创建 agent（带记忆）=====
agent = create_agent(
    "deepseek-v4-flash",
    checkpointer=InMemorySaver(),
)

# ===== FastAPI 后端 =====
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    thread_id: str = "thread_1"


def read_file_content(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    if ext == '.txt' or ext == '.md':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == '.pdf':
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                return '\n'.join([page.extract_text() or '' for page in pdf.pages])
        except:
            return f"[PDF文件: {Path(file_path).name}]"
    elif ext == '.docx':
        try:
            import docx
            doc = docx.Document(file_path)
            return '\n'.join([para.text for para in doc.paragraphs])
        except:
            return f"[DOCX文件: {Path(file_path).name}]"
    else:
        return f"[不支持的文件类型: {ext}]"


@app.post("/chat")
def chat(req: ChatRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    response = agent.invoke(
        {"messages": [HumanMessage(content=req.message)]},
        config,
    )
    reply = response["messages"][-1].content
    return {"reply": reply}


@app.post("/chat/upload")
async def chat_with_upload(
    message: str = Form(""),
    thread_id: str = Form("thread_1"),
    files: List[UploadFile] = File(...)
):
    file_contents = []
    for file in files:
        content = await file.read()
        temp_path = Path(f"temp_{file.filename}")
        with open(temp_path, "wb") as f:
            f.write(content)
        file_content = read_file_content(str(temp_path))
        file_contents.append(f"【{file.filename}】:\n{file_content}")
        temp_path.unlink()
    
    full_message = message
    if file_contents:
        doc_context = "\n\n".join(file_contents)
        full_message = f"{message}\n\n---文档内容---\n{doc_context}" if message else f"请分析以下文档:\n\n{doc_context}"
    
    config = {"configurable": {"thread_id": thread_id}}
    response = agent.invoke(
        {"messages": [HumanMessage(content=full_message)]},
        config,
    )
    reply = response["messages"][-1].content
    return {"reply": reply}


@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
