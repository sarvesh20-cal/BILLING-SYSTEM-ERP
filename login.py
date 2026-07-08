import customtkinter as ctk
from dashboard import Dashboard
from auth import AuthSystem
from tkinter import messagebox

class LoginPage:

    def __init__(self, root):
        self.root = root
        self.frame = ctk.CTkFrame(root, corner_radius= 15)
        self.frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        self.title = ctk.CTkLabel(
            self.frame,
            text = "Billing Management System",
            font = ("Times New Roman", 28, "bold")
        )

        self.title.pack(pady = 30)

        self.username = ctk.CTkEntry(
            self.frame,
            width= 300,
            height= 40,
            placeholder_text= "Username"
        )
        self.username.pack(pady = 10)


        self.password = ctk.CTkEntry(
            self.frame,
            width= 300,
            height= 40,
            placeholder_text= "Password",
            show = "*"
        )
        self.password.pack(pady = 10)


        self.login_btn = ctk.CTkButton(
            self.frame,
            text="Login",
            width=300,
            height=40,
            command= self.login
        )
        self.login_btn.pack(pady = 20)
    

    def login(self):
        
        username = self.username.get()
        password = self.password.get()

        auth = AuthSystem()

        result = auth.login_user(username, password)

        if result["status"]:
            messagebox.showinfo(
                "Login Success",
                f"Welcome {result['full_name']}"
            )

            self.frame.destroy()

            Dashboard(self.root)

        else:

            messagebox.showerror(
                "Login Failed",
                result["message"]
            )
