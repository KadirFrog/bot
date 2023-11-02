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
    link = search_youtube(name)[0]
    return link


print(get_song("After Dark"))


def convert_mp4_to_mp3(input_file, output_file):
    video_clip = VideoFileClip(input_file)
    audio_clip = video_clip.audio
    output_file = os.path.join(output_file, "files/")
    audio_clip.write_audiofile(output_file)
    audio_clip.close()
    os.remove(input_file)

def download_mp4(link):
    yt = YouTube(link)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download()
    os.rename(stream.default_filename, "ytd.mp4")

