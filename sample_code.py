"""
Sample code with various issues - use this to test the analyzer.

This file demonstrates that you can create your own code and analyze it!
The tests are NOT hardcoded for what you can analyze.
"""

import os
import sys
import json  # This import is unused!


def process_user_data(user_id, name, email, phone, address, country, status, role):
    """
    This function has too many parameters!
    Try analyzing this file to see it detected.
    """
    print(sys.version)
    
    # Deep nesting - this will be flagged
    if user_id:
        if name:
            if email:
                if phone:
                    result = {
                        'id': user_id,
                        'name': name,
                        'email': email
                    }
                    return result
    
    return None
    print("This is dead code!")  # This line is unreachable!


def calculate_discount(price, discount_percent):
    """Calculate discounted price."""
    if discount_percent > 100:
        raise ValueError("Invalid discount")
        print("This will never execute")  # More dead code!
    
    return price * (1 - discount_percent / 100)


if __name__ == "__main__":
    # Test the functions
    user = process_user_data(1, "John", "john@email.com", "123", "123 St", "US", "active", "admin")
    discounted = calculate_discount(100, 10)
    print(f"User: {user}, Price: {discounted}")
