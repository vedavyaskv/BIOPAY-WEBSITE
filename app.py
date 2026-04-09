# # import streamlit as st
# # import os
# # import geocoder
# # import plotly.graph_objects as go
# # from face_register import register_user, scan_biopay_qr
# # from model_utils import train_model
# # from face_auth import authenticate
# # from blink_auth import blink_verification
# # from user_utils import (
# #     get_all_users, get_user_data, update_profile_photo,
# #     update_failed_attempts, delete_user, rename_user
# # )
# # from risk_engine import calculate_risk
# # from otp_utils import send_otp

# # # ---------------- PAGE CONFIG & STYLING ----------------
# # st.set_page_config(page_title="BioPay | Secure Face Payments", layout="wide", page_icon="🛡️")

# # # Custom CSS for "Grand" Look and GPay-style Tick Animation
# # st.markdown("""
# #     <style>
# #     .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
# #     .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #ffffff; }
# #     .main-title {
# #         font-size: 3.5rem !important;
# #         font-weight: 800;
# #         text-align: center;
# #         background: -webkit-linear-gradient(#00d2ff, #3a7bd5);
# #         -webkit-background-clip: text;
# #         -webkit-text-fill-color: transparent;
# #         margin-bottom: 1rem !important;
# #     }
# #     div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown):not(:first-child) {
# #         background: none; border: none; box-shadow: none;
# #     }
# #     .stTabs [data-testid="stVerticalBlock"] {
# #         background: rgba(255, 255, 255, 0.05);
# #         backdrop-filter: blur(15px);
# #         border-radius: 20px;
# #         padding: 40px;
# #         border: 1px solid rgba(255, 255, 255, 0.1);
# #         box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
# #     }
# #     hr { margin: 1em 0 !important; border: 0 !important; border-top: 1px solid rgba(255,255,255,0.1) !important; background: transparent !important; }
# #     .stButton>button {
# #         border-radius: 12px;
# #         background: linear-gradient(45deg, #3a7bd5, #00d2ff);
# #         color: white; border: none; padding: 12px; font-weight: bold; transition: 0.3s;
# #     }
    
# #     /* Success Tick Animation CSS */
# #     .checkmark-circle {
# #         width: 150px; height: 150px;
# #         position: relative; display: inline-block; vertical-align: top;
# #         margin-left: auto; margin-right: auto; left: 0; right: 0; text-align: center;
# #     }
# #     .checkmark-circle .background { width: 150px; height: 150px; border-radius: 50%; background: #2ecc71; position: absolute; }
# #     .checkmark-circle .checkmark { border-radius: 5px; }
# #     .checkmark-circle .checkmark.draw:after {
# #         animation-delay: 100ms; animation-duration: 1s; animation-timing-function: ease;
# #         animation-name: checkmark; transform: scaleX(-1) rotate(135deg);
# #     }
# #     .checkmark-circle .checkmark:after {
# #         opacity: 1; height: 75px; width: 37.5px;
# #         transform-origin: left top; border-right: 15px solid white;
# #         border-top: 15px solid white; content: '';
# #         left: 37.5px; top: 75px; position: absolute;
# #     }
# #     @keyframes checkmark {
# #         0% { height: 0; width: 0; opacity: 1; }
# #         20% { height: 0; width: 37.5px; opacity: 1; }
# #         40% { height: 75px; width: 37.5px; opacity: 1; }
# #         100% { height: 75px; width: 37.5px; opacity: 1; }
# #     }
# #     </style>
# #     """, unsafe_allow_html=True)

# # st.markdown('<h1 class="main-title">BIOPAY SECURE SYSTEM</h1>', unsafe_allow_html=True)

# # # ---------------- SESSION STATE ----------------
# # if "balance" not in st.session_state:
# #     st.session_state.balance = 5000
# # if "qr_scanned_id" not in st.session_state:
# #     st.session_state.qr_scanned_id = ""
# # if "payment_step" not in st.session_state:
# #     st.session_state.payment_step = "input"
# # if "last_tx_details" not in st.session_state:
# #     st.session_state.last_tx_details = {}

# # # ---------------- TOP NAVIGATION ----------------
# # tab_home, tab_reg, tab_list, tab_pay = st.tabs(["🏠 HOME", "👤 REGISTER", "📂 DIRECTORY", "💸 PAYMENT"])

# # # ==================================================
# # # TAB 0: HOME DASHBOARD
# # # ==================================================
# # with tab_home:
# #     st.markdown("### 📱 Digital Wallet Dashboard")
# #     h_col1, h_col2, h_col3 = st.columns(3)
    
# #     with h_col1:
# #         st.markdown("#### QR Scanner")
# #         uploaded_qr = st.file_uploader("Upload QR Image", type=['png', 'jpg', 'jpeg'], key="qr_home")
# #         if st.button("🔍 OPEN CAMERA SCANNER"):
# #             scanned_id = scan_biopay_qr()
# #             if scanned_id:
# #                 st.session_state.qr_scanned_id = scanned_id
# #                 st.success(f"✅ ID Detected: {scanned_id}")
# #                 st.info("Switch to **PAYMENT** tab to complete.")
        
# #     with h_col2:
# #         st.markdown("#### Manual Pay")
# #         m_id_home = st.text_input("Enter Bio-ID", key="manual_home")
# #         if st.button("Proceed"):
# #             st.session_state.qr_scanned_id = m_id_home
# #             st.info("Details saved. Open **PAYMENT** tab.")

