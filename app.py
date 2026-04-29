import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(layout="wide")

st.title("🧱 Wall Cleanup Tool (Stable Version)")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    h, w = img_np.shape[:2]

    st.subheader("Step 1: Select area to clean")

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, use_column_width=True)

    with col2:
        st.write("Adjust selection box:")

        x1 = st.slider("Left (X1)", 0, w, int(w * 0.85))
        x2 = st.slider("Right (X2)", 0, w, w)

        y1 = st.slider("Top (Y1)", 0, h, int(h * 0.2))
        y2 = st.slider("Bottom (Y2)", 0, h, int(h * 0.8))

    if st.button("✨ Clean Image"):

        # Create mask
        mask = np.zeros((h, w), dtype=np.uint8)
        mask[y1:y2, x1:x2] = 255

        # Inpaint
        cleaned = cv2.inpaint(img_np, mask, 3, cv2.INPAINT_TELEA)

        st.subheader("✅ Cleaned Output")
        st.image(cleaned, use_column_width=True)

        # Download
        result_pil = Image.fromarray(cleaned)
        buf = io.BytesIO()
        result_pil.save(buf, format="PNG")

        st.download_button(
            "⬇ Download Clean Image",
            data=buf.getvalue(),
            file_name="cleaned.png",
            mime="image/png"
        )
