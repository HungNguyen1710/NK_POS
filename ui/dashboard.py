import customtkinter as ctk


class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=30)

        box = ctk.CTkFrame(self)
        box.pack(fill="x", padx=30)

        data = [
            ("💰 Doanh thu", "0 đ"),
            ("🧾 Đơn hàng", "0"),
            ("📦 Sản phẩm", "0"),
            ("🏪 Tồn kho", "0"),
        ]

        for name, value in data:
            card = ctk.CTkFrame(box)
            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=10,
                pady=10
            )

            ctk.CTkLabel(
                card,
                text=name,
                font=("Segoe UI", 16)
            ).pack(pady=(20,5))

            ctk.CTkLabel(
                card,
                text=value,
                font=("Segoe UI", 24, "bold")
            ).pack(pady=(5,20))