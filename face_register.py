# import cv2
# import os
# import json
# import qrcode
# import numpy as np
# from datetime import datetime

# # -------------------------------------------------
# # USER REGISTRATION WITH BIO-ID & QR GENERATION
# # -------------------------------------------------
# def register_user(
#     full_name,
#     email,
#     mobile,
#     native_city,
#     bank_name,
#     security_qna
# ):
#     # Folder name uses email (unique & realistic)
#     safe_name = email.replace("@", "_").replace(".", "_")
#     path = f"dataset/{safe_name}"
#     os.makedirs(path, exist_ok=True)

#     # ---------------- GENERATE UNIQUE BIO-ID ----------------
#     # Format: firstname.last4digits@bankname (e.g., vishal.6199@sbi)
#     clean_first_name = full_name.split()[0].lower()
#     last_four_mobile = mobile[-4:]
#     unique_id = f"{clean_first_name}.{last_four_mobile}@{bank_name.lower()}"

#     # ---------------- SAVE USER METADATA ----------------
#     user_data = {
#         "full_name": full_name,
#         "email": email,
#         "mobile": mobile,
#         "native_city": native_city,
#         "bank_name": bank_name,
#         "unique_id": unique_id,
#         "security_questions": security_qna,
#         "failed_attempts": 0,
#         "balance": 5000, # Default starting balance
#         "transactions": [],
#         "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }

#     with open(f"{path}/user.json", "w") as f:
#         json.dump(user_data, f, indent=4)

#     # ---------------- GENERATE QR CODE ----------------
#     qr = qrcode.QRCode(version=1, box_size=10, border=5)
#     qr.add_data(unique_id)
#     qr.make(fit=True)
#     qr_img = qr.make_image(fill_color="black", back_color="white")
#     qr_img.save(f"{path}/qr_code.png")

#     # ---------------- CAMERA SETUP ----------------
#     cam = cv2.VideoCapture(0)
#     if not cam.isOpened():
#         print("Error: Could not open camera.")
#         return

#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

#     face_count = 0
#     eye_count = 0
#     profile_saved = False

#     # ================= STAGE 1: FACE CAPTURE =================
#     while True:
#         ret, frame = cam.read()
#         if not ret: break

#         frame = cv2.flip(frame, 1)
#         clean_frame = frame.copy() # Clean frame for profile pic
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         h, w = frame.shape[:2]
#         fx1, fy1 = w//2 - 120, h//2 - 150
#         fx2, fy2 = w//2 + 120, h//2 + 150

#         # UI Overlay (Visible on screen only)
#         cv2.rectangle(frame, (fx1, fy1), (fx2, fy2), (0, 255, 0), 2)

#         faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#         for (x, y, fw, fh) in faces:
#             if x > fx1 and y > fy1 and x+fw < fx2 and y+fh < fy2:
#                 face = gray[y:y+fh, x:x+fw]
#                 face_count += 1
#                 cv2.imwrite(f"{path}/face_{face_count}.jpg", face)

#                 if not profile_saved:
#                     cv2.imwrite(f"{path}/profile.jpg", clean_frame)
#                     profile_saved = True

#         cv2.putText(frame, f"Face Capture {face_count}/30", (20, 40), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#         cv2.imshow("Registration - Face", frame)

#         if cv2.waitKey(1) == 27 or face_count >= 30: break

#     # ================= STAGE 2: EYE CAPTURE =================
#     while True:
#         ret, frame = cam.read()
#         if not ret: break

#         frame = cv2.flip(frame, 1)
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

#         for (x, y, ew, eh) in eyes:
#             eye = gray[y:y+eh, x:x+ew]
#             eye_count += 1
#             cv2.imwrite(f"{path}/eyes_{eye_count}.jpg", eye)

#         cv2.putText(frame, f"Eye Capture {eye_count}/20", (20, 40), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#         cv2.imshow("Registration - Eyes", frame)

#         if cv2.waitKey(1) == 27 or eye_count >= 20: break

#     cam.release()
#     cv2.destroyAllWindows()

# # -------------------------------------------------
# # QR SCANNER (CAMERA OR FILE)
# # -------------------------------------------------
# def scan_biopay_qr(image_file=None):
#     detector = cv2.QRCodeDetector()
    
#     # CASE 1: Scan from Uploaded Image (Streamlit FileUploader)
#     if image_file is not None:
#         file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
#         img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
#         if img is not None:
#             data, _, _ = detector.detectAndDecode(img)
#             return data
#         return None

#     # CASE 2: Scan from Live Camera
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         return None

#     data = ""
#     while True:
#         ret, frame = cap.read()
#         if not ret: break
        
#         # Detect and Decode
#         data, bbox, _ = detector.detectAndDecode(frame)
        
#         if data:
#             break
            
#         cv2.putText(frame, "Align BioPay QR in Frame", (20, 40), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
#         cv2.imshow("Scan BioPay QR", frame)
        
#         if cv2.waitKey(1) == 27: # ESC to cancel
#             break
            
#     cap.release()
#     cv2.destroyAllWindows()
#     return data



# // original code 
# import cv2, os, json, qrcode, numpy as np
# from datetime import datetime

# def register_user(name, email, mobile, city, bank, qna):
#     safe = email.replace("@","_").replace(".","_")
#     path = f"dataset/{safe}"
#     os.makedirs(path, exist_ok=True)
#     uid = f"{name.split()[0].lower()}.{mobile[-4:]}@{bank.lower()}"
    
