import customtkinter as ctk


class BanHangFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Tiêu đề
        title = ctk.CTkLabel(
            self,
            text="🛒 BÁN HÀNG",
            font=("Segoe UI", 24, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=15)

        # Khung trái
        left = ctk.CTkFrame(self)
        left.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Khung phải
        right = ctk.CTkFrame(self)
        right.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="nsew")

        # Ô tìm kiếm
        search = ctk.CTkEntry(
            left,
            placeholder_text="Tìm sản phẩm..."
        )
        search.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            left,
            text="Danh sách sản phẩm"
        ).pack(anchor="w", padx=10)

        products = ctk.CTkTextbox(left)
        products.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            right,
            text="Giỏ hàng"
        ).pack(pady=10)

        cart = ctk.CTkTextbox(right)
        cart.pack(fill="both", expand=True, padx=10)

        total = ctk.CTkLabel(
            right,
            text="Tổng tiền: 0 đ",
            font=("Segoe UI", 18, "bold")
        )
        total.pack(pady=15)

        pay = ctk.CTkButton(
            right,
            text="Thanh toán"
        )
        pay.pack(fill="x", padx=15, pady=10)