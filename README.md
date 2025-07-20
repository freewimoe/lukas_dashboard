
````markdown
# Lukas Dashboard 🕊️

A Streamlit-based web application built for the *Wir für Lukas* association to manage and visualize church, community, and cultural engagement data.  
This project is part of the **Portfolio Project 5** (PP5) in the Code Institute Full-Stack Software Development program.

---

## 📌 Project Purpose

The goal of this dashboard is to support the long-term use and sustainability of the Lukaskirche (Karlsruhe) as a multifunctional space for:

- 🙏 Church activities  
- 🏘️ Local community engagement  
- 🎭 Cultural programming and events

With tailored logins, each user group can view or manage specific aspects of the data.

---

## 🧩 Features

- 🔐 **Role-based Login System** using `streamlit-authenticator`
- 🗂️ Modular Page Structure:
  - `1_Kultur.py` – cultural programming
  - `2_Kirche.py` – church and parish activities
  - `3_Quartier.py` – neighborhood services and outreach
  - `4_Community.py` – general community tools
- 📁 Secure config with hashed passwords via `authenticator.yaml`
- 💾 Future expansion: PostgreSQL or SQLite-based data logging
- 🌐 Ready for deployment on Render or Hugging Face Spaces

---

## 🔒 Login Roles

```yaml
admin_user:
  role: admin
kultur_maria:
  role: kultur
quartier_hans:
  role: quartier
````

Access to dashboard pages is restricted by user role.
Admins see everything, other roles only relevant content.

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/freewimoe/lukas_dashboard.git
cd lukas_dashboard
```

### 2. Create virtual environment

```bash
python -m venv venv
.\venv\Scripts\activate  # on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Streamlit

```bash
streamlit run streamlit_app.py
```

---

## 📁 Project Structure

```plaintext
lukas_dashboard/
├── config/
│   └── authenticator.yaml         ← hashed passwords + user roles
├── pages/
│   ├── 1_Kultur.py
│   ├── 2_Kirche.py
│   ├── 3_Quartier.py
│   └── 4_Community.py
├── streamlit_app.py               ← main app with page routing
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📈 Roadmap

* [ ] Data logging (e.g. attendance, feedback, interactions)
* [ ] Admin dashboard with statistics
* [ ] Export functions (CSV, PDF)
* [ ] Upload zone for local groups
* [ ] Public dashboard (read-only version)

---

## ✍️ Author

**Friedrich-Wilhelm Möller**
[Wir für Lukas](https://wir-fuer-lukas.de)
Karlsruhe, Germany
GitHub: [freewimoe](https://github.com/freewimoe)

---

## 🧠 License

This project is for educational and community purposes.
Please contact the author before reuse or redistribution.

```

```