# #     with h_col3:
# #         st.markdown("#### Secure Balance")
# #         users = get_all_users()
# #         if users:
# #             u_check = st.selectbox("Select Profile", users, key="home_bal")
# #             if st.button("🔓 SHOW BALANCE"):
# #                 st.info("Verifying Biometrics...")
                
# #                 # --- THE MODIFICATION START ---
# #                 # authenticate() now strictly checks if 'u_check' is in front of the cam
# #                 if authenticate(u_check):
# #                     # We store the verified user in session_state to unlock the Payment Tab
# #                     st.session_state.current_authenticated_user = u_check 
                    
# #                     u_info = get_user_data(u_check)
# #                     bal = u_info.get('balance', 5000)
                    
# #                     st.metric("Verified Balance", f"₹{bal}")
# #                     st.success(f"✅ Identity Confirmed: {u_check}")
# #                     st.balloons() # Optional: small visual cue for successful login
# #                 else:
# #                     # If auth fails, we clear any previous session to prevent fraud
# #                     if "current_authenticated_user" in st.session_state:
# #                         del st.session_state.current_authenticated_user
# #                     st.error("❌ Face Mismatch! Access Denied.")
# #                 # --- THE MODIFICATION END ---
# # # ==================================================
# # # TAB 1: REGISTER USER
# # # ==================================================
# # with tab_reg:
# #     st.markdown("### ✨ Identity Enrollment")
# #     col1, col2 = st.columns(2)
# #     with col1:
# #         full_name = st.text_input("Full Name", key="reg_fn")
# #         email = st.text_input("Email ID", key="reg_em")
# #         bank_name = st.selectbox("Select Bank", ["SBI", "HDFC", "ICICI", "Axis", "PNB"], key="reg_bank")
# #     with col2:
# #         mobile = st.text_input("Mobile Number", key="reg_mb")
# #         native_city = st.text_input("Native City", key="reg_nc")
# #         agree = st.checkbox("I accept Privacy Terms", key="reg_ag")

# #     if st.button("🚀 INITIALIZE CAPTURE"):
# #         with st.status("Registering...") as status:
# #             register_user(full_name, email, mobile, native_city, bank_name, {})
# #             train_model()
# #             status.update(label="Complete!", state="complete")
# #         st.success("Registration Successful!")

# # # ==================================================
# # # TAB 2: DIRECTORY
# # # ==================================================
# # # ==================================================
# # # TAB 2: REGISTERED PROFILES (DIRECTORY)
# # # ==================================================
# # with tab_list:
# #     st.markdown("### 📂 Registered Biometric Profiles")
# #     users = get_all_users()
    
# #     if not users:
# #         st.info("No active biometric profiles found.")
# #     else:
# #         # Display users in a clean 3-column grid
# #         for i in range(0, len(users), 3):
# #             cols = st.columns(3)
# #             for j in range(3):
# #                 if i + j < len(users):
# #                     user_folder = users[i + j]
# #                     user_info = get_user_data(user_folder)
                    
# #                     # Metadata Extraction
# #                     full_name = user_info.get("full_name", "Unknown User")
# #                     bio_id = user_info.get("unique_id", "Not Assigned")
                    
# #                     with cols[j]:
# #                         with st.container(border=True):
# #                             # 1. Profile Photo
# #                             img_path = f"dataset/{user_folder}/profile.jpg"
# #                             if os.path.exists(img_path):
# #                                 st.image(img_path, width=250)
# #                             else:
# #                                 st.markdown("👤 **Photo Not Found**")
                            
# #                             st.markdown(f"#### {full_name}")
# #                             st.caption(f"🆔 {bio_id}")

# #                             # --- THE FIX: QR CODE FEATURE ---
# #                             qr_path = f"dataset/{user_folder}/qr_code.png"
# #                             if os.path.exists(qr_path):
# #                                 with st.expander("🔍 Show My QR Code"):
# #                                     st.image(qr_path, caption="Scan this to receive payments", width=200)
# #                             else:
# #                                 st.warning("⚠️ QR Code missing for this profile.")

# #                             # 2. Delete Action
# #                             if st.button("🗑️ Purge Profile", key=f"del_{user_folder}"):
# #                                 delete_user(user_folder)
# #                                 st.rerun()

# # # ==================================================
# # # TAB 3: PAYMENT (GRAND 3-STAGE LOGIC)
# # # ==================================================
# # # ==================================================
# # # TAB 3: PAYMENT (SECURE FLOW WITH SUCCESS SCREEN)
# # # ==================================================
# # with tab_pay:
# #     if "current_authenticated_user" not in st.session_state:
# #         st.warning("🔒 Please verify your identity in the HOME tab before making a payment.")
# #         st.stop()

# #     sender = st.session_state.current_authenticated_user
# #     u_info = get_user_data(sender)
# #     current_balance = u_info.get("balance", 5000)

# #     # ---------------- STAGE 1: INPUT ----------------
# #     if st.session_state.payment_step == "input":
# #         st.markdown("### 💸 Secure Payment Terminal")
# #         st.caption(f"Authenticated as: **{u_info.get('full_name')}**")

# #         col1, col2 = st.columns(2)

# #         with col1:
# #             st.markdown("#### 🔍 Scan Receiver QR")
# #             if st.button("OPEN QR SCANNER"):
# #                 rid = scan_biopay_qr()
# #                 if rid:
# #                     st.session_state.qr_scanned_id = rid
# #                     st.session_state.payment_step = "confirm"
# #                     st.rerun()

