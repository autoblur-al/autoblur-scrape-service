## Autoblur Scrape Service

This project scrapes car details from a website and generates a report. No advanced programming skills required!

---

### Step 1: Install Prerequisites

#### 1. Install Python 3.12

- Download Python from [python.org](https://www.python.org/downloads/release/python-3124/)
- Run the installer and follow the instructions. Make sure to check "Add Python to PATH" during installation.

#### 2. Install Poetry

- Poetry helps manage project dependencies easily.
- Open PowerShell (Windows) or Terminal (macOS/Linux).
- Run one of the following commands:
  - **Windows:**
    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```
  - **macOS/Linux:**
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```
- After installation, restart your terminal and run:
  ```sh
  poetry --version
  ```
  You should see the Poetry version printed.

---

### Step 2: Download the Project

1. Open your terminal and run:
   ```sh
   git clone https://github.com/YOUR_USERNAME/autoblur-scrape-service.git
   cd autoblur-scrape-service
   ```
   If you don't have git, download the ZIP from GitHub and extract it.

---

### Step 3: Install Project Dependencies

1. In the project folder, run:
   ```sh
   poetry install
   ```
   This will set up everything you need automatically.

---

### Step 4: Run the Application

1. Start the app with:
   ```sh
   poetry run python main.py
   ```
2. Follow the on-screen instructions in the app window.

---

### Troubleshooting

- If you see errors about missing Python or Poetry, double-check the installation steps above.
- If you need help, see the official Poetry docs: https://python-poetry.org/docs/#installation
