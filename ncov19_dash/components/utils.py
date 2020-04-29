def human_format(num):
    """Formats a number and returns a human-readable version of it in string
    form. Ex: 300,000 -> 300k

    :params num: number to be converted to a formatted string
    """
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format(
        "{:f}".format(
            num
            ).rstrip("0").rstrip("."), ["", "K", "M", "B", "T"][magnitude]
    )


def safe_div(x, y):
    return 0 if int(y) == 0 else int(x) / int(y)
