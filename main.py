import os
import requests
import json
import subprocess
import re
import shutil

# config
SERIES_JSON_URL = "https://raw.githubusercontent.com/TS-DEV-JAVA/Poke-dl-api/refs/heads/main/Api-db.json"
MOVIES_JSON_URL = "https://raw.githubusercontent.com/TS-DEV-JAVA/Poke-dl-api/refs/heads/main/Movies-db.json"
YTDLP_EXE = "yt-dlp"
OUTPUT_DIR = "downloaded"
MOV_OUTPUT = "downloaded-movies"

# color codes
RED = "\033[38;5;196m"
GREEN = "\033[38;5;46m"
YELLOW = "\033[38;5;226m"
BLUE = "\033[38;5;21m"
THAT = "\x1b[35m"
RESET = "\033[0m"

# coooool ahh banner
banner_lines = [
    f"{RED}╭────────────────────────────────────────────╮",
    f"{GREEN}│    ____        __              ____  __    │",
    f"{YELLOW}│   / __ \\____  / /_____        / __ \\/ /    │",
    f"{BLUE}│  / /_/ / __ \\/ //_/ _ \\______/ / / / /     │",
    f"{RED}│ / ____/ /_/ / ,< /  __/_____/ /_/ / /___   │",
    f"{GREEN}│/_/    \\____/_/|_|\\___/     /_____/_____/   │",
    f"{BLUE}│                 poke-dl -- © TS-DEV-JAVA   │{RESET}",
    f"{YELLOW}╰────────────────────────────────────────────╯{RESET}",
]

def print_banner():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    for line in banner_lines:
        print(line)
    print()

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def get_json(url):
    try:
        response = requests.get(url)
        return response.json()
    except:
        print(RED + "[!] Failed to fetch JSON from URL." + RESET)
        exit()

def select_from_list(options, label_color=GREEN):
    for i, option in enumerate(options, 1):
        print(f"{label_color}{i}. {option}{RESET}")
    while True:
        try:
            choice = int(input(YELLOW + "[?] Choose number: " + RESET))
            if 1 <= choice <= len(options):
                return options[choice - 1], choice - 1
        except:
            pass
        print(RED + "[!] Invalid choice." + RESET)

def search_items(data, is_movie=False):
    term = input(YELLOW + "[?] Enter search term: " + RESET).lower()
    results = []

    for show, episodes in data.items():
        for ep in episodes:
            if term in ep['title'].lower():
                results.append((show, ep))

    if not results:
        print(RED + "[!] No results found." + RESET)
        return

    print(BLUE + f"\n[+] Search Results:" + RESET)
    for i, (show, ep) in enumerate(results, 1):
        print(f"{GREEN}{i}. {ep['title']} ({show}){RESET}")

    while True:
        try:
            prompt = "[?] Pick a number: " if is_movie else "[?] Choose episode: "
            choice = int(input(YELLOW + prompt + RESET))
            if 1 <= choice <= len(results):
                return results[choice - 1]
        except:
            pass
        print(RED + "[!] Invalid choice." + RESET)

def handle_download(ep, show_name):
    file_title = sanitize_filename(f"{show_name} - {ep['title']}")

    if show_name == "Movie":
        print(f"{YELLOW}\n[~] Downloading: {ep['title']}{RESET}")
        print(f"{BLUE}[~] URL: {ep['url']}{RESET}")
        aria_cmd = [
            "aria2c",
            ep["url"],
            "-d", MOV_OUTPUT,
        ]
        subprocess.run(aria_cmd, check=True)
        print(f"{GREEN}[!] Saved to: /{MOV_OUTPUT}{RESET}")
        return

    print(f"{BLUE}\n[+] Choose Format:{RESET}")
    formats = [".mp4", ".mkv", ".webm", ".mov"]
    selected_format, _ = select_from_list(formats)

    print(f"{BLUE}\n[+] Choose Resolution:{RESET}")
    resolutions = ["1080p", "720p", "480p", "360p"]
    selected_resolution, _ = select_from_list(resolutions)

    resolution_num = selected_resolution[:-1]  # e.g., "720p" → "720"

    output_filename = f"{file_title} - {selected_resolution}{selected_format}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    print(f"{YELLOW}\n[~] Downloading: {ep['title']}{RESET}")
    print(f"{BLUE}[~] URL: {ep['url']}{RESET}")
    print(f"{GREEN}[~] Format: {selected_format}, Resolution: {selected_resolution}{RESET}")

    ytdlp_command = [
        YTDLP_EXE,
        "-f", f"bestvideo[height<={resolution_num}]+bestaudio/best",
        "--merge-output-format", selected_format[1:],  # remove leading dot (e.g., ".mp4" → "mp4")
        "-o", output_path,
        ep["url"]
    ]

    subprocess.run(ytdlp_command, check=True)
    print(f"{GREEN}[!] Saved to: {output_path}{RESET}")

