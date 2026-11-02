def get_product_from_db(product_id):
    pass

def is_expennsive(product_id):
    product = get_product_from_db(product_id)

    return product["price"] > 100 


