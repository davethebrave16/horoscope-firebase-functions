# Horoscope Firebase Functions

A modular Firebase Functions application for calculating astrological positions, aspects, and moon phases using Swiss Ephemeris.

## 🏗️ Project Structure

```
.
├── functions/                    # Firebase Functions directory
│   ├── main.py                  # Entry point (imports all functions)
│   ├── requirements.txt         # Production dependencies
│   ├── requirements-dev.txt     # Development dependencies
│   ├── README.md               # Detailed functions documentation
│   ├── src/
│   │   ├── api/                # API endpoints
│   │   │   ├── horoscope.py    # calculate_horoscope function
│   │   │   ├── aspects.py      # calculate_aspects function
│   │   │   ├── moon_phase.py   # moon_phase function
│   │   │   └── transits.py     # planetary_transits function
│   │   ├── core/               # Business logic
│   │   │   ├── config.py       # Configuration constants
│   │   │   ├── astro_calculations.py  # Pure astro logic
│   │   │   └── validation.py   # Request validation
│   │   └── utils/              # Utilities
│   │       └── response_utils.py  # Response formatting
│   └── tests/                  # Test modules
│       └── test_astro_calculations.py
├── api_docs/                   # Bruno API collection for testing
├── firebase.json              # Firebase configuration
└── README.md                  # This file
```

## ✨ Features

- **Planetary Positions**: Calculate positions of all major planets (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto)
- **House System**: Calculate Ascendant, Descendant, Midheaven, and Imum Coeli positions
- **Aspect Analysis**: Calculate planetary aspects with configurable orb tolerance
- **Moon Phase Detection**: Determine if the Moon is in ascending or descending phase
- **Planetary Transits**: Calculate when planets pass over cardinal points during a month
- **CORS Support**: Full CORS headers for web application integration
- **Error Handling**: Comprehensive validation and error responses
- **Modular Architecture**: Clean separation of concerns, easy to maintain and extend

## 🚀 Quick Start

### Prerequisites

1. **Firebase CLI**:
   ```bash
   npm install -g firebase-tools
   ```

2. **Python 3.12+**:
   ```bash
   python3.12 --version
   ```

### Setup

1. **Login to Firebase**:
   ```bash
   firebase login
   ```

2. **Set up environment variables**:
   ```bash
   echo 'API_KEY=your-api-key-here' > functions/.env
   ```

3. **Install dependencies**:
   ```bash
   cd functions
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Local Development

1. **Start the emulator**:
   ```bash
   cd functions
   firebase emulators:start --only functions
   ```

2. **Test the functions**:
   - Functions UI: http://127.0.0.1:4000/functions
   - Functions endpoint: http://127.0.0.1:5001
   - Use Bruno collection in `api_docs/` for testing

### Deployment

```bash
cd functions
firebase deploy --only functions
```

## 📡 API Endpoints

All endpoints require `Authorization` header with your API key.

### POST /calculate_horoscope

Calculate planetary and house positions for given birth data.

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

### POST /planetary_transits

Calculate when planets pass over cardinal points (Ascendant, Descendant, Midheaven, Imum Coeli) during a specified month.

**Request Body:**
```json
{
  "year": 2025,
  "month": 10,
  "latitude": 41.9028,
  "longitude": 12.4964,
  "timezone_offset_hours": 2.0,
  "planet": "Moon",
  "step_minutes": 15
}
```

**Parameters:**
- `year` (int, required): Year (1900-2100)
- `month` (int, required): Month (1-12)
- `latitude` (float, required): Location latitude (-90 to 90)
- `longitude` (float, required): Location longitude (-180 to 180)
- `timezone_offset_hours` (float, optional): Timezone offset from UTC (-12 to 14, defaults to 0)
- `planet` (string, optional): Planet name - Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto (defaults to "Moon")
- `step_minutes` (int, optional): Time step for scanning in minutes (1-60, defaults to 15)

**Response:**
```json
{
  "success": true,
  "transits": [
    {
      "planet": "Moon",
      "angle": "Ascendant",
      "datetime_local": "2025-10-01T00:25:00.000000",
      "longitude": 198.68,
      "sign": "Bilancia",
      "degree_in_sign": 18.68,
      "decan": 2
    }
  ],
  "parameters": { /* request parameters */ },
  "total_transits": 240
}
```

> **📖 API Examples**: See the Bruno collection in `api_docs/` for complete request/response examples.

## 🌟 Planetary Transits Feature

The new **planetary transits** endpoint calculates when planets cross the cardinal points (Ascendant, Descendant, Midheaven, Imum Coeli) during a specified month. This is essential for:

- **Timing Events**: Finding optimal moments for important activities
- **Astrological Analysis**: Understanding planetary influences on daily life
- **Chart Interpretation**: Identifying significant planetary movements

### Key Features:
- **Precise Timing**: Uses bisection method for ~30-second accuracy
- **All Cardinal Points**: Tracks Ascendant, Descendant, Midheaven, and Imum Coeli
- **Complete Data**: Returns sign, degree, decan, and exact timing
- **Flexible Parameters**: Supports all planets and customizable time steps

### Example Usage:

**Moon transits for Rome (October 2025):**
```bash
curl -X POST https://your-project.cloudfunctions.net/planetary_transits \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2025,
    "month": 10,
    "latitude": 41.9028,
    "longitude": 12.4964,
    "timezone_offset_hours": 2.0,
    "planet": "Moon"
  }'
