import os
import time

import face_recognition
import cv2

print('face_recognition: v{}'.format(face_recognition.__version__))
print('opencv: v{}'.format(cv2.__version__))
print(cv2.getBuildInformation())

INPUT_FOLDER = '/input'
OUTPUT_FOLDER = '/output'

os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'an'

class FPSMeter:

    def __init__(self):
        self.last = None

    def start(self):
        self.last = time.perf_counter()

    def tick(self, log_format=None):
        ts = time.perf_counter()
        ellapsed = ts - self.last if self.last else None
        self.last = ts
        if log_format and ellapsed:
            print(log_format.format(ellapsed=ellapsed, fps=1/ellapsed))
        return ellapsed

def main():
    downscale_fps = os.environ.get('DOWNSCALE_FPS', '')
    downscale_fps = int(downscale_fps) if downscale_fps != '' else 1
    downscale_res = os.environ.get('DOWNSCALE_RES', '')
    downscale_res = int(downscale_res) if downscale_res != '' else 1

    print('downscale fps:', downscale_fps)
    print('downscale resolution:', downscale_res)

    input_basenames = [f for f in os.listdir(INPUT_FOLDER) 
                    if os.path.isfile(os.path.join(INPUT_FOLDER, f)) and
                    not f.startswith('.')]

    output_basenames = [os.path.splitext(f)[0] + '.mp4' for f in input_basenames]

    input_filenames = [os.path.join(INPUT_FOLDER, f) for f in input_basenames]
    output_filenames = [os.path.join(OUTPUT_FOLDER, f) for f in output_basenames]
    for (input_filename, output_filename) in zip(input_filenames, output_filenames):
        try:
            process_video(input_filename, output_filename, downscale_fps, downscale_res)
        except FileNotFoundError:
            print(f'[WARNING] skipping {input_filename} (could not open as a video file)')

def get_video_info(cap):
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return width, height, fps, frame_count

def process_frame(frame):
    small_frame = frame
    face_locations = face_recognition.face_locations(small_frame, model='cnn')
    for top, right, bottom, left in face_locations:
        face_image = frame[top:bottom, left:right]
        face_image = cv2.GaussianBlur(face_image, (99, 99), 30)
        frame[top:bottom, left:right] = face_image    
    return frame, face_locations

def process_video(input_filename, output_filename, downscale_fps, downscale_res, fourcc='mp4v'):
    print('input filename:', input_filename)
    cap = cv2.VideoCapture(input_filename)
    if not cap.isOpened():
        raise FileNotFoundError(f'Could not open {input_filename}')

    width, height, fps, frame_count = get_video_info(cap)
    print(f' - resolution: {width} x {height}')
    print(f' - fps: {fps}')
    print(f' - frame_count: {frame_count}')

    out_fps = fps / downscale_fps
    out_width, out_height = int(width / downscale_res), int(height / downscale_res)
    print('output filename:', output_filename)
    print(f' - resolution: {out_width} x {out_height}')
    print(f' - fps: {out_fps}')
    print(f' - fourcc: {fourcc}')

    fourcc_ = cv2.VideoWriter_fourcc(*fourcc)
    out = cv2.VideoWriter(output_filename, fourcc_, out_fps, (out_width, out_height))

    frame_idx = 0
    procesed_cnt = 0
    fps = FPSMeter()
    fps.start()
    start = time.perf_counter()
    while True:
        _, frame = cap.read()
        if frame is None:
            break
        if frame_idx % downscale_fps == 0:
            if downscale_res > 1:
                frame = cv2.resize(frame, (out_width, out_height), interpolation=cv2.INTER_AREA)
            frame, face_locations = process_frame(frame)
            out.write(frame)
            fps.tick(log_format=
                f'frame {frame_idx}/{frame_count} ({(frame_idx)/frame_count:.02%}), '
                f'processing time: {{ellapsed:.04f}}s, processing fps: {{fps:.02f}}, '
                f'face count: {len(face_locations)}')
            procesed_cnt += 1
        frame_idx += 1

    total_time = time.perf_counter() - start
    print(f'Total processing time: {total_time:.02f}s\n'
          f'Average processing time per frame: {total_time/procesed_cnt:.02f}s\n'
          f'Average processing fps: {procesed_cnt/total_time:.02f}')
    cap.release()
    out.release()

if __name__ == '__main__':
    main()
