# 🧠 Contract Comparison & LLM Summary App

This Django web app compares two versions of contract files or text, highlights differences with color-coded diffs, and uses an LLM (via `Ollama`) to generate clause-wise summaries of changes.

---

## 🚀 Features

- 📄 Upload `.txt`, `.pdf`, or `.docx` files for comparison.

- 📊 View similarity score between documents.

- 🟥🟩🟨 Red/Green/Yellow color-coded diff:

  - 🟥 Removed

  - 🟩 Added

  - 🟨 Modified

- 🤖 LLM Summary for clause-level insights.

- 💾 Download PDF Report.

- 📜 History of previous comparisons.

---

## 🛠 Setup Instructions

### 1. Clone the Repo

git clone https://github.com/13virat/ContractChecker.git

cd contract_checker

2\. Create Virtual Environment

python -m venv venv

source venv/bin/activate  # Windows: venv\Scripts\activate

3\. Install Dependencies

pip install -r requirements.txt

4\. Apply Migrations

python manage.py migrate

5\. Run the Server

python manage.py runserver

🤖 LLM Integration

The app uses a local or remote Ollama model (e.g. LLaMA2, Mistral) to generate clause-level summaries.

Modify utils/ollama.py as needed to match your Ollama setup.

🗂 Project Structure

project/

│

├── templates/

│   ├── compare.html

│   ├── comparison_detail.html

│   ├── history.html

│   └── report_template.html

│

├── utils/

│   ├── extract_text.py

│   ├── clause_split.py

│   ├── clause_analyzer.py

│   └── ollama.py

│

├── views.py

├── models.py

├── urls.py

└── ...

📥 PDF Report

Click "⬇️ Download Report" to generate a PDF using weasyprint.

✅ To-Do

 Compare more than 2 versions

 Add clause-level risk classification

📃 License

MIT License

👨‍💻 Author

Made with ❤️ by [Virat Gupta]

---
