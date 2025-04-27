# AshaAI

AshaAI is an intelligent conversational AI platform built with React (frontend) and FastAPI (backend), leveraging RAG (Retrieval Augmented Generation) techniques, web search, and vector databases for enriched responses.

---

## ✨ Tech Stack

- **Frontend**: React.js
- **Backend**: FastAPI (Python)
- **Database**: MongoDB (for session and chat history)
- **Vector Database**: Nano VectorDB
- **Knowledge Graph**: Integrated with VectorDB
- **Web Search Engine**: Tavily API
- **RAG Strategy**: Path RAG (combines vector and graph knowledge)
- **Task Scheduling**: Background thread for asynchronous vector DB updates

---

## 🛠 Features

- **Context-Aware Chat**:  
  Each new user query is rephrased by considering the last 5 queries to maintain context.
  
- **Enhanced Retrieval**:  
  Uses both **Vector Search** and **Knowledge Graph Search** for better information retrieval.

- **Web Search Augmentation**:  
  Integrates Tavily web search results with RAG output to further improve response accuracy.

- **Background Data Ingestion**:  
  New web search results are asynchronously pushed into the vector database without delaying the user response.

- **Scalable and Modular**:  
  Separate modules for agents, RAG, database operations, and search ingestion.

---

## 📚 Full Chat Flow

1. **User submits a new query**.
2. **Backend loads** the past 5 queries for context.
3. **Agent rephrases** the current query based on history.
4. **Information is retrieved** from:
   - VectorDB + Knowledge Graph (via Path RAG)
   - Tavily Web Search
5. **All results are merged** into a structured JSON file.
6. **Response is rephrased nicely** and sent back to the user.
7. **In parallel**, a background task pushes new search results into Nano VectorDB.

---

## ⚙️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/BharatiPatra/Asha_ai-chatbot.git
cd AshaAI/chat_bot_final
```

### 2. Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

### 3. Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🗂 Project Structure

```
AshaAI/chat_bot_final
├── backend/
│   ├── agents/
│   ├── db/
│   ├── rag/
│   ├── scheduler/
│   └── app/main.py
├── frontend/
│   └── (React app)
├── README.md

```

---

## 📈 Future Improvements

- [ ] Fine-tune RAG models with domain-specific knowledge.
- [ ] Add real-time updates when background ingestion finishes.
- [ ] Integrate authentication and user profiles.

---

## 🤝 Contributions

Contributions, issues, and feature requests are welcome!

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## ✨ Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [ReactJS](https://react.dev/)
- [Nano VectorDB](https://nanovdb.dev/)
- [Tavily API](https://tavily.com/)
- [Path RAG Techniques](https://arxiv.org/abs/2310.06927)
