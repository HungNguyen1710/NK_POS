import customtkinter as ctk
from tkinter import ttk, messagebox

from services.product_service import ProductService


class SanPhamFrame(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.selected_code = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_widgets()

        self.load_products()

    # =====================================================
    # UI
    # =====================================================

    def create_widgets(self):

        # ==========================
        # TITLE
        # ==========================

        title = ctk.CTkLabel(
            self,
            text="📦 QUẢN LÝ SẢN PHẨM",
            font=("Arial", 24, "bold")
        )

        title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(15, 10),
            sticky="w"
        )

        # ==========================
        # BODY
        # ==========================

        body = ctk.CTkFrame(self)

        body.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=10
        )

        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # ==========================
        # LEFT
        # ==========================

        left = ctk.CTkFrame(body, width=320)

        left.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=(0, 15)
        )

        # --------------------------

        ctk.CTkLabel(
            left,
            text="Mã sản phẩm"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.ent_code = ctk.CTkEntry(left)

        self.ent_code.pack(
            fill="x",
            padx=15
        )

        # --------------------------

        ctk.CTkLabel(
            left,
            text="Tên sản phẩm"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.ent_name = ctk.CTkEntry(left)

        self.ent_name.pack(
            fill="x",
            padx=15
        )

        # --------------------------

        ctk.CTkLabel(
            left,
            text="Giá bán"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.ent_price = ctk.CTkEntry(left)

        self.ent_price.pack(
            fill="x",
            padx=15
        )

        # --------------------------

        ctk.CTkLabel(
            left,
            text="Tồn kho"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        self.ent_stock = ctk.CTkEntry(left)

        self.ent_stock.pack(
            fill="x",
            padx=15
        )

        # ==========================
        # BUTTONS
        # ==========================

        self.btn_add = ctk.CTkButton(
            left,
            text="➕ Thêm",
            command=self.add_product
        )

        self.btn_add.pack(
            fill="x",
            padx=15,
            pady=(20, 5)
        )

        self.btn_update = ctk.CTkButton(
            left,
            text="✏️ Sửa",
            command=self.update_product
        )

        self.btn_update.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.btn_delete = ctk.CTkButton(
            left,
            text="🗑️ Xóa",
            command=self.delete_product
        )

        self.btn_delete.pack(
            fill="x",
            padx=15,
            pady=5
        )

        self.btn_refresh = ctk.CTkButton(
            left,
            text="🔄 Làm mới",
            command=self.refresh
        )

        self.btn_refresh.pack(
            fill="x",
            padx=15,
            pady=5
        )

        # ==========================
        # RIGHT
        # ==========================

        right = ctk.CTkFrame(body)

        right.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        # ==========================
        # SEARCH
        # ==========================

        top = ctk.CTkFrame(right)

        top.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        top.grid_columnconfigure(0, weight=1)

        self.ent_search = ctk.CTkEntry(
            top,
            placeholder_text="Tìm theo mã hoặc tên..."
        )

        self.ent_search.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        self.btn_search = ctk.CTkButton(
            top,
            text="Tìm",
            width=90,
            command=self.search_product
        )

        self.btn_search.grid(
            row=0,
            column=1
        )

        # ==========================
        # TREEVIEW
        # ==========================

        tree_frame = ctk.CTkFrame(right)

        tree_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        columns = (
            "code",
            "name",
            "price",
            "stock"
        )

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading("code", text="Mã SP")
        self.tree.heading("name", text="Tên sản phẩm")
        self.tree.heading("price", text="Giá")
        self.tree.heading("stock", text="Tồn")

        self.tree.column("code", width=120)
        self.tree.column("name", width=280)
        self.tree.column("price", width=120, anchor="e")
        self.tree.column("stock", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_select
        )
    # =====================================================
    # LOAD PRODUCTS
    # =====================================================

    def load_products(self):

        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy dữ liệu
        products = ProductService.get_all()

        # Hiển thị
        for product in products:

            self.tree.insert(
                "",
                "end",
                values=(
                    product["product_code"],
                    product["name"],
                    f"{product['price']:,.0f}",
                    product["stock"]
                )
            )

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh(self):

        self.clear_form()

        self.load_products()

    # =====================================================
    # CLEAR FORM
    # =====================================================

    def clear_form(self):

        self.selected_code = None

        self.ent_code.configure(state="normal")

        self.ent_code.delete(0, "end")
        self.ent_name.delete(0, "end")
        self.ent_price.delete(0, "end")
        self.ent_stock.delete(0, "end")
        self.ent_search.delete(0, "end")

        # Sinh mã mới
        self.ent_code.insert(
            0,
            ProductService.generate_product_code()
        )

    # =====================================================
    # TREEVIEW SELECT
    # =====================================================

    def on_select(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(selected[0])

        values = item["values"]

        if not values:
            return

        code = values[0]

        product = ProductService.get_by_code(code)

        if product is None:
            return

        self.selected_code = code

        self.ent_code.configure(state="normal")

        self.ent_code.delete(0, "end")
        self.ent_name.delete(0, "end")
        self.ent_price.delete(0, "end")
        self.ent_stock.delete(0, "end")

        self.ent_code.insert(
            0,
            product["product_code"]
        )

        self.ent_name.insert(
            0,
            product["name"]
        )

        self.ent_price.insert(
            0,
            str(product["price"])
        )

        self.ent_stock.insert(
            0,
            str(product["stock"])
        )

        # Không cho sửa mã sản phẩm
        self.ent_code.configure(state="disabled")
    # =====================================================
    # ADD PRODUCT
    # =====================================================

    def add_product(self):

        try:

            ProductService.add(
                product_code=self.ent_code.get(),
                name=self.ent_name.get(),
                price=float(self.ent_price.get()),
                stock=int(self.ent_stock.get())
            )

            messagebox.showinfo(
                "Thông báo",
                "Thêm sản phẩm thành công."
            )

            self.refresh()

        except Exception as e:

            messagebox.showerror(
                "Lỗi",
                str(e)
            )

    # =====================================================
    # UPDATE PRODUCT
    # =====================================================

    def update_product(self):

        if self.selected_code is None:

            messagebox.showwarning(
                "Thông báo",
                "Vui lòng chọn sản phẩm."
            )

            return

        try:

            ProductService.update(
                product_code=self.selected_code,
                name=self.ent_name.get(),
                price=float(self.ent_price.get()),
                stock=int(self.ent_stock.get())
            )

            messagebox.showinfo(
                "Thông báo",
                "Cập nhật thành công."
            )

            self.refresh()

        except Exception as e:

            messagebox.showerror(
                "Lỗi",
                str(e)
            )

    # =====================================================
    # DELETE PRODUCT
    # =====================================================

    def delete_product(self):

        if self.selected_code is None:

            messagebox.showwarning(
                "Thông báo",
                "Vui lòng chọn sản phẩm."
            )

            return

        answer = messagebox.askyesno(
            "Xác nhận",
            f"Bạn có muốn xóa sản phẩm\n{self.selected_code} ?"
        )

        if not answer:
            return

        try:

            ProductService.delete(
                self.selected_code
            )

            messagebox.showinfo(
                "Thông báo",
                "Đã xóa sản phẩm."
            )

            self.refresh()

        except Exception as e:

            messagebox.showerror(
                "Lỗi",
                str(e)
            )
    # =====================================================
    # SEARCH PRODUCT
    # =====================================================

    def search_product(self):

        keyword = self.ent_search.get().strip()

        if keyword == "":
            self.load_products()
            return

        products = ProductService.search(keyword)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for product in products:

            self.tree.insert(
                "",
                "end",
                values=(
                    product["product_code"],
                    product["name"],
                    f"{product['price']:,.0f}",
                    product["stock"]
                )
            )

    # =====================================================
    # VALIDATE INPUT
    # =====================================================

    def validate_input(self):

        if self.ent_name.get().strip() == "":
            raise ValueError("Tên sản phẩm không được để trống.")

        try:
            price = float(self.ent_price.get())
        except ValueError:
            raise ValueError("Giá bán không hợp lệ.")

        if price < 0:
            raise ValueError("Giá bán phải lớn hơn hoặc bằng 0.")

        try:
            stock = int(self.ent_stock.get())
        except ValueError:
            raise ValueError("Tồn kho không hợp lệ.")

        if stock < 0:
            raise ValueError("Tồn kho phải lớn hơn hoặc bằng 0.")

        return True

    # =====================================================
    # SHORTCUTS
    # =====================================================

    def bind_events(self):

        self.ent_search.bind(
            "<Return>",
            lambda e: self.search_product()
        )

        self.tree.bind(
            "<Double-1>",
            self.on_select
        )

    # =====================================================
    # INITIALIZE
    # =====================================================

    def initialize(self):

        self.clear_form()

        self.load_products()

        self.bind_events()
        
