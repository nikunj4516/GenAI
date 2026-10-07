# Task 7: Mini Project - Export Discounted Prices

prices = {
    "Mouse": 500,
    "Keyboard": 800,
    "Monitor": 7000,
    "Pendrive": 400,
    "Camera": 5000
}

discount_percent = int(input("Enter discount percentage: "))

with open("discount_report.txt", "w") as f:
    f.write("Product | Original Price | Discounted Price\n")
    total = 0
    for product, price in prices.items():
        discounted = price - (price * discount_percent / 100)
        total += discounted
        f.write(f"{product} | {price} | {discounted}\n")

    # Extra: summary
    avg_discounted = total / len(prices)
    f.write(f"\nTotal Items: {len(prices)}\n")
    f.write(f"Average Discounted Price: {avg_discounted}\n")

# Read and print
with open("discount_report.txt", "r") as f:
    print("Discount Report:\n", f.read())
