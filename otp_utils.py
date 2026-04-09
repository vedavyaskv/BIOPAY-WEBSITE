# import smtplib
# import random

# def send_otp(receiver_email):
#     otp = random.randint(100000, 999999)

#     sender_email = "your_email@gmail.com"
#     sender_password = "your_app_password"  # Gmail App Password

#     message = f"Your OTP for payment verification is: {otp}"

#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(sender_email, sender_password)
#     server.sendmail(sender_email, receiver_email, message)
#     server.quit()

#     return otp


import smtplib
from email.message import EmailMessage

def send_transaction_mail(to_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = "vedavyaskodandapani@gmail.com" 

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("vedavyaskodandapani@gmail.com", "kxva dlgt ebts oxnx") 
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Mail Error: {e}")
        return False