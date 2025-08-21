"""
AMS Touch Interface - Core Configuration Module

Professional configuration management for the Activity Monitoring System.
Includes theme management, responsive design utilities, icon management, 
and application settings.

Features:
- Advanced theme system with dark/light modes
- Responsive design calculations 
- Professional icon management
- Session state management
- Application configuration
"""

import os
from datetime import datetime, timedelta
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.core.window import Window

class Theme:
    """
    Professional theme management system
    
    Provides comprehensive theming with dark/light mode support,
    consistent color palettes, and dynamic theme switching.
    """
    
    # Dark theme color palette (Material Design inspired)
    DARK = {
        'primary': get_color_from_hex('#2196F3'),          # Updated to Blue
        'primary_dark': get_color_from_hex('#1976D2'),     # Updated to Darker Blue
        'secondary': get_color_from_hex('#03DAC6'),        # Teal accent (unchanged)
        'success': get_color_from_hex('#4CAF50'),          # Green (unchanged)
        'warning': get_color_from_hex('#FF9800'),          # Orange (unchanged)
        'error': get_color_from_hex('#F44336'),            # Updated to Red
        'background': get_color_from_hex('#121212'),       # Dark background
        'surface': get_color_from_hex('#1E1E1E'),          # Surface color
        'surface_variant': get_color_from_hex('#2C2C2C'),  # Surface variant
        'on_surface': get_color_from_hex('#FFFFFF'),       # Text on surface
        'on_surface_variant': get_color_from_hex('#B0B0B0'), # Secondary text
        'outline': get_color_from_hex('#404040'),          # Border color
        'shadow': get_color_from_hex('#00000066'),         # Shadow color
        'scan_bar': get_color_from_hex('#00FF41'),         # Scanning animation
        'scan_bar_bg': get_color_from_hex('#001100'),      # Scan background
    }
    
    # Light theme color palette 
    LIGHT = {
        'primary': get_color_from_hex('#2196F3'),          # Updated to Blue
        'primary_dark': get_color_from_hex('#1976D2'),     # Updated to Darker Blue
        'secondary': get_color_from_hex('#E3F2FD'),        # Light blue accent
        'success': get_color_from_hex('#4CAF50'),          # Green (unchanged)
        'warning': get_color_from_hex('#FF9800'),          # Orange (unchanged)
        'error': get_color_from_hex('#F44336'),            # Red (unchanged)
        'background': get_color_from_hex('#FAFAFA'),       # Light background
        'surface': get_color_from_hex('#FFFFFF'),          # Surface color
        'surface_variant': get_color_from_hex('#F5F5F5'),  # Surface variant
        'on_surface': get_color_from_hex('#212121'),       # Text on surface
        'on_surface_variant': get_color_from_hex('#757575'), # Secondary text
        'outline': get_color_from_hex('#E0E0E0'),          # Border color
        'shadow': get_color_from_hex('#00000029'),         # Shadow color
        'scan_bar': get_color_from_hex('#4CAF50'),         # Scanning animation
        'scan_bar_bg': get_color_from_hex('#E8F5E8'),      # Scan background
    }
         
    # Current active theme
    current_theme = DARK
    
    @classmethod
    def toggle_theme(cls):
        """Toggle between dark and light themes"""
        cls.current_theme = cls.LIGHT if cls.current_theme == cls.DARK else cls.DARK
        return cls.current_theme == cls.DARK
    
    @classmethod
    def get(cls, color_name):
        """Get color value by name"""
        return cls.current_theme.get(color_name, cls.DARK['primary'])
    
    @classmethod
    def is_dark(cls):
        """Check if current theme is dark mode"""
        return cls.current_theme == cls.DARK
    
    @classmethod
    def get_theme_name(cls):
        """Get current theme name"""
        return "Dark" if cls.is_dark() else "Light"

