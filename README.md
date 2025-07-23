# poke-dl

**poke-dl** is a lightweight command-line tool for downloading Pokémon episodes from direct `.m3u8` stream links. Built for simplicity and speed, it's perfect for grabbing your favorite episodes easily.

---

## Features

- ✅ Download `.m3u8` video streams directly
- ✅ Automatically saves output in a `downloaded` folder
- ✅ Free
- ✅ Open src
- ✅ terminal prompts

---
## 📁 Project Structure

```python
/poke-dl
start.bat
install-needs.bat
main-v2.py
ffmpeg <---- get it from [Here](https://ffmpeg.org/download.html)
Api-db.json
downloaded <----- downloaded episodes go here, its a dir

## Requirements

- [`ffmpeg`](https://ffmpeg.org/download.html)
in the same folder as thw project
- Python 3.8+
- Internet Connection
- Pip packages:
  - `requests`
Install the dependencies:
```python
pip install requests
