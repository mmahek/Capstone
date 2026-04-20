"""
Configuration and Constants
"""

# API Configuration
OPENWEATHER_API_KEY = "99e415733ae7a9baaa6599ac9c54dffc"

# File Paths
KNOWLEDGE_BASE_PATH = "knowledge_base.json"
MODEL_PATH = "models/xgb_text_model.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"
ENCODER_PATH = "models/label_encoder.pkl"
CACHE_DIR = "cache"
WEATHER_CACHE_FILE = "cache/weather_cache.json"

# ML Configuration
ML_CONFIDENCE_THRESHOLD = 0.50

# Cache Duration (in seconds)
WEATHER_CACHE_DURATION = 10800  # 3 hours
AQI_CACHE_DURATION = 7200       # 2 hours

# Indian States for fallback (major cities per region)
REGIONAL_CITIES = {
    'north': ['Delhi', 'Chandigarh', 'Lucknow', 'Jaipur'],
    'south': ['Chennai', 'Bangalore', 'Hyderabad', 'Coimbatore'],
    'east': ['Kolkata', 'Bhubaneswar', 'Patna', 'Guwahati'],
    'west': ['Mumbai', 'Pune', 'Ahmedabad', 'Surat'],
    'central': ['Bhopal', 'Indore', 'Nagpur', 'Raipur']
}

# Seasonal averages (month: (temp, humidity, aqi))
SEASONAL_AVERAGES = {
    1: (18, 60, 180),   # January - Winter
    2: (20, 55, 170),   # February
    3: (25, 50, 150),   # March - Spring
    4: (30, 45, 130),   # April
    5: (34, 40, 120),   # May - Summer
    6: (33, 65, 90),    # June - Monsoon start
    7: (30, 80, 70),    # July - Monsoon
    8: (29, 85, 65),    # August - Monsoon
    9: (30, 75, 80),    # September
    10: (28, 60, 110),  # October - Post-monsoon
    11: (23, 55, 150),  # November - Winter start
    12: (18, 60, 180)   # December - Winter
}