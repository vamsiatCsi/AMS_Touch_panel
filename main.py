# AMS Touch Interface v3.0 Professional - Refactored Main Application
#
# Modular Entry Point for Activity Monitoring System
# 
# Features:
# - Professional modular architecture
# - Enhanced touch interface design
# - Comprehensive screen management
# - Continuous operation support
# - Production-ready deployment

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock

# Import core modules
from core.config import AppConfig, Theme
from core.navigation import NavigationManager

# Import screen modules  
from screens.main_screen import MainIdleScreen
from screens.auth_screen import AuthSelectionScreen
from screens.scan_screens import CardScanScreen, BiometricScanScreen
from screens.input_screens import PinEntryScreen, ActivityCodeScreen
from screens.emergency_screen import EmergencyAccessScreen
from screens.config_screen import ConfigurationScreen

class AMSApp(App):
    """
    Main AMS Touch Interface Application
    
    Features:
    - Modular architecture with organized screen management
    - Professional responsive design
    - Continuous operation support
    - Production-ready error handling
    """
    
    def build(self):
        """Build and configure the main application"""
        self.title = f'{AppConfig.APP_NAME} {AppConfig.APP_VERSION} - Refactored'
        
        # Initialize navigation manager
        self.nav_manager = NavigationManager()
        
        # Register all screens
        self._register_screens()
        
        # Configure window properties
        self._configure_window()
        
        # Setup continuous operation monitoring
        Clock.schedule_interval(self._monitor_system_health, 1)
        
        return self.nav_manager.screen_manager
    
    def _register_screens(self):
        """Register all application screens with the navigation manager"""
        screen_classes = [
            (MainIdleScreen, 'main_idle'),
            (AuthSelectionScreen, 'auth_selection'), 
            (CardScanScreen, 'card_scan'),
            (BiometricScanScreen, 'biometric_scan'),
            (PinEntryScreen, 'pin_entry'),
            (ActivityCodeScreen, 'activity_code'),
            (EmergencyAccessScreen, 'emergency_access'),
            (ConfigurationScreen, 'configuration')
        ]
        
        for screen_class, screen_name in screen_classes:
            screen = screen_class(name=screen_name)
            self.nav_manager.add_screen(screen)
        
        # Set initial screen
        self.nav_manager.set_current('main_idle')
    
    def _configure_window(self):
        """Configure window properties for optimal display"""
        Window.bind(on_resize=self._handle_window_resize)
        
        # Set minimum window size
        Window.minimum_width = 800
        Window.minimum_height = 600
        
    def _handle_window_resize(self, window, width, height):
        """Handle window resize events for responsive design"""
        # Refresh all screens to adapt to new size
        for screen in self.nav_manager.screen_manager.screens:
            if hasattr(screen, 'refresh_layout'):
                Clock.schedule_once(lambda dt, s=screen: s.refresh_layout(), 0.1)
    
    def _monitor_system_health(self, dt):
        """Monitor system health for continuous operation"""
        # This enables continuous operation by monitoring:
        # - System state consistency
        # - Screen navigation health
        # - Auto-recovery from invalid states
        
        if not hasattr(self.nav_manager, 'screen_manager'):
            return
            
        # Ensure we're always in a valid screen state
        current_screen = self.nav_manager.get_current_screen()
        if not current_screen:
            print("Warning: Invalid screen state detected, returning to main")
            self.nav_manager.set_current('main_idle')
    
    def on_start(self):
        """Application startup initialization"""
        print(f"\n{'='*70}")
        print(f"{AppConfig.APP_NAME} {AppConfig.APP_VERSION} - Initializing...")
        print(f"{'='*70}")
        print(f"Theme: {'Dark' if Theme.is_dark() else 'Light'} Mode")
        print(f"Screen Resolution: {Window.width}x{Window.height}")
        print(f"Screens Registered: {len(self.nav_manager.screen_manager.screens)}")
        
                
        # Verify all screens loaded successfully
        screen_names = [screen.name for screen in self.nav_manager.screen_manager.screens]
        print(f"\nLoaded Screens: {', '.join(screen_names)}")
        
        print(f"\n🚀 Application ready!")
        print(f"{'='*70}\n")
    
    def on_stop(self):
        """Application shutdown cleanup"""
        print(f"\n{AppConfig.APP_NAME} shutdown initiated...")
        
        # Cleanup any active sessions
        if hasattr(self, 'nav_manager'):
            self.nav_manager.cleanup()
            
        print(f"{AppConfig.APP_NAME} stopped gracefully")
        print("Thank you for using AMS Touch Interface Professional!")

def main():
    """Main application entry point"""
    try:
        # Configure Kivy settings before app creation
        Config.set('graphics', 'width', str(AppConfig.WINDOW_WIDTH))
        Config.set('graphics', 'height', str(AppConfig.WINDOW_HEIGHT))
        Config.set('graphics', 'resizable', True)
        Config.set('graphics', 'borderless', False)
        Config.set('graphics', 'vsync', '1')
        Config.set('input', 'mouse', 'mouse,disable_multitouch')
        
        # Create and run the application
        app = AMSApp()
        app.run()
        
    except Exception as e:
        print(f"Critical Application Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nPlease check your installation and try again.")
    
    finally:
        print("\nApplication terminated.")

if __name__ == '__main__':
    main()