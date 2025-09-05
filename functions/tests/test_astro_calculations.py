"""Tests for astrological calculation functions."""

import pytest
from src.core.astro_calculations import (
    get_sign_and_decan,
    calculate_positions,
    calculate_planetary_aspects,
    calculate_planetary_transits,
    calculate_lenormand_card,
    to_julian_date,
    calculate_moon_phase,
    Transit
)


class TestAstroCalculations:
    """Test cases for astrological calculations."""

    def test_get_sign_and_decan(self):
        """Test zodiac sign and decan calculation."""
        # Test Aries (0-30 degrees)
        sign, decan, degree = get_sign_and_decan(15.5)
        assert sign == "Aries"
        assert decan == 2
        assert degree == 15.5

        # Test Taurus (30-60 degrees)
        sign, decan, degree = get_sign_and_decan(45.0)
        assert sign == "Taurus"
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
            "Sun": ("Aries", 1, 10.0, 10.0),
            "Moon": ("Aries", 1, 15.0, 15.0),
            "Mars": ("Aries", 1, 20.0, 20.0)
        }
        
        aspects = calculate_planetary_aspects(positions, orb=10.0)
        
        # Should find aspects between planets
        assert len(aspects) > 0
        for aspect in aspects:
            assert "planet1" in aspect
            assert "planet2" in aspect
            assert "aspect" in aspect
            assert "degrees" in aspect


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

    def test_calculate_lenormand_card(self):
        """Test Lenormand card calculation based on Moon's sign and decan."""
        # Test valid combinations
        assert calculate_lenormand_card("Aries", 1) == "Rider"
        assert calculate_lenormand_card("Aries", 2) == "Clover"
        assert calculate_lenormand_card("Aries", 3) == "Ship"
        
        assert calculate_lenormand_card("Taurus", 1) == "House"
        assert calculate_lenormand_card("Taurus", 2) == "Tree"
        assert calculate_lenormand_card("Taurus", 3) == "Clouds"
        
        assert calculate_lenormand_card("Pisces", 1) == "Fish"
        assert calculate_lenormand_card("Pisces", 2) == "Anchor"
        assert calculate_lenormand_card("Pisces", 3) == "Cross"
        
        # Test invalid combinations
        assert calculate_lenormand_card("InvalidSign", 1) == "Unknown"
        assert calculate_lenormand_card("Aries", 4) == "Unknown"
        assert calculate_lenormand_card("Aries", 0) == "Unknown"

    def test_to_julian_date(self):
        """Test Julian date conversion."""
        # Test known date: January 1, 2000 12:00:00 UTC
        jd = to_julian_date(2000, 1, 1, 12, 0, 0)
        assert isinstance(jd, float)
        assert jd > 2451544  # Should be around 2451545 for Jan 1, 2000
        
        # Test without time (should default to 00:00:00)
        jd_midnight = to_julian_date(2000, 1, 1)
        assert jd_midnight < jd  # Midnight should be earlier than noon
        
        # Test different dates
        jd_2025 = to_julian_date(2025, 9, 5, 22, 30, 0)
        assert jd_2025 > jd  # 2025 should be later than 2000

    def test_calculate_moon_phase_basic(self):
        """Test basic moon phase calculation."""
        # Test with a known date
        result = calculate_moon_phase(2025, 9, 5, 22, 30, 0)
        
        # Check structure
        assert isinstance(result, dict)
        assert "phase_name" in result
        assert "age_days" in result
        assert "fraction_of_cycle" in result
        assert "illuminated_fraction" in result
        assert "julian_date" in result
        
        # Check data types
        assert isinstance(result["phase_name"], str)
        assert isinstance(result["age_days"], float)
        assert isinstance(result["fraction_of_cycle"], float)
        assert isinstance(result["illuminated_fraction"], float)
        assert isinstance(result["julian_date"], float)
        
        # Check value ranges
        assert 0 <= result["age_days"] <= 29.6  # Moon cycle is ~29.5 days
        assert 0 <= result["fraction_of_cycle"] <= 1
        assert 0 <= result["illuminated_fraction"] <= 1
        assert result["julian_date"] > 0

    def test_calculate_moon_phase_phase_names(self):
        """Test that moon phase names are valid."""
        # Test different dates to get different phases
        test_dates = [
            (2025, 1, 1, 0, 0, 0),
            (2025, 6, 15, 12, 0, 0),
            (2025, 12, 31, 23, 59, 59)
        ]
        
        valid_phases = [
            "New Moon", "Waxing Crescent", "First Quarter", 
            "Waxing Gibbous", "Full Moon", "Waning Gibbous", 
            "Last Quarter", "Waning Crescent"
        ]
        
        for year, month, day, hour, minute, second in test_dates:
            result = calculate_moon_phase(year, month, day, hour, minute, second)
            assert result["phase_name"] in valid_phases

    def test_calculate_moon_phase_consistency(self):
        """Test that moon phase calculation is consistent."""
        # Same date should give same result
        result1 = calculate_moon_phase(2025, 9, 5, 22, 30, 0)
        result2 = calculate_moon_phase(2025, 9, 5, 22, 30, 0)
        
        assert result1["phase_name"] == result2["phase_name"]
        assert result1["age_days"] == result2["age_days"]
        assert result1["fraction_of_cycle"] == result2["fraction_of_cycle"]
        assert result1["illuminated_fraction"] == result2["illuminated_fraction"]

    def test_calculate_moon_phase_time_progression(self):
        """Test that moon phase changes over time."""
        # Test progression over several days
        base_date = (2025, 9, 5, 12, 0, 0)
        results = []
        
        for day_offset in range(5):
            year, month, day, hour, minute, second = base_date
            day += day_offset
            result = calculate_moon_phase(year, month, day, hour, minute, second)
            results.append(result)
        
        # Age should increase over time
        for i in range(1, len(results)):
            assert results[i]["age_days"] >= results[i-1]["age_days"]
        
        # Fraction of cycle should generally increase (with wraparound)
        for i in range(1, len(results)):
            # Allow for wraparound at cycle end
            frac_diff = results[i]["fraction_of_cycle"] - results[i-1]["fraction_of_cycle"]
            assert frac_diff >= -0.1  # Allow small negative due to wraparound
