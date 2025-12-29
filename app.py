import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

st.set_page_config(page_title="Finger Counter", layout="centered")
st.title("✋ Finger Counting App")
st.write("Show your hand to the camera")

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Camera input
frame = st.camera_input("Turn on camera")

def count_fingers(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb (special case)
    fingers.append(
        hand_landmarks.landmark[tips[0]].x >
        hand_landmarks.landmark[tips[0] - 1].x
    )

    # Other 4 fingers
    for i in range(1, 5):
        fingers.append(
            hand_landmarks.landmark[tips[i]].y <
            hand_landmarks.landmark[tips[i] - 2].y
        )

    return fingers.count(True)

if frame is not None:
    # Convert image
    image = np.array(frame)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process image
    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            finger_count = count_fingers(hand_landmarks)
            st.success(f"🖐️ Fingers Detected: {finger_count}")
    else:
        st.warning("No hand detected. Show your hand clearly.")
