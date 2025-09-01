import secrets
import string
import re
from typing import Dict, List, Optional

class PasswordGenerator:
    """Secure password generator with customizable options."""
    
    def __init__(self):
        # Character sets
        self.LOWERCASE = string.ascii_lowercase
        self.UPPERCASE = string.ascii_uppercase
        self.DIGITS = string.digits
        self.SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Default settings
        self.default_length = 16
        self.default_include_lowercase = True
        self.default_include_uppercase = True
        self.default_include_digits = True
        self.default_include_symbols = True
        self.default_avoid_similar = True
        self.default_avoid_ambiguous = True
    
    def generate_password(self, 
                         length: int = None,
                         include_lowercase: bool = None,
                         include_uppercase: bool = None,
                         include_digits: bool = None,
                         include_symbols: bool = None,
                         avoid_similar: bool = None,
                         avoid_ambiguous: bool = None) -> str:
        """
        Generate a secure password with specified options.
        
        Args:
            length: Password length (default: 16)
            include_lowercase: Include lowercase letters (default: True)
            include_uppercase: Include uppercase letters (default: True)
            include_digits: Include digits (default: True)
            include_symbols: Include symbols (default: True)
            avoid_similar: Avoid similar characters like l, 1, I, O, 0 (default: True)
            avoid_ambiguous: Avoid ambiguous characters like braces, brackets, pipe, backslash, slash (default: True)
            
        Returns:
            Generated password string
        """
        # Use defaults if not specified
        length = length or self.default_length
        include_lowercase = include_lowercase if include_lowercase is not None else self.default_include_lowercase
        include_uppercase = include_uppercase if include_uppercase is not None else self.default_include_uppercase
        include_digits = include_digits if include_digits is not None else self.default_include_digits
        include_symbols = include_symbols if include_symbols is not None else self.default_include_symbols
        avoid_similar = avoid_similar if avoid_similar is not None else self.default_avoid_similar
        avoid_ambiguous = avoid_ambiguous if avoid_ambiguous is not None else self.default_avoid_ambiguous
        
        # Build character pool
        char_pool = ""
        
        if include_lowercase:
            char_pool += self.LOWERCASE
        if include_uppercase:
            char_pool += self.UPPERCASE
        if include_digits:
            char_pool += self.DIGITS
        if include_symbols:
            char_pool += self.SYMBOLS
        
        # Remove similar characters if requested
        if avoid_similar:
            similar_chars = "l1I|O0"
            char_pool = ''.join(c for c in char_pool if c not in similar_chars)
        
        # Remove ambiguous characters if requested
        if avoid_ambiguous:
            ambiguous_chars = "{}[]|\\/"
            char_pool = ''.join(c for c in char_pool if c not in ambiguous_chars)
        
        # Ensure we have at least one character from each selected set
        required_chars = []
        if include_lowercase:
            required_chars.append(secrets.choice(self.LOWERCASE))
        if include_uppercase:
            required_chars.append(secrets.choice(self.UPPERCASE))
        if include_digits:
            required_chars.append(secrets.choice(self.DIGITS))
        if include_symbols:
            required_chars.append(secrets.choice(self.SYMBOLS))
        
        # Generate the password
        if len(char_pool) == 0:
            raise ValueError("No character sets selected for password generation")
        
        # Generate random characters for the remaining length
        remaining_length = length - len(required_chars)
        if remaining_length < 0:
            raise ValueError(f"Length {length} is too short for the required character sets")
        
        random_chars = ''.join(secrets.choice(char_pool) for _ in range(remaining_length))
        
        # Combine required and random characters, then shuffle
        password_chars = required_chars + list(random_chars)
        password = ''.join(secrets.SystemRandom().sample(password_chars, len(password_chars)))
        
        return password
    
    def generate_memorable_password(self, 
                                   word_count: int = 4,
                                   separator: str = "-",
                                   include_numbers: bool = True,
                                   include_symbols: bool = True) -> str:
        """
        Generate a memorable password using word-based approach.
        
        Args:
            word_count: Number of words to use (default: 4)
            separator: Character to separate words (default: "-")
            include_numbers: Add random numbers (default: True)
            include_symbols: Add random symbols (default: True)
            
        Returns:
            Memorable password string
        """
        # Common words for memorable passwords (you could expand this list)
        words = [
            "apple", "banana", "cherry", "dragon", "eagle", "forest", "garden", "house",
            "island", "jungle", "knight", "lemon", "mountain", "ocean", "planet", "queen",
            "river", "star", "tiger", "umbrella", "village", "water", "xenon", "yellow",
            "zebra", "alpha", "beta", "gamma", "delta", "echo", "foxtrot", "golf",
            "hotel", "india", "juliet", "kilo", "lima", "mike", "november", "oscar",
            "papa", "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey",
            "xray", "yankee", "zulu"
        ]
        
        # Select random words
        selected_words = [secrets.choice(words) for _ in range(word_count)]
        
        # Capitalize some words randomly
        for i in range(len(selected_words)):
            if secrets.choice([True, False]):
                selected_words[i] = selected_words[i].capitalize()
        
        # Join words with separator
        password = separator.join(selected_words)
        
        # Add numbers if requested
        if include_numbers:
            password += str(secrets.randbelow(100))
        
        # Add symbols if requested
        if include_symbols:
            password += secrets.choice("!@#$%^&*")
        
        return password
    
    def generate_pronounceable_password(self, 
                                      length: int = 12,
                                      include_numbers: bool = True,
                                      include_symbols: bool = True) -> str:
        """
        Generate a pronounceable password using consonant-vowel patterns.
        
        Args:
            length: Password length (default: 12)
            include_numbers: Add random numbers (default: True)
            include_symbols: Add random symbols (default: True)
            
        Returns:
            Pronounceable password string
        """
        consonants = "bcdfghjklmnpqrstvwxz"
        vowels = "aeiouy"
        
        password = ""
        for i in range(length):
            if i % 2 == 0:  # Even positions get consonants
                password += secrets.choice(consonants)
            else:  # Odd positions get vowels
                password += secrets.choice(vowels)
        
        # Capitalize some letters randomly
        password_chars = list(password)
        for i in range(len(password_chars)):
            if secrets.choice([True, False]):
                password_chars[i] = password_chars[i].upper()
        password = ''.join(password_chars)
        
        # Add numbers if requested
        if include_numbers:
            password += str(secrets.randbelow(100))
        
        # Add symbols if requested
        if include_symbols:
            password += secrets.choice("!@#$%^&*")
        
        return password
    
    def get_generator_options(self) -> Dict:
        """Get default generator options."""
        return {
            'length': self.default_length,
            'include_lowercase': self.default_include_lowercase,
            'include_uppercase': self.default_include_uppercase,
            'include_digits': self.default_include_digits,
            'include_symbols': self.default_include_symbols,
            'avoid_similar': self.default_avoid_similar,
            'avoid_ambiguous': self.default_avoid_ambiguous
        }
    
    def validate_options(self, options: Dict) -> List[str]:
        """
        Validate generator options and return list of errors.
        
        Args:
            options: Dictionary of generator options
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        length = options.get('length', 16)
        if not isinstance(length, int) or length < 4:
            errors.append("Password length must be at least 4 characters")
        elif length > 128:
            errors.append("Password length cannot exceed 128 characters")
        
        # Check that at least one character set is selected
        char_sets = [
            options.get('include_lowercase', True),
            options.get('include_uppercase', True),
            options.get('include_digits', True),
            options.get('include_symbols', True)
        ]
        
        if not any(char_sets):
            errors.append("At least one character set must be selected")
        
        return errors
    
    def get_password_strength_info(self, password: str) -> Dict:
        """
        Get strength information for a generated password.
        
        Args:
            password: The password to analyze
            
        Returns:
            Dictionary with strength information
        """
        length = len(password)
        char_sets_used = {
            'lowercase': bool(re.search(r'[a-z]', password)),
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'digits': bool(re.search(r'\d', password)),
            'symbols': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        }
        
        # Calculate entropy
        charset_size = sum(char_sets_used.values()) * 26  # Approximate
        if charset_size == 0:
            charset_size = 95  # Basic ASCII
        entropy = length * (2 ** charset_size).bit_length()
        
        return {
            'length': length,
            'entropy': entropy,
            'character_sets': char_sets_used,
            'strength_level': self._get_strength_level(length, entropy, char_sets_used)
        }
    
    def _get_strength_level(self, length: int, entropy: float, char_sets: Dict) -> str:
        """Determine password strength level."""
        char_set_count = sum(char_sets.values())
        
        if length >= 16 and char_set_count >= 4 and entropy >= 64:
            return "Very Strong"
        elif length >= 12 and char_set_count >= 3 and entropy >= 48:
            return "Strong"
        elif length >= 8 and char_set_count >= 2 and entropy >= 32:
            return "Moderate"
        elif length >= 6:
            return "Weak"
        else:
            return "Very Weak"
