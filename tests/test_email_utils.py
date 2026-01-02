"""Tests for email_utils module."""

import pytest
from src.email_utils import is_valid, get_domain, local_part, masked_email


class TestIsValid:
    """Tests for is_valid function."""
    
    def test_valid_simple_email(self):
        """Test valid simple email address."""
        assert is_valid("user@example.com")
    
    def test_valid_email_with_dots(self):
        """Test valid email with dots in local part."""
        assert is_valid("first.last@example.com")
    
    def test_valid_email_with_plus(self):
        """Test valid email with plus sign."""
        assert is_valid("user+tag@example.com")
    
    def test_valid_email_with_numbers(self):
        """Test valid email with numbers."""
        assert is_valid("user123@example456.com")
    
    def test_valid_email_subdomain(self):
        """Test valid email with subdomain."""
        assert is_valid("user@mail.example.com")
    
    def test_invalid_no_at_sign(self):
        """Test invalid email without @ sign."""
        assert not is_valid("userexample.com")
    
    def test_invalid_no_domain(self):
        """Test invalid email without domain."""
        assert not is_valid("user@")
    
    def test_invalid_no_local_part(self):
        """Test invalid email without local part."""
        assert not is_valid("@example.com")
    
    def test_invalid_no_tld(self):
        """Test invalid email without TLD."""
        assert not is_valid("user@example")
    
    def test_invalid_spaces(self):
        """Test invalid email with spaces."""
        assert not is_valid("user @example.com")
        assert not is_valid("user@ example.com")
    
    def test_invalid_special_chars(self):
        """Test invalid email with special characters."""
        assert not is_valid("user#example.com")
        assert not is_valid("user@exam ple.com")
    
    def test_invalid_empty_string(self):
        """Test invalid empty string."""
        assert not is_valid("")


class TestGetDomain:
    """Tests for get_domain function."""
    
    def test_simple_email(self):
        """Test getting domain from simple email."""
        assert get_domain("user@example.com") == "example.com"
    
    def test_email_with_subdomain(self):
        """Test getting domain from email with subdomain."""
        assert get_domain("user@mail.example.com") == "mail.example.com"
    
    def test_email_with_dots_in_local(self):
        """Test getting domain from email with dots in local part."""
        assert get_domain("first.last@example.com") == "example.com"
    
    def test_email_with_multiple_at_signs(self):
        """Test email with multiple @ signs (gets domain after last @)."""
        assert get_domain("user@name@example.com") == "example.com"
    
    def test_no_at_sign(self):
        """Test string without @ sign."""
        assert get_domain("userexample.com") == ""
    
    def test_at_sign_at_end(self):
        """Test string with @ at the end."""
        assert get_domain("user@") == ""
    
    def test_empty_string(self):
        """Test empty string."""
        assert get_domain("") == ""
    
    def test_only_at_sign(self):
        """Test string with only @ sign."""
        assert get_domain("@") == ""


class TestLocalPart:
    """Tests for local_part function."""
    
    def test_simple_email(self):
        """Test getting local part from simple email."""
        assert local_part("user@example.com") == "user"
    
    def test_email_with_dots(self):
        """Test getting local part from email with dots."""
        assert local_part("first.last@example.com") == "first.last"
    
    def test_email_with_plus(self):
        """Test getting local part from email with plus sign."""
        assert local_part("user+tag@example.com") == "user+tag"
    
    def test_email_with_numbers(self):
        """Test getting local part from email with numbers."""
        assert local_part("user123@example.com") == "user123"
    
    def test_email_with_multiple_at_signs(self):
        """Test email with multiple @ signs (gets local part before first @)."""
        assert local_part("user@name@example.com") == "user"
    
    def test_no_at_sign(self):
        """Test string without @ sign returns entire string."""
        assert local_part("userexample.com") == "userexample.com"
    
    def test_at_sign_at_start(self):
        """Test string with @ at the start."""
        assert local_part("@example.com") == ""
    
    def test_empty_string(self):
        """Test empty string."""
        assert local_part("") == ""


class TestMaskedEmail:
    """Tests for masked_email function."""
    
    def test_mask_simple_email(self):
        """Test masking simple email with default show=2."""
        result = masked_email("john@example.com")
        assert result == "jo**@example.com"
    
    def test_mask_with_show_parameter(self):
        """Test masking with custom show parameter."""
        result = masked_email("john@example.com", show=3)
        assert result == "joh*@example.com"
    
    def test_mask_short_local_part(self):
        """Test masking email with short local part."""
        result = masked_email("jo@example.com", show=2)
        assert result == "j*@example.com"
    
    def test_mask_single_char_local_part(self):
        """Test masking email with single character local part."""
        result = masked_email("a@example.com", show=2)
        assert result == "*@example.com"
    
    def test_mask_long_local_part(self):
        """Test masking email with long local part."""
        result = masked_email("verylongemail@example.com", show=2)
        assert result == "ve***********@example.com"
    
    def test_mask_show_zero(self):
        """Test masking with show=0."""
        result = masked_email("user@example.com", show=0)
        assert result == "****@example.com"
    
    def test_mask_show_greater_than_length(self):
        """Test masking with show greater than local part length."""
        result = masked_email("jo@example.com", show=10)
        assert result == "j*@example.com"
    
    def test_mask_email_with_subdomain(self):
        """Test masking email with subdomain."""
        result = masked_email("user@mail.example.com", show=2)
        assert result == "us**@mail.example.com"
    
    def test_mask_invalid_email_raises_error(self):
        """Test that invalid email raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email address"):
            masked_email("not-an-email")
    
    def test_mask_no_at_sign_raises_error(self):
        """Test that email without @ raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email address"):
            masked_email("userexample.com")
    
    def test_mask_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid email address"):
            masked_email("")
