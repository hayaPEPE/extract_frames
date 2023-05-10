import cv2
import os
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar

print("program started")

def load_video(video_path):
    print("start video loading")
    video = cv2.VideoCapture(video_path)
    print("end video loading")
    return video

def extract_frames(video, output_dir):
    print("start extract frames")
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    for frame_number in range(frame_count):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()
        if ret:
            # 10桁の連番でファイル名を生成する
            output_path = os.path.join(output_dir, f"{frame_number:010d}.png")
            print(f"Saving frame {frame_number} to {output_path}")
            success = cv2.imwrite(output_path, frame)
            if not success:
                print(f"Failed to save frame {frame_number} to {output_path}")
        else:
            print(f"Failed to read frame {frame_number}")
    print("end extract frames")

def browse_video_file():
    print("start browsing video file")
    video_path.set(filedialog.askopenfilename())

def browse_output_dir():
    print("start browsing output directory")
    output_dir.set(filedialog.askdirectory())

def run_extraction():
    print("start running extraction")
    video = load_video(video_path.get())
    extract_frames(video, output_dir.get())
    video.release()

def main():
    root = Tk()
    root.title("画像抽出ツール")

    global video_path, output_dir
    video_path = StringVar()
    output_dir = StringVar()

    Label(root, text="動画ファイル:").grid(row=0, column=0, sticky="W")
    Entry(root, textvariable=video_path, width=40).grid(row=0, column=1)
    Button(root, text="参照", command=browse_video_file).grid(row=0, column=2)

    Label(root, text="出力ディレクトリ:").grid(row=1, column=0, sticky="W")
    Entry(root, textvariable=output_dir, width=40).grid(row=1, column=1)
    Button(root, text="参照", command=browse_output_dir).grid(row=1, column=2)

    Button(root, text="実行", command=run_extraction).grid(row=2, column=1)

    root.mainloop()

if __name__ == "__main__":
    print("main-program start")
    main()
