# Task 4: Apply GST using map()

prices = [100, 250, 400, 1200, 50]

# GST rate = 18%
prices_with_gst = list(map(lambda p: p + (p * 0.18), prices))

print("Original Prices:", prices)
print("Prices after GST:", prices_with_gst)
