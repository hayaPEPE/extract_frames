import cv2
import os
import time
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, IntVar, OptionMenu, Toplevel, Radiobutton
import tkinter.ttk as ttk

print("program started")


def load_video(video_path):
    print("start video loading")
    video = cv2.VideoCapture(video_path)
    print("end video loading")
    return video


def frames_to_time(frame_number, fps):
    seconds = frame_number / fps
    hh = int(seconds // 3600)
    mm = int((seconds % 3600) // 60)
    ss = seconds % 60
    return f"{hh:02d}:{mm:02d}:{ss:06.3f}"


def extract_frames(video, output_dir, image_extension, frame_interval, filename_type, progress_var, time_specified, start_time, end_time):
    print("start extract frames")
    fps = int(video.get(cv2.CAP_PROP_FPS))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_counter = 0

    progress_var.set(0)
    max_value = int(total_frames / frame_interval)
    progress['maximum'] = max_value

    for frame_number in range(0, total_frames, frame_interval):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()
        if ret:
            time_in_seconds = frame_number / fps
            if time_specified:
                if start_time <= time_in_seconds <= end_time:
                    if filename_type == "連番":
                        filename = f"{frame_counter:010d}.{image_extension}"
                    elif filename_type == "該当フレームの時間":
                        filename = f"{time_in_seconds:.3f}.{image_extension}"
                    else:
                        print("Invalid filename type")
                        return
                else:
                    continue
            else:
                if filename_type == "連番":
                    filename = f"{frame_counter:010d}.{image_extension}"
                elif filename_type == "該当フレームの時間":
                    filename = f"{time_in_seconds:.3f}.{image_extension}"
                else:
                    print("Invalid filename type")
                    return

            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, frame)
            frame_counter += 1

            progress_var.set(frame_counter)
            progress.update()

    print("end extract frames")


def browse_video_file():
    print("start browsing video file")
    video_path.set(filedialog.askopenfilename())


def browse_output_dir():
    print("start browsing output directory")
    output_dir.set(filedialog.askdirectory())


def run_extraction(progress_var):
    print("start running extraction")
    video = load_video(video_path.get())
    start_time = time.time()
    if time_specification.get() == 1:
        start_seconds = int(start_time_h.get()) * 3600 + int(start_time_m.get()) * 60 + float(start_time_s.get())
        end_seconds = int(end_time_h.get()) * 3600 + int(end_time_m.get()) * 60 + float(end_time_s.get())
        extract_frames(video, output_dir.get(), image_extension.get(), frame_interval.get(), filename_type.get(), progress_var, True, start_seconds, end_seconds)
    else:
        extract_frames(video, output_dir.get(), image_extension.get(), frame_interval.get(), filename_type.get(), progress_var, False, 0, 0)
        video.release()
        end_time = time.time()
        elapsed_time = end_time - start_time
        show_result_window(root, elapsed_time)

def show_result_window(parent, elapsed_time):
    result_window = Toplevel(parent)
    result_window.title("処理結果")
    Label(result_window, text=f"処理が終了しました。処理にかかった時間: {elapsed_time:.2f} 秒").pack(padx=20, pady=20)

def main(): global root, video_path, output_dir, image_extension, frame_interval, filename_type, progress, progress_var, time_specification, start_time_h, start_time_m, start_time_s, end_time_h, end_time_m, end_time_s

root = Tk()
root.title("画像抽出ツール")

video_path = StringVar()
output_dir = StringVar()
image_extension = StringVar()
frame_interval = IntVar()
filename_type = StringVar()
progress_var = IntVar()
time_specification = IntVar()
start_time_h = StringVar()
start_time_m = StringVar()
start_time_s = StringVar()
end_time_h = StringVar()
end_time_m = StringVar()
end_time_s = StringVar()

image_extensions = ["png", "jpg", "bmp", "tiff"]
frame_intervals = [1, 2, 5, 10, 20, 25, 30, 60]
filename_types = ["連番", "該当フレームの時間"]

image_extension.set(image_extensions[0])
frame_interval.set(frame_intervals[0])
filename_type.set(filename_types[0])
time_specification.set(0)

Label(root, text="動画ファイル:").grid(row=0, column=0, sticky="W")
Entry(root, textvariable=video_path, width=40).grid(row=0, column=1)
Button(root, text="参照", command=browse_video_file).grid(row=0, column=2)

Label(root, text="出力ディレクトリ:").grid(row=1, column=0, sticky="W")
Entry(root, textvariable=output_dir, width=40).grid(row=1, column=1)
Button(root, text="参照", command=browse_output_dir).grid(row=1, column=2)

Label(root, text="画像拡張子:").grid(row=2, column=0, sticky="W")
OptionMenu(root, image_extension, *image_extensions).grid(row=2, column=1)

Label(root, text="フレーム間隔:").grid(row=3, column=0, sticky="W")
OptionMenu(root, frame_interval, *frame_intervals).grid(row=3, column=1)

Label(root, text="ファイル名タイプ:").grid(row=4, column=0, sticky="W")
OptionMenu(root, filename_type, *filename_types).grid(row=4, column=1)

Radiobutton(root, text="時間指定なし", variable=time_specification, value=0).grid(row=5, column=0, sticky="W")
Radiobutton(root, text="時間指定あり", variable=time_specification, value=1).grid(row=5, column=1, sticky="W")

Label(root, text="開始時間 (HH:MM:SS.sss):").grid(row=6, column=0, sticky="W")
Entry(root, textvariable=start_time_h, width=3).grid(row=6, column=1, sticky="W")
Label(root, text=":").grid(row=6, column=1, sticky="W", padx=(25, 0))
Entry(root, textvariable=start_time_m, width=3).grid(row=6, column=1, sticky="W", padx=(35, 0))
Label(root, text=":").grid(row=6, column=1, sticky="W", padx=(60, 0))
Entry(root, textvariable=start_time_s, width=6).grid(row=6, column=1, sticky="W", padx=(70, 0))

Label(root, text="終了時間 (HH:MM:SS.sss):").grid(row=7, column=0, sticky="W")
Entry(root, textvariable=end_time_h, width=3).grid(row=7, column=1, sticky="W")
Label(root, text=":").grid(row=7, column=1, sticky="W", padx=(25, 0))
Entry(root, textvariable=end_time_m, width=3).grid(row=7, column=1, sticky="W", padx=(35, 0))
Label(root, text=":").grid(row=7, column=1, sticky="W", padx=(60, 0))
Entry(root, textvariable=end_time_s, width=6).grid(row=7, column=1, sticky="W", padx=(70, 0))

progress = ttk.Progressbar(root, variable=progress_var, mode='determinate')
progress.grid(row=8, column=0, columnspan=3, padx=20, pady=(10, 5), sticky="WE")

Button(root, text="実行", command=lambda: run_extraction(progress_var)).grid(row=9, column=0, padx=(20, 5), pady=(5, 20), sticky="E")

root.mainloop()
if __name__ == "__main__":
    try:
        from tkinter import ttk
        main()
    except ImportError:
        print("Error: tkinter and ttk not found. Please install tkinter.")