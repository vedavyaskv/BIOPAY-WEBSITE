import os
import shutil
import cv2
import numpy as np
import json

# -------------------------------------------------
# CHECK IF USER DATA ALREADY EXISTS
# -------------------------------------------------
def check_user_exists(email, full_name, mobile):
    """
    Scans all registered users to check if the new credentials 
    already exist in the system.
    """
    base_path = "dataset"
    if not os.path.exists(base_path):
        return False, ""

    # Iterate through every folder in the dataset
    for user_folder in os.listdir(base_path):
        json_path = f"{base_path}/{user_folder}/user.json"
        
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                try:
                    data = json.load(f)
                    # Check for matches against unique enrollment criteria
                    if data.get("email") == email:
                        return True, "Email ID already registered"
                    if data.get("full_name") == full_name:
                        return True, "Full Name already exists"
                    if data.get("mobile") == mobile:
                        return True, "Mobile Number already exists"
                except json.JSONDecodeError:
                    continue
                    
    return False, ""

# -------------------------------------------------
# GET ALL REGISTERED USERS
# -------------------------------------------------
def get_all_users():
    """Returns a list of folder names (sanitized emails) from the dataset."""
    if not os.path.exists("dataset"):
        return []
    return [
        u for u in os.listdir("dataset")
        if os.path.isdir(f"dataset/{u}")
    ]


# -------------------------------------------------
# READ USER METADATA
# -------------------------------------------------
def get_user_data(username):
    """Fetches full JSON metadata for a specific user folder."""
    user_file = f"dataset/{username}/user.json"
    if not os.path.exists(user_file):
        return None

    with open(user_file, "r") as f:
        return json.load(f)


# -------------------------------------------------
# UPDATE FAILED ATTEMPTS
# -------------------------------------------------
def update_failed_attempts(username, success):
    """Resets or increments failed login attempts in user metadata."""
    user_file = f"dataset/{username}/user.json"
    if not os.path.exists(user_file):
        return

    with open(user_file, "r") as f:
        data = json.load(f)

    if success:
        data["failed_attempts"] = 0
    else:
        # Initialize key if it doesn't exist to prevent crashes
        data["failed_attempts"] = data.get("failed_attempts", 0) + 1

    with open(user_file, "w") as f:
        json.dump(data, f, indent=4)


# -------------------------------------------------
# UPDATE WALLET BALANCE & TRANSACTIONS
# -------------------------------------------------
# def update_transaction(username, amount, receiver_id):
#     """Updates the user's balance and records the transaction history."""
#     user_file = f"dataset/{username}/user.json"
#     if not os.path.exists(user_file):
#         return False

#     with open(user_file, "r") as f:
#         data = json.load(f)

#     # Deduct amount from balance
#     current_balance = data.get("balance", 0)
#     if current_balance >= amount:
#         data["balance"] = current_balance - amount
        
#         # Log transaction
#         transaction_entry = {
#             "to": receiver_id,
#             "amount": amount,
#             "timestamp": os.popen('date').read().strip() # Simplified timestamp
#         }
        
#         if "transactions" not in data:
#             data["transactions"] = []
#         data["transactions"].append(transaction_entry)

#         with open(user_file, "w") as f:
#             json.dump(data, f, indent=4)
#         return True
    
#     return False

# import os, shutil, cv2, numpy as np, json

# def get_all_users():
#     if not os.path.exists("dataset"): return []
#     return [u for u in os.listdir("dataset") if os.path.isdir(f"dataset/{u}")]

# def get_user_data(username):
#     path = f"dataset/{username}/user.json"
#     if not os.path.exists(path): return None
#     with open(path, "r") as f: return json.load(f)

# def update_transaction(username, amount, receiver_id):
#     path = f"dataset/{username}/user.json"
#     data = get_user_data(username)
#     if not data: return False
    
#     curr_bal = float(data.get("balance", 0))
#     if curr_bal >= amount:
#         data["balance"] = curr_bal - amount
#         if "transactions" not in data: data["transactions"] = []
#         data["transactions"].append({"to": receiver_id, "amount": amount})
#         with open(path, "w") as f: json.dump(data, f, indent=4)
#         return True
#     return False

# def check_user_exists(email, name, mobile):
#     for u in get_all_users():
#         d = get_user_data(u)
#         if d['email'] == email or d['mobile'] == mobile: return True, "User Exists"
#     return False, ""

# def delete_user(u):
#     if os.path.exists(f"dataset/{u}"): shutil.rmtree(f"dataset/{u}")
# # -------------------------------------------------
# # UPDATE PROFILE PHOTO
# # -------------------------------------------------
# def update_profile_photo(username, uploaded_file):
#     path = f"dataset/{username}/profile.jpg"

