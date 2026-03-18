# ani-uanm

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

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

- Python 3.14.2 (recommended as it's the only version tested)
- `uv` installed as a cli tool and in yout path
- `mpv` installed and available in your system PATH (windows installation needs mpv .dll in the project folder)
- Git

---

## 🚀 Installation & Setup

### Download the project
```bash
git clone https://github.com/ProfesionalFailer/ani-uanm
cd ani-uanm
```

### Create venv
```bash
uv venv
```

### Install

#### Locally in Linux
```bash
source .venv/bin/activate
uv pip install -e ".[cli]"
```

#### Locally in Windows
```powershell
.\.venv\Scripts\activate.ps1
uv pip install -e ".[cli]"
```
#### Globally in both
```bash
uv tool install -e ".[cli]"
```

### Run (example)
``` bash
ani-uanm-cli "Naruto" --episode 12 --dub
```
> This will be executed only inside the venv if installed locally.

---

### 🔗 Adding URL to Sources

Create a `.env` file in the root directory:

```env
ANIMEUNITY_URL=your_animeunity_url_here
REDIRECT_PORT=a_free_port_to_host_the_redirector_server
```

> The `ANIMEUNITY_URL` is NOT provided out of the box and must be set manually. Ensure the url is formatted like 'https://www.<url>.'

---

### About discord integration

Discord rich presence is enabled by default, to disable it just add:

```env
DISCORD_RPC=false
```

## 🛠 Project Status

Currently:

- ✅ Backend logic implemented
- ✅ AnimeUnity backend support
- ✅ Streaming support
- ✅ Cli app
- ✅ Global install through uv
- ✅ Discord rich presence integration
- ❌ No bundled app
- ❌ No way to change video quality
- ❌ No download support yet
- ❌ No GUI yet
- ❌ No additional providers yet


---

## 🔮 Next Features

- Improve the command line application
- Allow downloading
- AniList integration
- MyAnimeList integration
- Add AnimeSaturn support
- Eventually build a GUI

---

## 📜 License

This project is licensed under the **MIT License**.

