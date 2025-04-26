import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import hashlib
import os
import base64
import re
import smtplib
import ssl
import secrets
import datetime
from pymongo import MongoClient
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# db connection
MONGO_URI = "mongodb+srv://jdeloughery:xpblAePTm7rInt1q@useraccountsdd.28j3v.mongodb.net/?retryWrites=true&w=majority&appName=UserAccountsDD"
client = MongoClient(MONGO_URI)
db = client["DiamondDealers"]
users_collection = db["users"]

# pw recovery email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "diamonddealerpr@gmail.com"
SENDER_PASSWORD = "fdbw myda kdsn kmtl"

# utility
def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return salt, key

def verify_password(stored_salt, stored_key, provided_password):
    _, key = hash_password(provided_password, stored_salt)
    return key == stored_key

def password_strength(password):
    if len(password) < 6:
        return "Weak", "red"
    elif re.search(r"[A-Z]", password) and re.search(r"\d", password) and len(password) >= 8:
        return "Strong", "green"
    else:
        return "Medium", "orange"

def is_valid_email(email):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.fullmatch(pattern, email) is not None

def is_valid_phone(phone):
    digits_only = re.sub(r"[^\d]", "", phone)
    return 7 <= len(digits_only) <= 15

def deposit_option_changed(*args):
    if deposit_amount_var.get() == "Other":
        deposit_other_entry.grid(row=9, column=1, padx=5, pady=5, sticky="w")
    else:
        deposit_other_entry.grid_forget()

def update_strength_label(event):
    password = password_entry_create.get().strip()
    strength, color = password_strength(password)
    strength_label.config(text=f"Strength: {strength}", fg=color)

def toggle_password(entry, toggle_button):
    """Toggles password visibility between hidden and shown."""
    if entry.cget("show") == "*":
        entry.config(show="")
        toggle_button.config(text="Hide")
    else:
        entry.config(show="*")
        toggle_button.config(text="Show")

# account creation/ sign in
def user_exists(username):
    return users_collection.find_one({"username": username}) is not None

def create_account():
    username = username_entry_create.get().strip()
    email = email_entry_create.get().strip()
    phone = phone_entry_create.get().strip()
    phone_clean = re.sub(r"[^\d]", "", phone)
    password = password_entry_create.get().strip()
    is_18 = age_verified.get()
    payment_method = payment_method_var.get()
    deposit_option = deposit_amount_var.get()
    deposit_amount = None

    if deposit_option == "Other":
        deposit_str = deposit_other_entry.get().strip()
        if not deposit_str.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric deposit amount for 'Other'.")
            return
        deposit_amount = int(deposit_str)
    else:
        deposit_amount = int(deposit_option.replace("$", ""))

    if not username or not email or not phone or not password or not payment_method:
        messagebox.showerror("Error", "Please complete all fields.")
        return

    if not is_valid_email(email):
        messagebox.showerror("Error", "Please enter a valid email address.")
        return

    if not is_valid_phone(phone):
        messagebox.showerror("Error", "Please enter a valid phone number (7-15 digits).")
        return

    if not is_18:
        messagebox.showerror("Error", "You must verify that you are at least 18 years old to create an account.")
        return

    if user_exists(username):
        messagebox.showerror("Error", "Username already exists!")
        return

    if password_strength(password)[0] == "Weak":
        messagebox.showerror("Error", "Password too weak! Use at least 8 characters, including uppercase letters and numbers.")
        return

    if len(password) > 64:
        messagebox.showerror("Error", "Password too long! Maximum is 64 characters.")
        return

    salt, key = hash_password(password)
    salt_str = base64.b64encode(salt).decode("utf-8")
    key_str = base64.b64encode(key).decode("utf-8")

    users_collection.insert_one({
        "username": username,
        "email": email,
        "phone": phone_clean,
        "payment_method": payment_method,
        "deposit_amount": deposit_amount,
        "salt": salt_str,
        "key": key_str,
        "failed_login_attempts": 0
    })

    messagebox.showinfo("Success", "Account created successfully!")

def login():
    username = username_entry_login.get().strip()
    password = password_entry_login.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Please enter a username and password.")
        return

    user = users_collection.find_one({"username": username})

    if user:
        if user.get("failed_login_attempts", 0) >= 20:
            messagebox.showerror("Error", "Account locked due to too many failed login attempts!")
            return

        stored_salt = base64.b64decode(user["salt"])
        stored_key = base64.b64decode(user["key"])
        if verify_password(stored_salt, stored_key, password):
            users_collection.update_one({"username": username}, {"$set": {"failed_login_attempts": 0}})
            messagebox.showinfo("Success", "Logged in successfully!")
            return

    users_collection.update_one({"username": username}, {"$inc": {"failed_login_attempts": 1}})
    messagebox.showerror("Error", "Invalid username or password.")

