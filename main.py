import yt_dlp
from dataclasses import dataclass
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Button, Entry
from PIL import Image, ImageTk
import os

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
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
            "outtmpl": str(self.download_dir / "%(title)s.%(ext)s")
        }
    
    def get_video_info(self, url: str):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as v:
                info = v.extract_info(url, download=False)
                return VideoInfo(
                    title = info.get("title", "No Title Found"),
                    duration = info.get("duration", 0),
                    url = url
                )
        except Exception as e:
            print(f"Error getting video info: {e}")
            return f"Error getting video info: {e}"

    def download_video(self, video_info:VideoInfo) -> bool:
        try:
            print(f"Downloading: {video_info.title}")
            with yt_dlp.YoutubeDL(self.ydl_opts) as v:
                v.download([video_info.url])
            return "Download completed successfully."
        except Exception as e:
            print(f"Download failed: {e}")
            return f"Download failed: {e}"

class Colors:
    def __init__(self) -> None:
        self.colors = {
            "primary": "#3B71CA",
            "secondary": "#9FA6B2",
            "success": "#14A44D",
            "danger": "#DC4C64",
            "warning": "#E4A11B",
            "info": "#54B4D3",
            "light": "#FBFBFB",
            "dark": "#332D2D",
            "grey": "#D9D9D9",
        }

    def get_color(self, name: str):
        return self.colors.get(name, "#000000")

class App(Tk):
    def __init__(self, downloader: VideoDownloader):
        super().__init__()
        self.downloader = downloader
        self.video_info = None

        self.icon = Path("image/file.png")

        # Create the window for the GUI
        self.title("Video Downloader")
        self.geometry("800x500")
        self.url_input = StringVar()
        self.widget(Colors())

    def show_cli(self, title = None, info: str = None) -> None:
        self.cli_command.config(state="normal")
        cli_output = ""  # Initialize cli_output here

        if info:
            cli_output += f"{info}\n"

        if title:
            cli_output += f"Downloading: {title}\n"
        
        self.cli_command.insert(END, cli_output)
        self.cli_command.see(END)
        self.cli_command.config(state="disabled")

    def onClick(self) -> None:
        try:
            # print("Button Click")
            url = self.url_input.get()
            video_info = self.downloader.get_video_info(url)
            if isinstance(video_info, str):  # Check if it's an error message
                self.show_cli(info=video_info)
                return
            
            self.show_cli(video_info.title)
            download_message = self.downloader.download_video(video_info)
            self.show_cli(info=download_message)

        except Exception as e:
            print(f"onClick function error: {e}")
            self.show_cli(info=f"onClick function error {e}")
            # print(f"Duration: {video_info.duration} seconds")

    def browseFiles(self):
        try:
            filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=[("Text files", "*.txt")])
            self.show_cli(info=f"Open file: {filename}")
            with open(filename, "r") as file:
                urls = file.readlines()

            for url in urls:
                url = url.strip()
                if not url:
                    continue

                video_info = self.downloader.get_video_info(url)
                if isinstance(video_info, str):
                    self.show_cli(info=video_info)
                    continue
                
                self.show_cli(video_info.title)
                try:
                    download_message = self.downloader.download_video(video_info)
                    self.show_cli(info=download_message)
                except Exception as download_error:
                    self.show_cli(info=f"Download failder for {video_info.title}: {download_error}")
                
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    
    def widget(self, color: Colors):
        main_f = Frame(self)
        main_f.pack(padx=34, pady=34)


        # Create the frame for the title
        title_f = Frame(main_f, height=30, width=210)
        title_f.pack(fill="x")
        title = Label(title_f, text="Video Downloader", font=("Arial", 24))
        title.pack()

        # Create the frame for the content
        content_f = Frame(main_f, bg=color.get_color("grey"), height=383, width=702, borderwidth=1, relief="solid")
        content_f.pack_propagate(False)
        content_f.pack(pady=(19, 0), fill="both")

        # Create the frame for the function
        function_f = Frame(content_f, bg=color.get_color("grey"), height=40, width=565)
        function_f.pack_propagate(False)
        function_f.pack(pady=(46, 0))

        # url input
        url_entry = Entry(function_f, font=("Arial", 12), textvariable=self.url_input)
        url_entry.place(x=0, y=0, width=387, height=40)

        # select file button
        image_obj = PhotoImage(file=self.icon)
        file_button = Button(function_f, image=image_obj, command=self.browseFiles, width=40)
        file_button.image = image_obj
        file_button.place(x=394, y=0, width=40, height=40)
        # file_button.pack()

        # download button
        download_button = Button(function_f, text="Download", command=self.onClick)
        download_button.place(x=441, y=0, width=124, height=40)

        # CLI frame
        self.cli_f = Frame(content_f, height=223, width=565, bg=color.get_color("light"))
        self.cli_f.pack_propagate(False)
        self.cli_f.pack(pady=35)

        # Text Field
        self.cli_command = Text(self.cli_f, wrap="word", state="normal")
        self.cli_command.pack(expand=True, fill='both')

    

def main():
    downloader = VideoDownloader()
    app = App(downloader)
    try:
        app.mainloop()
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
    