class ResponsiveUtils:
    """
    Professional responsive design utility system
    
    Provides consistent scaling, sizing, and spacing calculations
    across different screen sizes and resolutions.
    """
    
    # Enhanced base sizes for better touch interface
    BASE_FONT_SIZE = 18      # Increased from 14sp for better readability
    BASE_ICON_SIZE = 28      # Increased from 24dp for better visibility  
    BASE_BUTTON_HEIGHT = 65  # Increased from 55dp for better touch targets
    BASE_SPACING = 18        # Increased from 12dp for better visual separation
    
    @staticmethod
    def get_scale_factor():
        """Calculate responsive scale factor based on current window size"""
        screen_width = Window.width
        screen_height = Window.height
        base_width = 1280
        base_height = 800
        
        scale_x = screen_width / base_width
        scale_y = screen_height / base_height
        
        # Use minimum scale to maintain aspect ratio, with slight boost
        return min(scale_x, scale_y) * 1.1
    
    @staticmethod
    def responsive_dp(base_dp):
        """Convert base dp value to responsive dp"""
        return dp(base_dp * ResponsiveUtils.get_scale_factor())
    
    @staticmethod
    def responsive_sp(base_sp):
        """Convert base sp value to responsive sp"""
        return sp(base_sp * ResponsiveUtils.get_scale_factor())
    
    @staticmethod
    def font_size(size_type='normal'):
        """Get responsive font size by type"""
        sizes = {
            'tiny': ResponsiveUtils.BASE_FONT_SIZE * 0.6,
            'small': ResponsiveUtils.BASE_FONT_SIZE * 0.8,
            'normal': ResponsiveUtils.BASE_FONT_SIZE,
            'medium': ResponsiveUtils.BASE_FONT_SIZE * 1.2,
            'large': ResponsiveUtils.BASE_FONT_SIZE * 1.5,
            'xlarge': ResponsiveUtils.BASE_FONT_SIZE * 2.0,
            'title': ResponsiveUtils.BASE_FONT_SIZE * 2.5,
            'hero': ResponsiveUtils.BASE_FONT_SIZE * 3.0
        }
        return ResponsiveUtils.responsive_sp(sizes.get(size_type, sizes['normal']))
    
    @staticmethod
    def icon_size(size_type='normal'):
        """Get responsive icon size by type"""
        sizes = {
            'tiny': ResponsiveUtils.BASE_ICON_SIZE * 0.6,
            'small': ResponsiveUtils.BASE_ICON_SIZE * 0.8,
            'normal': ResponsiveUtils.BASE_ICON_SIZE,
            'medium': ResponsiveUtils.BASE_ICON_SIZE * 1.5,
            'large': ResponsiveUtils.BASE_ICON_SIZE * 2.0,
            'xlarge': ResponsiveUtils.BASE_ICON_SIZE * 3.0,
            'hero': ResponsiveUtils.BASE_ICON_SIZE * 4.0
        }
        return ResponsiveUtils.responsive_dp(sizes.get(size_type, sizes['normal']))
    
    @staticmethod
    def button_size(size_type='normal'):
        """Get responsive button dimensions by type"""
        base_height = ResponsiveUtils.BASE_BUTTON_HEIGHT
        sizes = {
            'tiny': (ResponsiveUtils.responsive_dp(80), ResponsiveUtils.responsive_dp(40)),
            'small': (ResponsiveUtils.responsive_dp(120), ResponsiveUtils.responsive_dp(50)),
            'normal': (ResponsiveUtils.responsive_dp(160), ResponsiveUtils.responsive_dp(base_height)),
            'medium': (ResponsiveUtils.responsive_dp(200), ResponsiveUtils.responsive_dp(75)),
            'large': (ResponsiveUtils.responsive_dp(300), ResponsiveUtils.responsive_dp(85)),
            'xlarge': (ResponsiveUtils.responsive_dp(400), ResponsiveUtils.responsive_dp(95)),
            'hero': (ResponsiveUtils.responsive_dp(500), ResponsiveUtils.responsive_dp(110))
        }
        return sizes.get(size_type, sizes['normal'])
    
    @staticmethod
    def spacing(size_type='normal'):
        """Get responsive spacing value by type"""
        sizes = {
            'tiny': ResponsiveUtils.BASE_SPACING * 0.25,
            'small': ResponsiveUtils.BASE_SPACING * 0.5,
            'normal': ResponsiveUtils.BASE_SPACING,
            'medium': ResponsiveUtils.BASE_SPACING * 1.5,
            'large': ResponsiveUtils.BASE_SPACING * 2.0,
            'xlarge': ResponsiveUtils.BASE_SPACING * 3.0,
            'hero': ResponsiveUtils.BASE_SPACING * 4.0
        }
        return ResponsiveUtils.responsive_dp(sizes.get(size_type, sizes['normal']))