# pw recovery
def forgot_password():
    def send_reset_token():
        email = email_entry.get().strip()
        if not email:
            messagebox.showerror("Error", "Please enter your registered email address.")
            return

        user = users_collection.find_one({"email": email})
        if user:
            token = secrets.token_urlsafe(16)
            expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            users_collection.update_one({"email": email}, {"$set": {"reset_token": token, "token_expiration": expiration}})

            try:
                message = MIMEMultipart("alternative")
                message["Subject"] = "Password Reset Code - Diamond Dealers"
                message["From"] = SENDER_EMAIL
                message["To"] = email

                text = f"Hello,\n\nYour password reset code is: {token}\n\nIt will expire in 1 hour."
                html = f"""
                <html>
                  <body>
                    <p>Hello,<br><br>
                       Your password reset code is: <b>{token}</b><br><br>
                       It will expire in 1 hour.
                    </p>
                  </body>
                </html>
                """

                part1 = MIMEText(text, "plain")
                part2 = MIMEText(html, "html")
                message.attach(part1)
                message.attach(part2)

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
                    server.login(SENDER_EMAIL, SENDER_PASSWORD)
                    server.sendmail(SENDER_EMAIL, email, message.as_string())

                messagebox.showinfo("Success", "A reset code has been sent to your email!")
                recovery_window.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to send email: {e}")
        else:
            messagebox.showerror("Error", "Email not found!")

    recovery_window = tk.Toplevel(root)
    recovery_window.title("Forgot Password")
    recovery_window.configure(bg="#003300")

    tk.Label(recovery_window, text="Enter your registered email:", font=label_font, fg="gold", bg="#003300").pack(pady=10)
    email_entry = tk.Entry(recovery_window, width=30)
    email_entry.pack(pady=5)

    submit_button = tk.Button(recovery_window, text="Send Reset Code", font=button_font, bg="darkred", fg="gold", command=send_reset_token)
    submit_button.pack(pady=10)

def reset_password():
    def perform_reset():
        email = email_entry.get().strip()
        token = token_entry.get().strip()
        new_password = new_password_entry.get().strip()

        user = users_collection.find_one({"email": email, "reset_token": token})
        if user and datetime.datetime.utcnow() < user.get("token_expiration", datetime.datetime.min):
            if password_strength(new_password)[0] == "Weak" or len(new_password) > 64:
                messagebox.showerror("Error", "Invalid new password!")
                return

            salt, key = hash_password(new_password)
            salt_str = base64.b64encode(salt).decode("utf-8")
            key_str = base64.b64encode(key).decode("utf-8")

            users_collection.update_one({"email": email}, {"$set": {"salt": salt_str, "key": key_str}, "$unset": {"reset_token": "", "token_expiration": ""}})
            messagebox.showinfo("Success", "Password reset successfully!")
            reset_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid or expired token!")

    reset_window = tk.Toplevel(root)
    reset_window.title("Reset Password")
    reset_window.configure(bg="#003300")

    tk.Label(reset_window, text="Email:", font=label_font, fg="gold", bg="#003300").pack(pady=5)
    email_entry = tk.Entry(reset_window, width=30)
    email_entry.pack(pady=5)

    tk.Label(reset_window, text="Reset Code:", font=label_font, fg="gold", bg="#003300").pack(pady=5)
    token_entry = tk.Entry(reset_window, width=30)
    token_entry.pack(pady=5)

    tk.Label(reset_window, text="New Password:", font=label_font, fg="gold", bg="#003300").pack(pady=5)
    new_password_entry = tk.Entry(reset_window, width=30, show="*")
    new_password_entry.pack(pady=5)

    submit_button = tk.Button(reset_window, text="Reset Password", font=button_font, bg="darkred", fg="gold", command=perform_reset)
    submit_button.pack(pady=10)

# gui
root = tk.Tk()
root.title("Diamond Dealers Sign Up and Login")
root.configure(bg="#003300")

heading_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
label_font = tkFont.Font(family="Helvetica", size=12)
button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

heading_label = tk.Label(root, text="Diamond Dealers Sign Up and Login", font=heading_font, fg="gold", bg="#003300")
heading_label.pack(pady=10)

create_frame = tk.Frame(root, bg="#003300")
create_frame.pack(pady=20)

# username
tk.Label(create_frame, text="Username:", font=label_font, fg="gold", bg="#003300").grid(row=0, column=0, padx=5, sticky="e")
username_entry_create = tk.Entry(create_frame)
username_entry_create.grid(row=0, column=1, padx=5)

