# scraper.py

def scrape_amazon(product_name, budget=None):
    # Include budget in search query so results are price-relevant
    if budget and budget > 0:
        budget = int(budget)
        # Search query includes price — e.g. "pendrive under 300"
        search_query = f"{product_name} under {budget}".replace(" ", "+")
        price_label  = f"Under ₹{budget}"

        platforms = {
            "Amazon": (
                f"https://www.amazon.in/s?k={search_query}"
                f"&rh=p_36%3A100-{budget * 100}"
                f"&s=price-asc-rank"
            ),
            "Flipkart": (
                f"https://www.flipkart.com/search?q={search_query}"
                f"&p%5B%5D=facets.price_range.from%3D1"
                f"&p%5B%5D=facets.price_range.to%3D{budget}"
                f"&sort=price_asc"
            ),
            "Myntra": (
                f"https://www.myntra.com/{search_query}"
                f"?f=Price%3A0%20TO%20{budget}"
                f"&sort=price_asc"
            ),
            "Nykaa": (
                f"https://www.nykaa.com/search/result/?q={search_query}"
                f"&price_max={budget}"
                f"&sort=price_asc"
            ),
            "Meesho": (
                f"https://www.meesho.com/search?q={search_query}"
                f"&f_Price=0_{budget}"
            ),
        }
    else:
        search_query = product_name.replace(" ", "+")
        price_label  = "Click to view prices"

        platforms = {
            "Amazon":   f"https://www.amazon.in/s?k={search_query}",
            "Flipkart": f"https://www.flipkart.com/search?q={search_query}",
            "Myntra":   f"https://www.myntra.com/{search_query}",
            "Nykaa":    f"https://www.nykaa.com/search/result/?q={search_query}",
            "Meesho":   f"https://www.meesho.com/search?q={search_query}",
        }

    results = []
    for name, link in platforms.items():
        results.append({
            "title": f"Search '{product_name}' on {name}",
            "price": price_label,
            "link":  link
        })

    return results