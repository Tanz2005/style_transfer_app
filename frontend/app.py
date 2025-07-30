import streamlit as st
from PIL import Image
from io import BytesIO
import requests

st.set_page_config(page_title="🎨 Neural Style Transfer Web App")

st.title("🎨 Neural Style Transfer Web App")
st.write("Upload a content image and a style image to generate stylized art using Flask backend.")

content_file = st.file_uploader("Upload Content Image", type=["jpg", "jpeg", "png"])
style_file = st.file_uploader("Upload Style Image", type=["jpg", "jpeg", "png"])

def convert_image_to_bytes(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

if content_file and style_file:
    content_img = Image.open(content_file).convert("RGB")
    style_img = Image.open(style_file).convert("RGB")

    st.subheader("Original Images")
    col1, col2 = st.columns(2)
    with col1:
        st.image(content_img, caption="Content Image", use_container_width=True)
    with col2:
        st.image(style_img, caption="Style Image", use_container_width=True)

    style_strength = st.slider("Style Strength", 0.0, 1.0, 1.0, step=0.1)

    if st.button("🎨 Stylize"):
        with st.spinner("Sending to backend..."):
            response = requests.post(
                "http://localhost:5000/stylize",
                files={
                    "content": content_file.getvalue(),
                    "style": style_file.getvalue()
                },
                data={"strength": style_strength}
            )
            if response.status_code == 200:
                result_img = Image.open(BytesIO(response.content))
                st.image(result_img, caption="Stylized Image", use_container_width=True)
                st.download_button(
                    label="⬇️ Download Stylized Image",
                    data=convert_image_to_bytes(result_img),
                    file_name="stylized_output.png",
                    mime="image/png"
                )
            else:
                st.error("Error from backend: " + response.text)
else:
    st.info("👇 Please upload both a content and style image to begin.")