#     file_bytes = np.asarray(
#         bytearray(uploaded_file.read()),
#         dtype=np.uint8
#     )

#     img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
#     if img is not None:
#         cv2.imwrite(path, img)


# # -------------------------------------------------
# # DELETE USER COMPLETELY
# # -------------------------------------------------
# def delete_user(username):
#     """Removes all files, photos, and QR codes associated with the user."""
#     path = f"dataset/{username}"
#     if os.path.exists(path):
#         shutil.rmtree(path)


# # -------------------------------------------------
# # RENAME USER (FOLDER LEVEL)
# # -------------------------------------------------
# def rename_user(old_name, new_name):
#     old_path = f"dataset/{old_name}"
#     new_path = f"dataset/{new_name}"

#     if not os.path.exists(old_path) or os.path.exists(new_path):
#         return False

#     os.rename(old_path, new_path)
#     return True

import os
import shutil
import cv2
import numpy as np
import json
from otp_utils import send_transaction_mail  # Ensure this function is in otp_utils.py

def get_all_users():
    if not os.path.exists("dataset"): return []
    return [u for u in os.listdir("dataset") if os.path.isdir(f"dataset/{u}")]

def get_user_data(username):
    path = f"dataset/{username}/user.json"
    if not os.path.exists(path): return None
    with open(path, "r") as f: return json.load(f)

# -------------------------------------------------
# DUAL-USER TRANSACTION LOGIC
# -------------------------------------------------
def update_transaction(username, amount, receiver_id):
    """
    Subtracts money from sender, adds to receiver, and sends dual emails.
    """
    sender_path = f"dataset/{username}/user.json"
    sender_data = get_user_data(username)
    if not sender_data: return False

    # 1. Check Sender Balance
    curr_sender_bal = float(sender_data.get("balance", 0))
    if curr_sender_bal < amount:
        return False

    # 2. Find Receiver Folder in Dataset
    receiver_folder = None
    receiver_data = None
    for u in get_all_users():
        temp_data = get_user_data(u)
        if temp_data and temp_data.get("unique_id") == receiver_id:
            receiver_folder = u
            receiver_data = temp_data
            break
    
    if not receiver_data:
        print("Receiver ID not found in system.")
        return False

    # 3. Update Sender Balance
    sender_data["balance"] = curr_sender_bal - amount
    if "transactions" not in sender_data: sender_data["transactions"] = []
    sender_data["transactions"].append({
        "type": "Debit",
        "to": receiver_id, 
        "amount": amount,
        "status": "Success"
    })

    # 4. Update Receiver Balance
    curr_receiver_bal = float(receiver_data.get("balance", 0))
    receiver_data["balance"] = curr_receiver_bal + amount
    if "transactions" not in receiver_data: receiver_data["transactions"] = []
    receiver_data["transactions"].append({
        "type": "Credit",
        "from": sender_data.get("unique_id"), 
        "amount": amount,
        "status": "Success"
    })

    # 5. Save Both JSON Files
    with open(sender_path, "w") as f: 
        json.dump(sender_data, f, indent=4)
    with open(f"dataset/{receiver_folder}/user.json", "w") as f: 
        json.dump(receiver_data, f, indent=4)

    # 6. Send Dual Email Notifications
    # To Sender
    send_transaction_mail(
        sender_data['email'], 
        "Debit Alert: BioPay Transaction", 
        f"Hello {sender_data['full_name']},\n\n₹{amount} has been deducted from your account for payment to {receiver_id}.\nUpdated Balance: ₹{sender_data['balance']}"
    )
    # To Receiver
    send_transaction_mail(
        receiver_data['email'], 
        "Credit Alert: BioPay Transaction", 
        f"Hello {receiver_data['full_name']},\n\n₹{amount} has been credited to your account from {sender_data.get('unique_id')}.\nUpdated Balance: ₹{receiver_data['balance']}"
    )

    return True

def check_user_exists(email, name, mobile):
    for u in get_all_users():
        d = get_user_data(u)
        if d:
            if d.get('email') == email or d.get('mobile') == mobile: 
                return True, "User with this Email or Mobile already exists."
    return False, ""

def update_profile_photo(username, uploaded_file):
    path = f"dataset/{username}/profile.jpg"
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is not None:
        cv2.imwrite(path, img)

def delete_user(username):
    """Removes all files, photos, and QR codes associated with the user."""
    path = f"dataset/{username}"
    if os.path.exists(path):
        shutil.rmtree(path)

def rename_user(old_name, new_name):
    old_path = f"dataset/{old_name}"
    new_path = f"dataset/{new_name}"
    if not os.path.exists(old_path) or os.path.exists(new_path):
        return False
    os.rename(old_path, new_path)
    return True