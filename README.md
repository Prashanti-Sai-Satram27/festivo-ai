# 🎉 Festivo AI

**Festivo AI** is an interactive chatbot that helps users explore festivals, holidays, and global observance days. Powered by Dify and deployed on Streamlit, this app delivers a conversational experience with a clean UI and real-time responses.

![Festivo AI Banner](./logo.png)

---

## 🚀 Live Demo

👉 [Click to Try Festivo AI](https://festivo-ai-wmfdyb69sjeccgxoyxtrhc.streamlit.app/)

---

## ✨ Features

- 🗨️ Chat interface with user & assistant message bubbles
- 🎊 Festivo AI logo always visible in the header
- 💬 Starter questions for quick interactions
- 👍 👎 Feedback buttons with optional comments
- 🆕 "+ New Chat" button in sidebar to reset session
- 🌍 Ask about festivals, observance days, and global events
- 💡 Fully responsive & styled using custom CSS

---

## 📁 Project Structure

```
📦festivo-ai/
├── app.py                  # Main Streamlit application
├── .streamlit/
│   └── secrets.toml        # API keys and configuration
├── logo.png                # App logo for branding
├── requirements.txt        # Dependencies
└── README.md               # You're here!
```

---

## 🔐 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/festivo-ai.git
cd festivo-ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Secrets
Create a `.streamlit/secrets.toml` file and add your Dify API credentials:
```toml
DIFY_API_KEY = "your-dify-api-key"
DIFY_CHAT_URL = "https://api.dify.ai/v1/chat-messages"
DIFY_FEEDBACK_URL_TEMPLATE = "https://api.dify.ai/v1/messages/{message_id}/feedbacks"
```

### 4. Run Locally
```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push your code to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) → `New App`.
3. Connect your repo and branch.
4. Add secrets in the `Secrets` tab.
5. Click **Deploy** 🚀

---

## 📦 Requirements

- Python 3.8+
- Streamlit
- Requests
- Dify API Key

---

## 🙌 Credits

Built by [Your Name] using:
- [Streamlit](https://streamlit.io/)
- [Dify.ai](https://dify.ai/)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Connect

Have feedback or want to contribute? Feel free to open issues or pull requests!  
📧 sprashantisai@gmail.com 
