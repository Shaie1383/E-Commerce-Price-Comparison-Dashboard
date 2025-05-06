from collections import defaultdict
from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    with open('../scraper/products.json', 'r', encoding='utf-8') as f:
        data = json.load(f)["products"]

    # Filters
    query = request.args.get("search", "").lower()
    platform = request.args.get("platform", "")
    availability = request.args.get("availability", "")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)

    filtered = []
    for p in data:
        if query and query not in p["name"].lower():
            continue
        if platform and p["platform"] != platform:
            continue
        if availability and p["stock_status"] != availability:
            continue
        if min_price is not None and p["price"] < min_price:
            continue
        if max_price is not None and p["price"] > max_price:
            continue
        filtered.append(p)

    # Charts
    stock_count = defaultdict(int)
    price_sum = defaultdict(float)
    product_count = defaultdict(int)

    for p in filtered:
        plat = p["platform"]
        if p["stock_status"] == "In Stock":
            stock_count[plat] += 1
        price_sum[plat] += p["price"]
        product_count[plat] += 1

    avg_price = {plat: round(price_sum[plat] / product_count[plat], 2) for plat in price_sum}

    return render_template("index.html", products=filtered,
                           stock_data=dict(stock_count),
                           avg_price_data=avg_price)

# ✅ This part is CRITICAL to make it run:
if __name__ == "__main__":
    app.run(debug=True)