from youtubesearchpython import VideosSearch
from moviepy.editor import VideoFileClip
from pytube import YouTube
import os


def search_youtube(query, max_results=10):
    videos = VideosSearch(query, limit=max_results)

    video_urls = []

    for video in videos.result()["result"]:
        video_urls.append(f"https://www.youtube.com/watch?v={video['id']}")

    return video_urls


def get_song(name):
    try:
        link = search_youtube(name)[0]
        video = YouTube(link)
        if name in video.title:
            return link
        else:
            return search_youtube(name)[1]
    except IndexError:
        print("Song not found")
        return ""


async def download_mp3(link, name):
    try:
        yt = YouTube(link)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download()
        os.rename(stream.default_filename, os.path.join("files", f"m{name}.mp3"))

        return 1
    except Exception as e:
        print(f"Error while downloading MP3: {e}")

def get_video_name(url):
    video = YouTube(url)
    return video.title

