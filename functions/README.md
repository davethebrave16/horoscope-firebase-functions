# Horoscope Firebase Functions

A modular Firebase Functions application for astrological calculations using Swiss Ephemeris.

## Project Structure

```
functions/
├── main.py                 # Entry point - imports all functions
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── src/
│   ├── api/               # API endpoint modules
│   │   ├── __init__.py
│   │   ├── horoscope.py   # calculate_horoscope function
│   │   ├── aspects.py     # calculate_aspects function
│   │   └── moon_phase.py  # moon_phase function
│   ├── core/              # Core business logic
│   │   ├── __init__.py
│   │   ├── config.py      # Configuration constants
│   │   ├── astro_calculations.py  # Astrological calculations
│   │   └── validation.py  # Request validation
│   └── utils/             # Utility modules
│       ├── __init__.py
│       └── response_utils.py  # Response formatting
└── tests/                 # Test modules
    ├── __init__.py
    └── test_astro_calculations.py
```

## API Endpoints

### 1. Calculate Horoscope
- **Function**: `calculate_horoscope`
- **Method**: POST
- **Purpose**: Calculate planetary and house positions

### 2. Calculate Aspects
- **Function**: `calculate_aspects`
- **Method**: POST
- **Purpose**: Calculate aspects between planets and houses

### 3. Moon Phase
- **Function**: `moon_phase`
- **Method**: POST
- **Purpose**: Determine if Moon is ascending or descending

## Development

### Setup
1. Install dependencies:
   ```bash
   cd functions
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. Set environment variables:
   ```bash
   export API_KEY="your-api-key-here"
   ```

### Testing
```bash
cd functions
pytest tests/
```

### Local Development
```bash
firebase emulators:start --only functions
```

### Deployment
```bash
firebase deploy --only functions
```

## Configuration

All configuration constants are centralized in `src/core/config.py`:
- CORS headers
- Zodiac signs
- Aspect definitions
- Default values
- Firebase region

## Security

- API key authentication required for all endpoints
- Input validation on all requests
- CORS headers configured for web access
- Environment variables for sensitive data
