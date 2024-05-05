def pagination_validator(per_page: int) -> str:
    if per_page not in [15, 25, 50, 100]:
        raise ValueError("per_page must be 15 or 25 or 50 or 100")
    return f"&per_page={per_page}"
