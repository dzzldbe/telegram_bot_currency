def get_flag_emoji(currency_code: str) -> str:
    code = currency_code.strip().lower()

    # 1. Manual mapping for crypto, metals, and complex unions
    exceptions = {
        "1inch": "🪙",
        "aave": "🪙",
        "ada": "🪙",
        "algo": "🪙",
        "amp": "🪙",
        "ar": "🪙",
        "avax": "🪙",
        "axs": "🪙",
        "bch": "🪙",
        "bnb": "🪙",
        "bsv": "🪙",
        "btc": "🪙",
        "btcb": "🪙",
        "btg": "🪙",
        "busd": "🪙",
        "celo": "🪙",
        "chz": "🪙",
        "comp": "🪙",
        "cro": "🪙",
        "crv": "🪙",
        "cvx": "🪙",
        "dai": "🪙",
        "doge": "🪙",
        "dot": "🪙",
        "enj": "🪙",
        "eos": "🪙",
        "etc": "🪙",
        "eth": "🪙",
        "fantom": "🪙",
        "fet": "🪙",
        "fil": "🪙",
        "ftm": "🪙",
        "ftt": "🪙",
        "gno": "🪙",
        "grt": "🪙",
        "hnt": "🪙",
        "hot": "🪙",
        "icp": "🪙",
        "imx": "🪙",
        "inj": "🪙",
        "ltc": "🪙",
        "luna": "🪙",
        "lunc": "🪙",
        "man": "🪙",
        "mana": "🪙",
        "matic": "🪙",
        "near": "🪙",
        "neo": "🪙",
        "nex": "🪙",
        "nexo": "🪙",
        "one": "🪙",
        "qnt": "🪙",
        "shib": "🪙",
        "sol": "🪙",
        "stx": "🪙",
        "theta": "🪙",
        "trx": "🪙",
        "ttt": "🪙",
        "uni": "🪙",
        "usdc": "🪙",
        "usdp": "🪙",
        "usdt": "🪙",
        "vet": "🪙",
        "wbtc": "🪙",
        "xaut": "🪙",
        "xch": "🪙",
        "xdc": "🪙",
        "xlm": "🪙",
        "xmr": "🪙",
        "xrp": "🪙",
        "xtz": "🪙",
        "zec": "🪙",
        "zil": "🪙",
        # Precious Metals
        "xag": "🥈",
        "xau": "🥇",
        "xpd": "💎",
        "xpt": "💎",
        # Special Unions (Don't match 2-letter country codes)
        "eur": "🇪🇺",  # Eurozone
        "ang": "🇨🇼",  # Netherlands Antilles -> Curaçao
        "xaf": "🇨🇲",  # Central African CFA franc (Cameroon flag used frequently)
        "xof": "🇸🇳",  # West African CFA franc (Senegal flag used frequently)
        "xcd": "🇦🇬",  # East Caribbean Dollar (Antigua flag used frequently)
    }

    if code in exceptions:
        return exceptions[code]

    # 2. Dynamic generation for standard 3-letter fiat codes (e.g., 'usd' -> 'US' -> 🇺🇸)
    # Most fiat currencies use the first two letters for the ISO country code.
    country_code = code[:2].upper()

    if len(country_code) == 2 and country_code.isalpha():
        try:
            # Regional Indicator Symbol Letter A is U+1F1E6 (127462)
            # ASCII 'A' is 65. Magic offset = 127462 - 65 = 127397
            return "".join(chr(ord(char) + 127397) for char in country_code)
        except ValueError:
            return "🏳️"  # Fallback for unexpected generation errors

    return "🏳️"  # Final fallback flag if code format is completely unknown


def clean_and_convert(value_str):
    value_str = value_str.strip()
    if "," in value_str and "." in value_str:
        if value_str.index(",") < value_str.index("."):
            value_str = value_str.replace(",", "")
        else:
            value_str = value_str.replace(".", "").replace(",", ".")

    elif "," in value_str:
        value_str = value_str.replace(",", ".")

    return float(value_str)


def is_float(val):
    try:
        clean_and_convert(val)
        return True
    except ValueError:
        return False


def chunk_text(text, limit=4000):
    # 1. Start with an empty list to hold our text chunks
    chunks = []

    # 2. Loop through the indices of the text, jumping by the 'limit' size each time
    for i in range(0, len(text), limit):
        # 3. Slice the text from the current index 'i' to 'i + limit'
        current_chunk = text[i : i + limit]

        # 4. Add this fresh slice to our chunks list
        chunks.append(current_chunk)

    # 5. Send the finished list back
    return chunks
