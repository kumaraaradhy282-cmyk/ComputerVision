import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Finger Counter", layout="centered")
st.title("✋ Finger Counting MVP")
st.write("Show one hand clearly on a plain background")

image_file = st.camera_input("Turn on Camera")

def count_fingers(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (35, 35), 0)

    _, thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return 0

    hand = max(contours, key=cv2.contourArea)
    hull = cv2.convexHull(hand, returnPoints=False)

    if hull is None or len(hull) < 3:
        return 0

    defects = cv2.convexityDefects(hand, hull)

    if defects is None:
        return 1

    count = 0
    for i in range(defects.shape[0]):
        _, _, _, depth = defects[i, 0]
        if depth > 10000:
            count += 1

    return count + 1

if image_file is not None:
    img = np.array(image_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    fingers = count_fingers(img)
    st.success(f"🖐️ Fingers Detected: {fingers}")
