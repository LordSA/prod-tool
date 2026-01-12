# 🧹 Sudo clean

**Sudo clean** is an intelligent desktop automation tool that eliminates digital clutter using **natural language commands**.  
Just tell it what to do — it understands your intent and organizes your files automatically.

> “Clear old zip files from my downloads.”  
> “Sort my invoices.”  
> “Clean everything from yesterday.”

---

## ✨ Features

- 🧠 Natural language–based file management
- 📂 Context-aware intelligent sorting
- 🕵️ Background clutter monitoring
- 🔒 Safe, transparent operations
- ⚡ Lightweight and fast

---

## 🛠 Overview

**sudo clean** works as a **local desktop agent**.  
It translates human-friendly text into executable file system actions using the **Google Gemini API**.

### Operating Modes

- **Active Mode (Chat-Based)**  
  Execute file operations instantly via chat commands.

- **Passive Mode (Background Monitor)**  
  Silently monitors the Downloads folder and suggests cleanups.

---

## 🧠 Core Functionality

### 1. Natural Language Processing (The Brain)

The system integrates a Large Language Model (LLM) to interpret user intent.

**Example Input :**
Clear old zip files in downloads this morning


**AI Analysis**
- Target files: `.zip`
- Time constraint: < 12 hours
- Action: Move files

**Output**
- Files are moved
- Action is confirmed in chat

---

### 2. Intelligent File Sorting

Files are not dumped into a single folder.  
The system dynamically creates folders based on context.

- 📁 Context-based destinations  
  _Invoices → Invoices folder_
- 🧩 Extension grouping  
  _Images → .jpg, .png, .webp_
- 🚀 Non-blocking file movement

---

### 3. Background Clutter Monitor (Watchdog)

A background thread monitors your Downloads folder.

**What it does**
- Detects stale files (default: 24 hours)
- Sends non-intrusive alerts
- Offers one-click cleanup

**Example Notification :**
Found 17 unused old files. Clean now?


---

### 4. Safety & Transparency

- ✅ User confirmation before risky operations
- ❌ Graceful error handling
- 📝 Clear reporting for locked or inaccessible files

---

## 💬 Command Examples

| Command Type | User Input | System Action |
|-------------|-----------|---------------|
| Specific | Move all my PDFs to Work | Moves PDFs to `~/Documents/Work` |
| Time-Based | Clean up everything from yesterday | Moves files older than 24 hours |
| Contextual | Sort the vacation photos | Detects images and sorts |
| General | Clear out my Downloads | Cleans Downloads directory |
| Complex | Move the installer I downloaded an hour ago | Moves recent `.exe` / `.dmg` files |

---

## 🧱 System Architecture

**sudo clean** follows a simple **three-layer architecture**:

### 1️⃣ GUI Layer (Tkinter)
- Chat interface
- Popup notifications

### 2️⃣ Logic Layer (Python)
- File system operations
- Background threads
- Safety checks

### 3️⃣ Intelligence Layer (Gemini API)
- Natural language understanding
- Returns structured JSON:
  - Source paths
  - Destination paths
  - Filters

---

## 🚀 Tech Stack

- Python
- Tkinter
- Google Gemini API
- OS File System APIs

---

## 📌 Future Enhancements

- Scheduled cleanups
- Custom rules engine
- Cross-platform support
- Voice commands
- Learning user preferences

---

## 🙌 Acknowledgements

- Google Gemini API
- Python open-source ecosystem

## Getting Started
````
python3 -m venv venv

source venv/bin/activate

pip3 install U -r requirements.txt

python main.py
````
