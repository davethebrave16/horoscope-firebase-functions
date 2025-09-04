"""Tests for astrological calculation functions."""

import pytest
from src.core.astro_calculations import (
    get_sign_and_decan,
    calculate_positions,
    calculate_planetary_aspects,
    moon_ascending_descending
)


class TestAstroCalculations:
    """Test cases for astrological calculations."""

    def test_get_sign_and_decan(self):
        """Test zodiac sign and decan calculation."""
        # Test Aries (0-30 degrees)
        sign, decan, degree = get_sign_and_decan(15.5)
        assert sign == "Ariete"
        assert decan == 2
        assert degree == 15.5

        # Test Taurus (30-60 degrees)
        sign, decan, degree = get_sign_and_decan(45.0)
        assert sign == "Toro"
        assert decan == 2
        assert degree == 15.0

    def test_calculate_positions_basic(self):
        """Test basic position calculation."""
        date = (2000, 1, 1)
        time = (12, 0, 0)
        latitude = 40.0
        longitude = 14.0
        
        positions = calculate_positions(date, time, latitude, longitude)
        
        # Check that all planets are present
        expected_planets = ["Sun", "Moon", "Mercury", "Venus", "Mars", 
                           "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
        for planet in expected_planets:
            assert planet in positions
            assert len(positions[planet]) == 4  # sign, decan, degree, longitude

    def test_calculate_planetary_aspects(self):
        """Test aspect calculation."""
        # Create mock positions for testing
        positions = {
            "Sun": ("Ariete", 1, 10.0, 10.0),
            "Moon": ("Ariete", 1, 15.0, 15.0),
            "Mars": ("Ariete", 1, 20.0, 20.0)
        }
        
        aspects = calculate_planetary_aspects(positions, orb=10.0)
        
        # Should find aspects between planets
        assert len(aspects) > 0
        for aspect in aspects:
            assert "planet1" in aspect
            assert "planet2" in aspect
            assert "aspect" in aspect
            assert "degrees" in aspect

    def test_moon_ascending_descending(self):
        """Test moon phase determination."""
        # Create mock positions
        positions = {
            "Moon": ("Ariete", 1, 10.0, 10.0),
            "Ascendant": ("Ariete", 1, 5.0, 5.0),
            "Descendant": ("Bilancia", 1, 5.0, 185.0)
        }
        
        result = moon_ascending_descending(positions)
        assert "ascending" in result.lower() or "descending" in result.lower()