class IconManager:
    """
    Professional icon management system
    
    Handles icon file loading, fallback text, and asset management
    for a consistent visual experience.
    """
    
    # Icon file mappings (support multiple formats)
    ICON_MAPPINGS = {
        'home': ['icon-home.svg', 'icon-home.png'],
        'card': ['icon-card.svg', 'icon-card.png'], 
        'fingerprint': ['icon-fingerprint.png', 'icon-fingerprint.svg'],
        'emergency': ['icon-emergency.svg', 'icon-emergency.png'],
        'config': ['icon-config.svg', 'icon-config.png'],
        'back': ['icon-back.svg', 'icon-back.png'],
        'forward': ['icon-forward.svg', 'icon-forward.png'],
        'check': ['icon-check.svg', 'icon-check.png'],
        'clear': ['icon-clear.svg', 'icon-clear.png'],
        'warning': ['icon-warning.svg', 'icon-warning.png'],
        'success': ['icon-success.svg', 'icon-success.png'],
        'error': ['icon-error.svg', 'icon-error.png'],
        'lock': ['icon-lock.svg', 'icon-lock.png'],
        'unlock': ['icon-unlock.svg', 'icon-unlock.png'],
        'key': ['icon-key.svg', 'icon-key.png'],
        'door': ['icon-door.svg', 'icon-door.png'],
        'user': ['icon-user.svg', 'icon-user.png'],
        'time': ['icon-time.svg', 'icon-time.png'],
        'calendar': ['icon-calendar.svg', 'icon-calendar.png'],
        'network': ['icon-network.svg', 'icon-network.png'],
        'scan': ['icon-scan.svg', 'icon-scan.png'],
        'moon': ['icon-moon.svg', 'icon-moon.png'],
        'sun': ['icon-sun.svg', 'icon-sun.png'],
    }
    
    # Professional fallback text
    FALLBACK_TEXT = {
        'home': 'HOME',
        'card': 'CARD',
        'fingerprint': 'SCAN',
        'emergency': ' ',
        'config': ' ',
        'back': '← BACK',
        'forward': 'NEXT →',
        'check': '✓',
        'clear': '✗',
        'warning': '⚠',
        'success': '✓',
        'error': '✗',
        'lock': '🔒',
        'unlock': '🔓', 
        'key': '🔑',
        'door': '🚪',
        'user': '👤',
        'time': '🕒',
        'calendar': '📅',
        'network': '📡',
        'scan': '📊',
        'moon': '🌙',
        'sun': '☀',
    }
    
    @classmethod
    def get_icon_path(cls, icon_name):
        """Get the first available icon file path"""
        if icon_name in cls.ICON_MAPPINGS:
            # Try each possible file format
            for icon_file in cls.ICON_MAPPINGS[icon_name]:
                # Check in assets/icons/ directory first
                assets_path = os.path.join('assets', 'icons', icon_file)
                if os.path.exists(assets_path):
                    return assets_path
                # Check in root directory
                if os.path.exists(icon_file):
                    return icon_file
        return None
    
    @classmethod
    def get_fallback_text(cls, icon_name):
        """Get fallback text for icon"""
        return cls.FALLBACK_TEXT.get(icon_name, icon_name.upper())
    
    @classmethod
    def get_scanner_image(cls, scan_type):
        """Get scanner device image path"""
        scanner_files = {
            'card': ['scanner-card.png', 'scanner-card.svg'],
            'fingerprint': ['scanner-fingerprint.png', 'scanner-fingerprint.svg']
        }
        
        if scan_type in scanner_files:
            for scanner_file in scanner_files[scan_type]:
                # Check in assets/images/ directory first
                assets_path = os.path.join('assets', 'images', scanner_file)
                if os.path.exists(assets_path):
                    return assets_path
                # Check in root directory
                if os.path.exists(scanner_file):
                    return scanner_file
        return None

class AppConfig:
    """
    Application configuration and constants
    
    Central configuration management for all application settings,
    credentials, timeouts, and display parameters.
    """
    
    # Application Information
    APP_NAME = "AMS Touch Interface"
    APP_VERSION = "3.0 Professional"
    SITE_NAME = "DAKC RO-001"
    BUILD_INFO = "Modular Refactored Architecture"
    
    # Security Configuration
    DEFAULT_PIN = "12345"
    ADMIN_PIN = "00000" 
    EMERGENCY_PIN = "99999"
    PIN_LENGTH = 5
    MAX_PIN_ATTEMPTS = 3
    
    # Session Management
    SESSION_TIMEOUT_MINUTES = 30
    AUTO_DISMISS_SECONDS = 5
    SCAN_ANIMATION_SECONDS = 3
    INACTIVITY_WARNING_MINUTES = 25
    
    # Display Configuration  
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 800
    FULLSCREEN_MODE = False
    LANDSCAPE_MODE = True
    
    # Animation Settings
    TRANSITION_DURATION = 0.3
    BUTTON_ANIMATION_DURATION = 0.15
    SCAN_FPS = 30
    FADE_DURATION = 0.25
    
    # Input Configuration
    MAX_ACTIVITY_CODE_LENGTH = 8
    MIN_ACTIVITY_CODE_LENGTH = 3
    KEYPAD_REPEAT_DELAY = 0.5
    
    # Development Settings
    DEBUG_MODE = False
    LOG_LEVEL = "INFO"
    DEMO_MODE = False
    
    @staticmethod
    def get_datetime_string():
        """Get current formatted datetime string"""
        return datetime.now().strftime('%A, %B %d, %Y - %I:%M:%S %p')
    
    @staticmethod
    def get_time_string():
        """Get current time string"""
        return datetime.now().strftime('%I:%M:%S %p')
    
    @staticmethod
    def get_date_string():
        """Get current date string"""
        return datetime.now().strftime('%B %d, %Y')
    
    @staticmethod
    def format_time(dt):
        """Format datetime for display"""
        return dt.strftime('%I:%M:%S %p')
    
    @staticmethod
    def format_date(dt):
        """Format date for display"""  
        return dt.strftime('%B %d, %Y')
    
    @classmethod
    def get_version_info(cls):
        """Get complete version information"""
        return f"{cls.APP_NAME} {cls.APP_VERSION} - {cls.BUILD_INFO}"

