# Horoscope Firebase Functions

Firebase Functions for calculating astrological positions, aspects, and moon phases using Swiss Ephemeris.

## Features

- **Planetary Positions**: Calculate positions of all major planets (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto)
- **House System**: Calculate Ascendant, Descendant, Midheaven, and Imum Coeli positions
- **Aspect Analysis**: Calculate planetary aspects with configurable orb tolerance
- **Moon Phase Detection**: Determine if the Moon is in ascending or descending phase
- **CORS Support**: Full CORS headers for web application integration
- **Error Handling**: Comprehensive validation and error responses

## Setup

1. Install Firebase CLI:
```bash
npm install -g firebase-tools
```

2. Login to Firebase:
```bash
firebase login
```

3. Initialize the project:
```bash
firebase init functions
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Local Development

Run the Firebase emulator:
```bash
firebase emulators:start --only functions
```

The functions will be available at:
```
http://localhost:5001/YOUR_PROJECT_ID/us-central1/calculate_horoscope
http://localhost:5001/YOUR_PROJECT_ID/us-central1/calculate_aspects
http://localhost:5001/YOUR_PROJECT_ID/us-central1/moon_phase
```

## API Endpoints

### POST /calculate_horoscope

Calculate planetary and house positions for a given birth data.

**Request Body:**
```json
{
  "date": [1990, 5, 15],
  "time": [14, 30, 0],
  "latitude": 41.9028,
  "longitude": 12.4964,
  "timezone_offset_hours": 1.0
}
```

**Response:**
```json
{
  "success": true,
  "horoscope": {
    "planets": {
      "Sun": {
        "sign": "Toro",
        "decan": 1,
        "degree_in_sign": 25.5,
        "absolute_longitude": 55.5
      },
      "Moon": {
        "sign": "Gemelli",
        "decan": 2,
        "degree_in_sign": 15.2,
        "absolute_longitude": 75.2
      }
    },
    "houses": {
      "Ascendant": {
        "sign": "Ariete",
        "decan": 1,
        "degree_in_sign": 12.3,
        "absolute_longitude": 12.3
      }
    }
  },
  "birth_data": {
    "date": {"year": 1990, "month": 5, "day": 15},
    "time": {"hour": 14, "minute": 30, "second": 0},
    "location": {
      "latitude": 41.9028,
      "longitude": 12.4964,
      "timezone_offset_hours": 1.0
    }
  }
}
```

### POST /calculate_aspects

Calculate aspects between planets and houses.

**Request Body:**
```json
{
  "date": [1990, 5, 15],
  "time": [14, 30, 0],
  "latitude": 41.9028,
  "longitude": 12.4964,
  "timezone_offset_hours": 1.0,
  "orb": 6.0
}
```

**Response:**
```json
{
  "success": true,
  "aspects": [
    {
      "planet1": "Sun",
      "planet2": "Moon",
      "aspect": "Trine",
      "degrees": 120.0,
      "orb": 2.5
    }
  ],
  "aspect_count": 1,
  "orb_used": 6.0,
  "birth_data": {
    "date": {"year": 1990, "month": 5, "day": 15},
    "time": {"hour": 14, "minute": 30, "second": 0},
    "location": {
      "latitude": 41.9028,
      "longitude": 12.4964,
      "timezone_offset_hours": 1.0
    }
  }
}
```

### POST /moon_phase

Determine if the Moon is in ascending or descending phase.

**Request Body:**
```json
{
  "date": [1990, 5, 15],
  "time": [14, 30, 0],
  "latitude": 41.9028,
  "longitude": 12.4964,
  "timezone_offset_hours": 1.0
}
```

**Response:**
```json
{
  "success": true,
  "moon_phase": "The Moon is in ascending phase (from Asc to Dsc).",
  "moon_position": {
    "sign": "Gemelli",
    "decan": 2,
    "degree_in_sign": 15.2,
    "absolute_longitude": 75.2
  },
  "reference_points": {
    "ascendant_longitude": 12.3,
    "descendant_longitude": 192.3
  },
  "birth_data": {
    "date": {"year": 1990, "month": 5, "day": 15},
    "time": {"hour": 14, "minute": 30, "second": 0},
    "location": {
      "latitude": 41.9028,
      "longitude": 12.4964,
      "timezone_offset_hours": 1.0
    }
  }
}
```

## Data Format

### Birth Data Parameters

- **date**: Array `[year, month, day]` (required)
- **time**: Array `[hour, minute, second]` (required)
- **latitude**: Float in degrees (required)
- **longitude**: Float in degrees (required)
- **timezone_offset_hours**: Float offset from UTC in hours (optional, defaults to 0)

### Position Format

Each position contains:
- **sign**: Zodiac sign name in Italian
- **decan**: Decan number (1, 2, or 3)
- **degree_in_sign**: Degree within the sign (0-30)
- **absolute_longitude**: Absolute ecliptic longitude

### Supported Aspects

- **Conjunction**: 0°
- **Sextile**: 60°
- **Square**: 90°
- **Trine**: 120°
- **Opposition**: 180°

### Zodiac Signs (Italian)

Ariete, Toro, Gemelli, Cancro, Leone, Vergine, Bilancia, Scorpione, Sagittario, Capricorno, Acquario, Pesci

## Error Handling

All endpoints return standardized error responses:

```json
{
  "error": "Error message description"
}
```

Common error scenarios:
- Missing required fields
- Invalid data format
- Method not allowed (only POST supported)
- Internal server errors

## Deployment

Deploy to Firebase:
```bash
firebase deploy --only functions
```

## Dependencies

- `pyswisseph==2.10.3.2`: Swiss Ephemeris library for astronomical calculations
- `firebase-functions==0.1.0`: Firebase Functions framework
- `firebase-admin==6.*`: Firebase Admin SDK
- `functions-framework==3.*`: Functions framework for local development

## API Testing

Bruno API collection files are included in the `api_docs/` directory for testing all endpoints locally.
