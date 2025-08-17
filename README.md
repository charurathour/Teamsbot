# 🤖 Teamsbot - Software Installation Assistant

## Video Link 
https://drive.google.com/file/d/1a4Wf237mxQOd7GslngRsiFpR8-8uvLad/view?usp=sharing

A **Streamlit + LangGraph + Groq-powered chatbot** that automates software installation requests.  
It follows an **agentic workflow** where the LLM can decide when to call tools for handling tasks.

---

## ✨ Features
- 💬 Conversational AI (Groq + LangGraph)
- 🛠️ **Tool calls**:
  - Install requested software
  - Create/update installation tickets
  - Write logs to **SQLite DB** & **ticket request CSV**
- ✅ Final confirmation message to user

---

## ⚙️ Setup
1. Clone repo & create virtual environment  
2. Install dependencies  
   ```bash
   pip install -r requirements.txt

3. add .env
  GROQ_API_KEY=your_api_key_here
  EXCEL_PATH=./tickets.xlsx
  DB_PATH=./installations.db

  ## Run
  streamlit run app.py