# email
tk.Label(create_frame, text="Email:", font=label_font, fg="gold", bg="#003300").grid(row=1, column=0, padx=5, sticky="e")
email_entry_create = tk.Entry(create_frame)
email_entry_create.grid(row=1, column=1, padx=5)

# phone
tk.Label(create_frame, text="Phone Number:", font=label_font, fg="gold", bg="#003300").grid(row=2, column=0, padx=5, sticky="e")
phone_entry_create = tk.Entry(create_frame)
phone_entry_create.grid(row=2, column=1, padx=5)

# $payment$
tk.Label(create_frame, text="Payment Method:", font=label_font, fg="gold", bg="#003300").grid(row=3, column=0, padx=5, sticky="e")
payment_method_var = tk.StringVar(value="CashApp")
payment_methods = ["CashApp", "PayPal", "Credit Card", "eCheck"]
payment_menu = tk.OptionMenu(create_frame, payment_method_var, *payment_methods)
payment_menu.config(font=label_font, bg="#710F20", fg="gold", highlightthickness=0)
payment_menu["menu"].config(font=label_font, bg="#710F20", fg="gold")
payment_menu.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# pw
tk.Label(create_frame, text="Password:", font=label_font, fg="gold", bg="#003300").grid(row=4, column=0, padx=5, sticky="e")
password_entry_create = tk.Entry(create_frame, show="*")
password_entry_create.grid(row=4, column=1, padx=5)

# show pw
password_toggle_btn = tk.Button(create_frame, text="Show", font=button_font, bg="#710F20", fg="gold", command=lambda: toggle_password(password_entry_create, password_toggle_btn))
password_toggle_btn.grid(row=4, column=2, padx=5)

# pw strength
strength_label = tk.Label(create_frame, text="Strength: ", font=label_font, fg="gold", bg="#003300")
strength_label.grid(row=5, column=1)
password_entry_create.bind("<KeyRelease>", update_strength_label)

# age
age_verified = tk.BooleanVar()
tk.Checkbutton(create_frame, text="I confirm that I am 18 years or older", font=label_font, fg="gold", bg="#003300", variable=age_verified, selectcolor="#003300").grid(row=6, column=1, pady=5)

# $deposit$
tk.Label(create_frame, text="Deposit Amount:", font=label_font, fg="gold", bg="#003300").grid(row=7, column=0, padx=5, sticky="e")
deposit_amount_var = tk.StringVar(value="$50")
deposit_options = ["$50", "$100", "$200", "Other"]
deposit_menu = tk.OptionMenu(create_frame, deposit_amount_var, *deposit_options)
deposit_menu.config(font=label_font, bg="#710F20", fg="gold", highlightthickness=0)
deposit_menu["menu"].config(font=label_font, bg="#710F20", fg="gold")
deposit_menu.grid(row=7, column=1, padx=5, pady=5, sticky="w")

deposit_other_entry = tk.Entry(create_frame, width=10, font=label_font)
deposit_amount_var.trace("w", deposit_option_changed)

# create
create_button = tk.Button(create_frame, text="Create Account", font=button_font, bg="#710F20", fg="gold", command=create_account)
create_button.grid(row=10, column=1, pady=10)

# frame
login_frame = tk.Frame(root, bg="#003300")
login_frame.pack(pady=20)

# login username
tk.Label(login_frame, text="Username:", font=label_font, fg="gold", bg="#003300").grid(row=0, column=0, padx=5, sticky="e")
username_entry_login = tk.Entry(login_frame)
username_entry_login.grid(row=0, column=1, padx=5)

# login pw
tk.Label(login_frame, text="Password:", font=label_font, fg="gold", bg="#003300").grid(row=1, column=0, padx=5, sticky="e")
password_entry_login = tk.Entry(login_frame, show="*")
password_entry_login.grid(row=1, column=1, padx=5)

# show login pw
login_toggle_btn = tk.Button(login_frame, text="Show", font=button_font, bg="#710F20", fg="gold", command=lambda: toggle_password(password_entry_login, login_toggle_btn))
login_toggle_btn.grid(row=1, column=2, padx=5)

# login button
login_button = tk.Button(login_frame, text="Login", font=button_font, bg="#710F20", fg="gold", command=login)
login_button.grid(row=2, column=1, pady=10)

# forgot pw button
forgot_password_button = tk.Button(login_frame, text="Forgot Password?", font=button_font, bg="#710F20", fg="gold", command=forgot_password)
forgot_password_button.grid(row=3, column=1, pady=5)

# reset pw button
reset_password_button = tk.Button(login_frame, text="Reset Password", font=button_font, bg="#710F20", fg="gold", command=reset_password)
reset_password_button.grid(row=4, column=1, pady=5)

root.mainloop()


root.mainloop()
