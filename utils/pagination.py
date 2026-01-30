def paginate_all(fetch_fn, **kwargs):
    """
    Utility to fetch all pages from an API using a fetch function.
    The fetch function should take a 'page' argument and return a list of items.
    """
    all_items = []
    page = 1
    
    while True:
        items = fetch_fn(page=page, **kwargs)
        if not items:
            break
        all_items.extend(items)
        page += 1
        
    return all_items
