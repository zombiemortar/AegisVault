import re
import math
from typing import Dict, List, Tuple

class PasswordStrengthAnalyzer:
    """Analyzes password strength and provides recommendations."""
    
    def __init__(self):
        # Character set sizes for entropy calculation
        self.LOWERCASE = 26
        self.UPPERCASE = 26
        self.DIGITS = 10
        self.SYMBOLS = 32  # Common symbols: !@#$%^&*()_+-=[]{}|;:,.<>?
        
    def analyze_password(self, password: str) -> Dict:
        """
        Analyzes password strength and returns comprehensive analysis.
        
        Args:
            password: The password to analyze
            
        Returns:
            Dictionary containing strength analysis
        """
        if not password:
            return self._empty_analysis()
            
        # Calculate various metrics
        length = len(password)
        entropy = self._calculate_entropy(password)
        strength_score = self._calculate_strength_score(password)
        strength_level = self._get_strength_level(strength_score)
        issues = self._identify_issues(password)
        suggestions = self._generate_suggestions(password, issues)
        
        return {
            'password': password,
            'length': length,
            'entropy': entropy,
            'strength_score': strength_score,
            'strength_level': strength_level,
            'issues': issues,
            'suggestions': suggestions,
            'character_sets': self._analyze_character_sets(password),
            'common_patterns': self._check_common_patterns(password)
        }
    
    def _calculate_entropy(self, password: str) -> float:
        """Calculate password entropy (bits of randomness)."""
        if not password:
            return 0.0
            
        # Determine character set size
        charset_size = 0
        if re.search(r'[a-z]', password):
            charset_size += self.LOWERCASE
        if re.search(r'[A-Z]', password):
            charset_size += self.UPPERCASE
        if re.search(r'\d', password):
            charset_size += self.DIGITS
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            charset_size += self.SYMBOLS
            
        # If no character sets detected, assume basic ASCII
        if charset_size == 0:
            charset_size = 95  # Basic ASCII printable characters
            
        # Calculate entropy: log2(charset_size^length)
        entropy = math.log2(charset_size ** len(password))
        return round(entropy, 2)
    
    def _calculate_strength_score(self, password: str) -> int:
        """Calculate a strength score from 0-100."""
        if not password:
            return 0
            
        score = 0
        
        # Length bonus (up to 25 points)
        if len(password) >= 8:
            score += min(25, len(password) * 2)
        
        # Character variety bonus (up to 40 points)
        if re.search(r'[a-z]', password):
            score += 8
        if re.search(r'[A-Z]', password):
            score += 8
        if re.search(r'\d', password):
            score += 8
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 16
        
        # Complexity bonus (up to 20 points)
        if len(set(password)) > len(password) * 0.7:  # Good character variety
            score += 10
        if not re.search(r'(.)\1{2,}', password):  # No repeated characters
            score += 10
        
        # Penalties
        if re.search(r'(.)\1{3,}', password):  # Heavily repeated characters
            score -= 15
        if re.search(r'(123|abc|qwe|asd|password|123456)', password.lower()):
            score -= 20  # Common patterns
        if len(password) < 6:
            score -= 10  # Too short
            
        return max(0, min(100, score))
    
    def _get_strength_level(self, score: int) -> str:
        """Convert score to strength level."""
        if score >= 80:
            return 'Very Strong'
        elif score >= 60:
            return 'Strong'
        elif score >= 40:
            return 'Moderate'
        elif score >= 20:
            return 'Weak'
        else:
            return 'Very Weak'
    
    def _identify_issues(self, password: str) -> List[str]:
        """Identify specific issues with the password."""
        issues = []
        
        if len(password) < 8:
            issues.append("Too short (minimum 8 characters recommended)")
        
        if not re.search(r'[a-z]', password):
            issues.append("Missing lowercase letters")
            
        if not re.search(r'[A-Z]', password):
            issues.append("Missing uppercase letters")
            
        if not re.search(r'\d', password):
            issues.append("Missing numbers")
            
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            issues.append("Missing special characters")
            
        if re.search(r'(.)\1{3,}', password):
            issues.append("Too many repeated characters")
            
        if re.search(r'(123|abc|qwe|asd|password|123456)', password.lower()):
            issues.append("Contains common patterns")
            
        if len(set(password)) < len(password) * 0.5:
            issues.append("Low character variety")
            
        return issues
    
    def _generate_suggestions(self, password: str, issues: List[str]) -> List[str]:
        """Generate specific suggestions for improvement."""
        suggestions = []
        
        if len(password) < 8:
            suggestions.append("Increase length to at least 8 characters")
            
        if not re.search(r'[a-z]', password):
            suggestions.append("Add lowercase letters (a-z)")
            
        if not re.search(r'[A-Z]', password):
            suggestions.append("Add uppercase letters (A-Z)")
            
        if not re.search(r'\d', password):
            suggestions.append("Add numbers (0-9)")
            
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            suggestions.append("Add special characters (!@#$%^&*)")
            
        if re.search(r'(.)\1{3,}', password):
            suggestions.append("Avoid repeating characters more than twice")
            
        if re.search(r'(123|abc|qwe|asd|password|123456)', password.lower()):
            suggestions.append("Avoid common patterns and sequences")
            
        if len(set(password)) < len(password) * 0.5:
            suggestions.append("Use more diverse characters")
            
        # Add general suggestions
        if len(password) < 12:
            suggestions.append("Consider using 12+ characters for maximum security")
            
        suggestions.append("Use a mix of random words, numbers, and symbols")
        suggestions.append("Avoid personal information (names, birthdays, etc.)")
        
        return suggestions
    
    def _analyze_character_sets(self, password: str) -> Dict[str, bool]:
        """Analyze which character sets are used."""
        return {
            'lowercase': bool(re.search(r'[a-z]', password)),
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'digits': bool(re.search(r'\d', password)),
            'symbols': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        }
    
    def _check_common_patterns(self, password: str) -> List[str]:
        """Check for common weak patterns."""
        patterns = []
        
        # Common sequences
        sequences = ['123', 'abc', 'qwe', 'asd', 'password', '123456', 'qwerty']
        for seq in sequences:
            if seq in password.lower():
                patterns.append(f"Contains '{seq}' sequence")
                
        # Repeated characters
        if re.search(r'(.)\1{3,}', password):
            patterns.append("Repeated characters")
            
        # Keyboard patterns
        keyboard_patterns = ['qwerty', 'asdfgh', 'zxcvbn']
        for pattern in keyboard_patterns:
            if pattern in password.lower():
                patterns.append("Keyboard pattern detected")
                
        return patterns
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis for empty passwords."""
        return {
            'password': '',
            'length': 0,
            'entropy': 0.0,
            'strength_score': 0,
            'strength_level': 'Very Weak',
            'issues': ['No password entered'],
            'suggestions': ['Enter a password to analyze'],
            'character_sets': {
                'lowercase': False,
                'uppercase': False,
                'digits': False,
                'symbols': False
            },
            'common_patterns': []
        }
    
    def get_strength_color(self, strength_level: str) -> str:
        """Get Bootstrap color class for strength level."""
        color_map = {
            'Very Strong': 'success',
            'Strong': 'info',
            'Moderate': 'warning',
            'Weak': 'danger',
            'Very Weak': 'danger'
        }
        return color_map.get(strength_level, 'secondary')
    
    def get_entropy_color(self, entropy: float) -> str:
        """Get color based on entropy value."""
        if entropy >= 64:
            return 'success'
        elif entropy >= 48:
            return 'info'
        elif entropy >= 32:
            return 'warning'
        else:
            return 'danger'

