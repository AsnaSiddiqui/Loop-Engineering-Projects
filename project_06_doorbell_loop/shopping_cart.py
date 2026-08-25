def calculate_total(prices, discount_percent=0):
    """Calculate total price after applying a discount."""
    subtotal = sum(prices)
    discount = subtotal * (discount_percent / 100)
    return subtotal - discount

def apply_tax(amount, tax_rate=0.08):
    """Apply tax to an amount."""
    return amount * (1 + tax_rate)
