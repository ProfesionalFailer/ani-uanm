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
- Mpv wrapper
- Https redirector for mpv playlists

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
git clone https://github.com/ProfesionalFailer/ani-uanm
cd ani-uanm

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run (example)
python ani-uanm-cli.py "Naruto" --episode 12 --dub
```

Create a `.env` file in the root directory:

```env
ANIMEUNITY_URL=your_animeunity_url_here
REDIRECT_PORT=a_free_port_to_host_the_redirector_server
```

> The `ANIMEUNITY_URL` is NOT provided out of the box and must be set manually.

---

### 🔹 Windows

```powershell
# Clone the repository
git clone https://github.com/ProfesionalFailer/ani-uanm
cd ani-uanm

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run (example)
python ani-uanm-cli.py "Naruto" --episode 12 --dub
```

---

### 🔗 Adding URL to Sources

Create a `.env` file in the root directory:

```env
ANIMEUNITY_URL=your_animeunity_url_here
REDIRECT_PORT=a_free_port_to_host_the_redirector_server
```

> The `ANIMEUNITY_URL` is NOT provided out of the box and must be set manually.

---

## 🛠 Project Status

Currently:

- ✅ Backend logic implemented
- ✅ AnimeUnity backend support
- ✅ Streaming support
- ✅ Cli app
- ❌ No bundled app
- ❌ No way to change video quality
- ❌ No download support yet
- ❌ No UI yet
- ❌ No additional providers yet


---

## 🔮 Next Features

- Improve the command line application
- Allow downloading
- Make a Discord Rich Presence integration
- AniList integration
- MyAnimeList integration
- Add AnimeSaturn support
- Eventually build a GUI

---

## 📜 License

This project is licensed under the **MIT License**.
