import tkinter

import customtkinter as ctk
from pytube import YouTube
from tkinter import ttk
import os


def download_video():
    try:

        ytlink = link.get()
        ytObject = YouTube(ytlink, on_progress_callback= progress)

        print(ytObject.title) #prints the title of the video
        video = ytObject.streams.get_highest_resolution()
        print("Your video will be downloaded in:", os.getcwd())
        video.download()
        #downloading the captions
        try:
            en_captions = ytObject.captions['en']
            if en_captions:
                srt_captions = en_captions.generate_srt_captions()  
                with open('video_captions.srt', 'w', encoding='utf-8') as file:
                    file.write(srt_captions)
        except:
            
             print("No English captions found.")

    except Exception as e:
        print("Download failed")
        print(e)

def progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentOfComp = bytes_downloaded /total_size * 100
    per = str(int(percentOfComp))
    percent.configure(text = per + "%")
    percent.update()
# Create a root window
root = ctk.CTk()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

#title of the window
root.title("Youtube Downloader")

# set min and max
root.geometry("720x480")
root.minsize(720,480)
root.maxsize(1080,720)

# to start the app


content_frame = ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH, expand = True, padx=10, pady=10)

#create a label and entry widget for the video url
urlV = tkinter.StringVar()
url_label = ctk.CTkLabel(content_frame, text="Insert a youtube link below")
link = ctk.CTkEntry(content_frame, width=400, height=40, placeholder_text="paste youtube url here", textvariable= urlV)

url_label.pack(pady=(10, 5))
link.pack(pady=(10, 5))

#download progress
percent = ctk.CTkLabel(content_frame, text="0%")
percent.pack()

progressBar= ctk.CTkProgressBar(content_frame, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)
#download is finished
finish = ctk.CTkLabel(content_frame, text="")
finish.pack()


download_button = ctk.CTkButton(content_frame, text="Download", command=download_video)
download_button.pack(pady=(10, 5))



root.mainloop()
