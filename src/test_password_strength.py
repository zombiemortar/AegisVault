#!/usr/bin/env python3
"""
Test script for Password Strength Analyzer
"""

from password_strength import PasswordStrengthAnalyzer

def test_password_analyzer():
    """Test various password scenarios."""
    analyzer = PasswordStrengthAnalyzer()
    
    # Test passwords with different strength levels
    test_passwords = [
        "",  # Empty password
        "123",  # Very weak
        "password",  # Weak
        "Password123",  # Moderate
        "SecurePass123!",  # Strong
        "K9#mP$2vL@8nQ&5wR",  # Very strong
        "qwerty123",  # Common pattern
        "aaa",  # Repeated characters
        "MySecurePassword2024!",  # Strong with symbols
    ]
    
    print("🔐 Password Strength Analysis Test Results\n")
    print("=" * 60)
    
    for password in test_passwords:
        print(f"\n📝 Password: '{password}'")
        analysis = analyzer.analyze_password(password)
        
        print(f"   Length: {analysis['length']}")
        print(f"   Entropy: {analysis['entropy']} bits")
        print(f"   Score: {analysis['strength_score']}/100")
        print(f"   Level: {analysis['strength_level']}")
        
        # Character sets
        char_sets = analysis['character_sets']
        print(f"   Character Sets: ", end="")
        if char_sets['lowercase']: print("a-z ", end="")
        if char_sets['uppercase']: print("A-Z ", end="")
        if char_sets['digits']: print("0-9 ", end="")
        if char_sets['symbols']: print("!@# ", end="")
        print()
        
        # Issues
        if analysis['issues']:
            print(f"   Issues:")
            for issue in analysis['issues']:
                print(f"     ❌ {issue}")
        
        # Suggestions
        if analysis['suggestions']:
            print(f"   Suggestions:")
            for suggestion in analysis['suggestions']:
                print(f"     💡 {suggestion}")
        
        print("-" * 40)

def test_edge_cases():
    """Test edge cases and special characters."""
    analyzer = PasswordStrengthAnalyzer()
    
    print("\n🧪 Edge Cases and Special Characters Test\n")
    print("=" * 60)
    
    edge_passwords = [
        "a" * 50,  # Very long with single character
        "ab" * 25,  # Long with pattern
        "!@#$%^&*()",  # Only symbols
        "1234567890",  # Only digits
        "abcdefghij",  # Only lowercase
        "ABCDEFGHIJ",  # Only uppercase
        "P@ssw0rd!",  # Common but with substitutions
        "Tr0ub4dor&3",  # XKCD style
        "correct horse battery staple",  # Passphrase
    ]
    
    for password in edge_passwords:
        print(f"\n🔍 Testing: '{password[:30]}{'...' if len(password) > 30 else ''}'")
        analysis = analyzer.analyze_password(password)
        
        print(f"   Length: {analysis['length']}")
        print(f"   Entropy: {analysis['entropy']} bits")
        print(f"   Score: {analysis['strength_score']}/100")
        print(f"   Level: {analysis['strength_level']}")
        
        if analysis['common_patterns']:
            print(f"   Patterns: {', '.join(analysis['common_patterns'])}")

if __name__ == "__main__":
    print("🚀 Starting Password Strength Analyzer Tests...\n")
    
    try:
        test_password_analyzer()
        test_edge_cases()
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