# #         with col2:
# #             st.markdown("#### ⌨️ Manual Receiver Entry")
# #             rid = st.text_input("Receiver Bio-ID", value=st.session_state.qr_scanned_id)
# #             if st.button("Proceed"):
# #                 if rid:
# #                     st.session_state.qr_scanned_id = rid
# #                     st.session_state.payment_step = "confirm"
# #                     st.rerun()

# #     # ---------------- STAGE 2: CONFIRM ----------------
# #     elif st.session_state.payment_step == "confirm":
# #         st.markdown("### 🛡️ Confirm Transaction")

# #         with st.container(border=True):
# #             c1, c2 = st.columns(2)
# #             with c1:
# #                 st.write("**Receiver Bio-ID**")
# #                 st.info(st.session_state.qr_scanned_id)
# #                 amount = st.number_input("Amount (₹)", min_value=1, value=100)

# #             with c2:
# #                 st.write("**Sender**")
# #                 st.success(u_info.get("full_name"))
# #                 st.metric("Available Balance", f"₹{current_balance}")

# #         if amount > current_balance:
# #             st.error("❌ Insufficient balance")
# #             can_pay = False
# #         else:
# #             can_pay = True

# #         b1, b2 = st.columns(2)
# #         with b1:
# #             if st.button("CANCEL"):
# #                 st.session_state.payment_step = "input"
# #                 st.rerun()

# #         with b2:
# #             if st.button("AUTHENTICATE & PAY", disabled=not can_pay):
# #                 st.info("🔐 Face Verification")
# #                 if authenticate(sender):
# #                     st.info("👁️ Liveness Verification")
# #                     if blink_verification():
# #                         # --- SUCCESS PATH ---
# #                         from user_utils import update_transaction
# #                         update_transaction(sender, amount, st.session_state.qr_scanned_id)

# #                         st.session_state.last_tx_details = {
# #                             "sender": sender,
# #                             "receiver": st.session_state.qr_scanned_id,
# #                             "amount": amount
# #                         }

# #                         st.session_state.payment_step = "success"
# #                         st.rerun()
# #                     else:
# #                         st.error("❌ Liveness failed (Blink not detected)")
# #                 else:
# #                     st.error("❌ Face mismatch")

# #     # ---------------- STAGE 3: SUCCESS ----------------
# #     elif st.session_state.payment_step == "success":
# #         tx = st.session_state.last_tx_details

# #         # SUCCESS TICK
# #         st.markdown("""
# #         <div style="text-align:center; padding:40px;">
# #             <div class="checkmark-circle">
# #                 <div class="background"></div>
# #                 <div class="checkmark draw"></div>
# #             </div>
# #             <h1 style="color:#2ecc71; margin-top:20px;">Transaction Successful</h1>
# #         </div>
# #         """, unsafe_allow_html=True)

# #         # TRANSACTION RECEIPT
# #         with st.container(border=True):
# #             st.markdown("### 📄 Transaction Status")

# #             c1, c2 = st.columns(2)
# #             with c1:
# #                 st.write("**Sender Bio-ID**")
# #                 st.code(tx["sender"])
# #                 st.write("**Receiver Bio-ID**")
# #                 st.code(tx["receiver"])

# #             with c2:
# #                 st.write("**Amount Paid**")
# #                 st.markdown(f"<h2 style='color:#2ecc71;'>₹ {tx['amount']}</h2>", unsafe_allow_html=True)
# #                 st.write("**Status**")
# #                 st.success("SUCCESS")

# #         if st.button("DONE"):
# #             st.session_state.payment_step = "input"
# #             st.session_state.qr_scanned_id = ""
# #             st.session_state.last_tx_details = {}
# #             st.rerun()

# import streamlit as st
# import os
# import geocoder
# import plotly.graph_objects as go
# import pickle
# from face_register import register_user, scan_biopay_qr
# from model_utils import train_model
# from face_auth import authenticate
# from blink_auth import blink_verification
# from user_utils import (
#     get_all_users, get_user_data, update_profile_photo,
#     update_failed_attempts, delete_user, rename_user, update_transaction
# )

# # ---------------- PAGE CONFIG & STYLING ----------------
# st.set_page_config(page_title="BioPay | Secure Face Payments", layout="wide", page_icon="🛡️")

# st.markdown("""
#     <style>
#     .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
#     .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #ffffff; }
#     .main-title {
#         font-size: 3.5rem !important;
#         font-weight: 800;
#         text-align: center;
#         background: -webkit-linear-gradient(#00d2ff, #3a7bd5);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 1rem !important;
#     }
#     .stTabs [data-testid="stVerticalBlock"] {
#         background: rgba(255, 255, 255, 0.05);
#         backdrop-filter: blur(15px);
#         border-radius: 20px;
#         padding: 40px;
#         border: 1px solid rgba(255, 255, 255, 0.1);
#     }
#     .stButton>button {
#         border-radius: 12px;
#         background: linear-gradient(45deg, #3a7bd5, #00d2ff);
#         color: white; font-weight: bold; width: 100%;
#     }
#     .checkmark-circle {
#         width: 150px; height: 150px;
#         position: relative; display: inline-block;
#         margin: 0 auto; text-align: center;
#     }
#     .checkmark-circle .background { width: 150px; height: 150px; border-radius: 50%; background: #2ecc71; position: absolute; }
#     .checkmark-circle .checkmark.draw:after {
#         animation-delay: 100ms; animation-duration: 1s; animation-timing-function: ease;
#         animation-name: checkmark; transform: scaleX(-1) rotate(135deg);
#     }
#     .checkmark-circle .checkmark:after {
#         opacity: 1; height: 75px; width: 37.5px;
#         transform-origin: left top; border-right: 15px solid white;
#         border-top: 15px solid white; content: '';
#         left: 37.5px; top: 75px; position: absolute;
#     }
#     @keyframes checkmark {
#         0% { height: 0; width: 0; opacity: 1; }
#         20% { height: 0; width: 37.5px; opacity: 1; }
#         40% { height: 75px; width: 37.5px; opacity: 1; }
#         100% { height: 75px; width: 37.5px; opacity: 1; }
#     }
#     </style>
#     """, unsafe_allow_html=True)

