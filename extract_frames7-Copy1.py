import cv2
import os
import time
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar, IntVar, OptionMenu, Radiobutton, Frame, Toplevel
from tkinter.ttk import Progressbar

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


def extract_frames(video, output_dir, image_extension, frame_interval, filename_type, progress_var, time_specification, start_time, end_time, stop_flag):
    print("start extract frames")
    fps = int(video.get(cv2.CAP_PROP_FPS))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_counter = 0

    progress_var.set(0)
    start_frame = 0
    end_frame = total_frames

    if time_specification == "時間指定あり":
        start_frame = int(start_time * fps)
        end_frame = int(end_time * fps)

    max_value = int((end_frame - start_frame) / frame_interval)
    progress['maximum'] = max_value

    for frame_number in range(start_frame, end_frame, frame_interval):
        if stop_flag[0]:
            break

        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()
        if ret:
            if filename_type == "連番":
                filename = f"{frame_counter:010d}.{image_extension}"
            elif filename_type == "該当フレームの時間":
                time_in_seconds = frame_number / fps
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


def run_extraction(progress_var, stop_flag):
    print("start running extraction")
    video = load_video(video_path.get())
    start_time_value = time.time()

    time_specification_value = time_specification.get()

    start_time_sec = float(start_time_h.get() or 0) * 3600 + float(start_time_m.get() or 0) * 60 + float(start_time_s.get() or 0)
    end_time_sec = float(end_time_h.get() or 0) * 3600 + float(end_time_m.get() or 0) * 60 + float(end_time_s.get() or 0)

    extract_frames(video, output_dir.get(), image_extension.get(), frame_interval.get(), filename_type.get(), progress_var, time_specification_value, start_time_sec, end_time_sec, stop_flag)

    video.release()
    end_time_value = time.time()
    elapsed_time = end_time_value - start_time_value

    if not stop_flag[0]:
        show_result_window(f"処理が正常に終了しました。", elapsed_time)
    else:
        show_result_window("処理が中止されました。", elapsed_time)


def show_result_window(message, elapsed_time):
    result_window = Toplevel(root)
    result_window.title("結果")
    result_window.geometry("300x100")

    Label(result_window, text=message, font=("Arial", 14)).pack(pady=10)
    Label(result_window, text=f"処理にかかった時間: {elapsed_time:.2f} 秒", font=("Arial", 14)).pack(pady=5)


def stop_extraction(stop_flag):
    stop_flag[0] = True


root = Tk()
root.title("画像抽出ツール")
root.geometry("800x300")

video_path = StringVar()
output_dir = StringVar()
image_extension = StringVar()
frame_interval = IntVar()
filename_type = StringVar()
progress_var = IntVar()
time_specification = StringVar()
start_time_h = StringVar()
start_time_m = StringVar()
start_time_s = StringVar()
end_time_h = StringVar()
end_time_m = StringVar()
end_time_s = StringVar()

image_extensions = ["png", "jpg", "bmp", "tiff"]
frame_intervals = [1, 2, 5, 10, 20, 25, 30, 60]
filename_types = ["連番", "該当フレームの時間"]
time_specifications = ["時間指定なし", "時間指定あり"]

image_extension.set(image_extensions[0])
frame_interval.set(frame_intervals[0])
filename_type.set(filename_types[0])
time_specification.set(time_specifications[0])

Label(root, text="動画ファイル:", font=("Arial", 14)).grid(row=0, column=0, sticky="W")
Entry(root, textvariable=video_path, width=40, font=("Arial", 14)).grid(row=0, column=1)
Button(root, text="参照", command=browse_video_file, font=("Arial", 14)).grid(row=0, column=2)

Label(root, text="出力ディレクトリ:", font=("Arial", 14)).grid(row=1, column=0, sticky="W")
Entry(root, textvariable=output_dir, width=40, font=("Arial", 14)).grid(row=1, column=1)
Button(root, text="参照", command=browse_output_dir, font=("Arial", 14)).grid(row=1, column=2)

Label(root, text="画像拡張子:", font=("Arial", 14)).grid(row=2, column=0, sticky="W")
OptionMenu(root, image_extension, *image_extensions).grid(row=2, column=1)

Label(root, text="フレーム間隔:", font=("Arial", 14)).grid(row=3, column=0, sticky="W")
OptionMenu(root, frame_interval, *frame_intervals).grid(row=3, column=1)

Label(root, text="ファイル名タイプ:", font=("Arial", 14)).grid(row=4, column=0, sticky="W")
OptionMenu(root, filename_type, *filename_types).grid(row=4, column=1)

time_specification_frame = Frame(root)
time_specification_frame.grid(row=5, column=0, sticky="W")
Radiobutton(time_specification_frame, text="時間指定なし", variable=time_specification, value=time_specifications[0], font=("Arial", 14)).grid(row=0, column=0)
Radiobutton(time_specification_frame, text="時間指定あり", variable=time_specification, value=time_specifications[1], font=("Arial", 14)).grid(row=0, column=1)
Label(root, text="時間指定:", font=("Arial", 14)).grid(row=5, column=0, sticky="W")
time_specification_frame.grid(row=5, column=1)

Label(root, text="開始時間:", font=("Arial", 14)).grid(row=6, column=0, sticky="W")
start_time_frame = Frame(root)
start_time_frame.grid(row=6, column=1)
Entry(start_time_frame, textvariable=start_time_h, width=5, font=("Arial", 14)).grid(row=0, column=0)
Label(start_time_frame, text="時", font=("Arial", 14)).grid(row=0, column=1)
Entry(start_time_frame, textvariable=start_time_m, width=5, font=("Arial", 14)).grid(row=0, column=2)
Label(start_time_frame, text="分", font=("Arial", 14)).grid(row=0, column=3)
Entry(start_time_frame, textvariable=start_time_s, width=5, font=("Arial", 14)).grid(row=0, column=4)
Label(start_time_frame, text="秒", font=("Arial", 14)).grid(row=0, column=5)

Label(root, text="終了時間:", font=("Arial", 14)).grid(row=7, column=0, sticky="W")
end_time_frame = Frame(root)
end_time_frame.grid(row=7, column=1)
Entry(end_time_frame, textvariable=end_time_h, width=5, font=("Arial", 14)).grid(row=0, column=0)
Label(end_time_frame, text="時", font=("Arial", 14)).grid(row=0, column=1)
Entry(end_time_frame, textvariable=end_time_m, width=5, font=("Arial", 14)).grid(row=0, column=2)
Label(end_time_frame, text="分", font=("Arial", 14)).grid(row=0, column=3)
Entry(end_time_frame, textvariable=end_time_s, width=5, font=("Arial", 14)).grid(row=0, column=4)
Label(end_time_frame, text="秒", font=("Arial", 14)).grid(row=0, column=5)

progress = Progressbar(root, variable=progress_var, length=500)
progress.grid(row=8, column=0, columnspan=3, pady=10)

stop_flag = [False]
Button(root, text="実行", command=lambda: run_extraction(progress_var, stop_flag), font=("Arial", 14)).grid(row=9, column=0)
Button(root, text="中止", command=lambda: stop_extraction(stop_flag), font=("Arial", 14)).grid(row=9, column=1)
Button(root, text="閉じる", command=root.quit, font=("Arial", 14)).grid(row=9, column=2)

root.mainloop()

#if __name__ == "__main__":
    #print("main-program start")
   # main()