class SessionState:
    """
    Global application session state management
    
    Handles user sessions, authentication state, key management,
    and session lifecycle for continuous operation.
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reset()
        return cls._instance
    
    def reset(self):
        """Reset session to initial state"""
        self.current_user = None
        self.login_time = None
        self.activity_code = None
        self.authentication_method = None
        self.session_active = False
        self.accessible_keys = []
        self.removed_keys = []
        self.returned_keys = []
        self.failed_attempts = 0
        self.theme_changed = False
        self.session_id = None
    
    def start_session(self, username, auth_method='unknown'):
        """Start a new user session"""
        self.current_user = username
        self.authentication_method = auth_method
        self.login_time = datetime.now()
        self.session_active = True
        self.session_id = f"{username}_{self.login_time.strftime('%Y%m%d_%H%M%S')}"
        self.failed_attempts = 0
        self.load_accessible_keys()
        
        print(f"Session started: {self.session_id} ({auth_method})")
    
    def load_accessible_keys(self):
        """Load keys accessible to current user based on role"""
        if not self.current_user:
            self.accessible_keys = []
            return
            
        user_lower = str(self.current_user).lower()
        
        if any(role in user_lower for role in ['supervisor', 'admin', 'manager']):
            # Supervisor/Admin access - all keys
            self.accessible_keys = [
                {"name": "Main Office Entrance", "slot": 1, "status": "available"},
                {"name": "Server Room A-1", "slot": 2, "status": "available"},
                {"name": "Lab Section 3B", "slot": 3, "status": "available"},
                {"name": "Storage Unit #7", "slot": 4, "status": "available"},
                {"name": "Conference Room 1", "slot": 5, "status": "available"},
                {"name": "Data Center Main", "slot": 6, "status": "available"},
                {"name": "Research Lab G", "slot": 7, "status": "available"},
                {"name": "Executive Office", "slot": 8, "status": "available"},
            ]
        else:
            # Standard user access - limited keys
            self.accessible_keys = [
                {"name": "Main Office Entrance", "slot": 1, "status": "available"},
                {"name": "Conference Room 1", "slot": 5, "status": "available"},
                {"name": "Storage Unit #7", "slot": 4, "status": "available"},
            ]
    
    def remove_key(self, slot):
        """Remove a key from the cabinet"""
        for key in self.accessible_keys:
            if key["slot"] == slot and key["status"] == "available":
                key["status"] = "removed"
                self.removed_keys.append({
                    "name": key["name"],
                    "slot": slot,
                    "time_removed": datetime.now(),
                    "session_id": self.session_id
                })
                return True
        return False
    
    def return_key(self, slot):
        """Return a key to the cabinet"""
        for key in self.accessible_keys:
            if key["slot"] == slot and key["status"] == "removed":
                key["status"] = "available"
                self.returned_keys.append({
                    "name": key["name"],
                    "slot": slot,
                    "time_returned": datetime.now(),
                    "session_id": self.session_id
                })
                return True
        return False
    
    def end_session(self):
        """End current session and return summary"""
        if not self.session_active:
            return None
            
        end_time = datetime.now()
        duration = end_time - self.login_time if self.login_time else timedelta(0)
        
        summary = {
            "session_id": self.session_id,
            "user": self.current_user,
            "auth_method": self.authentication_method,
            "login_time": self.login_time,
            "end_time": end_time,
            "duration": duration,
            "activity_code": self.activity_code,
            "keys_removed": len(self.removed_keys),
            "keys_returned": len(self.returned_keys),
            "removed_keys": self.removed_keys.copy(),
            "returned_keys": self.returned_keys.copy(),
            "failed_attempts": self.failed_attempts
        }
        
        print(f"Session ended: {self.session_id} (Duration: {duration})")
        
        # Reset for next session but preserve summary
        self.reset()
        return summary
    
    def get_session_duration(self):
        """Get current session duration"""
        if not self.session_active or not self.login_time:
            return timedelta(0)
        return datetime.now() - self.login_time
    
    def is_session_expired(self):
        """Check if session has expired"""
        if not self.session_active:
            return True
        duration = self.get_session_duration()
        return duration.total_seconds() > (AppConfig.SESSION_TIMEOUT_MINUTES * 60)

# Global application state instance
app_state = SessionState()