# st.markdown('<h1 class="main-title">BIOPAY SECURE SYSTEM</h1>', unsafe_allow_html=True)

# if "qr_scanned_id" not in st.session_state: st.session_state.qr_scanned_id = ""
# if "payment_step" not in st.session_state: st.session_state.payment_step = "input"
# if "last_tx_details" not in st.session_state: st.session_state.last_tx_details = {}

# tab_home, tab_reg, tab_list, tab_pay = st.tabs(["🏠 HOME", "👤 REGISTER", "📂 DIRECTORY", "💸 PAYMENT"])

# with tab_home:
#     st.markdown("### 📱 Dashboard")
#     h_col1, h_col2, h_col3 = st.columns(3)
#     with h_col1:
#         if st.button("🔍 OPEN CAMERA SCANNER"):
#             scanned = scan_biopay_qr()
#             if scanned:
#                 st.session_state.qr_scanned_id = scanned
#                 st.success(f"ID Detected: {scanned}")
#     with h_col2:
#         m_id = st.text_input("Manual Bio-ID Entry")
#         if st.button("Save ID"): st.session_state.qr_scanned_id = m_id
#     with h_col3:
#         users = get_all_users()
#         if users:
#             u_check = st.selectbox("Select Profile", users)
#             if st.button("🔓 SHOW BALANCE"):
#                 if authenticate(u_check):
#                     st.session_state.current_authenticated_user = u_check
#                     u_data = get_user_data(u_check)
#                     st.metric("Balance", f"₹{u_data.get('balance', 0)}")
#                     st.success("Identity Verified")

# with tab_reg:
#     st.markdown("### ✨ Enrollment")
#     fn = st.text_input("Full Name")
#     em = st.text_input("Email")
#     bn = st.selectbox("Bank", ["SBI", "HDFC", "ICICI", "Axis"])
#     mb = st.text_input("Mobile")
#     nc = st.text_input("Native City")
#     if st.button("🚀 REGISTER"):
#         register_user(fn, em, mb, nc, bn, {})
#         train_model()
#         st.success("User Registered!")

# with tab_list:
#     users = get_all_users()
#     for u in users:
#         with st.expander(f"User: {u}"):
#             u_info = get_user_data(u)
#             st.write(f"Bio-ID: {u_info.get('unique_id')}")
#             if os.path.exists(f"dataset/{u}/qr_code.png"):
#                 st.image(f"dataset/{u}/qr_code.png", width=150)
#             if st.button("🗑️ Delete", key=f"del_{u}"):
#                 delete_user(u); st.rerun()

# # with tab_pay:
# #     if "current_authenticated_user" not in st.session_state:
# #         st.warning("🔒 Please verify identity in HOME tab first.")
# #         st.stop()

# #     sender = st.session_state.current_authenticated_user
# #     u_info = get_user_data(sender)
    
# #     if st.session_state.payment_step == "input":
# #         st.markdown("### 💸 Payment Terminal")
# #         st.caption(f"Payer: {u_info.get('full_name')}")
# #         rid = st.text_input("Recipient Bio-ID", value=st.session_state.qr_scanned_id)
# #         if st.button("Proceed to Pay"):
# #             st.session_state.qr_scanned_id = rid
# #             st.session_state.payment_step = "confirm"
# #             st.rerun()

# #     elif st.session_state.payment_step == "confirm":
# #         st.markdown("### 🛡️ Confirm Transaction")
# #         current_bal = u_info.get("balance", 0)
# #         c1, c2 = st.columns(2)
# #         with c1:
# #             st.info(f"To: {st.session_state.qr_scanned_id}")
# #             amt = st.number_input("Amount (₹)", min_value=1, value=100)
# #         with c2:
# #             st.metric("Your Balance", f"₹{current_bal}")
        
# #         if st.button("⚡ AUTHENTICATE & SEND", disabled=(amt > current_bal)):
# #             status = st.empty()
# #             with status.container():
# #                 st.write("⏳ Step 1: Face Auth...")
# #                 if authenticate(sender):
# #                     st.write("✅ Step 1 Success")
# #                     st.write("⏳ Step 2: Liveness...")
# #                     if blink_verification():
# #                         if update_transaction(sender, amt, st.session_state.qr_scanned_id):
# #                             st.session_state.last_tx_details = {
# #                                 "sender": u_info.get('unique_id'),
# #                                 "receiver": st.session_state.qr_scanned_id,
# #                                 "amount": amt
# #                             }
# #                             st.session_state.payment_step = "success"
# #                             st.rerun()
# #                     else: st.error("Liveness Failed")
# #                 else: st.error("Face Auth Failed")

