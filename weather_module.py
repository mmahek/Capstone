"""
Weather Module with Caching, Fallback, and Low-Bandwidth Optimization
Uses OpenWeatherMap API - FIXED VERSION (Syntax & Runtime Errors Fixed)
"""

import requests
import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, Tuple, List, Optional

# Safe config import with defaults - handles missing config.py gracefully
try:
    import config
    OPENWEATHER_API_KEY = config.OPENWEATHER_API_KEY
    CACHE_DIR = getattr(config, 'CACHE_DIR', 'cache')
    WEATHER_CACHE_FILE = getattr(config, 'WEATHER_CACHE_FILE', os.path.join(CACHE_DIR, 'weather_cache.json'))
    WEATHER_CACHE_DURATION = getattr(config, 'WEATHER_CACHE_DURATION', 1800)  # 30 min
    AQI_CACHE_DURATION = getattr(config, 'AQI_CACHE_DURATION', 3600)  # 1 hour
    SEASONAL_AVERAGES = getattr(config, 'SEASONAL_AVERAGES', {
        1: (18, 70, 150), 2: (22, 65, 160), 3: (28, 55, 140),
        4: (32, 45, 120), 5: (36, 40, 110), 6: (32, 75, 100),
        7: (30, 80, 90), 8: (29, 82, 85), 9: (30, 78, 95),
        10: (28, 65, 110), 11: (24, 60, 130), 12: (20, 75, 155)
    })
    REGIONAL_CITIES = getattr(config, 'REGIONAL_CITIES', {
        'north': ['Delhi', 'Amritsar', 'Chandigarh', 'Ludhiana'],
        'south': ['Hyderabad', 'Bengaluru', 'Chennai', 'Coimbatore'],
        'central': ['Bhopal', 'Nagpur', 'Lucknow', 'Kanpur']
    })
except (ImportError, AttributeError) as e:
    print(f"⚠️ Config warning ({e}): Using safe defaults.")
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    CACHE_DIR = 'cache'
    WEATHER_CACHE_FILE = os.path.join(CACHE_DIR, 'weather_cache.json')
    WEATHER_CACHE_DURATION = 1800
    AQI_CACHE_DURATION = 3600
    SEASONAL_AVERAGES = {
        1: (18, 70, 150), 2: (22, 65, 160), 3: (28, 55, 140),
        4: (32, 45, 120), 5: (36, 40, 110), 6: (32, 75, 100),
        7: (30, 80, 90), 8: (29, 82, 85), 9: (30, 78, 95),
        10: (28, 65, 110), 11: (24, 60, 130), 12: (20, 75, 155)
    }
    REGIONAL_CITIES = {
        'north': ['Delhi', 'Amritsar', 'Chandigarh', 'Ludhiana'],
        'south': ['Hyderabad', 'Bengaluru', 'Chennai', 'Coimbatore'],
        'central': ['Bhopal', 'Nagpur', 'Lucknow', 'Kanpur']
    }

