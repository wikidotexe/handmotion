import cv2
import mediapipe as mp
import math
import numpy as np

# Setup MediaPipe Hands & Face
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.7)

mp_draw = mp.solutions.drawing_utils

# Buka kamera
cap = cv2.VideoCapture(0)

# Variabel zoom
zoom_scale = 1.0
zoom_step = 0.02

# Filters
def apply_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def apply_sepia(frame):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia = cv2.transform(frame, kernel)
    sepia = np.clip(sepia, 0, 255).astype(np.uint8)
    return sepia

def apply_invert(frame):
    return cv2.bitwise_not(frame)

def apply_sketch(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    inv = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(inv, (21,21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

def apply_blur(frame):
    return cv2.GaussianBlur(frame, (15, 15), 0)

def apply_edge_detection(frame):
    edges = cv2.Canny(frame, 100, 200)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

def apply_emboss(frame):
    kernel = np.array([[ -2, -1, 0],
                       [ -1,  1, 1],
                       [  0,  1, 2]])
    emboss = cv2.filter2D(frame, -1, kernel) + 128
    return np.clip(emboss, 0, 255).astype(np.uint8)

filters = [None, apply_grayscale, apply_sepia, apply_invert, apply_sketch, apply_blur, apply_edge_detection, apply_emboss]
current_filter = 0
filter_changed = False

# Fungsi deteksi tangan mekar (open) atau genggam (closed)
def is_hand_open(landmarks):
    fingers_open = 0
    # Thumb → cek X
    if landmarks[4][0] > landmarks[3][0]:
        fingers_open += 1
    # Other fingers → cek Y
    tips_ids = [8, 12, 16, 20]
    pip_ids = [6, 10, 14, 18]
    for tip, pip in zip(tips_ids, pip_ids):
        if landmarks[tip][1] < landmarks[pip][1]:
            fingers_open += 1
    return fingers_open >= 3

# Fungsi hitung jarak 2 titik
def distance(pt1, pt2):
    return math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Proses tangan
    hand_results = hands.process(frame_rgb)

    # Proses face
    face_results = face_detection.process(frame_rgb)

    hand_status = "No hand"
    dist = 0
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm_list = []
            for lm in hand_landmarks.landmark:
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            # Cek buka tangan → ganti filter
            if is_hand_open(lm_list):
                hand_status = "Hand Open"
                if not filter_changed:
                    current_filter = (current_filter + 1) % len(filters)
                    filter_changed = True
            else:
                hand_status = "Hand Closed"
                filter_changed = False

            # Zoom gesture (thumb–index)
            thumb_tip = lm_list[4]
            index_tip = lm_list[8]
            dist = distance(thumb_tip, index_tip)

            if dist > 150:
                zoom_scale += zoom_step
            elif dist < 50:
                zoom_scale -= zoom_step

            zoom_scale = max(1.0, min(2.0, zoom_scale))

    # Apply filter
    filtered_frame = frame.copy()
    if filters[current_filter]:
        filtered_frame = filters[current_filter](filtered_frame)

    # Deteksi wajah dan gambar kotak
    face_count = 0
    if face_results.detections:
        for detection in face_results.detections:
            bboxC = detection.location_data.relative_bounding_box
            xmin = int(bboxC.xmin * w)
            ymin = int(bboxC.ymin * h)
            box_width = int(bboxC.width * w)
            box_height = int(bboxC.height * h)

            cv2.rectangle(filtered_frame, (xmin, ymin), (xmin + box_width, ymin + box_height), (255, 0, 0), 2)
            face_count += 1

    # Zoom effect
    center_x, center_y = w // 2, h // 2
    radius_x, radius_y = int(w / (2 * zoom_scale)), int(h / (2 * zoom_scale))
    min_x, max_x = center_x - radius_x, center_x + radius_x
    min_y, max_y = center_y - radius_y, center_y + radius_y

    cropped = filtered_frame[min_y:max_y, min_x:max_x]
    frame_zoomed = cv2.resize(cropped, (w, h))

    # Info text
    filter_name = filters[current_filter].__name__ if filters[current_filter] else "None"
    cv2.putText(frame_zoomed, f'Filter: {filter_name}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.putText(frame_zoomed, f'Hand: {hand_status}', (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.putText(frame_zoomed, f'Distance: {int(dist)} px', (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.putText(frame_zoomed, f'Zoom: {zoom_scale:.2f}x', (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.putText(frame_zoomed, f'Faces: {face_count}', (10, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

    cv2.imshow("Hand & Face Tracker Camera", frame_zoomed)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