# #     elif st.session_state.payment_step == "success":
# #         tx = st.session_state.last_tx_details
# #         st.markdown("""
# #             <div style="text-align:center; padding:30px;">
# #                 <div class="checkmark-circle"><div class="background"></div><div class="checkmark draw"></div></div>
# #                 <h1 style="color:#2ecc71;">Transaction Successful</h1>
# #             </div>""", unsafe_allow_html=True)
# #         with st.container(border=True):
# #             st.write(f"**From ID:** {tx['sender']}")
# #             st.write(f"**To ID:** {tx['receiver']}")
# #             st.markdown(f"## ₹ {tx['amount']}")
# #         if st.button("DONE"):
# #             st.session_state.payment_step = "input"
# #             st.session_state.qr_scanned_id = ""
# #             st.rerun()

# # with tab_pay:
# #     # 1. Verification Check: Ensure a sender has logged in via the HOME tab
# #     if "current_authenticated_user" not in st.session_state:
# #         st.warning("🔒 Verification Required: Please authenticate your face in the **HOME** tab first.")
# #         st.stop()

# #     sender_folder = st.session_state.current_authenticated_user
# #     u_info = get_user_data(sender_folder)
# #     sender_bio_id = u_info.get("unique_id", "Not Assigned")
    
# #     # --- STAGE 1: TRANSACTION INPUT ---
# #     if st.session_state.payment_step == "input":
# #         st.markdown(f"### 💸 Secure Payment Terminal")
        
# #         # Display IDs as Markdown options for clarity
# #         st.markdown(f"**Sender Bio-ID:** `{sender_bio_id}`")
        
# #         col_scan, col_manual = st.columns(2)
# #         with col_scan:
# #             st.markdown("#### 📷 Scan QR Code")
# #             if st.button("🚀 OPEN QR CAMERA", width="stretch"):
# #                 # Opens camera module to scan receiver's QR
# #                 scanned_id = scan_biopay_qr() 
# #                 if scanned_id:
# #                     st.session_state.qr_scanned_id = scanned_id
# #                     st.session_state.payment_step = "confirm"
# #                     st.rerun()

# #         with col_manual:
# #             st.markdown("#### ⌨️ Manual Entry")
# #             m_id = st.text_input("Enter Receiver Bio-ID", value=st.session_state.qr_scanned_id)
# #             if st.button("Proceed to Verify"):
# #                 if m_id:
# #                     st.session_state.qr_scanned_id = m_id
# #                     st.session_state.payment_step = "confirm"
# #                     st.rerun()

# #     # --- STAGE 2: IMAGE VERIFICATION & CONFIRMATION ---
# #     elif st.session_state.payment_step == "confirm":
# #         current_bal = u_info.get("balance", 0)
# #         st.markdown("### 🛡️ Secure Transaction Confirmation")
        
# #         # Displaying IDs in Markdown format
# #         st.markdown(f"**Sender:** `{sender_bio_id}`")
# #         st.markdown(f"**Receiver:** `{st.session_state.qr_scanned_id}`")
        
# #         with st.container(border=True):
# #             pay_col1, pay_col2 = st.columns(2)
# #             with pay_col1:
# #                 amount = st.number_input("Transaction Value (₹)", min_value=1, value=100)
# #             with pay_col2:
# #                 st.metric("Available Balance", f"₹{current_bal}")

# #         if amount > current_bal:
# #             st.error("🛑 Money limit exceeded.")
# #             can_pay = False
# #         else:
# #             can_pay = True

# #         if st.button("⚡ VERIFY IMAGE & SEND", disabled=not can_pay):
# #             status = st.empty()
# #             with status.container():
# #                 st.write("⏳ **Opening Camera for Face Verification...**")
# #                 # Sender must take an image (via camera) to verify identity
# #                 if authenticate(sender_folder):
# #                     st.write("✅ **Face Authenticated Successfully!**")
# #                     st.write("⏳ **Performing Liveness Check...**")
                    
# #                     if blink_verification():
# #                         # Execute the backend balance update
# #                         if update_transaction(sender_folder, amount, st.session_state.qr_scanned_id):
# #                             st.session_state.last_tx_details = {
# #                                 "sender": sender_bio_id,
# #                                 "receiver": st.session_state.qr_scanned_id,
# #                                 "amount": amount
# #                             }
# #                             st.session_state.payment_step = "success"
# #                             st.rerun()
# #                     else:
# #                         st.error("Liveness Failed.")
# #                 else:
# #                     st.error("Identity Mismatch.")

# #     # --- STAGE 3: SUCCESS & RECEIPT ---
# #     elif st.session_state.payment_step == "success":
# #         tx = st.session_state.last_tx_details
# #         st.markdown("""
# #             <div style="text-align:center; padding:30px;">
# #                 <div class="checkmark-circle"><div class="background"></div><div class="checkmark draw"></div></div>
# #                 <h1 style="color:#2ecc71;">Transaction Successful</h1>
# #             </div>""", unsafe_allow_html=True)
        
        
        
# #         with st.container(border=True):
# #             st.markdown(f"**From ID:** `{tx['sender']}`")
# #             st.markdown(f"**To ID:** `{tx['receiver']}`")
# #             st.markdown(f"## ₹ {tx['amount']}")
        
# #         if st.button("DONE"):
# #             st.session_state.payment_step = "input"
# #             st.session_state.qr_scanned_id = ""
# #             st.rerun()

# with tab_pay:
#     if "current_authenticated_user" not in st.session_state:
#         st.warning("🔒 Verification Required: Please authenticate your face in the **HOME** tab first.")
#         st.stop()

#     # Pass the specific folder name to authenticate() for targeted checking
#     sender_folder = st.session_state.current_authenticated_user
#     u_info = get_user_data(sender_folder)
#     sender_bio_id = u_info.get("unique_id", "Not Assigned")
    
