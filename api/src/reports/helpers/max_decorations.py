def max_decorations(query) -> int:
    """
    Extract maximum decorations count from ProductVariant query
    query: ProductVariant query
    """

    # Extract all product variants
    pvs = query.all()

    # Extract count of decorations from each product variant
    decoration_counts = [len(x.decorations) for x in pvs]

    try:
        max_count = max(decoration_counts)
    except Exception:
        max_count = 0

    return max_count
