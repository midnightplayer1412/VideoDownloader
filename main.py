import yt_dlp
from dataclasses import dataclass
from pathlib import Path
from tkinter import *
from tkinter.ttk import Button, Entry

@dataclass
class VideoInfo:
    title: str
    duration: int
    url: str

class VideoDownloader:
    def __init__(self) -> None:
        self.download_dir = Path("downloaded_video")
        self.ffmpeg_path = Path("ffmpeg/bin")
        self.setup_dir()
    
    def setup_dir(self) -> None:
        if self.download_dir.exists() and self.download_dir.is_dir():
            print("Have directory")
        else:
            print("No directory")
            self.download_dir.mkdir(exist_ok=True)
            print(f"Directory created at : {self.download_dir}")

    @property
    def ydl_opts(self) -> dict:
        return {
            "ffmpeg_location": str(self.ffmpeg_path),
            "formaat": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
            "outtmpl": str(self.download_dir / "%(title)s.%(ext)s")
        }
    
    def get_video_info(self, url: str):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as v:
                info = v.extract_info(url, download=False)
                return VideoInfo(
                    title = info.get("title", "No Title Found"),
                    duration = info.get("duration", "No Duration Available"),
                    url = url
                )
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None

    def download_video(self, video_info:VideoInfo) -> bool:
        try:
            print(f"Downloading: {video_info.title}")
            with yt_dlp.YoutubeDL(self.ydl_opts) as v:
                v.download([video_info.url])
            return True
        except Exception as e:
            print(f"Download failed: {e}")
            return False

def main():
    downloader = VideoDownloader()
    
    try:
        url = input("Enter the video URL: ")
        video_info = downloader.get_video_info(url)
        
        if video_info:
            print(f"Title: {video_info.title}")
            print(f"Duration: {video_info.duration} seconds")
            downloader.download_video(video_info)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
    