#     if st.session_state.payment_step == "input":
#         st.markdown(f"### 💸 Secure Payment Terminal")
#         st.markdown(f"**Sender Bio-ID:** `{sender_bio_id}`")
#         # ... (Existing QR scan and Manual input code) ...

#     elif st.session_state.payment_step == "confirm":
#         current_bal = u_info.get("balance", 0)
#         st.markdown(f"**Sender:** `{sender_bio_id}`")
#         st.markdown(f"**Receiver:** `{st.session_state.qr_scanned_id}`")
        
#         # Validation and Verify Button
#         if st.button("⚡ VERIFY IMAGE & SEND"):
#             status = st.empty()
#             with status.container():
#                 st.write("⏳ **Opening Camera for Face Verification...**")
                
#                 # STRICT AUTHENTICATION: Pass sender_folder to ensure only their face works
#                 if authenticate(sender_folder):
#                     st.write("✅ **Face Authenticated Successfully!**")
#                     if blink_verification():
#                         if update_transaction(sender_folder, amount, st.session_state.qr_scanned_id):
#                             st.session_state.last_tx_details = {
#                                 "sender": sender_bio_id,
#                                 "receiver": st.session_state.qr_scanned_id,
#                                 "amount": amount
#                             }
#                             st.session_state.payment_step = "success"
#                             st.rerun()
#                 else:
#                     st.error(f"❌ Security Alert: Face does not match account holder ({sender_folder}).")

import streamlit as st
import os
import geocoder
import plotly.graph_objects as go
import pickle
from face_register import register_user, scan_biopay_qr
from model_utils import train_model
from face_auth import authenticate
from blink_auth import blink_verification
from user_utils import (
    get_all_users, get_user_data, update_profile_photo,
    update_failed_attempts, delete_user, rename_user, update_transaction
)

