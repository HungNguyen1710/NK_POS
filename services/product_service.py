from database.db import (
    execute,
    fetch_all,
    fetch_one
)



def add_product(product_code, name, price, stock):
    """
    Thêm sản phẩm
    """

    query = """
    INSERT INTO products
    (
        product_code,
        name,
        price,
        stock
    )
    VALUES (?, ?, ?, ?)
    """

    return execute(
        query,
        (
            product_code,
            name,
            price,
            stock
        )
    )



def get_products():
    """
    Lấy toàn bộ sản phẩm
    """

    query = """
    SELECT *
    FROM products
    ORDER BY id DESC
    """

    return fetch_all(query)



def get_product_by_code(product_code):
    """
    Tìm sản phẩm theo mã
    """

    query = """
    SELECT *
    FROM products
    WHERE product_code = ?
    """

    return fetch_one(
        query,
        (product_code,)
    )



def update_stock(product_code, new_stock):
    """
    Cập nhật tồn kho
    """

    query = """
    UPDATE products
    SET stock = ?
    WHERE product_code = ?
    """

    return execute(
        query,
        (
            new_stock,
            product_code
        )
    )



def update_product(
        product_code,
        name,
        price,
        stock
):
    """
    Sửa thông tin sản phẩm
    """

    query = """
    UPDATE products

    SET
        name=?,
        price=?,
        stock=?

    WHERE product_code=?
    """


    return execute(
        query,
        (
            name,
            price,
            stock,
            product_code
        )
    )



def delete_product(product_code):
    """
    Xóa sản phẩm
    """

    query = """
    DELETE FROM products
    WHERE product_code=?
    """

    return execute(
        query,
        (product_code,)
    )



def search_product(keyword):
    """
    Tìm kiếm sản phẩm
    theo mã hoặc tên
    """

    query = """
    SELECT *
    FROM products

    WHERE
        product_code LIKE ?
        OR
        name LIKE ?

    ORDER BY name
    """


    key = f"%{keyword}%"


    return fetch_all(
        query,
        (
            key,
            key
        )
    )



def create_sample_products():
    """
    Tạo dữ liệu test lần đầu
    """

    samples = [

        (
            "SP001",
            "Cà phê sữa",
            15000,
            100
        ),

        (
            "SP002",
            "Trà đào",
            25000,
            50
        ),

        (
            "SP003",
            "Nước suối",
            10000,
            200
        )

    ]


    for item in samples:

        exists = get_product_by_code(
            item[0]
        )

        if not exists:

            add_product(
                item[0],
                item[1],
                item[2],
                item[3]
            )