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
│   │   │   └── moon_phase.py   # moon_phase function
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

> **📖 API Examples**: See the Bruno collection in `api_docs/` for complete request/response examples.

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
- ✅ **4 tests passing** - All core astrological calculations tested
- ✅ **96% coverage** on core business logic (`astro_calculations.py`)
- ✅ **Tests cover**: Sign/decan calculation, position calculation, aspects, moon phases

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
- `pr-test.yml` - Tests only (for PRs)
- `test.yml` - Tests on push to main branches
- `deploy.yml` - Tests + Deploy to Firebase

## 🤝 Contributing

1. **Create a branch** from master
2. **Make your changes** following the existing code structure
3. **Add tests** for new features
4. **Create a PR** - tests will run automatically
5. **Ensure all tests pass** before merging
6. **Update documentation** as needed

## 📄 License

This project is for astrological calculations using Swiss Ephemeris.