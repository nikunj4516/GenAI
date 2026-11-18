
import pandas as pd

# Create our own raw text dataset
data = {
    "id": list(range(1, 26)),
    "text": [
        "THIS PHONE IS AMAZING!!! I LOVE IT 😍",
        "The battery lasts for 24 hours. Very useful!",
        "   Great   product   with   excellent   quality   ",
        "Sooooo good!!! I really like this mobile.",
        "Visit www.example.com for more details.",
        "Contact us at abc@gmail.com for support.",
        "<p>This laptop is very fast and powerful.</p>",
        "I bought this phone for 15000 rupees!!!",
        "gr8 product, u should buy it.",
        "The headphones are AMAZING 🔥🔥🔥",
        "Worst product ever!!! Very disappointed.",
        "Battery life is not good... I hate it.",
        "This mobile has 8GB RAM and 128GB storage.",
        "Check this offer https://shop.example.com now!",
        "The camera quality is sooo good 😍",
        "I am not satisfied with this product!!!",
        "Delivery was fast, and packaging was excellent.",
        "OMG!!! This laptop is superrrrr fast.",
        "Please email support@shop.com for help.",
        "<div>Excellent service and good customer support</div>",
        "The price is 25000 but quality is average.",
        "u are providing a gr8 service. Thank you!",
        "I received my order yesterday... Very happy!",
        "THIS IS THE WORST PURCHASE OF MY LIFE 😡",
        "Good product!!!     Affordable price.   "
    ]
}

# Convert dictionary into DataFrame
df = pd.DataFrame(data)

# Display first 5 records
print(df.head())

# Display dataset information
print("\nDataset Information:")
print(df.info())

# Check dataset shape
print("\nDataset Shape:", df.shape)

# Save dataset as CSV
df.to_csv("product_reviews_dataset.csv", index=False)

print("\nDataset created and saved successfully!")
