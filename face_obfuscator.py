import face_recognition
import cv2

print('face_recognition: v{}'.format(face_recognition.__version__))
print('opencv: v{}'.format(cv2.__version__))

input_filename = '/opt/face_recognition/examples/short_hamilton_clip.mp4'
output_filename = '/workspace/short_hamilton_clip_blur.mp4'

def get_video_info(cap):
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return width, height, fps, frame_count

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

def process_frame(frame):
    # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    small_frame = frame

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(small_frame, model='cnn')

    if face_locations:
        print('found faces')

    # Display the results
    for top, right, bottom, left in face_locations:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        # top *= 4
        # right *= 4
        # bottom *= 4
        # left *= 4

        # Extract the region of the image that contains the face
        face_image = frame[top:bottom, left:right]

        # Blur the face image
        face_image = cv2.GaussianBlur(face_image, (99, 99), 30)

        # Put the blurred face region back into the frame image
        frame[top:bottom, left:right] = face_image
    
    return frame

frame_count = 0
while True:
    ret, frame = cap.read()
    if frame is None:
        break
    frame = process_frame(frame)
    out.write(frame)
    print(frame_count)
    frame_count += 1

cap.release()
out.release()
