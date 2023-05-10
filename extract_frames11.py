import cv2
import os
import time
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, IntVar, OptionMenu, Radiobutton
from tkinter.ttk import Progressbar

print("program started")

def load_video(video_path):
    print("start video loading")
    video = cv2.VideoCapture(video_path)
    print("end video loading")
    return video

def frames_to_time_ms(frame_number, fps):
    seconds = frame_number / fps
    hh = int(seconds // 3600)
    mm = int((seconds % 3600) // 60)
    ss = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{hh:02d}-{mm:02d}-{ss:02d}.{ms:03d}"

def frames_to_time(frame_number, fps):
    seconds = frame_number / fps
    hh = int(seconds // 3600)
    mm = int((seconds % 3600) // 60)
    ss = int(seconds % 60)
    return f"{hh:02d}-{mm:02d}-{ss:02d}"

def time_to_frame(time_string, fps):
    hh, mm, ss = map(int, time_string.split(':'))
    return int((hh * 3600 + mm * 60 + ss) * fps)

def extract_frames(video, output_dir, image_extension, frame_interval, filename_type, progress_var, start_time, end_time, is_time_range):
    print("start extract frames")
    fps = int(video.get(cv2.CAP_PROP_FPS))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_counter = 0

    start_frame = 0
    end_frame = total_frames

    if is_time_range.get() == 1:
        start_frame = time_string_to_frame(start_time, fps)
        end_frame = time_string_to_frame(end_time, fps)

    progress_var.set(0)
    max_value = int((end_frame - start_frame) / frame_interval)
    progress['maximum'] = max_value

    for frame_number in range(start_frame, end_frame, frame_interval):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()
        if ret:
            if filename_type == "連番":
                filename = f"{frame_counter:010d}.{image_extension}"
            elif filename_type == "該当フレームの時間":
                time_string = frames_to_time(frame_number, fps)
                filename = f"{time_string}.{image_extension}"
            elif filename_type == "該当フレームの時間(ミリ秒まで)":
                time_string = frames_to_time_ms(frame_number, fps)
                filename = f"{time_string}.{image_extension}"
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
    
def time_string_to_frame(time_string, fps):
    hh, mm, ss_ms = time_string.split(':')
    ss, ms = ss_ms.split('.')
    total_seconds = int(hh) * 3600 + int(mm) * 60 + int(ss) + int(ms) / 1000
    return int(total_seconds * fps)


def run_extraction(progress_var):
    print("start running extraction")
    video = load_video(video_path.get())
    start_time = time.time()
    extract_frames(video, output_dir.get(), image_extension.get(), frame_interval.get(), filename_type.get(), progress_var, start_time_entry.get(), end_time_entry.get(), is_time_range)
    video.release()
    end_time = time.time()
    elapsed_time = end_time - start_time

    # 新しいウィンドウを作成して処理結果を表示
    result_window = Tk()
    result_window.title("処理結果")
    result_window.geometry("300x100")  # ウィンドウのサイズを変更

    # ラベルのフォントサイズを変更
    Label(result_window, text=f"処理が終了しました。", font=("Arial", 14)).pack()
    Label(result_window, text=f"処理にかかった時間: {elapsed_time:.2f} 秒", font=("Arial", 14)).pack()
    result_window.mainloop()

def main():
    global video_path, output_dir, image_extension, frame_interval, filename_type, progress, progress_var, start_time_entry, end_time_entry, is_time_range

    root = Tk()
    root.title("画像抽出ツール")

    video_path = StringVar()
    output_dir = StringVar()
    image_extension = StringVar()
    frame_interval = IntVar()
    filename_type = StringVar()
    progress_var = IntVar()
    start_time_entry = StringVar(value="00:00:00.000")
    end_time_entry = StringVar(value="00:00:00.000")
    is_time_range = IntVar()

    image_extensions = ["png", "jpg", "bmp", "tiff"]
    frame_intervals = [1, 2, 5, 10, 20, 25, 30, 60]
    filename_types = ["連番", "該当フレームの時間", "該当フレームの時間(ミリ秒まで)"]

    image_extension.set(image_extensions[0])
    frame_interval.set(frame_intervals[0])
    filename_type.set(filename_types[0])

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

    Label(root, text="開始時間 (HH:mm:ss):").grid(row=5, column=0, sticky="W")
    Entry(root, textvariable=start_time_entry).grid(row=5, column=1)

    Label(root, text="終了時間 (HH:mm:ss):").grid(row=6, column=0, sticky="W")
    Entry(root, textvariable=end_time_entry).grid(row=6, column=1)

    Label(root, text="時間指定:").grid(row=7, column=0, sticky="W")
    Radiobutton(root, text="する", variable=is_time_range, value=1).grid(row=7, column=1, sticky="W")
    Radiobutton(root, text="しない", variable=is_time_range, value=0).grid(row=7, column=1)

    progress = Progressbar(root, variable=progress_var, maximum=100)
    progress.grid(row=8, column=0, columnspan=3, sticky="WE")

    Button(root, text="実行", command=lambda: run_extraction(progress_var)).grid(row=9, column=1)

    root.mainloop()

if __name__ == "__main__":
    print("main-program start")
    main()
