# Korean Mate — AI-Powered Korean Language Tutor

Korean Mate is an AI-powered Korean language learning assistant built using Python, Streamlit, and Hugging Face Inference Providers. It helps beginners learn Korean through translations, grammar explanations, vocabulary building, sentence correction, and interactive practice.

## ✨ Features

- 🌐 **Translate to Korean:** Translate words and sentences into Korean.
- 📚 **Grammar Explanations:** Understand Korean grammar in simple language.
- 💬 **Conversation Practice:** Practice everyday Korean conversations.
- ✍️ **Sentence Correction:** Identify and correct Korean sentence mistakes.
- 📖 **Vocabulary Learning:** Discover useful Korean words and expressions.
- 🧠 **Quiz Generator:** Test your Korean knowledge with practice questions.
- 🤖 **AI-Powered Responses:** Get explanations and learning assistance using a pretrained language model.
- 📱 **Responsive Web Interface:** Access the application through a web browser.

## 🛠️ Technologies Used

- **Python** — Application logic
- **Streamlit** — Interactive web interface
- **Hugging Face Inference Providers** — AI model inference
- **huggingface_hub** — Connect to Hugging Face models
- **python-dotenv** — Manage environment variables securely

## 📂 Project Structure

```text
Korean-Mate/
├── app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: The structure above represents the expected files. Keep only the files that actually exist in your project.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Kanika-Sharma-20/Korean-Mate.git
cd Korean-Mate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure your Hugging Face token

Create a `.env` file in the project directory and add your token:

```env
HF_TOKEN=your_huggingface_token_here
```

Replace the placeholder with your own Hugging Face access token.

**Security:** Never upload your `.env` file or expose your access token on GitHub.

### 4. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser. If it does not open automatically, visit:

`http://localhost:8501`

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `HF_TOKEN` | Hugging Face access token used for model inference |

## 🚀 Future Enhancements

- Deploy the application for public access.
- Improve the mobile user interface.
- Add pronunciation and listening exercises.
- Introduce user progress tracking.
- Add structured lessons for beginner, intermediate, and advanced learners.

## 🎯 Project Objective

The objective of Korean Mate is to make Korean language learning more accessible and interactive by combining a user-friendly web interface with AI-powered language assistance.

## 👩‍💻 Author

**Kanika Sharma**

GitHub: [Kanika-Sharma-20](https://github.com/Kanika-Sharma-20)

---

*Built with Python, Streamlit, and Hugging Face to make learning Korean easier and more interactive.*
