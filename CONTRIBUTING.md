# 🌟 Contributing to EventEase AI Bot

Hello there 👋 and thank you for your interest in contributing to **EventEase AI Bot**!  
We strongly believe that collaboration makes projects better, and every single contribution — whether it's fixing a typo, improving documentation, or adding a whole new feature — is valuable.  

This guide will help you understand how to **set up the project locally**, **run and test it**, and **contribute effectively**.  

---

## 🚀 Our Contribution Philosophy

We want EventEase AI Bot to be:  
- **Reliable** 🛡️ – code should be stable and well-tested.  
- **Accessible** 📖 – easy for new contributors to understand and run.  
- **Collaborative** 🤝 – open to new ideas and improvements.  

We value:  
- Clean, maintainable code.  
- Clear and up-to-date documentation.  
- Respectful and constructive collaboration.  

---

## 🛠️ Setting Up the Project Locally

Follow these steps to get started with development.

### 1️⃣ Fork & Clone the Repository
```bash
git clone https://github.com/<your-username>/EventEase-Ai-Bot.git
cd EventEase-Ai-Bot
```
👉 Always fork first! This keeps your work separate from the main repo.

---

### 2️⃣ Backend Setup (Python)
1. Navigate to backend folder:
   ```bash
   cd app
   ```

2. Create a **virtual environment** (isolates dependencies):
   ```bash
   python -m venv venv
   ```

3. Activate the environment:
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     venv\Scripts\activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

---

### 3️⃣ Frontend Setup (React)
1. Navigate to frontend folder:
   ```bash
   cd ../eventease-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

4. Open: `http://localhost:3000`  

---

### 4️⃣ Environment Variables
Secrets like API keys & DB connections live in `.env`.  
- Copy the example file:
  ```bash
  cp .env.production.example .env
  ```
- Fill in your values.

---

## 🧪 Running Tests

Before submitting contributions, make sure **all tests pass**.  

- Backend (Python / pytest):
  ```bash
  pytest
  ```

- Frontend (React / Jest):
  ```bash
  npm test
  ```

✅ Writing tests for new features is highly encouraged!

---

## 📌 Contribution Workflow

We follow the **GitHub Flow**:

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

   Use prefixes like:
   - `feature/...` → New features  
   - `fix/...` → Bug fixes  
   - `docs/...` → Documentation changes  

---

2. **Make your changes**
   - Follow coding conventions (PEP8 for Python, ES6+ for JS).  
   - Update documentation if needed.  
   - Add tests where applicable.  

---

3. **Commit changes**
   ```bash
   git commit -m "Add: new event reminder feature"
   ```
   ✅ Use clear, descriptive commit messages.  
   ✅ Reference issues if relevant (`Fixes #42`).  

---

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

---

5. **Open a Pull Request (PR)**
   - Clearly describe what you changed and why.  
   - Link related issues.  
   - Add screenshots if it’s a UI change.  

---

## ✅ Code Style Guidelines

- **Python (backend):** Follow [PEP8](https://peps.python.org/pep-0008/).  
- **JavaScript/React (frontend):** Use ES6+ syntax and meaningful variable names.  
- **Documentation:** Keep README and docs updated.  

---

## 🙋 Communication & Etiquette

- Use [GitHub Issues](../../issues) for bugs and feature requests.  
- Be respectful and constructive in reviews.  
- Collaboration > competition 💡  

---

## 📜 Code of Conduct

We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/).  
By participating, you help maintain a **welcoming and inclusive environment**.  

---

## 🎉 Final Words

Thank you for making **EventEase AI Bot** better!  
Your contributions — no matter how big or small — mean a lot to us. Let’s build something amazing together 🚀

---
