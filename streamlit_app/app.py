import streamlit as st
from model_helper import predict_damage

st.title("Vehicle Damage Detection")
st.subheader("Upload an image of a vehicle to detect damage.")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image_path ="temp_file.jpg"

    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())

    st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

    damage_prediction = predict_damage(image_path)
    st.info(f"Prediction: {damage_prediction}")
