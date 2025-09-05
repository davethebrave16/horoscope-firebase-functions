"""Tests for astrological calculation functions."""

import pytest
from src.core.astro_calculations import (
    get_sign_and_decan,
    calculate_positions,
    calculate_planetary_aspects,
    moon_ascending_descending,
    calculate_planetary_transits,
    Transit
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

    def test_calculate_planetary_transits_basic(self):
        """Test basic planetary transits calculation."""
        # Test with Sun for a specific month (fewer transits than Moon)
        transits = calculate_planetary_transits(
            year=2025,
            month=10,
            lat=41.9028,  # Rome
            lon=12.4964,
            tz_offset_hours=2.0,
            planet_name="Sun",
            step_minutes=60  # Larger step for faster test
        )
        
        # Should return a list of Transit objects
        assert isinstance(transits, list)
        assert len(transits) > 0
        
        # Check first transit structure
        first_transit = transits[0]
        assert isinstance(first_transit, Transit)
        assert first_transit.planet == "Sun"
        assert first_transit.angle in ["Ascendant", "Descendant", "Midheaven", "Imum Coeli"]
        assert hasattr(first_transit, 'datetime_local')
        assert hasattr(first_transit, 'longitude')
        assert hasattr(first_transit, 'sign')
        assert hasattr(first_transit, 'degree_in_sign')
        assert hasattr(first_transit, 'decan')

    def test_calculate_planetary_transits_invalid_planet(self):
        """Test transits calculation with invalid planet."""
        with pytest.raises(ValueError, match="Planet .* not supported"):
            calculate_planetary_transits(
                year=2025,
                month=10,
                lat=41.9028,
                lon=12.4964,
                tz_offset_hours=2.0,
                planet_name="InvalidPlanet"
            )

    def test_calculate_planetary_transits_moon(self):
        """Test Moon transits (should have many transits)."""
        transits = calculate_planetary_transits(
            year=2025,
            month=10,
            lat=41.9028,
            lon=12.4964,
            tz_offset_hours=2.0,
            planet_name="Moon",
            step_minutes=30  # Medium step
        )
        
        # Moon should have many transits (multiple per day)
        assert len(transits) > 50
        
        # All transits should be for Moon
        for transit in transits:
            assert transit.planet == "Moon"
            assert transit.angle in ["Ascendant", "Descendant", "Midheaven", "Imum Coeli"]

    def test_calculate_planetary_transits_different_locations(self):
        """Test transits calculation for different locations."""
        # Test Rome
        transits_rome = calculate_planetary_transits(
            year=2025,
            month=10,
            lat=41.9028,
            lon=12.4964,
            tz_offset_hours=2.0,
            planet_name="Sun",
            step_minutes=60
        )
        
        # Test New York
        transits_ny = calculate_planetary_transits(
            year=2025,
            month=10,
            lat=40.7128,
            lon=-74.0060,
            tz_offset_hours=-5.0,
            planet_name="Sun",
            step_minutes=60
        )
        
        # Both should return transits but with different times
        assert len(transits_rome) > 0
        assert len(transits_ny) > 0
        
        # Times should be different due to different locations
        assert transits_rome[0].datetime_local != transits_ny[0].datetime_local

    def test_calculate_planetary_transits_transit_structure(self):
        """Test that transit objects have correct structure and data types."""
        transits = calculate_planetary_transits(
            year=2025,
            month=10,
            lat=41.9028,
            lon=12.4964,
            tz_offset_hours=2.0,
            planet_name="Sun",
            step_minutes=60
        )
        
        if transits:  # Only test if we have transits
            transit = transits[0]
            
            # Check data types
            assert isinstance(transit.planet, str)
            assert isinstance(transit.angle, str)
            assert hasattr(transit.datetime_local, 'year')  # datetime object
            assert isinstance(transit.longitude, float)
            assert isinstance(transit.sign, str)
            assert isinstance(transit.degree_in_sign, float)
            assert isinstance(transit.decan, int)
            
            # Check value ranges
            assert 0 <= transit.longitude < 360
            assert 0 <= transit.degree_in_sign < 30
            assert transit.decan in [1, 2, 3]
            assert transit.angle in ["Ascendant", "Descendant", "Midheaven", "Imum Coeli"]
