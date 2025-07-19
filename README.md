# 🏳️ Flag Quiz Application

An educational flag quiz application built with Streamlit for learning world flags and countries. The application uses online APIs to fetch flag images in real-time.

## Features

- 🏳️ Interactive flag-to-country quiz with multiple choice questions
- 🌐 **Real-time flag loading from multiple online APIs**
- 📊 Customizable quiz length (10, 30, 100 questions, or all countries)
- ⏱️ Built-in timer to track completion time and answer speed
- 📈 Comprehensive results with accuracy and timing feedback
- 🎯 Real-time progress tracking during quiz
- 🌍 Covers 164 flags from countries worldwide
- 🔄 **Automatic fallback system** (API → Local files)
- 📱 SNS sharing functionality for quiz results

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Launch the application:
```bash
streamlit run main.py
```

3. Open your browser and start learning!

**Note:** The application automatically fetches flag images from online APIs. No manual setup required!

## Project Structure

```
flags/
├── main.py             # Main Streamlit application
├── data/
│   ├── countries.json  # Country data with ISO codes and flag mappings
│   └── flags/          # Local flag images (backup/fallback)
├── requirements.txt    # Python dependencies
├── download_flags.py   # Utility script for downloading flags
└── README.md          # Project documentation
```

## How to Use

1. Open the application in your browser
2. Select your preferred quiz length
3. Look at each flag and choose the correct country from 4 options
4. Complete the quiz and review your results

## Flag Image System

### Online API Sources (Primary)
The application uses multiple flag APIs for real-time image fetching:

1. **Flagcdn.com** (Primary)
   - URL: `https://flagcdn.com/w320/{country_code}.png`
   - High-quality PNG images, 320px width
   - Free CDN service by Flagpedia.net

2. **FlagsAPI.com** (Fallback 1)
   - URL: `https://flagsapi.com/{COUNTRY_CODE}/flat/256.png`
   - Flat design style, 256px size
   - Free REST API service

3. **CountryFlagsAPI** (Fallback 2)
   - URL: `https://countryflagsapi.netlify.app/flag/{country_code}.svg`
   - SVG format for crisp display
   - Netlify-hosted free service

### Local Fallback System
- If all APIs fail, the app falls back to local images in `data/flags/`
- Local images serve as backup for offline usage
- Automatic error handling and user notification

## Technical Details

### Countries Data Structure
Each country in `countries.json` contains:
```json
{
  "name": "日本",
  "flag": "japan.png", 
  "code": "JP"
}
```

- `name`: Country name in Japanese
- `flag`: Local filename (for fallback)
- `code`: ISO 3166-1 alpha-2 country code (for API calls)

### Network Requirements
- Internet connection required for optimal experience
- Application works offline with local flag images
- Automatic fallback ensures functionality in all scenarios

## Educational Purpose

This application is designed as an educational tool to help users learn and memorize world flags and their corresponding countries through interactive quizzing. The real-time API integration ensures users always see the most up-to-date flag designs.