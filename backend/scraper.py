# def scrape_amazon(product_name):
#     search_query = product_name.replace(" ", "+")
    
#     amazon_link = f"https://www.amazon.in/s?k={search_query}"
#     flipkart_link = f"https://www.flipkart.com/search?q={search_query}"
    
#     return [
#         {
#             "title": f"Search '{product_name}' on Amazon",
#             "price": "Click to view prices",
#             "link": amazon_link
#         },
#         {
#             "title": f"Search '{product_name}' on Flipkart",
#             "price": "Click to view prices",
#             "link": flipkart_link
#         }
#     ]
def scrape_amazon(product_name):
    search_query = product_name.replace(" ", "+")

    platforms = {
        "Amazon": f"https://www.amazon.in/s?k={search_query}",
        "Flipkart": f"https://www.flipkart.com/search?q={search_query}",
        "Myntra": f"https://www.myntra.com/{search_query}",
        "Nykaa": f"https://www.nykaa.com/search/result/?q={search_query}",
        "Meesho": f"https://www.meesho.com/search?q={search_query}"
    }

    results = []

    for name, link in platforms.items():
        results.append({
            "title": f"Search '{product_name}' on {name}",
            "price": "Click to view prices",
            "link": link
        })

    return results