#     data = {"full_name": name, "email": email, "mobile": mobile, "bank_name": bank, 
#             "unique_id": uid, "balance": 5000, "transactions": []}
#     with open(f"{path}/user.json", "w") as f: json.dump(data, f, indent=4)
    
#     qr = qrcode.make(uid)
#     qr.save(f"{path}/qr_code.png")
    
#     cam = cv2.VideoCapture(0)
#     count = 0
#     detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     while count < 30:
#         ret, img = cam.read()
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = detector.detectMultiScale(gray, 1.3, 5)
#         for (x,y,w,h) in faces:
#             count += 1
#             cv2.imwrite(f"{path}/face_{count}.jpg", gray[y:y+h, x:x+w])
#             if count == 1: cv2.imwrite(f"{path}/profile.jpg", img)
#         cv2.imshow("Registering...", img)
#         cv2.waitKey(1)
#     cam.release(); cv2.destroyAllWindows()

# def scan_biopay_qr(file=None):
#     det = cv2.QRCodeDetector()
#     if file:
#         img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), 1)
#         val, _, _ = det.detectAndDecode(img)
#         return val
#     cam = cv2.VideoCapture(0)
#     while True:
#         _, img = cam.read()
#         val, _, _ = det.detectAndDecode(img)
#         if val: cam.release(); cv2.destroyAllWindows(); return val
#         cv2.imshow("Scanner", img)
#         if cv2.waitKey(1) == 27: break
#     cam.release(); cv2.destroyAllWindows(); return None



import cv2
import os
import json
import qrcode
import numpy as np
from datetime import datetime

def register_user(full_name, email, mobile, native_city, bank_name, security_qna):
    # Create unique folder based on email
    safe_name = email.replace("@", "_").replace(".", "_")
    path = f"dataset/{safe_name}"
    os.makedirs(path, exist_ok=True)

    # 1. Generate Unique Bio-ID
    clean_first_name = full_name.split()[0].lower()
    last_four_mobile = mobile[-4:]
    unique_id = f"{clean_first_name}.{last_four_mobile}@{bank_name.lower()}"

    # 2. Save Metadata
    user_data = {
        "full_name": full_name,
        "email": email,
        "mobile": mobile,
        "native_city": native_city,
        "bank_name": bank_name,
        "unique_id": unique_id,
        "security_questions": security_qna,
        "balance": 5000,
        "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(f"{path}/user.json", "w") as f:
        json.dump(user_data, f, indent=4)

    # 3. Generate QR Code
    qr = qrcode.make(unique_id)
    qr.save(f"{path}/qr_code.png")

    # 4. Initialize Camera and Detectors
    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    face_count = 0
    eye_count = 0

    # ================= STAGE 1: FACE CAPTURE (30 PICS) =================
    while face_count < 30:
        ret, frame = cam.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Define Green Alignment Box
        h, w = frame.shape[:2]
        fx1, fy1 = w//2 - 120, h//2 - 150
        fx2, fy2 = w//2 + 120, h//2 + 150
        cv2.rectangle(frame, (fx1, fy1), (fx2, fy2), (0, 255, 0), 2)
        cv2.putText(frame, "ALIGN FACE IN GREEN BOX", (fx1, fy1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, fw, fh) in faces:
            # Capture only if within alignment box
            if x > fx1 and y > fy1 and x+fw < fx2 and y+fh < fy2:
                face_count += 1
                cv2.imwrite(f"{path}/face_{face_count}.jpg", gray[y:y+fh, x:x+fw])
                if face_count == 1: cv2.imwrite(f"{path}/profile.jpg", frame)

        cv2.putText(frame, f"Face: {face_count}/30", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Enrollment Step 1: Face", frame)
        if cv2.waitKey(1) == 27: break

    cv2.destroyWindow("Enrollment Step 1: Face")

    # ================= STAGE 2: EYE CAPTURE (20 PICS) =================
    while eye_count < 20:
        ret, frame = cam.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        eyes = eye_cascade.detectMultiScale(gray, 1.3, 10)
        for (x, y, ew, eh) in eyes:
            eye_count += 1
            cv2.imwrite(f"{path}/eyes_{eye_count}.jpg", gray[y:y+eh, x:x+ew])
        
        cv2.putText(frame, f"Eyes: {eye_count}/20", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, "BLINK OR MOVE EYES SLIGHTLY", (120, 450), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.imshow("Enrollment Step 2: Eyes", frame)
        if cv2.waitKey(1) == 27: break

    cam.release()
    cv2.destroyAllWindows()

# ================= NEW: QR SCANNER FUNCTION =================
def scan_biopay_qr(image_file=None):
    detector = cv2.QRCodeDetector()
    
    # CASE 1: Scan from Uploaded Image (Streamlit FileUploader)
    if image_file is not None:
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is not None:
            data, _, _ = detector.detectAndDecode(img)
            return data
        return None

    # CASE 2: Scan from Live Camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None

    data = ""
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        # Detect and Decode
        data, bbox, _ = detector.detectAndDecode(frame)
        
        if data:
            break
            
        cv2.putText(frame, "Align BioPay QR in Frame", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.imshow("Scan BioPay QR", frame)
        
        if cv2.waitKey(1) == 27: # ESC to cancel
            break
            
    cap.release()
    cv2.destroyAllWindows()
    return data