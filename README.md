# 🌍 GlobEx: Global Economy Bot Template

GlobEx is a professional, modular Discord economy bot template. Unlike standard bots, GlobEx uses a **Global Economy** model—meaning a user's balance follows them across every server that uses the bot.

---

## 🛠️ Phase 1: Prerequisites

Before you begin, ensure you have the following installed:
* Python 3.8 or higher
* Git
* A Discord Bot Token (Get one at the Discord Developer Portal)

---

## 🚀 Phase 2: Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mrpandolaofficial-art/GlobEx.git
```

### 2. Navigate to the Directory
```bash
cd GlobEx
```

### 3. Create a Virtual Environment
```bash
python3 -m venv venv
```
Make sure you activate the .venv
```bash
source venv/bin/activate
```

### 4. Install Requirements
```bash
pip install -r requirements.txt
```

---

## ⚙️ Phase 3: Configuration

### 1. Set Up Environment Variables
Rename `env.example` to `.env`.

### 2. Add Your Token
Open the `.env` file and paste:
```env
DISCORD_TOKEN=your_token_here
```

---

## 🎮 Phase 4: Running the Bot

To start GlobEx, run:
```bash
python3 main.py
```

---

## 📜 Available Commands

| Command | Description | Cooldown |
| :--- | :--- | :--- |
| !balance | Check your wallet and bank. | None |
| !beg | Ask for some spare change. | 30s |
| !work | Work a job for higher pay. | 1h |
| !pay @user | Transfer money to another player. | None |
| !slots | Gamble your money (1x, 2x, or 5x). | None |
| !leaderboard | See the top 10 richest players. | None |