def stream_episode(data):
    shows = list(data.keys())
    print(BLUE + "\n[+] Available Series:" + RESET)
    show_name, _ = select_from_list(shows)
    episodes = data[show_name]
    episode_titles = [ep['title'] for ep in episodes]
    selected_title, index = select_from_list(episode_titles)
    selected_ep = episodes[index]

    m3u8_url = selected_ep.get("url")
    if not m3u8_url:
        print(RED + "[!] Missing URL in episode data." + RESET)
        return

    print(BLUE + "\n[+] Choose Stream Option:" + RESET)
    stream_options = [
        "360p",
        "720p",
        "1080p",
        "Use raw m3u8 (direct stream)"
    ]
    selected_option, selected_index = select_from_list(stream_options)

    if selected_index == 3:  # use raw m3u8
        print(GREEN + f"[~] Streaming (original .m3u8): {selected_ep['title']}" + RESET)
        print(BLUE + f"[~] URL: {m3u8_url}" + RESET)
        mpv_cmd = [
            "mpv",
            f"--title={selected_ep['title']} (original)",
            "--no-sub",
            m3u8_url
        ]
        subprocess.run(mpv_cmd)
        return

    resolution = selected_option
    base_url = m3u8_url.rsplit("/", 1)[0]
    video_url = f"{base_url}/video_h264_{resolution}.mp4"
    audio_url = f"{base_url}/audio_en.mp4"

    print(GREEN + f"[~] Playing: {selected_ep['title']} ({resolution})" + RESET)
    print(BLUE + f"[~] Video: {video_url}" + RESET)
    print(BLUE + f"[~] Audio: {audio_url}" + RESET)

    mpv_cmd = [
        "mpv",
        f"--title={selected_ep['title']} ({resolution})",
        "--audio-file=" + audio_url,
        video_url
    ]

    subprocess.run(mpv_cmd)

def main_menu():
    print(BLUE + "[+] Main Menu:" + RESET)
    options = [
        "Pokèmon Series",
        "Pokèmon Movies",
        "Search",
        "Fixer",
        "Download from watch URL",
        "Stream",
        "Exit Poke-dl"
    ]
    choice, _ = select_from_list(options)

    if choice == "Exit Poke-dl":
        print(RED + "[!] Exiting." + RESET)
        exit()

    elif choice == "Fixer":
        subprocess.run(["python", os.path.join("tools", "fixer.dll")])

    elif choice == "Download from watch URL":
        subprocess.run(["python", os.path.join("tools", "m3u8-extractor.dll")])

    elif choice == "Pokèmon Series":
        data = get_json(SERIES_JSON_URL)
        shows = list(data.keys())
        print(BLUE + "\n[+] Available Series:" + RESET)
        show_name, _ = select_from_list(shows)
        episodes = data[show_name]
        episode_titles = [ep['title'] for ep in episodes]
        selected_title, index = select_from_list(episode_titles)
        selected_ep = episodes[index]
        handle_download(selected_ep, show_name)

    elif choice == "Pokèmon Movies":
        data = get_json(MOVIES_JSON_URL)
        titles = [ep['title'] for ep in data]
        print(BLUE + "\n[+] Available Movies:" + RESET)
        selected_title, index = select_from_list(titles)
        selected_ep = data[index]
        handle_download(selected_ep, "Movie")

    elif choice == "Search":
        print(BLUE + "\n[+] Search Type:" + RESET)
        search_options = ["Search Pokèmon Series", "Search Pokèmon Movies"]
        search_choice, _ = select_from_list(search_options)
        if "Series" in search_choice:
            data = get_json(SERIES_JSON_URL)
            result = search_items(data)
            if result:
                show, ep = result
                handle_download(ep, show)
        else:
            movie_list = get_json(MOVIES_JSON_URL)
            movie_data = {"Movies": movie_list}
            result = search_items(movie_data, is_movie=True)
            if result:
                _, ep = result
                handle_download(ep, "Movie")

    elif choice == "Stream":
        data = get_json(SERIES_JSON_URL)
        stream_episode(data)

def main():
    print_banner()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(MOV_OUTPUT, exist_ok=True)

    if not shutil.which(YTDLP_EXE):
        print(RED + f"[!] {YTDLP_EXE} not found. Install it with: pip install yt-dlp" + RESET)
        exit()

    if not shutil.which("aria2c"):
        print(RED + "[!] aria2c not found. Install it from: https://aria2.github.io/" + RESET)
        exit()

    if not shutil.which("mpv"):
        print(RED + "[!] mpv not found. Install it from: https://mpv.io/" + RESET)
        exit()

    while True:
        try:
            main_menu()
        except KeyboardInterrupt:
            print(RED + "\n[!] Interrupted." + RESET)
            break

if __name__ == "__main__":
    main()

