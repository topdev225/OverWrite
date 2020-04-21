from typing import List


def attributes(query) -> List[str]:
    """
    Extract ProductAttribute model from each product variant
    query: ProductVariant query
    """

    # Define storage
    attributes = []

    # Extract all product variants
    pvs = query.all()

    # Extract attributes from product variants
    for pv in pvs:
        attributes += pv.product.product_type.product_attributes

    return list({pa.id: pa for pa in attributes}.values())
