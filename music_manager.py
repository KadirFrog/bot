import os

from youtube_music import download_mp3, get_song

def clear_preload(folder_path: str = "files"):
    # Check if the folder path exists
    if os.path.exists(folder_path):
        # List all files in the folder
        files = os.listdir(folder_path)

        # Iterate through the files and delete them
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                print(f"Skipping {file} as it is not a file.")
    else:
        print(f"The folder {folder_path} does not exist.")
def create_playlist(name):
    name = os.path.join("playlists/", name)
    with open(name, "w") as f:
        f.write("\n")

def add_song_to_playlist(pn, su):
    pn = os.path.join("playlists/", pn)
    su = get_song(su)
    with open(pn, "w") as f:
        f.write(f"{su}\n")

def preload(pn):
    pn = os.path.join("playlists/", pn)
    f = open(pn, "r")
    p = f.read().splitlines()
    sc = 0
    clear_preload()
    for url in p:
        sc += 1
        download_mp3(url, "id=" + str(sc))
