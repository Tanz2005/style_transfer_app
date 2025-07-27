import streamlit as st
from PIL import Image
from utils import style_transfer
from io import BytesIO

st.set_page_config(page_title="🎨 Neural Style Transfer Web App")

st.title("🎨 Neural Style Transfer Web App")
st.write("Upload a content image and a style image to generate stylized art.")

# Upload section
content_file = st.file_uploader("Upload Content Image", type=["jpg", "jpeg", "png"])
style_file = st.file_uploader("Upload Style Image", type=["jpg", "jpeg", "png"])

# Function to convert PIL image to byte stream for download
def convert_image_to_bytes(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Main processing
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
        with st.spinner("Applying style transfer..."):
            output_img = style_transfer(content_img, style_img, strength=style_strength)
        st.image(output_img, caption="Stylized Image", use_container_width=True)

        st.download_button(
            label="⬇️ Download Stylized Image",
            data=convert_image_to_bytes(output_img),
            file_name="stylized_output.png",
            mime="image/png"
        )

else:
    st.info("👆 Please upload both a content and style image to begin.")