```

**Sun transits with custom step:**
```bash
curl -X POST https://your-project.cloudfunctions.net/planetary_transits \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2025,
    "month": 10,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezone_offset_hours": -5.0,
    "planet": "Sun",
    "step_minutes": 30
  }'
```

## 🧪 Testing

### Run Tests
```bash
cd functions
source venv/bin/activate
pytest tests/ -v
```

### Run Tests with Coverage
```bash
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

### Test Results
- ✅ **9 tests passing** - All core astrological calculations tested
- ✅ **96% coverage** on core business logic (`astro_calculations.py`)
- ✅ **Tests cover**: Sign/decan calculation, position calculation, aspects, moon phases, planetary transits

## 🏛️ Architecture

This project follows **Clean Code** and **Firebase Functions** best practices:

- **Single Responsibility**: Each module has one clear purpose
- **Separation of Concerns**: API, business logic, and utilities are separated
- **Modularity**: Easy to test, maintain, and extend
- **Configuration**: Centralized constants and settings
- **Error Handling**: Consistent error responses across all endpoints

## 📦 Dependencies

- `pyswisseph==2.10.3.2`: Swiss Ephemeris library for astronomical calculations
- `firebase-functions==0.1.0`: Firebase Functions framework
- `firebase-admin==6.*`: Firebase Admin SDK
- `functions-framework==3.*`: Functions framework for local development

## 🔧 Development

### Adding New Functions

1. Create new endpoint in `src/api/`
2. Import in `main.py`
3. Add tests in `tests/`
4. Update documentation

### Code Organization

- **`src/api/`**: Firebase function endpoints
- **`src/core/`**: Business logic and validation
- **`src/utils/`**: Common utilities
- **`tests/`**: Test modules

## 📚 Documentation

- **Root README**: This file - project overview and quick start
- **Functions README**: `functions/README.md` - detailed API documentation
- **Refactoring Summary**: `REFACTORING_SUMMARY.md` - architecture details

## 🚀 CI/CD

This project uses GitHub Actions for automated testing and deployment:

### **Pull Requests**
- ✅ **Automated Tests**: Runs on every PR
- ✅ **Coverage Report**: Shows test coverage
- ✅ **Quality Gates**: Fails if tests don't pass

### **Deployment**
- ✅ **Auto Deploy**: Deploys to Firebase on push to master/main
- ✅ **Test First**: Runs tests before deployment
- ✅ **Zero Downtime**: Seamless function updates

### **Workflows**
- `test.yml` - Tests on pull requests
- `deploy.yml` - Tests + Deploy to Firebase on push to master

## 🤝 Contributing

1. **Create a branch** from master
2. **Make your changes** following the existing code structure
3. **Add tests** for new features
4. **Create a PR** - tests will run automatically
5. **Ensure all tests pass** before merging
6. **Update documentation** as needed

## 📄 License

This project is for astrological calculations using Swiss Ephemeris.