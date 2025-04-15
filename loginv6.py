import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import hashlib
import os
import base64
from pymongo import MongoClient
import re

# MongoDB Atlas Connection String 
MONGO_URI = "mongodb+srv://jdeloughery:xpblAePTm7rInt1q@useraccountsdd.28j3v.mongodb.net/?retryWrites=true&w=majority&appName=UserAccountsDD"
client = MongoClient(MONGO_URI)
db = client["DiamondDealers"]  # Database name
users_collection = db["users"]  # Collection name

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)  # Generate a random salt
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return salt, key

def verify_password(stored_salt, stored_key, provided_password):
    _, key = hash_password(provided_password, stored_salt)
    return key == stored_key

def password_strength(password):
    """Evaluates password strength based on length and character variety."""
    if len(password) < 6:
        return "Weak", "red"
    elif re.search(r"[A-Z]", password) and re.search(r"\d", password) and len(password) >= 8:
        return "Strong", "green"
    else:
        return "Medium", "orange"

def update_strength_label(event):
    """Updates the password strength label dynamically."""
    password = password_entry_create.get().strip()
    strength, color = password_strength(password)
    strength_label.config(text=f"Strength: {strength}", fg=color)

def toggle_password(entry, toggle_button):
    """Toggles password visibility."""
    if entry.cget("show") == "*":
        entry.config(show="")
        toggle_button.config(text="Hide")
    else:
        entry.config(show="*")
        toggle_button.config(text="Show")

def is_valid_email(email):
    """Basic regex to check if an email is in a valid format."""
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.fullmatch(pattern, email) is not None

def deposit_option_changed(*args):
    """Shows or hides the 'Other Amount' entry based on the selected deposit option."""
    if deposit_amount_var.get() == "Other":
        deposit_other_entry.grid(row=8, column=1, padx=5, pady=5, sticky="w")
    else:
        deposit_other_entry.grid_forget()

def create_account():
    username = username_entry_create.get().strip()
    email = email_entry_create.get().strip()
    password = password_entry_create.get().strip()
    is_18 = age_verified.get()
    payment_method = payment_method_var.get()
    deposit_option = deposit_amount_var.get()
    deposit_amount = None

    # Determine deposit amount
    if deposit_option == "Other":
        deposit_str = deposit_other_entry.get().strip()
        if not deposit_str.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric deposit amount for 'Other'.")
            return
        deposit_amount = int(deposit_str)
    else:
        # Remove the "$" and convert to integer
        deposit_amount = int(deposit_option.replace("$", ""))

    if not username or not email or not password or not payment_method:
        messagebox.showerror("Error", "Please enter a username, email, password, and select a payment method.")
        return

    if not is_valid_email(email):
        messagebox.showerror("Error", "Please enter a valid email address.")
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

    salt, key = hash_password(password)
    salt_str = base64.b64encode(salt).decode("utf-8")
    key_str = base64.b64encode(key).decode("utf-8")

    # Store username, email, payment method, deposit, salt, and hashed password
    users_collection.insert_one({
        "username": username,
        "email": email,
        "payment_method": payment_method,
        "deposit_amount": deposit_amount,
        "salt": salt_str,
        "key": key_str
    })

    messagebox.showinfo("Success", "Account created successfully!")

def user_exists(username):
    return users_collection.find_one({"username": username}) is not None

def login():
    username = username_entry_login.get().strip()
    password = password_entry_login.get().strip()

    if not username or not password:
        messagebox.showerror("Error", "Please enter a username and password.")
        return

    user = users_collection.find_one({"username": username})

    if user:
        stored_salt = base64.b64decode(user["salt"])
        stored_key = base64.b64decode(user["key"])
        if verify_password(stored_salt, stored_key, password):
            messagebox.showinfo("Success", "Logged in successfully!")
            return

    messagebox.showerror("Error", "Invalid username or password.")

# Tkinter GUI setup with a casino style and dark green background (#003300)
root = tk.Tk()
root.title("Diamond Dealers Sign Up and Login")
root.configure(bg="#003300")

# Define fonts for headings, labels, and buttons
heading_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
label_font = tkFont.Font(family="Helvetica", size=12)
button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

# Top heading label
heading_label = tk.Label(root, text="Diamond Dealers Sign Up and Login", font=heading_font, fg="gold", bg="#003300")
heading_label.pack(pady=10)

# Create Account Frame with dark green background
create_frame = tk.Frame(root, bg="#003300")
create_frame.pack(pady=20)

