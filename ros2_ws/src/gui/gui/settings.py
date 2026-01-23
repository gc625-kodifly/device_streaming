import json
from pathlib import Path
from typing import Any

SETTINGS_FILE = Path(__file__).parent / 'config.json'

DEFAULT_SETTINGS = {
    'camera': {
        'exposure': 10000,
        'gain': 0,
        'brightness': 50,
        'contrast': 50,
        'trigger_mode': 'Continuous',
        'auto_exposure': True,
        'auto_white_balance': True,
    },
    'stream': {
        'resolution': '1920x1080',
        'framerate': 30,
        'bitrate': 4000,
        'codec': 'H.264',
    },
    'ptz': {
        'pan_speed': 32,
        'tilt_speed': 32,
        'invert_pan': False,
        'invert_tilt': False,
    },
    'slam': {
        'enabled': True,
        'algorithm': 'ORB-SLAM3',
        'max_features': 1000,
        'scale_factor': 1.2,
        'num_levels': 8,
        'loop_closure': True,
        'relocalization': True,
        'save_map': False,
    },
    'map': {
        'default_lat': 22.42667,
        'default_lon': 114.198,
        'zoom': 16,
    },
}


class Settings:
    def __init__(self):
        self._settings = self.load()
    
    def load(self) -> dict:
        """Load settings from JSON file, or return defaults if not found."""
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    loaded = json.load(f)
                # Merge with defaults to handle new settings
                return self._merge_defaults(loaded)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading settings: {e}, using defaults")
                return DEFAULT_SETTINGS.copy()
        return self._deep_copy(DEFAULT_SETTINGS)
    
    def save(self) -> bool:
        """Save current settings to JSON file."""
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self._settings, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving settings: {e}")
            return False
    
    def reset(self):
        """Reset settings to defaults."""
        self._settings = self._deep_copy(DEFAULT_SETTINGS)
    
    def get(self, category: str, key: str) -> Any:
        """Get a setting value."""
        return self._settings.get(category, {}).get(key)
    
    def set(self, category: str, key: str, value: Any):
        """Set a setting value."""
        if category not in self._settings:
            self._settings[category] = {}
        self._settings[category][key] = value
    
    def get_category(self, category: str) -> dict:
        """Get all settings in a category."""
        return self._settings.get(category, {})
    
    @property
    def camera(self) -> dict:
        return self._settings.get('camera', {})
    
    @property
    def stream(self) -> dict:
        return self._settings.get('stream', {})
    
    @property
    def ptz(self) -> dict:
        return self._settings.get('ptz', {})
    
    @property
    def slam(self) -> dict:
        return self._settings.get('slam', {})
    
    @property
    def map(self) -> dict:
        return self._settings.get('map', {})
    
    def _merge_defaults(self, loaded: dict) -> dict:
        """Merge loaded settings with defaults to handle missing keys."""
        result = self._deep_copy(DEFAULT_SETTINGS)
        for category, values in loaded.items():
            if category in result and isinstance(values, dict):
                result[category].update(values)
            else:
                result[category] = values
        return result
    
    def _deep_copy(self, d: dict) -> dict:
        """Create a deep copy of a dictionary."""
        return json.loads(json.dumps(d))


# Global settings instance
settings = Settings()

