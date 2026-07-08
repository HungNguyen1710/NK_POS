import customtkinter as ctk

from database.db import init_database

from ui.sidebar import Sidebar
from ui.dashboard import DashboardFrame
from ui.banhang import BanHangFrame
from ui.sanpham import SanPhamFrame


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("NK POS")
        self.geometry("1300x760")

        init_database()

        # ===== Layout =====
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = Sidebar(self, self.show_page)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Vùng hiển thị
        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")

        self.current_frame = None

        # Mở Dashboard mặc định
        self.show_page(DashboardFrame)

    def show_page(self, page_class):
        """Hiển thị một trang"""

        if self.current_frame is not None:
            self.current_frame.destroy()

        # Tạm thời Hóa đơn chưa có
        if page_class is None:
            return

        self.current_frame = page_class(self.content)
        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()