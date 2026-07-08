import customtkinter as ctk

from ui.dashboard import DashboardFrame
from ui.banhang import BanHangFrame
from ui.sanpham import SanPhamFrame

# Tạm thời chưa có file hoadon.py
try:
    from ui.hoadon import HoaDonFrame
except ImportError:
    HoaDonFrame = None


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, show_page):
        super().__init__(master, width=220, corner_radius=0)

        self.show_page = show_page

        self.grid_propagate(False)

        # ===== Logo =====
        logo = ctk.CTkLabel(
            self,
            text="QUYNHANH POS",
            font=("Arial", 22, "bold")
        )
        logo.pack(pady=(30, 40))

        # ===== Menu =====
        self.create_button("🏠 Dashboard", DashboardFrame)
        self.create_button("🛒 Bán hàng", BanHangFrame)
        self.create_button("📦 Sản phẩm", SanPhamFrame)
        self.create_button("🧾 Hóa đơn", HoaDonFrame)

        # ===== Khoảng trống =====
        ctk.CTkLabel(self, text="").pack(expand=True)

        # ===== Footer =====
        version = ctk.CTkLabel(
            self,
            text="Version 1.0",
            text_color="gray"
        )
        version.pack(pady=20)

    def create_button(self, text, page):

        btn = ctk.CTkButton(
            self,
            text=text,
            height=45,
            corner_radius=8,
            anchor="w",
            command=lambda: self.show_page(page)
        )

        btn.pack(fill="x", padx=15, pady=6)