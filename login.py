from PIL import Image
import customtkinter as ctk

from dashboard import Dashboard
from signup import SignupPage
from auth import AuthSystem

from tkinter import messagebox


class LoginPage:

    def __init__(self, root):

        self.root = root

        # ==========================================
        # COLOR PALETTE
        # ==========================================

        self.primary = "#111827"
        self.primary_hover = "#000000"

        self.gold = "#D4AF37"



        self.white = "#FFFFFF"

        self.gray = "#CBD5E1"

        self.border = "#E5E7EB"

        self.bg = "#F8FAFC"

        self.card = "#FFFFFF"

        # ==========================================
        # LEFT PANEL
        # ==========================================

        self.left_frame = ctk.CTkFrame(
            root,
            width=560,
            fg_color=self.primary,
            corner_radius=0
        )

        self.left_frame.pack(
            side="left",
            fill="both"
        )

        self.left_frame.pack_propagate(False)

        # ==========================================
        # RIGHT PANEL
        # ==========================================

        self.right_frame = ctk.CTkFrame(
            root,
            fg_color=self.bg,
            corner_radius=0
        )

        self.right_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ==========================================
        # LOGIN CARD SHADOW
        # ==========================================

        self.shadow = ctk.CTkFrame(
            self.right_frame,
            width=510,
            height=650,
            fg_color="#D1D5DB",
            corner_radius=32
        )

        self.shadow.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # ==========================================
        # LOGIN CARD
        # ==========================================

        self.frame = ctk.CTkFrame(
            self.right_frame,
            width=520,
            height=670,
            fg_color=self.card,
            corner_radius=30,
            border_width=1,
            border_color="#ECECEC"
        )

        self.frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.frame.pack_propagate(False)

        # ==========================================
        # LEFT BACKGROUND IMAGE
        # ==========================================

        try:

            self.bg_image = ctk.CTkImage(
                light_image=Image.open("assets/login_bg.png"),
                dark_image=Image.open("assets/login_bg.png"),
                size=(900,1000)
            )

            bg = ctk.CTkLabel(
                self.left_frame,
                image=self.bg_image,
                text=""
            )

            bg.place(
                relwidth=1,
                relheight=1
            )

        except Exception as e:

            print("Background :", e)

        # ==========================================
        # GLASS HERO CARD
        # ==========================================

        self.overlay = ctk.CTkFrame(
            self.left_frame,
            width=420,
            height=720,
            fg_color="#161E2F",
            corner_radius=35
        )

        self.overlay.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # ==========================================
        # LOGO
        # ==========================================

        try:

            self.logo = ctk.CTkImage(
                light_image=Image.open("assets/logo.png"),
                dark_image=Image.open("assets/logo.png"),
                size=(85,85)
            )

            logo = ctk.CTkLabel(
                self.overlay,
                image=self.logo,
                text=""
            )

            logo.pack(
                pady=(50,20)
            )

        except Exception as e:

            print("Logo :", e)

        # ==========================================
        # BILLING ERP TITLE
        # ==========================================

        title_frame = ctk.CTkFrame(
            self.overlay,
            fg_color="transparent"
        )

        title_frame.pack()

        billing = ctk.CTkLabel(
            title_frame,
            text="Billing",
            font=("Segoe UI",40,"bold"),
            text_color="white"
        )

        billing.pack(side="left")

        erp = ctk.CTkLabel(
            title_frame,
            text=" ERP",
            font=("Segoe UI",40,"bold"),
            text_color=self.gold
        )

        erp.pack(side="left")

        # ==========================================
        # SUBTITLE
        # ==========================================

        subtitle = ctk.CTkLabel(
            self.overlay,
            text="Business Management Suite",
            font=("Segoe UI",17,"bold"),
            text_color="#E3B341"
        )

        module = ctk.CTkLabel(
            self.overlay,
            text="Inventory • Billing • Reports • Analytics",
            font=("Segoe UI",13),
            text_color="#CBD5E1"
        )

        subtitle.pack(
            pady=(15,35)
        )
        module.pack(pady=(8,30))

        # ==========================================
        # DESCRIPTION
        # ==========================================

        description = ctk.CTkLabel(
            self.overlay,
            text=(
                "One intelligent platform\n"
                "to manage billing,\n"
                "inventory and business\n"
                "operations efficiently."
            ),
            font=("Segoe UI",17),
            justify="center",
            text_color="#E5E7EB"
        )

        description.pack()

        # ==========================================
        # DIVIDER
        # ==========================================

        divider = ctk.CTkFrame(
            self.overlay,
            width=300,
            height=3,
            fg_color=self.gold
        )

        divider.pack(
            pady=(35,35)
        )

        # ==========================================
        # FEATURES
        # ==========================================
        
        feature_title = ctk.CTkLabel(
            self.overlay,
            text="CORE MODULES",
            font=("Segoe UI",12,"bold"),
            text_color="#E3B341"
        )

        feature_title.pack(pady=(0,20))


        feature_list = [
            "📄 Smart Billing",
            "📦 Inventory Tracking",
            "👥 Customer Management",
            "🚚 Supplier Management",
            "📊 GST Ready"
        ]

        for item in feature_list:

            row = ctk.CTkFrame(
                self.overlay,
                fg_color="transparent"
            )

            row.pack(
                anchor="w",
                padx=55,
                pady=7
            )

            check = ctk.CTkLabel(
                row,
                text="✔",
                font=("Segoe UI",20,"bold"),
                text_color=self.gold
            )

            check.pack(
                side="left"
            )

            text = ctk.CTkLabel(
                row,
                text=item,
                font=("Segoe UI",19),
                text_color="white"
            )

            text.pack(
                side="left",
                padx=(12,0)
            )

        # ==========================================
        # FOOTER
        # ==========================================

        footer = ctk.CTkLabel(
            self.overlay,
            text="Version 1.0 • Powered by Billing ERP",
            font=("Segoe UI",11),
            text_color="#94A3B8"
        )

        footer.pack(
            side="bottom",
            pady=25
        )


                # =====================================================
        # LOGIN HEADER ICON
        # =====================================================

        self.user_icon = ctk.CTkFrame(
            self.frame,
            width=80,
            height=80,
            corner_radius=40,
            fg_color=self.primary
        )

        self.user_icon.pack(
            pady=(35,15)
        )

        self.user_icon.pack_propagate(False)

        icon = ctk.CTkLabel(
            self.user_icon,
            text="👤",
            font=("Segoe UI Emoji",34),
            text_color="white"
        )

        icon.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # =====================================================
        # TITLE
        # =====================================================

        title = ctk.CTkLabel(
            self.frame,
            text="Welcome Back!",
            font=("Segoe UI",30,"bold"),
            text_color="#111827"
        )

        title.pack()

        subtitle = ctk.CTkLabel(
            self.frame,
            text="Login to continue to your Billing ERP",
            font=("Segoe UI",14),
            text_color="#6B7280"
        )

        subtitle.pack(
            pady=(8,30)
        )

        # =====================================================
        # USERNAME
        # =====================================================

        self.username = ctk.CTkEntry(
            self.frame,
            width=360,
            height=55,
            corner_radius=16,
            border_width=1,
            border_color="#FAFAFA",
            placeholder_text="👤 Username",
            font=("Segoe UI",15)
        )

        self.username.pack(
            pady=10
        )

        # =====================================================
        # PASSWORD FRAME
        # =====================================================

        password_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        password_frame.pack(
            pady=10
        )

        self.password = ctk.CTkEntry(
            password_frame,
            width=315,
            height=55,
            corner_radius=16,
            border_width=1,
            border_color="#D1D5DB",
            placeholder_text="🔒 Password",
            show="*",
            font=("Segoe UI",15)
        )

        self.password.pack(
            side="left"
        )

        self.show_password = False

        self.eye_btn = ctk.CTkButton(
            password_frame,
            width=40,
            height=55,
            text="👁",
            fg_color="transparent",
            hover=False,
            text_color="#374151",
            command=self.toggle_password
        )

        self.eye_btn.pack(
            side="left",
            padx=(5,0)
        )

        # =====================================================
        # REMEMBER + FORGOT
        # =====================================================

        options = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        options.pack(
            fill="x",
            padx=55,
            pady=(10,20)
        )

        self.remember = ctk.CTkCheckBox(
            options,
            text="Remember Me",
            checkbox_width=18,
            checkbox_height=18,
            font=("Segoe UI",13)
        )

        self.remember.pack(
            side="left"
        )

        forgot = ctk.CTkLabel(
            options,
            text="Forgot Password?",
            text_color=self.gold,
            cursor="hand2",
            font=("Segoe UI",13,"underline")
        )

        forgot.pack(
            side="right"
        )

        forgot.bind(
            "<Button-1>",
            lambda e:self.open_forgot()
        )

        # =====================================================
        # LOGIN BUTTON
        # =====================================================

        self.login_btn = ctk.CTkButton(
            self.frame,
            text="LOGIN →",
            width=360,
            height=55,
            corner_radius=16,
            fg_color=self.primary,
            hover_color="#1F2937",
            font=("Segoe UI",16,"bold"),
            command=self.login
        )

        self.login_btn.pack(
            pady=(10,25)
        )

        # =====================================================
        # OR DIVIDER
        # =====================================================

        divider_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        divider_frame.pack(
            fill="x",
            padx=50,
            pady=10
        )

        left = ctk.CTkFrame(
            divider_frame,
            height=1,
            fg_color="#E5E7EB"
        )

        left.pack(
            side="left",
            fill="x",
            expand=True,
            pady=8
        )

        or_label = ctk.CTkLabel(
            divider_frame,
            text=" OR ",
            text_color="#9CA3AF",
            font=("Segoe UI",12)
        )

        or_label.pack(
            side="left",
            padx=10
        )

        right = ctk.CTkFrame(
            divider_frame,
            height=1,
            fg_color="#D1D5DB"
        )

        right.pack(
            side="left",
            fill="x",
            expand=True,
            pady=8
        )

        # =====================================================
        # SIGNUP BUTTON
        # =====================================================

        self.signup_btn = ctk.CTkButton(
            self.frame,
            text="Create New Account",
            width=360,
            height=55,
            corner_radius=16,
            fg_color="white",
            text_color=self.gold,
            border_width=2,
            border_color=self.gold,
            hover_color="#FFF8E7",
            font=("Segoe UI",15,"bold"),
            command=self.open_signup
        )

        self.signup_btn.pack(
            pady=(20,10)
        )

        # =====================================================
        # VERSION
        # =====================================================

        version = ctk.CTkLabel(
            self.frame,
            text="Version 1.0",
            font=("Segoe UI",11),
            text_color="#9CA3AF"
        )

        version.pack(
            side="bottom",
            pady=18
        )


            # ==========================================================
    # LOGIN FUNCTION
    # ==========================================================

    def login(self):

        username = self.username.get().strip()
        password = self.password.get()

        # ---------- Validation ----------

        if username == "":
            messagebox.showwarning(
                "Username Required",
                "Please enter your username."
            )
            self.username.focus()
            return

        if password == "":
            messagebox.showwarning(
                "Password Required",
                "Please enter your password."
            )
            self.password.focus()
            return

        # ---------- Loading State ----------

        self.login_btn.configure(
            text="Logging in...\n" 
                 "Logging in...\n"
                 "Logging in...\n",
            state="disabled"
        )

        self.root.update()

        try:

            auth = AuthSystem()

            result = auth.login_user(
                username,
                password
            )

            if result["status"]:

                messagebox.showinfo(
                    "Login Successful",
                    f"Welcome, {result['full_name']}!"
                )

                self.left_frame.destroy()
                self.right_frame.destroy()

                Dashboard(self.root)

            else:

                self.login_btn.configure(
                    text="LOGIN",
                    state="normal"
                )

                messagebox.showerror(
                    "Login Failed",
                    result["message"]
                )

        except Exception as e:

            self.login_btn.configure(
                text="LOGIN",
                state="normal"
            )

            messagebox.showerror(
                "Error",
                str(e)
            )

    # ==========================================================
    # SHOW / HIDE PASSWORD
    # ==========================================================

    def toggle_password(self):

        if self.show_password:

            self.password.configure(show="*")

            self.eye_btn.configure(text="👁")

        else:

            self.password.configure(show="")

            self.eye_btn.configure(text="🙈")

        self.show_password = not self.show_password

    # ==========================================================
    # OPEN SIGNUP PAGE
    # ==========================================================

    def open_signup(self):

        self.left_frame.destroy()
        self.right_frame.destroy()

        SignupPage(self.root)

    # ==========================================================
    # FORGOT PASSWORD
    # ==========================================================

    def open_forgot(self):

        messagebox.showinfo(
            "Forgot Password",
            "Forgot Password functionality will be available soon."
        )

    # ==========================================================
    # ENTER KEY SUPPORT
    # ==========================================================

    def bind_keys(self):

        self.username.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.password.bind(
            "<Return>",
            lambda event: self.login()
        ) 

        self.bind_keys()
