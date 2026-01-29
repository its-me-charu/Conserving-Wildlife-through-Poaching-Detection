import streamlit as st
from io import BytesIO
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import cv2
import pickle
from poaching_detection import detect_poachers, read_video
from face_detection import compare_faces_and_track_unique
import os
import base64
import tempfile
import smtplib
from email.message import EmailMessage
import ssl

users = {
    "authority": "securepass",
    "admin": "admin123",
}

if 'rerun_flag' not in st.session_state:
    st.session_state['rerun_flag'] = False

def fake_rerun():
    st.session_state['rerun_flag'] = not st.session_state['rerun_flag']

def send_email_with_report(receiver_email, subject, body, attachment_path, attachment_filename):
    sender_email = "poaching_detection@gmail.com"
    sender_password = "*******"  

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=attachment_filename)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)

# -------------------- PDF Report Generation --------------------
def generate_pdf_report(video_name, resolution, total_frames, poacher_frames, unique_poacher_frames, frames):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, 750, "Poaching Detection Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Report Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 700, f"Video File: {video_name}")
    c.drawString(50, 680, f"Resolution: {resolution[0]} x {resolution[1]}")
    c.drawString(50, 660, f"Total Frames Analyzed: {total_frames}")

    if poacher_frames and len(poacher_frames) > 0:
        c.drawString(50, 640, f"Poacher Detected: YES")
        c.drawString(50, 620, f"Detected in {len(poacher_frames)} frames")
        c.drawString(50, 600, f"Unique Poacher Appearances: {len(unique_poacher_frames)}")

        y_pos = 580
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_pos, "Thumbnails of Detected Poachers:")
        y_pos -= 20

        for i, idx in enumerate(unique_poacher_frames[:5]):
            img = frames[idx]
            img_path = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg').name
            cv2.imwrite(img_path, img)
            image_reader = ImageReader(img_path)

            img_width, img_height = image_reader.getSize()
            aspect = img_height / img_width
            display_width = 100
            display_height = display_width * aspect

            x = 50 + (i % 3) * 160
            c.drawImage(image_reader, x, y_pos - display_height, width=display_width, height=display_height)
            c.drawString(x, y_pos - display_height - 15, f"Frame {idx + 1}")
            os.remove(img_path)

            if (i + 1) % 3 == 0:
                y_pos -= display_height + 40

        c.showPage()
    else:
        c.drawString(50, 640, "Poacher Detected: NO")
        c.drawString(50, 620, "No suspicious activity found in the analyzed frames.")

    c.save()
    buffer.seek(0)
    return buffer

# -------------------- Model Loading --------------------
model_path = pickle.load(open('model.pkl', 'rb'))

# -------------------- Login Page --------------------
def login_page():
    st.markdown("<h1 style='color: #2c3e50;'>Poaching Detection System Login</h1>", unsafe_allow_html=True)
    st.markdown("---")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state['logged_in'] = True
            fake_rerun()
        else:
            st.error("Invalid username or password")

# -------------------- Detection Page --------------------
def detection_page():
    st.markdown(
        """
        <div style='
            background-color: #2c3e50;
            padding: 20px;
            border-radius: 10px;
            color: white;
            margin-bottom: 20px;'>
            <h2>Wildlife Conservation: Poaching Detection</h2>
            <p>Our system analyzes video footage from protected areas, identifies suspicious activities, and generates alerts to help safeguard wildlife and preserve biodiversity.</p>
        </div>
        """, unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Upload a video file (mp4, avi, mov)", type=["mp4", "avi", "mov"])

    if uploaded_file:
        video_path = "temp_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("Video uploaded successfully!")

        with st.spinner("Processing video for poaching detection. Please wait..."):
            poacher_frames, resolution = detect_poachers(model_path, video_path)
            frames, _, _ = read_video(video_path)

        if poacher_frames is None:
            st.error("Could not process the video.")
        elif len(poacher_frames) == 0:
            st.success("No poachers detected in the video.")
            unique_poacher_frames = []
        else:
            # Play alarm
            alarm_path = 'C:\\Users\\charu\\OneDrive\\Documents\\PythonProject\\Poaching Detection\\poaching-detection-main\\alarm.wav'
            with open(alarm_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            audio_html = f"""
                <audio autoplay>
                    <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

            st.warning(f"Poachers detected in {len(poacher_frames)} frames.")
            unique_poacher_frames = compare_faces_and_track_unique(poacher_frames, frames)

            st.markdown("<h4>Unique Poacher Appearances:</h4>", unsafe_allow_html=True)
            img_cols = st.columns(5)
            for idx, col in zip(unique_poacher_frames[:5], img_cols):
                with col:
                    st.image(cv2.cvtColor(frames[idx], cv2.COLOR_BGR2RGB), caption=f"Frame {idx + 1}", use_column_width=True)

        with st.spinner("Generating PDF report..."):
            pdf_buffer = generate_pdf_report(
                uploaded_file.name,
                resolution,
                len(frames),
                poacher_frames,
                unique_poacher_frames,
                frames
            )
        st.success("PDF report generated successfully.")

        with st.expander("Preview Report"):
            base64_pdf = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)

        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name="poaching_report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.markdown("---")
        with st.form("email_form"):
            st.subheader("Send Report via Email")
            receiver_email = st.text_input("Recipient Email")
            subject = st.text_input("Subject", value="Poaching Detection Report")
            body = st.text_area("Message", value="Please find the attached poaching detection report.")
            send_btn = st.form_submit_button("Send Email")

            if send_btn:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(pdf_buffer.getvalue())
                    tmp_path = tmp_file.name

                try:
                    send_email_with_report(receiver_email, subject, body, tmp_path, "poaching_report.pdf")
                    st.success("Email sent successfully.")
                except Exception as e:
                    st.error(f"Failed to send email: {e}")
                finally:
                    os.remove(tmp_path)

        st.markdown("<hr style='border-top: 2px solid #2c3e50;'>", unsafe_allow_html=True)

# -------------------- Main --------------------
def main():
    st.set_page_config(page_title="Poaching Detection System", layout="wide")
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        login_page()
    else:
        detection_page()

if __name__ == "__main__":
    main()
