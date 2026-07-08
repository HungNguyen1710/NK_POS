import customtkinter as ctk
from tkinter import ttk, messagebox

from services.product_service import (
    add_product,
    get_products,
    update_product,
    delete_product,
    search_product
)



class SanPhamFrame(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.pack(fill="both", expand=True)


        # ======================
        # TITLE
        # ======================

        title = ctk.CTkLabel(
            self,
            text="📦 QUẢN LÝ SẢN PHẨM",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=15
        )



        # ======================
        # FORM
        # ======================

        form = ctk.CTkFrame(self)

        form.pack(
            fill="x",
            padx=20
        )


        self.code = self.create_input(
            form,
            "Mã SP"
        )

        self.name = self.create_input(
            form,
            "Tên SP"
        )

        self.price = self.create_input(
            form,
            "Giá"
        )

        self.stock = self.create_input(
            form,
            "Tồn kho"
        )



        # ======================
        # BUTTON
        # ======================


        btn_frame = ctk.CTkFrame(
            self
        )

        btn_frame.pack(
            pady=10
        )


        ctk.CTkButton(
            btn_frame,
            text="➕ Thêm",
            command=self.add
        ).grid(
            row=0,
            column=0,
            padx=5
        )


        ctk.CTkButton(
            btn_frame,
            text="✏ Sửa",
            command=self.edit
        ).grid(
            row=0,
            column=1,
            padx=5
        )


        ctk.CTkButton(
            btn_frame,
            text="🗑 Xóa",
            command=self.remove
        ).grid(
            row=0,
            column=2,
            padx=5
        )



        # ======================
        # SEARCH
        # ======================


        search_frame = ctk.CTkFrame(
            self
        )

        search_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )


        self.keyword = ctk.CTkEntry(
            search_frame,
            placeholder_text="Tìm mã hoặc tên sản phẩm..."
        )

        self.keyword.pack(
            side="left",
            fill="x",
            expand=True
        )


        ctk.CTkButton(
            search_frame,
            text="🔎 Tìm",
            command=self.search
        ).pack(
            side="left",
            padx=5
        )



        # ======================
        # TABLE
        # ======================


        table_frame = ctk.CTkFrame(
            self
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )


        columns = (
            "id",
            "code",
            "name",
            "price",
            "stock"
        )


        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )


        headings = {

            "id":"ID",

            "code":"Mã SP",

            "name":"Tên sản phẩm",

            "price":"Giá",

            "stock":"Tồn"

        }


        for col in columns:

            self.table.heading(
                col,
                text=headings[col]
            )

            self.table.column(
                col,
                width=100
            )


        self.table.pack(
            fill="both",
            expand=True
        )


        self.table.bind(
            "<ButtonRelease-1>",
            self.select_row
        )


        self.load_data()



    # =================================
    # CREATE INPUT
    # =================================

    def create_input(self, parent, text):

        frame = ctk.CTkFrame(
            parent
        )

        frame.pack(
            side="left",
            padx=10,
            pady=10
        )


        label = ctk.CTkLabel(
            frame,
            text=text
        )

        label.pack()


        entry = ctk.CTkEntry(
            frame,
            width=150
        )

        entry.pack()


        return entry



    # =================================
    # LOAD DATA
    # =================================

    def load_data(self):

        for row in self.table.get_children():

            self.table.delete(row)



        products = get_products()


        for p in products:

            self.table.insert(
                "",
                "end",
                values=(

                    p["id"],

                    p["product_code"],

                    p["name"],

                    p["price"],

                    p["stock"]

                )
            )



    # =================================
    # ADD
    # =================================


    def add(self):

        try:

            add_product(

                self.code.get(),

                self.name.get(),

                float(self.price.get()),

                int(self.stock.get())

            )


            messagebox.showinfo(
                "Thông báo",
                "Đã thêm sản phẩm"
            )


            self.clear()

            self.load_data()


        except Exception as e:

            messagebox.showerror(
                "Lỗi",
                str(e)
            )



    # =================================
    # EDIT
    # =================================


    def edit(self):

        try:

            update_product(

                self.code.get(),

                self.name.get(),

                float(self.price.get()),

                int(self.stock.get())

            )


            self.load_data()


        except Exception as e:

            messagebox.showerror(
                "Lỗi",
                str(e)
            )



    # =================================
    # DELETE
    # =================================


    def remove(self):

        code = self.code.get()


        if not code:

            return


        if messagebox.askyesno(
            "Xác nhận",
            "Xóa sản phẩm này?"
        ):


            delete_product(
                code
            )


            self.load_data()

            self.clear()



    # =================================
    # SEARCH
    # =================================


    def search(self):

        key = self.keyword.get()


        for row in self.table.get_children():

            self.table.delete(row)



        products = search_product(
            key
        )


        for p in products:

            self.table.insert(
                "",
                "end",
                values=(

                    p["id"],
                    p["product_code"],
                    p["name"],
                    p["price"],
                    p["stock"]

                )
            )



    # =================================
    # SELECT TABLE ROW
    # =================================


    def select_row(self,event):

        selected = self.table.selection()


        if not selected:

            return


        data = self.table.item(
            selected[0]
        )["values"]


        self.code.delete(0,"end")
        self.code.insert(0,data[1])


        self.name.delete(0,"end")
        self.name.insert(0,data[2])


        self.price.delete(0,"end")
        self.price.insert(0,data[3])


        self.stock.delete(0,"end")
        self.stock.insert(0,data[4])



    # =================================
    # CLEAR
    # =================================


    def clear(self):

        for item in [

            self.code,

            self.name,

            self.price,

            self.stock

        ]:

            item.delete(
                0,
                "end"
            )