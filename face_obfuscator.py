import os
import time

import face_recognition
import cv2

print('face_recognition: v{}'.format(face_recognition.__version__))
print('opencv: v{}'.format(cv2.__version__))
print(cv2.getBuildInformation())

INPUT_FOLDER = '/input'
OUTPUT_FOLDER = '/output'

class FPSMeter:

    def __init__(self):
        self.last = None

    def tick(self, log_format=None):
        ts = time.perf_counter()
        ellapsed = ts - self.last if self.last else None
        self.last = ts
        if log_format and ellapsed:
            print(log_format.format(ellapsed=ellapsed, fps=1/ellapsed))
        return ellapsed

def main():

    input_basenames = [f for f in os.listdir(INPUT_FOLDER) 
                    if os.path.isfile(os.path.join(INPUT_FOLDER, f)) and
                    not f.startswith('.')]

    output_basenames = [os.path.splitext(f)[0] + '.mp4' for f in input_basenames]

    input_filenames = [os.path.join(INPUT_FOLDER, f) for f in input_basenames]
    output_filenames = [os.path.join(OUTPUT_FOLDER, f) for f in output_basenames]
    for (input_filename, output_filename) in zip(input_filenames, output_filenames):
        print('input filename:', input_filename)
        print('output filename:', output_filename)
        try:
            process_video(input_filename, output_filename)
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

def process_video(input_filename, output_filename):
    cap = cv2.VideoCapture(input_filename)
    if not cap.isOpened():
        raise FileNotFoundError(f'Could not open {input_filename}')

    print(f'opened {input_filename}')

    width, height, fps, frame_count = get_video_info(cap)
    print(f' - resolution: {width} x {height}')
    print(f' - fps: {fps}')
    print(f' - frame_count: {frame_count}')

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    frame_idx = 0
    fps = FPSMeter()
    while True:
        _, frame = cap.read()
        if frame is None:
            break
        frame_idx += 1
        frame, face_locations = process_frame(frame)
        out.write(frame)
        fps.tick(log_format=
            f'frame {frame_idx}/{frame_count} ({frame_idx/frame_count:.02%}), '
            f'{{ellapsed:.02f}}s, fps={{fps}}'
            f'face count: {len(face_locations)}')
        print(f'frame {frame_idx}/{frame_count} ({frame_idx/frame_count:.02%}), '
              f'face count: {len(face_locations)}')
        
    cap.release()
    out.release()

if __name__ == '__main__':
    main()
