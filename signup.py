# signup.py

import customtkinter as ctk
import mysql.connector
import bcrypt
import re
from tkinter import messagebox


class SignupPage:

    def __init__(self, root):

        self.root = root

        self.frame = ctk.CTkFrame(
            root,
            width=500,
            height=650
        )

        self.frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        title = ctk.CTkLabel(
            self.frame,
            text="Create Account",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=20)

        self.full_name = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Full Name"
        )
        self.full_name.pack(pady=10)

        self.phone = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Phone Number"
        )
        self.phone.pack(pady=10)

        self.email = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Email Address"
        )
        self.email.pack(pady=10)

        self.username = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack(pady=10)

        self.confirm_password = ctk.CTkEntry(
            self.frame,
            width=300,
            placeholder_text="Confirm Password",
            show="*"
        )
        self.confirm_password.pack(pady=10)

        create_btn = ctk.CTkButton(
            self.frame,
            text="Create Account",
            width=300,
            command=self.create_account
        )
        create_btn.pack(pady=15)

        login_btn = ctk.CTkButton(
            self.frame,
            text="Back to Login",
            width=300,
            command=self.back_to_login
        )
        login_btn.pack(pady=5)

    def create_account(self):

        name = self.full_name.get().strip()
        phone = self.phone.get().strip()
        email = self.email.get().strip()
        username = self.username.get().strip()
        password = self.password.get()
        confirm = self.confirm_password.get()

        # Validation

        if not name:
            messagebox.showerror(
                "Error",
                "Full Name is required"
            )
            return

        if not phone:
            messagebox.showerror(
                "Error",
                "Phone Number is required"
            )
            return

        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror(
                "Error",
                "Enter a valid 10 digit phone number"
            )
            return

        if not email:
            messagebox.showerror(
                "Error",
                "Email is required"
            )
            return

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(email_pattern, email):
            messagebox.showerror(
                "Error",
                "Invalid Email Address"
            )
            return

        if not username:
            messagebox.showerror(
                "Error",
                "Username is required"
            )
            return

        if len(username) < 4:
            messagebox.showerror(
                "Error",
                "Username must contain at least 4 characters"
            )
            return

        if not password:
            messagebox.showerror(
                "Error",
                "Password is required"
            )
            return

        if len(password) < 8:
            messagebox.showerror(
                "Error",
                "Password must be at least 8 characters long"
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Error",
                "Passwords do not match"
            )
            return

        try:

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="billing_system",
                port=3306
            )

            cursor = conn.cursor()

            # Check duplicate username

            cursor.execute(
                """
                SELECT user_id
                FROM users
                WHERE username=%s
                """,
                (username,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                messagebox.showerror(
                    "Error",
                    "Username already exists"
                )

                cursor.close()
                conn.close()
                return

            # Hash Password

            hashed_password = bcrypt.hashpw(
                password.encode(),
                bcrypt.gensalt()
            ).decode()

            query = """
            INSERT INTO users
            (
                full_name,
                username,
                password,
                role,
                phone,
                email
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """

            values = (
                name,
                username,
                hashed_password,
                "Employee",
                phone,
                email
            )

            cursor.execute(
                query,
                values
            )

            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Account created successfully"
            )

            self.back_to_login()

        except mysql.connector.Error as err:

            messagebox.showerror(
                "Database Error",
                str(err)
            )

    def back_to_login(self):

        self.frame.destroy()

        from login import LoginPage
        LoginPage(self.root)