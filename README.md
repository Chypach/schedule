## 🤖 Modular Telegram Schedule Bot

This repository contains the source code for a modular Telegram bot designed to streamline the academic scheduling process for university students. By replacing cumbersome manual tracking of week parity and navigation of static PDF schedules with an interactive interface, this bot significantly enhances operational efficiency and user quality of life (QoL).

The system is built on a layered architecture in Python, leveraging asynchronous programming (`aiogram`) and an embedded database (`sqlite3`) for persistent user personalization.

---

## ✨ Features

The bot fulfills several core objectives to provide a robust and personalized scheduling experience:

* **📅 Daily & Weekly Schedule Retrieval:** Instantly retrieve the schedule for the current day, the next day, or the entire academic week.
* **🔄 Automated Parity Calculation:** Reliably calculates the current academic week parity (even/odd) to ensure schedule accuracy.
* **🧑‍💻 User Personalization:** Persistently stores and applies the user's specific English language sub-group assignment (Group 1 or 2).
* **🌐 Bilingual Interface:** Supports a switchable user interface and response messages in both **Russian** and **English**.
* **💾 Persistent Configuration:** Uses an SQLite database to store user preferences (`user_id`, preferred language, and group number).
* **🔑 Interactive UI:** Utilizes both **Reply Keyboards** (for primary commands) and **Inline Keyboards** (for dynamic configuration like group selection).

---

## 🏗️ System Architecture

The project employs a clean, layered, modular architecture based on the Single Responsibility Principle, ensuring high maintainability and clarity.

| Module | Responsibility | Key Technologies |
| :--- | :--- | :--- |
| **`Main.py`** | Core Application Logic, Control Flow, Dispatcher Initialization, User Input Processing. | `aiogram`, `asyncio`, `tracemalloc` |
| **`SQL.py`** | Data Persistence Layer. Manages user configuration (language, group) in the SQLite database. | `sqlite3` |
| **`TEST.py`** | Schedule Data Access Layer. Handles complex retrieval of schedule content from JSON files. | `json` |
| **`TTime.py`** | Date and Time Utilities. Provides functions for identifying days and date formatting. | `datetime` |
| **`EvenOddWeek.py`** | Week Parity Logic. Determines the current academic week type. | `openpyxl` |
| **`CFG.py`** | Configuration Layer. Securely loads environment variables (BOT_TOKEN) and provides core utilities. | `python-dotenv` |

---

## 🛠️ Installation and Setup

### Prerequisites

1.  **Python 3.x**
2.  A **Telegram Bot Token** (obtained from BotFather).

### Setup Steps

1.  **Clone the Repository:**

    ```bash
    git clone [https://github.com/your-username/telegram-schedule-bot.git](https://github.com/your-username/telegram-schedule-bot.git)
    cd telegram-schedule-bot
    ```

2.  **Install Dependencies:**

    ```bash
    # Create a requirements.txt file with the following content:
    # aiogram
    # python-dotenv
    # openpyxl
    
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**

    Create a file named **`.env`** in the root directory and add your bot token:

    ```env
    BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
    ```

4.  **Prepare Data Files:**

    * Ensure your schedule data is correctly structured in **JSON files** that `TEST.py` is configured to read.
    * Ensure the week parity data is available in the expected **`weeks.xlsx`** file (or update the logic to a pure arithmetic calculation).

5.  **Run the Bot:**

    ```bash
    python Main.py
    ```

---

## 🚀 Usage

1.  **Start Interaction:**
    Send the `/start` command to the bot on Telegram.

2.  **Onboarding:**
    * The bot will check the database for your configuration.
    * New users will be prompted to select their preferred language and English group number.

3.  **Primary Commands (Reply Keyboard):**
    Use the primary commands provided by the Reply Keyboard for quick access:
    * "Schedule for today"
    * "Schedule for tomorrow"
    * "Weekly Schedule"

4.  **Configuration (Inline Keyboard):**
    Access the "Menu" or configuration prompts to dynamically change your preferred language or English group assignment using the Inline Keyboards.

---

## 📈 Future Development Roadmap

We are committed to continuous improvement. The following enhancements are planned for future releases:

1.  **🔔 Proactive Notification System:** Implement scheduled messages to send users the upcoming day's schedule at a specified time.
2.  **💻 Web Component Integration:** Develop a companion web interface for schedule viewing and, upon authorized access, modification.
3.  **🗄️ Database Enhancement:** Migrate schedule data from static JSON files directly into the SQLite database for optimized speed and resource utilization.
4.  **👨‍🏫 Instructor Search:** Add functionality to search schedules by instructor name.
5.  **⚙️ Platform Migration:** Porting the core logic to a framework like **ASP.NET Core** to improve stability and response speed on target hosting environments.

---

## 🤝 Contributing

Contributions are welcome! If you find a bug or have an idea for an enhancement, please feel free to open an issue or submit a pull request.
