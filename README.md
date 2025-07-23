# poke-dl

![Banner](https://files.catbox.moe/cyrinw.png)

**poke-dl** is a lightweight command-line tool for downloading Pokémon episodes from direct `.m3u8` stream links. Built for simplicity and speed, it's perfect for grabbing your favorite episodes easily.

---

## Features

- Download `.m3u8` video streams directly  
- Automatically saves output in a `downloaded` folder  
- Free  
- Open src  
- Terminal prompts  

---

## Needs

- [**ffmpeg**](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z)  
- [**python**](https://python.org)  
- Only `ffmpeg.exe` from the bin folder  

---

## Project Structure

```Structure
/poke-dl
start.bat
install-needs.bat
main-v2.py
ffmpeg <---- get it yourself
Api-db.json
downloaded <----- downloaded episodes go here, its a dir
