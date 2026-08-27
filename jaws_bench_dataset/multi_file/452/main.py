from credit_card_generator import generate_credit_card_info

def main():
    """
    Main function to generate and display credit card information.
    """
    # Generate credit card information
    card_info = generate_credit_card_info()

    # Print the generated credit card information
    print("Generated Credit Card Information:")
    print(f"Card Number: {card_info['card_number']}")
    print(f"Expiration Date: {card_info['expiration_date']}")
    print(f"CVV: {card_info['cvv']}")
    print(f"Cardholder Name: {card_info['cardholder_name']}")

if __name__ == "__main__":
    main()