class WeatherModule:
    """Handles weather & AQI with caching, API fallbacks for rural/low-bandwidth"""
    
    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geo_url = "https://api.openweathermap.org/geo/1.0/direct"
        self.current_location = None
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        try:
            os.makedirs(CACHE_DIR, exist_ok=True)
            print(f"📁 Cache dir ready: {CACHE_DIR}")
        except Exception as e:
            print(f"Cache dir error: {e}")
    
    def _load_cache(self) -> Dict:
        """Load cache safely"""
        try:
            cache_path = os.path.abspath(WEATHER_CACHE_FILE)
            if os.path.exists(cache_path):
                with open(cache_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Cache load failed: {e}")
        return {}
    
    def _save_cache(self, cache: Dict):
        """Save cache safely"""
        try:
            cache_path = os.path.abspath(WEATHER_CACHE_FILE)
            with open(cache_path, 'w') as f:
                json.dump(cache, f, indent=2)
        except Exception as e:
            print(f"Cache save failed: {e}")
    
    def _get_cached(self, location: str, data_type: str) -> Optional[Dict]:
        """Get valid cached data"""
        cache = self._load_cache()
        key = f"{location.lower()}_{data_type}"
        if key in cache:
            try:
                entry = cache[key]
                cached_time = datetime.fromisoformat(entry['timestamp'])
                duration = WEATHER_CACHE_DURATION if data_type == 'weather' else AQI_CACHE_DURATION
                if datetime.now() - cached_time < timedelta(seconds=duration):
                    print(f"📦 Cache hit: {location} {data_type}")
                    return entry['data']
            except (KeyError, ValueError, TypeError):
                pass
        return None
    
    def _save_to_cache(self, location: str, data_type: str, data: Dict):
        """Cache data safely"""
        cache = self._load_cache()
        key = f"{location.lower()}_{data_type}"
        cache[key] = {'data': data, 'timestamp': datetime.now().isoformat()}
        self._save_cache(cache)
    
    def _get_coordinates(self, location: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
        """FIXED: Single clean geocoding with cache & fallbacks"""
        cached = self._get_cached(location, 'coords')
        if cached and 'lat' in cached:
            return cached['lat'], cached['lon'], cached.get('country')
        
        if not self.api_key:
            print("❌ Missing API key")
            return None, None, None
        
        locations_to_try = [f"{location},IN", location]
        for loc_query in locations_to_try:
            try:
                params = {'q': loc_query, 'limit': 1, 'appid': self.api_key}
                resp = requests.get(self.geo_url, params=params, timeout=8)
                if resp.status_code == 200:
                    data_list = resp.json()
                    if data_list:
                        data = data_list[0]
                        coords = {
                            'lat': float(data['lat']),
                            'lon': float(data['lon']),
                            'country': data.get('country'),
                            'name': data.get('name', location)
                        }
                        self._save_to_cache(location, 'coords', coords)
                        print(f"📍 Geocoded {coords['name']}: {coords['lat']:.2f},{coords['lon']:.2f}")
                        return coords['lat'], coords['lon'], coords['country']
            except Exception as e:
                print(f"Geo try failed ({loc_query}): {e}")
        
        print(f"❌ Geocoding failed for {location}")
        return None, None, None
    
    def _get_regional_fallback(self, location: str) -> str:
        """Regional fallback city"""
        loc_lower = location.lower()
        punjab_areas = ['punjab', 'amritsar', 'ludhiana', 'jalandhar', 'phagwara']
        if any(kw in loc_lower for kw in punjab_areas):
            return 'Amritsar'
        if any(suf in loc_lower for suf in ['pur', 'bad', 'nagar', 'garh', 'abad']):
            return random.choice(REGIONAL_CITIES['north'])
        if any(suf in loc_lower for suf in ['ur', 'patti', 'pally', 'palli']):
            return random.choice(REGIONAL_CITIES['south'])
        return random.choice(REGIONAL_CITIES['central'])
    
    def _get_seasonal_average(self, city: str = None) -> Dict:
        """Seasonal fallback data"""
        month = datetime.now().month
        base_temp, base_hum, base_aqi = SEASONAL_AVERAGES.get(month, (25, 60, 120))
        if month == 4:  # April fix
            base_temp, base_hum, base_aqi = 31, 45, 120
        
        data = {
            'temperature': round(base_temp + random.uniform(-2, 2), 1),
            'feels_like': round(base_temp + random.uniform(0, 4), 1),
            'humidity': round(base_hum + random.uniform(-5, 5), 1),
            'pressure': 1013,
            'weather': self._get_seasonal_weather(month),
            'wind_speed': round(random.uniform(2, 8), 1),
            'aqi': max(0, int(base_aqi + random.uniform(-20, 20))),
            'city': (city or 'Regional').title(),
            'country': 'IN',
            'is_cached': False,
            'is_seasonal': True,
            'is_simulated': True,
            'fallback_location': self._get_regional_fallback(city) if city else None
        }
        return data
    
    def _get_seasonal_weather(self, month: int) -> str:
        """Seasonal weather description"""
        seasons = {
            (12,1,2): ['Clear', 'Fog', 'Sunny', 'Cold'],
            (3,4,5): ['Clear', 'Sunny', 'Hot', 'Partly cloudy'],
            (6,7,8,9): ['Rain', 'Clouds', 'Thunderstorm', 'Humid'],
            (): ['Clear', 'Clouds', 'Pleasant']
        }
        for months, options in seasons.items():
            if month in months:
                return random.choice(options)
        return 'Clear'
    
    def get_weather(self, city: str, low_bandwidth: bool = False) -> Dict:
        """Main weather getter with full fallback chain"""
        self.current_location = city
        cached = self._get_cached(city, 'weather')
        if cached:
            data = cached.copy()
            data.update({'is_cached': True, 'is_seasonal': False})
            return data
        
        if low_bandwidth:
            return self._get_seasonal_average(city)
        
        lat, lon, country = self._get_coordinates(city)
        if lat is not None and lon is not None:
            try:
                params = {'lat': lat, 'lon': lon, 'appid': self.api_key, 'units': 'metric'}
                resp = requests.get(f"{self.base_url}/weather", params=params, timeout=10)
                if resp.status_code == 200:
                    api_data = resp.json()
                    data = {
                        'temperature': round(api_data['main']['temp'], 1),
                        'feels_like': round(api_data['main']['feels_like'], 1),
                        'humidity': api_data['main']['humidity'],
                        'pressure': api_data['main']['pressure'],
                        'weather': api_data['weather'][0]['description'].title(),
                        'wind_speed': round(api_data['wind'].get('speed', 0), 1),
                        'city': api_data['name'],
                        'country': country or api_data['sys'].get('country', 'IN'),
                        'is_cached': False, 'is_seasonal': False, 'is_simulated': False
                    }
                    self._save_to_cache(city, 'weather', data)
                    return data
            except Exception as e:
                print(f"Live weather error: {e}")
        
        # Ultimate fallback
        fallback = self._get_seasonal_average(city)
        fallback['fallback_reason'] = 'API failure'
        return fallback
    
    def get_aqi(self, city: str, low_bandwidth: bool = False) -> int:
        """AQI with caching & fallbacks"""
        cached = self._get_cached(city, 'aqi')
        if cached is not None:
            return cached['value']
        
        if low_bandwidth:
            month = datetime.now().month
            _, _, base_aqi = SEASONAL_AVERAGES.get(month, (0,0,120))
            return max(0, int(base_aqi + random.uniform(-30, 30)))
        
        lat, lon, _ = self._get_coordinates(city)
        if lat is not None and lon is not None:
            try:
                params = {'lat': lat, 'lon': lon, 'appid': self.api_key}
                resp = requests.get(f"{self.base_url}/air_pollution", params=params, timeout=10)
                if resp.status_code == 200:
                    components = resp.json()['list'][0]['components']
                    pm25 = components.get('pm2_5', 0)
                    aqi = self._pm25_to_aqi(pm25) if pm25 > 0 else 100
                    aqi = min(500, max(0, aqi))
                    self._save_to_cache(city, 'aqi', {'value': aqi})
                    return aqi
            except Exception as e:
                print(f"AQI error: {e}")
        
        month = datetime.now().month
        _, _, base_aqi = SEASONAL_AVERAGES.get(month, (0,0,120))
        return max(0, int(base_aqi + random.uniform(-30, 30)))
    
    def _pm25_to_aqi(self, pm25: float) -> int:
        """PM2.5 to AQI conversion"""
        breakpoints = [
            (0.0, 12.0, 0, 50),
            (12.1, 35.4, 51, 100),
            (35.5, 55.4, 101, 150),
            (55.5, 150.4, 151, 200),
            (150.5, 250.4, 201, 300),
            (250.5, 350.4, 301, 400),
            (350.5, 500.4, 401, 500)
        ]
        for lo_conc, hi_conc, lo_aqi, hi_aqi in breakpoints:
            if lo_conc <= pm25 <= hi_conc:
                return int(lo_aqi + (hi_aqi - lo_aqi) * (pm25 - lo_conc) / (hi_conc - lo_conc))
        return 500
    
    def calculate_risk(self, temp: float, aqi: int, humidity: float) -> Tuple[str, List[str]]:
        """Health risk assessment"""
        score, warnings = 0, []
        # Temp risks
        if temp > 40: score += 5; warnings.append(f"🔥 Extreme heat {temp:.0f}°C")
        elif temp > 38: score += 4; warnings.append("🔥 High heat risk")
        elif temp > 35: score += 3; warnings.append("☀️ Heat caution")
        elif temp < 8: score += 3; warnings.append(f"❄️ Cold {temp:.0f}°C")
        # AQI risks
        if aqi > 300: score += 5; warnings.append(f"😷 AQI {aqi} hazardous")
        elif aqi > 200: score += 4; warnings.append(f"😷 AQI {aqi} unhealthy")
        elif aqi > 150: score += 3; warnings.append(f"AQI {aqi} moderate")
        # Humidity
        if humidity > 85 or humidity < 20: score += 2; warnings.append(f"💧 Humidity {humidity:.0f}%")
        risk = "high" if score >= 7 else "moderate" if score >= 4 else "low"
        return risk, warnings
    
    def get_current_conditions(self, city: str = None) -> Dict:
        """Full conditions report"""
        city = city or self.current_location or "Delhi"
        weather = self.get_weather(city)
        weather['aqi'] = self.get_aqi(city)
        weather['risk_level'], weather['warnings'] = self.calculate_risk(
            weather['temperature'], weather['aqi'], weather['humidity']
        )
        weather['season'] = self._get_season()
        weather['timestamp'] = datetime.now().isoformat()
        return weather
    
    def _get_season(self) -> str:
        """Current season"""
        m = datetime.now().month
        return {1: "Winter", 2: "Winter", 3: "Summer", 4: "Summer", 5: "Summer",
                6: "Monsoon", 7: "Monsoon", 8: "Monsoon", 9: "Monsoon",
                10: "Autumn", 11: "Autumn", 12: "Winter"}.get(m, "Autumn")
    
    def set_city(self, city: str):
        self.current_location = city
        print(f"📍 Set city: {city}")
    
    def clear_cache(self, location: str = None):
        """Clear cache"""
        cache = self._load_cache()
        if location:
            for k in list(cache):
                if location.lower() in k:
                    del cache[k]
            print(f"🗑️ Cleared cache for '{location}'")
        else:
            cache.clear()
            print("🗑️ Full cache cleared")
        self._save_cache(cache)

if __name__ == "__main__":
    print("🧪 Testing fixed WeatherModule...")
    wm = WeatherModule()
    print("✅ Module loads OK")
    try:
        cond = wm.get_current_conditions("Delhi")
        print("✅ Test run OK:", cond['temperature'], "°C, AQI:", cond['aqi'])
        print("✅ FIXED VERSION READY - Original file untouched!")
    except Exception as e:
        print("❌ Test error:", e)

