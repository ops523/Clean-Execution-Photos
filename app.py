import streamlit as st
import cv2
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.set_page_config(layout="wide")

st.title("🧱 Wall Cleanup Tool (Pixel-Safe Editing)")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(image)

    h, w = img_np.shape[:2]

    st.subheader("Step 1: Draw over unwanted area (G, T, wires, etc.)")

    canvas = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",  # transparent red
        stroke_width=15,
        stroke_color="#FF0000",
        background_image=image,
        update_streamlit=True,
        height=h,
        width=w,
        drawing_mode="freedraw",
        key="canvas",
    )

    if st.button("✨ Clean Image"):
        if canvas.image_data is not None:

            # Convert canvas mask
            mask = canvas.image_data[:, :, 0]  # take red channel
            mask = np.where(mask > 0, 255, 0).astype("uint8")

            # Inpaint
            cleaned = cv2.inpaint(img_np, mask, 3, cv2.INPAINT_TELEA)

            st.subheader("✅ Cleaned Output")
            st.image(cleaned, use_column_width=True)

            # Download
            result_pil = Image.fromarray(cleaned)
            st.download_button(
                "⬇ Download Clean Image",
                data=result_pil.tobytes(),
                file_name="cleaned.png",
                mime="image/png"
            )
