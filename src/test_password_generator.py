#!/usr/bin/env python3
"""
Test script for the password generator functionality.
"""

from password_generator import PasswordGenerator

def test_password_generator():
    """Test the password generator functionality."""
    print("🔧 Testing Password Generator...")
    print("=" * 50)
    
    generator = PasswordGenerator()
    
    # Test 1: Default random password
    print("\n1. Testing default random password generation:")
    try:
        password = generator.generate_password()
        print(f"   Generated: {password}")
        print(f"   Length: {len(password)}")
        strength_info = generator.get_password_strength_info(password)
        print(f"   Strength: {strength_info['strength_level']}")
        print(f"   Entropy: {strength_info['entropy']} bits")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Custom random password
    print("\n2. Testing custom random password generation:")
    try:
        password = generator.generate_password(
            length=20,
            include_lowercase=True,
            include_uppercase=True,
            include_digits=True,
            include_symbols=False,
            avoid_similar=True,
            avoid_ambiguous=True
        )
        print(f"   Generated: {password}")
        print(f"   Length: {len(password)}")
        strength_info = generator.get_password_strength_info(password)
        print(f"   Strength: {strength_info['strength_level']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Memorable password
    print("\n3. Testing memorable password generation:")
    try:
        password = generator.generate_memorable_password(
            word_count=4,
            separator="-",
            include_numbers=True,
            include_symbols=True
        )
        print(f"   Generated: {password}")
        print(f"   Length: {len(password)}")
        strength_info = generator.get_password_strength_info(password)
        print(f"   Strength: {strength_info['strength_level']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Pronounceable password
    print("\n4. Testing pronounceable password generation:")
    try:
        password = generator.generate_pronounceable_password(
            length=12,
            include_numbers=True,
            include_symbols=True
        )
        print(f"   Generated: {password}")
        print(f"   Length: {len(password)}")
        strength_info = generator.get_password_strength_info(password)
        print(f"   Strength: {strength_info['strength_level']}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Options validation
    print("\n5. Testing options validation:")
    try:
        # Test invalid length
        errors = generator.validate_options({'length': 2})
        print(f"   Invalid length (2): {errors}")
        
        # Test no character sets
        errors = generator.validate_options({
            'include_lowercase': False,
            'include_uppercase': False,
            'include_digits': False,
            'include_symbols': False
        })
        print(f"   No character sets: {errors}")
        
        # Test valid options
        errors = generator.validate_options({
            'length': 16,
            'include_lowercase': True,
            'include_uppercase': True,
            'include_digits': True,
            'include_symbols': True
        })
        print(f"   Valid options: {errors}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 6: Get default options
    print("\n6. Testing default options:")
    try:
        options = generator.get_generator_options()
        print(f"   Default options: {options}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Password Generator Tests Completed!")

if __name__ == "__main__":
    test_password_generator()
