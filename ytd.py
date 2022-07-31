import argparse
import os
import shutil
import time
from random import randint
from pytube import YouTube
from pytube.cli import on_progress
from pytube.exceptions import RegexMatchError

parser = argparse.ArgumentParser(description='4k video downloader')
parser.add_argument('url')
parser.add_argument('-r', '--resolution', help='8k, 2k or fhd, 4k by default', required=False)
args = vars(parser.parse_args())


def get_video(video_url):
    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)
        video_title = yt.title
        print(video_title)
        if len(video_title.encode("utf-8")) > 126:
            video_title = video_title[:30]
        resolutions_video = ["2160p", "1440p", "1080p"]
        if args["resolution"] == "8k":
            resolutions_video.insert(0, "4320p")
        if args["resolution"] == "2k":
            resolutions_video.remove("2160p")
        if args["resolution"] == "fhd":
            resolutions_video = ["1080p"]
        quality_audio = ["160kbps", "128kbps", "70kbps", "50kbps", "48kbps"]
        videos_list = []
        audios_list = []
        for res in resolutions_video:
            stream = yt.streams.filter(res=res).first()
            if stream:
                videos_list.append(stream)
        for abr in quality_audio:
            stream = yt.streams.filter(abr=abr).first()
            if stream:
                audios_list.append(stream)
    except RegexMatchError:
        print("[ERROR] Url is not valid")
        return False
    if videos_list and audios_list:
        print("[INFO] Downloading video")
        videos_list[0].download(output_path='temp', filename='vid')
        print("\n")
        print("[INFO] Downloading audio")
        audios_list[0].download(output_path='temp', filename='aud')
        print("\n")
        os.system(f"ffmpeg -hide_banner -i temp/vid -i temp/aud -c copy output.mkv")
        shutil.rmtree("temp")
        time.sleep(1)
        try:
            os.rename("output.mkv", f"{video_title}.mkv")
        except Exception:
            print("[INFO] It is not possible to save a file with the correct name")
            title = f"{randint(10000, 100000)}.mkv"
            os.rename("output.mkv", title)
        print(f"[INFO] Resolution - {videos_list[0].resolution}")
    else:
        print("[INFO] There is low resolution only")
        yt.streams.get_highest_resolution().download()
    print("[INFO] Done")


if __name__ == '__main__':
    get_video(args["url"])
