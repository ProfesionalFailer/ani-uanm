# ani-uanm

**ani-uanm** is a Python application designed to stream and download anime with Italian subtitles or dubbing from various sources.

It is inspired by the popular `ani-cli` and uses `mpv` as the media player for streaming.

> ⚠️ This project is currently a work in progress.

---

## 🐍 Python Version

The project is currently written and tested with:

**Python 3.14.2**

Compatibility with other Python versions is currently unknown and not guaranteed.

---

## ✨ Current Features

- Backend logic implemented
- AnimeUnity backend support

---

## 📦 Requirements

- Python 3.14.2 (recommended)
- `mpv` installed and available in your system PATH (windows installation needs mpv .dll in the project folder)
- Git

---

## 🚀 Installation & Setup

### 🔹 Linux

```bash
# Clone the repository
git clone https://github.com/yourusername/ani-uanm.git
cd ani-uanm

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the root directory:

```env
ANIMEUNITY_URL=your_animeunity_url_here
```

> The `ANIMEUNITY_URL` is NOT provided out of the box and must be set manually.

---

### 🔹 Windows

```powershell
# Clone the repository
git clone https://github.com/yourusername/ani-uanm.git
cd ani-uanm

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### 🔗 Adding URL to Sources

Create a `.env` file in the root directory:

```env
ANIMEUNITY_URL=your_animeunity_url_here
```

> The `ANIMEUNITY_URL` is NOT provided out of the box and must be set manually.

---

## ▶️ Running the Project

Actually project is still _WIP_ and has no final program to run. You can test the anime_unity backend by implementing it into your script.

---

## 🛠 Project Status

Currently:

- ✅ Backend logic implemented
- ✅ AnimeUnity backend support
- ❌ No streaming support yet
- ❌ No download support yet
- ❌ No UI yet
- ❌ No additional providers yet

At the moment, only backend work for AnimeUnity is implemented.
A UI is currently in progress.

---

## 🔮 Next Features

- Build a `mpv` wrapper
- Allow downloading
- Make a Discord Rich Presence integration
- AniList integration
- MyAnimeList integration
- Add AnimeSaturn support
- Improve the command line application
- Build a TUI (Terminal User Interface)
- Eventually build a GUI

---

## 📜 License

This project is licensed under the **MIT License**.
