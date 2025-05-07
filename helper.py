def clean_title(title: str) -> str:
    # remove all non alphanumeric characters
    title_clean = "".join(char for char in title if char.isalnum()).lower()

    return title_clean
