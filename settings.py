import customtkinter as ctk

class SettingsPage:

    def __init__(self, parent):

        title = ctk.CTkLabel(
            parent,
            text="Settings",
            font=("Segoe UI", 26, "bold")
        )
        title.pack(pady=20)

        form = ctk.CTkFrame(parent)
        form.pack(fill="x", padx=20, pady=20)

        company = ctk.CTkEntry(
            form,
            placeholder_text="Company Name",
            width=400
        )
        company.pack(pady=10)

        gst = ctk.CTkEntry(
            form,
            placeholder_text="GST Number",
            width=400
        )
        gst.pack(pady=10)

        email = ctk.CTkEntry(
            form,
            placeholder_text="Business Email",
            width=400
        )
        email.pack(pady=10)

        save_btn = ctk.CTkButton(
            form,
            text="Save Settings",
            width=200
        )
        save_btn.pack(pady=20)