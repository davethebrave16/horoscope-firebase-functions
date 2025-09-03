# Horoscope Firebase Functions

Firebase Functions for calculating astrological positions using Swiss Ephemeris.

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

The function will be available at:
```
http://localhost:5001/YOUR_PROJECT_ID/us-central1/calculate_horoscope
```

## API Usage

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
  "positions": {
    "Sun": ["Toro", 1, 25.5, 55.5],
    "Moon": ["Gemelli", 2, 15.2, 75.2],
    ...
  },
  "input_data": {
    "date": [1990, 5, 15],
    "time": [14, 30, 0],
    "latitude": 41.9028,
    "longitude": 12.4964,
    "timezone_offset_hours": 1.0
  }
}
```

**Position Format:**
Each position returns `[sign, decan, degree_in_sign, absolute_longitude]`

## Deployment

Deploy to Firebase:
```bash
firebase deploy --only functions
```

## Dependencies

- `pyswisseph`: Swiss Ephemeris library for astronomical calculations
- `firebase-functions`: Firebase Functions framework
- `firebase-admin`: Firebase Admin SDK
