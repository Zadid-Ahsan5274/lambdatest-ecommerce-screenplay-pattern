import re

def parse_price(text:str)->float:
    match = re.search(r"\d[\d,]*\.?\d*", text)
    if not match:
        raise ValueError(f"No price found in {text!r}")
    return float(match.group().replace(",",""))

def safe_name(value:str,max_length:int = 150)->str:
    return re.sub(r"[^\w\-.]+", "_", value)[:max_length]