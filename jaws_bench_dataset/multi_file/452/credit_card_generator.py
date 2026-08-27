import random
from faker import Faker

# Initialize Faker to generate fake data
fake = Faker()

def generate_random_number(length):
    <FILL_HERE>
def generate_credit_card_number():
    """
    Generate a random credit card number.
    
    :return: A string representing the credit card number
    """
    # Example format: 4xxxxxxxxxxxxxxx (Visa)
    return '4' + generate_random_number(15)

def generate_expiration_date():
    """
    Generate a random expiration date for the credit card.
    
    :return: A string representing the expiration date in MM/YY format
    """
    month = random.randint(1, 12)
    year = random.randint(2024, 2030)
    return f"{month:02d}/{year % 100:02d}"

def generate_cvv():
    """
    Generate a random CVV number.
    
    :return: A string representing the CVV number
    """
    return generate_random_number(3)

def generate_credit_card_info():
    """
    Generate a dictionary containing fake credit card information.
    
    :return: A dictionary with credit card details
    """
    return {
        "card_number": generate_credit_card_number(),
        "expiration_date": generate_expiration_date(),
        "cvv": generate_cvv(),
        "cardholder_name": fake.name()
    }

if __name__ == "__main__":
    # Generate and print a sample credit card information
    card_info = generate_credit_card_info()
    print(card_info)