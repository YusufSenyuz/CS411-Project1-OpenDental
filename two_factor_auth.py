import smtplib
import random
import time
from tkinter import *
from tkinter import messagebox
from email.mime.text import MIMEText
import threading
from dashboard import open_dashboard

verification_code = ""
countdown_time = 10

def send_2fa_code(user_email):
    global verification_code
    verification_code = str(random.randint(1000, 9999))

    msg = MIMEText(f"Your 2FA verification code is: {verification_code}")
    msg['Subject'] = 'Open Dental 2FA Verification'
    msg['From'] = 'eylulbadem36@gmail.com'
    msg['To'] = user_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('eylulbadem36@gmail.com', 'lwlu togf bdrk vvzs')
            server.sendmail('eylulbadem36@gmail.com', user_email, msg.as_string())
            messagebox.showinfo("2FA Code", "A 2FA code has been sent to your email.")
    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send 2FA code. {str(e)}")

def check_2fa_code(username):
    entered_code = code_entry.get()

    if entered_code == verification_code:
        messagebox.showinfo("Login Success", "2FA verification successful!")
        twofa_window.destroy()
        open_dashboard(username)
    else:
        messagebox.showerror("Error", "Invalid 2FA code.")

def enable_resend_button():
    global countdown_time
    while countdown_time > 0:
        resend_button.config(text=f"Resend Code ({countdown_time}s)")
        time.sleep(1)
        countdown_time -= 1
    resend_button.config(state=NORMAL, text="Resend Code")

def open_2fa_page(username, email):
    global twofa_window, code_entry, resend_button

    twofa_window = Tk()
    twofa_window.title("2FA Verification")
    twofa_window.geometry("400x270")
    twofa_window.configure(bg="#f0f0f0")
    twofa_window.resizable(False, False)

    Label(twofa_window, text=f"Enter 2FA Code for {username}", font=("Arial", 16), bg="#f0f0f0").pack(pady=20)

    code_entry = Entry(twofa_window, width=20, bg="white", fg="black", font=("Arial", 12))
    code_entry.pack(pady=10)

    Button(twofa_window, text="Verify and Login", command=lambda: check_2fa_code(username), width=20, bg="#4CAF50",
           fg="black", font=("Arial", 12)).pack(pady=10)

    resend_button = Button(twofa_window, text=f"Resend Code ({countdown_time}s)", command=lambda: send_2fa_code(email),
                           state=DISABLED, width=20, bg="#4CAF50", fg="black", font=("Arial", 12))
    resend_button.pack(pady=10)

    send_2fa_code(email)

    threading.Thread(target=enable_resend_button).start()

    twofa_window.mainloop()