# ---------------- PAGE CONFIG & STYLING ----------------
st.set_page_config(page_title="BioPay | Secure Face Payments", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #ffffff; }
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(#00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem !important;
    }
    .stTabs [data-testid="stVerticalBlock"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(45deg, #3a7bd5, #00d2ff);
        color: white; font-weight: bold; width: 100%;
    }
    .checkmark-circle {
        width: 150px; height: 150px;
        position: relative; display: inline-block;
        margin: 0 auto; text-align: center;
    }
    .checkmark-circle .background { width: 150px; height: 150px; border-radius: 50%; background: #2ecc71; position: absolute; }
    .checkmark-circle .checkmark.draw:after {
        animation-delay: 100ms; animation-duration: 1s; animation-timing-function: ease;
        animation-name: checkmark; transform: scaleX(-1) rotate(135deg);
    }
    .checkmark-circle .checkmark:after {
        opacity: 1; height: 75px; width: 37.5px;
        transform-origin: left top; border-right: 15px solid white;
        border-top: 15px solid white; content: '';
        left: 37.5px; top: 75px; position: absolute;
    }
    @keyframes checkmark {
        0% { height: 0; width: 0; opacity: 1; }
        20% { height: 0; width: 37.5px; opacity: 1; }
        40% { height: 75px; width: 37.5px; opacity: 1; }
        100% { height: 75px; width: 37.5px; opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">BIOPAY SECURE SYSTEM</h1>', unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "qr_scanned_id" not in st.session_state: st.session_state.qr_scanned_id = ""
if "payment_step" not in st.session_state: st.session_state.payment_step = "input"
if "last_tx_details" not in st.session_state: st.session_state.last_tx_details = {}

tab_home, tab_reg, tab_list, tab_pay = st.tabs(["🏠 HOME", "👤 REGISTER", "📂 DIRECTORY", "💸 PAYMENT"])

# ==================================================
# TAB 0: HOME
# ==================================================
with tab_home:
    st.markdown("### 📱 Digital Wallet Dashboard")
    h_col1, h_col2, h_col3 = st.columns(3)
    with h_col1:
        if st.button("🔍 OPEN CAMERA SCANNER"):
            scanned = scan_biopay_qr()
            if scanned:
                st.session_state.qr_scanned_id = scanned
                st.success(f"ID Detected: {scanned}")
    with h_col2:
        m_id = st.text_input("Manual Bio-ID Entry", key="m_id_home")
        if st.button("Save ID"): st.session_state.qr_scanned_id = m_id
    with h_col3:
        users = get_all_users()
        if users:
            u_check = st.selectbox("Select Profile to Login", users)
            if st.button("🔓 SHOW BALANCE / LOGIN"):
                if authenticate(u_check):
                    st.session_state.current_authenticated_user = u_check
                    u_data = get_user_data(u_check)
                    st.metric("Balance", f"₹{u_data.get('balance', 0)}")
                    st.success(f"Identity Verified: {u_check}")
                else:
                    if "current_authenticated_user" in st.session_state:
                        del st.session_state.current_authenticated_user
                    st.error("❌ Face Mismatch! Access Denied.")

# ==================================================
# TAB 1: REGISTER
# ==================================================
# with tab_reg:
#     st.markdown("### ✨ Enrollment")
#     fn = st.text_input("Full Name")
#     em = st.text_input("Email")
#     bn = st.selectbox("Bank", ["SBI", "HDFC", "ICICI", "Axis"])
#     mb = st.text_input("Mobile")
#     nc = st.text_input("Native City")
#     if st.button("🚀 REGISTER"):
#         register_user(fn, em, mb, nc, bn, {})
#         train_model()
#         st.success("User Registered!")

with tab_reg:
    st.markdown("### ✨ Identity Enrollment")
    
    # Row 1: Primary Details
    col1, col2 = st.columns(2)
    with col1:
        fn = st.text_input("Full Name")
        em = st.text_input("Email")
        
        # Bank selectbox with placeholder
        bank_list = [
            "Choose your bank", "SBI", "HDFC", "ICICI", "Axis", 
            "Bank of Baroda", "PNB", "Canara Bank", 
            "Kotak Mahindra", "IndusInd Bank"
        ]
        bn = st.selectbox("Bank Name", options=bank_list, index=0)
        
    with col2:
        mb = st.text_input("Mobile", placeholder="10-digit number")
        nc = st.text_input("Native City")
        
        # Spacer to align checkbox
        st.write("<div style='height: 28px;'></div>", unsafe_allow_html=True) 
        agree = st.checkbox("I consent to Biometric Data Capture")

    st.markdown("---")
    
    # Row 2: Security Recovery Setup
    st.markdown("#### 🛡️ Security Recovery Setup")
    sq_col, sa_col = st.columns([2, 1])
    
    with sq_col:
        sq = st.selectbox("Select a Security Question", [
            "What was the name of your first school?",
            "What is your mother's maiden name?",
            "What was your first pet's name?",
            "In which city were you born?"
        ])
    with sa_col:
        sa = st.text_input("Secret Answer", type="password", help="Used for account recovery")

    # Data Validation Logic
    can_reg = False
    validation_box = st.empty()

    if fn and em and mb and sa and agree:
        # Check if user details already exist
        from user_utils import check_user_exists
        exists, msg = check_user_exists(em, fn, mb)
        
        if exists:
            validation_box.error(f"🛑 {msg}")
        elif bn == "Choose your bank":
            validation_box.warning("⚠️ Please select your bank to continue.")
        elif len(mb) != 10:
            validation_box.warning("⚠️ Please enter a valid 10-digit mobile number.")
        else:
            validation_box.success("✅ Form validated. Ready for capture.")
            can_reg = True

    # Action Button
    st.write("")
    if st.button("🚀 INITIALIZE BIOMETRIC CAPTURE", width="stretch", disabled=not can_reg):
        with st.status("Initializing Biometric Module...", expanded=True) as status:
            # 1. Capture 30 face and 20 eye images
            register_user(fn, em, mb, nc, bn, {sq: sa})
            
            # 2. Train the recognizer
            status.write("Training AI model with new samples...")
            train_model() 
            
            status.update(label="Enrollment Complete!", state="complete", expanded=False)
        
        # Display results
        new_uid = f"{fn.split()[0].lower()}.{mb[-4:]}@{bn.lower()}"
        st.success(f"Registration Successful! Your Bio-ID is: `{new_uid}`")


# ==================================================
# TAB 2: DIRECTORY
# ==================================================
with tab_list:
    st.markdown("### 📂 Registered Biometric Profiles")
    users = get_all_users()
    if not users:
        st.info("No active profiles found.")
    else:
        for u in users:
            with st.expander(f"User Profile: {u}"):
                u_info = get_user_data(u)
                st.write(f"**Bio-ID:** `{u_info.get('unique_id')}`")
                if os.path.exists(f"dataset/{u}/qr_code.png"):
                    st.image(f"dataset/{u}/qr_code.png", width=150)
                if st.button("🗑️ Delete Profile", key=f"del_{u}"):
                    delete_user(u); st.rerun()

# ==================================================
# TAB 3: PAYMENT
# ==================================================
# with tab_pay:
#     if "current_authenticated_user" not in st.session_state:
#         st.warning("🔒 Verification Required: Please authenticate your face in the **HOME** tab first.")
#         st.stop()

#     sender_folder = st.session_state.current_authenticated_user
#     u_info = get_user_data(sender_folder)
#     sender_bio_id = u_info.get("unique_id", "Not Assigned")
    
#     if st.session_state.payment_step == "input":
#         st.markdown(f"### 💸 Secure Payment Terminal")
#         st.markdown(f"**Sender Bio-ID:** `{sender_bio_id}`")
        
#         col_scan, col_manual = st.columns(2)
#         with col_scan:
#             if st.button("🚀 OPEN QR CAMERA"):
#                 rid = scan_biopay_qr()
#                 if rid:
#                     st.session_state.qr_scanned_id = rid
#                     st.session_state.payment_step = "confirm"; st.rerun()

#         with col_manual:
#             rid_input = st.text_input("Receiver Bio-ID", value=st.session_state.qr_scanned_id)
#             if st.button("Proceed to Verify"):
#                 if rid_input:
#                     st.session_state.qr_scanned_id = rid_input
#                     st.session_state.payment_step = "confirm"; st.rerun()

#     elif st.session_state.payment_step == "confirm":
#         st.markdown("### 🛡️ Confirm Transaction")
#         current_bal = u_info.get("balance", 0)
        
#         st.markdown(f"**Sender ID:** `{sender_bio_id}`")
#         st.markdown(f"**Receiver ID:** `{st.session_state.qr_scanned_id}`")
        
#         with st.container(border=True):
#             c1, c2 = st.columns(2)
#             with c1:
#                 # amount defined here so it is available to the verification block
#                 amount = st.number_input("Amount (₹)", min_value=1, value=100)
#             with c2:
#                 st.metric("Available Balance", f"₹{current_bal}")
        
#         if st.button("⚡ VERIFY IMAGE & SEND", disabled=(amount > current_bal)):
#             status = st.empty()
#             with status.container():
#                 st.write("⏳ Step 1: Targeted Face Authentication...")
#                 # Targeted check: Rahul only matches Rahul
#                 if authenticate(sender_folder):
#                     st.write("✅ Identity Confirmed!")
#                     st.write("⏳ Step 2: Liveness Verification...")
#                     if blink_verification():
#                         if update_transaction(sender_folder, amount, st.session_state.qr_scanned_id):
#                             st.session_state.last_tx_details = {
#                                 "sender": sender_bio_id,
#                                 "receiver": st.session_state.qr_scanned_id,
#                                 "amount": amount
#                             }
#                             st.session_state.payment_step = "success"; st.rerun()
#                     else: st.error("❌ Liveness Failed")
#                 else: st.error(f"❌ Security Alert: Face does not match account ({sender_folder})")

#     elif st.session_state.payment_step == "success":
#         tx = st.session_state.last_tx_details
#         st.markdown("""
#             <div style="text-align:center; padding:30px;">
#                 <div class="checkmark-circle"><div class="background"></div><div class="checkmark draw"></div></div>
#                 <h1 style="color:#2ecc71;">Transaction Successful</h1>
#             </div>""", unsafe_allow_html=True)
        
#         with st.container(border=True):
#             st.markdown(f"**From Sender ID:** `{tx['sender']}`")
#             st.markdown(f"**To Receiver ID:** `{tx['receiver']}`")
#             st.markdown(f"## ₹ {tx['amount']}")
        
#         if st.button("DONE"):
#             st.session_state.payment_step = "input"; st.session_state.qr_scanned_id = ""; st.rerun()

with tab_pay:
    # 1. AUTHENTICATION CHECK
    # Ensure the sender has verified their face in the HOME tab before proceeding
    if "current_authenticated_user" not in st.session_state:
        st.warning("🔒 Verification Required: Please authenticate your face in the **HOME** tab first.")
        st.stop()

    sender_folder = st.session_state.current_authenticated_user
    u_info = get_user_data(sender_folder)
    sender_bio_id = u_info.get("unique_id", "Not Assigned")
    
    # ---------------- STAGE 1: INPUT ----------------
    if st.session_state.payment_step == "input":
        st.markdown(f"### 💸 Secure Payment Terminal")
        st.markdown(f"**Sender Bio-ID:** `{sender_bio_id}`")
        
        col_scan, col_manual = st.columns(2)
        with col_scan:
            if st.button("🚀 OPEN QR CAMERA"):
                # Scans receiver's QR code and moves to confirmation
                rid = scan_biopay_qr()
                if rid:
                    st.session_state.qr_scanned_id = rid
                    st.session_state.payment_step = "confirm"
                    st.rerun()

        with col_manual:
            rid_input = st.text_input("Receiver Bio-ID", value=st.session_state.qr_scanned_id)
            if st.button("Proceed to Verify"):
                if rid_input:
                    st.session_state.qr_scanned_id = rid_input
                    st.session_state.payment_step = "confirm"
                    st.rerun()

    # ---------------- STAGE 2: CONFIRMATION & AUTH ----------------
    elif st.session_state.payment_step == "confirm":
        st.markdown("### 🛡️ Confirm Transaction")
        current_bal = u_info.get("balance", 0)
        
        st.markdown(f"**Sender ID:** `{sender_bio_id}`")
        st.markdown(f"**Receiver ID:** `{st.session_state.qr_scanned_id}`")
        
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                amount = st.number_input("Amount (₹)", min_value=1, value=100)
            with c2:
                st.metric("Available Balance", f"₹{current_bal}")
        
        # Enable payment only if balance is sufficient
        if st.button("⚡ VERIFY IMAGE & SEND", disabled=(amount > current_bal)):
            status = st.empty()
            with status.container():
                st.write("⏳ Step 1: Targeted Face Authentication...")
                
                # Targeted check ensures ONLY the logged-in user can authorize
                if authenticate(sender_folder):
                    st.write("✅ Identity Confirmed!")
                    st.write("⏳ Step 2: Liveness Verification...")
                    
                    # Blink detection prevents photo-based spoofing
                    if blink_verification():
                        # Executes dual-user balance update and sends SMTP mail alerts
                        if update_transaction(sender_folder, amount, st.session_state.qr_scanned_id):
                            st.session_state.last_tx_details = {
                                "sender": sender_bio_id,
                                "receiver": st.session_state.qr_scanned_id,
                                "amount": amount
                            }
                            st.session_state.payment_step = "success"
                            st.rerun()
                        else:
                            st.error("❌ Transaction failed (Invalid Receiver or Balance error)")
                    else: 
                        st.error("❌ Liveness Failed (Blink not detected)")
                else: 
                    st.error(f"❌ Security Alert: Face does not match account ({sender_folder})")

    # ---------------- STAGE 3: SUCCESS ----------------
    elif st.session_state.payment_step == "success":
        tx = st.session_state.last_tx_details
        
        # GPay-style success tick animation
        st.markdown("""
            <div style="text-align:center; padding:30px;">
                <div class="checkmark-circle"><div class="background"></div><div class="checkmark draw"></div></div>
                <h1 style="color:#2ecc71;">Transaction Successful</h1>
            </div>""", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown(f"**From Sender ID:** `{tx['sender']}`")
            st.markdown(f"**To Receiver ID:** `{tx['receiver']}`")
            st.markdown(f"<h2 style='color:#2ecc71;'>₹ {tx['amount']}</h2>", unsafe_allow_html=True)
            st.info("📧 Debit/Credit notifications have been sent to registered emails.")

        if st.button("DONE"):
            st.session_state.payment_step = "input"
            st.session_state.qr_scanned_id = ""
            st.rerun()