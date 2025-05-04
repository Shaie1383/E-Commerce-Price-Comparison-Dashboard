import json
from tabulate import tabulate
import os

def load_products():
    # Check if the file exists
    json_file_path = '../scraper/products.json'  # Path relative to compare_products.py
    if not os.path.exists(json_file_path):
        print(f"Error: {json_file_path} not found. Please run the scraper first.")
        return []
    
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            return data.get("products", [])
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return []

def compare_products(products):
    if not products:
        print("No products to compare.")
        return
    
    # Sort by product name
    products.sort(key=lambda x: x['name'])

    # Text table (optional for console)
    table = [
        [p["name"], p["price"], p["stock_status"], p["platform"]]
        for p in products
    ]
    headers = ["Product Name", "Price (₹)", "Availability", "Platform"]
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    # HTML table generation
    html_table = tabulate(table, headers=headers, tablefmt="html")
    html_content = f"""
   <html>
<head>
    <title>Product Comparison Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            padding: 20px;
        }}
        h1 {{
            color: #333;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
            cursor: pointer;
        }}
        th {{
            background-color: #007bff;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        select {{
            margin-top: 10px;
            padding: 5px;
        }}
    </style>
</head>
<body>
    <h1>Product Comparison Report</h1>

    <label for="platformFilter">Filter by Platform:</label>
    <select id="platformFilter" onchange="filterTable()">
        <option value="All">All</option>
        <option value="Amazon">Amazon</option>
        <option value="Flipkart">Flipkart</option>
        <option value="Myntra">Myntra</option>
    </select>

    {html_table}

    <script>
        function filterTable() {{
            var platform = document.getElementById("platformFilter").value;
            var rows = document.querySelectorAll("table tr");

            rows.forEach((row, index) => {{
                if (index === 0) return;  // header
                const platformCell = row.cells[3];
                if (!platformCell) return;
                row.style.display = (platform === "All" || platformCell.innerText === platform) ? "" : "none";
            }});
        }}

        // Sort by column when header clicked
        document.querySelectorAll("th").forEach((th, idx) => {{
            th.addEventListener("click", () => {{
                const table = th.closest("table");
                const rows = Array.from(table.querySelectorAll("tr:nth-child(n+2)"));
                const ascending = th.classList.toggle("asc");

                rows.sort((a, b) => {{
                    let aText = a.children[idx].innerText;
                    let bText = b.children[idx].innerText;

                    const aNum = parseFloat(aText.replace(/[₹,]/g, ''));
                    const bNum = parseFloat(bText.replace(/[₹,]/g, ''));
                    const isNumeric = !isNaN(aNum) && !isNaN(bNum);

                    return ascending
                        ? (isNumeric ? aNum - bNum : aText.localeCompare(bText))
                        : (isNumeric ? bNum - aNum : bText.localeCompare(aText));
                }});

                rows.forEach(row => table.appendChild(row));
            }});
        }});
    </script>
</body>
</html>
"""
    # Save the report as an HTML file
    with open("product_comparison_report.html", "w", encoding="utf-8") as file:
        file.write(html_content)
        print("\n✅ HTML report saved as product_comparison_report.html")

if __name__ == "__main__":
    products = load_products()
    if products:
        compare_products(products)
