"""Price calculation."""


def calculate_total_price(
    price: float, quantity: int, discount_percent: float = 0
) -> float:
    """
    Calculate total price with optional discount.

    Args:
        price: Unit price
        quantity: Number of items
        discount_percent: Discount percentage (0-100)

    Returns:
        Total price after discount

    Raises:
        ValueError: if price or quantity is negative, or the discount is
            outside the 0-100 range.
    """
    if price < 0 or quantity < 0:
        raise ValueError("Price and quantity must be non-negative")

    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")

    subtotal = price * quantity
    discount_amount = subtotal * (discount_percent / 100)
    return subtotal - discount_amount