# Username Entry
tk.Label(create_frame, text="Username:", font=label_font, fg="gold", bg="#003300").grid(row=0, column=0, padx=5, sticky="e")
username_entry_create = tk.Entry(create_frame)
username_entry_create.grid(row=0, column=1, padx=5)

# Email Entry
tk.Label(create_frame, text="Email:", font=label_font, fg="gold", bg="#003300").grid(row=1, column=0, padx=5, sticky="e")
email_entry_create = tk.Entry(create_frame)
email_entry_create.grid(row=1, column=1, padx=5)

# Payment Method Dropdown
tk.Label(create_frame, text="Payment Method:", font=label_font, fg="gold", bg="#003300").grid(row=2, column=0, padx=5, sticky="e")
payment_method_var = tk.StringVar(value="CashApp")
payment_methods = ["CashApp", "PayPal", "Credit Card", "eCheck"]
payment_menu = tk.OptionMenu(create_frame, payment_method_var, *payment_methods)
payment_menu.config(font=label_font, bg="darkred", fg="gold", highlightthickness=0)
payment_menu["menu"].config(font=label_font, bg="darkred", fg="gold")
payment_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Password Entry
tk.Label(create_frame, text="Password:", font=label_font, fg="gold", bg="#003300").grid(row=3, column=0, padx=5, sticky="e")
password_entry_create = tk.Entry(create_frame, show="*")
password_entry_create.grid(row=3, column=1, padx=5)
password_entry_create.bind("<KeyRelease>", update_strength_label)

# Toggle Password Button for Account Creation
toggle_button_create = tk.Button(create_frame, text="Show", font=button_font, bg="darkred", fg="gold", 
                                 command=lambda: toggle_password(password_entry_create, toggle_button_create))
toggle_button_create.grid(row=3, column=2, padx=5)

# Password Strength Label
strength_label = tk.Label(create_frame, text="Strength: ", font=label_font, fg="gold", bg="#003300")
strength_label.grid(row=4, column=1)

# Age Verification Checkbox
age_verified = tk.BooleanVar()
age_check = tk.Checkbutton(create_frame, text="I confirm that I am 18 years or older", font=label_font, 
                           fg="gold", bg="#003300", variable=age_verified, selectcolor="#003300")
age_check.grid(row=5, column=1, pady=5)

# Deposit Amount Option
tk.Label(create_frame, text="Deposit Amount:", font=label_font, fg="gold", bg="#003300").grid(row=6, column=0, padx=5, sticky="e")
deposit_amount_var = tk.StringVar(value="$50")
deposit_options = ["$50", "$100", "$200", "Other"]
deposit_menu = tk.OptionMenu(create_frame, deposit_amount_var, *deposit_options)
deposit_menu.config(font=label_font, bg="darkred", fg="gold", highlightthickness=0)
deposit_menu["menu"].config(font=label_font, bg="darkred", fg="gold")
deposit_menu.grid(row=6, column=1, padx=5, pady=5, sticky="w")

# Entry for "Other" deposit amount (initially hidden)
deposit_other_entry = tk.Entry(create_frame, width=10, font=label_font)

# Monitor changes to deposit selection
deposit_amount_var.trace("w", deposit_option_changed)

# Create Account Button
create_button = tk.Button(create_frame, text="Create Account", font=button_font, bg="darkred", fg="gold", command=create_account)
create_button.grid(row=9, column=1, pady=10)

# Login Frame with dark green background
login_frame = tk.Frame(root, bg="#003300")
login_frame.pack(pady=20)

# Username for Login
tk.Label(login_frame, text="Username:", font=label_font, fg="gold", bg="#003300").grid(row=0, column=0, padx=5, sticky="e")
username_entry_login = tk.Entry(login_frame)
username_entry_login.grid(row=0, column=1, padx=5)

# Password for Login
tk.Label(login_frame, text="Password:", font=label_font, fg="gold", bg="#003300").grid(row=1, column=0, padx=5, sticky="e")
password_entry_login = tk.Entry(login_frame, show="*")
password_entry_login.grid(row=1, column=1, padx=5)

# Toggle Password Button for Login
toggle_button_login = tk.Button(login_frame, text="Show", font=button_font, bg="darkred", fg="gold", 
                                command=lambda: toggle_password(password_entry_login, toggle_button_login))
toggle_button_login.grid(row=1, column=2, padx=5)

# Login Button
login_button = tk.Button(login_frame, text="Login", font=button_font, bg="darkred", fg="gold", command=login)
login_button.grid(row=2, column=1, pady=10)

root.mainloop()
