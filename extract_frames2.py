import cv2
import os
import re
from moviepy.editor import VideoFileClip
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar

print("program started")

def load_video(video_path):
    print("start video loading")
    video = cv2.VideoCapture(video_path)
    print("end video loading")
    return video

def timestamp_to_frames(timestamp, fps):
    print("start timestamp to frame")
    if not re.match(r'\d{2}:\d{2}:\d{2}', timestamp):
        print(f"Invalid timestamp format: {timestamp}")
        return None
    hh, mm, ss = map(float, timestamp.split(':'))
    seconds = hh * 3600 + mm * 60 + ss
    frames = int(seconds * fps)
    print("end timestamp to frame")
    return frames

def extract_frames(video, timestamps, output_dir):
    print("start extract frames")
    fps = int(video.get(cv2.CAP_PROP_FPS))
    for timestamp in timestamps:
        frame_number = timestamp_to_frames(timestamp, fps)
        if frame_number is None:
            continue
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()
        if ret:
            sanitized_timestamp = timestamp.replace(':', '-')
            output_path = os.path.join(output_dir, f"{sanitized_timestamp}.png")
            print(f"Saving frame {frame_number} to {output_path}")
            success = cv2.imwrite(output_path, frame)
            if not success:
                print(f"Failed to save frame {frame_number} to {output_path}")
        else:
            print(f"Failed to read frame {frame_number}")
    print("end extract frames")


def read_timestamps(timestamps_file):
    print("start read timestamps")
    with open(timestamps_file, "r") as file:
        timestamps = file.readlines()
    print("end read timestamps")
    return [ts.strip() for ts in timestamps]

def browse_video_file():
    print("start browsing video file")
    video_path.set(filedialog.askopenfilename())

def browse_timestamp_file():
    print("start browsing timestamp file")
    timestamps_path.set(filedialog.askopenfilename())

def browse_output_dir():
    print("start browsing output directory")
    output_dir.set(filedialog.askdirectory())

def run_extraction():
    print("start runnning extraction")
    video = load_video(video_path.get())
    timestamps = read_timestamps(timestamps_path.get())
    extract_frames(video, timestamps, output_dir.get())
    video.release()

def main():
    root = Tk()
    root.title("画像抽出ツール")

    global video_path, timestamps_path, output_dir
    video_path = StringVar()
    timestamps_path = StringVar()
    output_dir = StringVar()

    Label(root, text="動画ファイル:").grid(row=0, column=0, sticky="W")
    Entry(root, textvariable=video_path, width=40).grid(row=0, column=1)
    Button(root, text="参照", command=browse_video_file).grid(row=0, column=2)

    Label(root, text="タイムスタンプファイル:").grid(row=1, column=0, sticky="W")
    Entry(root, textvariable=timestamps_path, width=40).grid(row=1, column=1)
    Button(root, text="参照", command=browse_timestamp_file).grid(row=1, column=2)

    Label(root, text="出力ディレクトリ:").grid(row=2, column=0, sticky="W")
    Entry(root, textvariable=output_dir, width=40).grid(row=2, column=1) 
    Button(root, text="参照", command=browse_output_dir).grid(row=2, column=2)
    Button(root, text="実行", command=run_extraction).grid(row=3, column=1)

    root.mainloop()

if __name__ == "__main__":
    print("main-program start")
    main()