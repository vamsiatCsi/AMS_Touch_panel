"""
AMS Touch Interface - Navigation Management System

Professional navigation system for managing screen transitions,
navigation history, and screen lifecycle in the Activity Monitoring System.

Features:
- Centralized screen management
- Navigation history tracking  
- Smooth transition handling
- Screen lifecycle management
- Error recovery and validation
"""

from kivy.uix.screenmanager import ScreenManager, SlideTransition, FadeTransition
from kivy.clock import Clock
from core.config import AppConfig, app_state

class NavigationManager:
    """
    Professional navigation management system
    
    Provides centralized screen management with navigation history,
    transition control, and screen lifecycle management.
    """
    
    def __init__(self):
        """Initialize navigation manager"""
        self.screen_manager = ScreenManager()
        self.navigation_history = []
        self.screen_registry = {}
        
        # Configure default transitions
        self.setup_transitions()
        
        # Navigation validation rules
        self.navigation_rules = self._setup_navigation_rules()
        
        print("NavigationManager initialized")
    
    def setup_transitions(self):
        """Setup screen transition animations"""
        # Default smooth slide transition
        self.screen_manager.transition = SlideTransition(
            direction='left',
            duration=AppConfig.TRANSITION_DURATION
        )
    
    def _setup_navigation_rules(self):
        """Setup navigation validation rules"""
        return {
            # Define allowed navigation paths
            'main_idle': ['auth_selection', 'emergency_access', 'configuration'],
            'auth_selection': ['main_idle', 'card_scan', 'biometric_scan'],
            'card_scan': ['auth_selection', 'pin_entry'],
            'biometric_scan': ['auth_selection', 'pin_entry'], 
            'pin_entry': ['card_scan', 'biometric_scan', 'activity_code'],
            'activity_code': ['pin_entry', 'main_idle'],
            'emergency_access': ['main_idle'],
            'configuration': ['main_idle']
        }
    
    def add_screen(self, screen):
        """Add a screen to the navigation system"""
        if hasattr(screen, 'name') and screen.name:
            self.screen_manager.add_widget(screen)
            self.screen_registry[screen.name] = screen
            
            # Set navigation manager reference in screen
            if hasattr(screen, 'set_navigation_manager'):
                screen.set_navigation_manager(self)
                
            print(f"Screen registered: {screen.name}")
        else:
            print(f"Warning: Screen {screen.__class__.__name__} has no name attribute")
    
    def get_screen(self, screen_name):
        """Get screen by name"""
        return self.screen_registry.get(screen_name)
    
    def get_current_screen(self):
        """Get currently active screen"""
        if hasattr(self.screen_manager, 'current_screen'):
            return self.screen_manager.current_screen
        return None
    
    def get_current_screen_name(self):
        """Get name of currently active screen"""
        return self.screen_manager.current
    
    def set_current(self, screen_name, direction='left'):
        """Navigate to specified screen with validation"""
        current_screen = self.get_current_screen_name()
        
        # Validate navigation
        if not self._validate_navigation(current_screen, screen_name):
            print(f"Navigation blocked: {current_screen} -> {screen_name}")
            return False
        
        # Set transition direction
        if direction:
            self.screen_manager.transition.direction = direction
        
        # Record navigation history
        self._record_navigation(current_screen, screen_name)
        
        # Perform navigation
        try:
            # Notify current screen of exit
            current_screen_obj = self.get_current_screen()
            if current_screen_obj and hasattr(current_screen_obj, 'on_screen_exit'):
                current_screen_obj.on_screen_exit()
            
            # Navigate to new screen
            self.screen_manager.current = screen_name
            
            # Notify new screen of entry
            new_screen_obj = self.get_screen(screen_name)
            if new_screen_obj and hasattr(new_screen_obj, 'on_screen_enter'):
                new_screen_obj.on_screen_enter()
            
            print(f"Navigation successful: {current_screen} -> {screen_name}")
            return True
            
        except Exception as e:
            print(f"Navigation error: {e}")
            return False
    
    def _validate_navigation(self, from_screen, to_screen):
        """Validate if navigation is allowed"""
        # Always allow navigation to main_idle (safety screen)
        if to_screen == 'main_idle':
            return True
        
        # Check navigation rules
        if from_screen in self.navigation_rules:
            allowed_destinations = self.navigation_rules[from_screen]
            return to_screen in allowed_destinations
        
        # Default to allow if no rules defined
        return True
    
    def _record_navigation(self, from_screen, to_screen):
        """Record navigation in history"""
        navigation_event = {
            'from': from_screen,
            'to': to_screen,
            'timestamp': app_state.current_user if hasattr(app_state, 'current_user') else 'system',
            'session_id': app_state.session_id if hasattr(app_state, 'session_id') else None
        }
        
        self.navigation_history.append(navigation_event)
        
        # Keep history manageable (last 50 navigations)
        if len(self.navigation_history) > 50:
            self.navigation_history = self.navigation_history[-50:]
    
    def go_back(self):
        """Navigate back to previous screen"""
        if len(self.navigation_history) >= 2:
            # Get previous screen from history
            previous_navigation = self.navigation_history[-2]
            previous_screen = previous_navigation['from']
            
            # Navigate back with right direction
            return self.set_current(previous_screen, direction='right')
        else:
            # Default to main screen if no history
            return self.set_current('main_idle', direction='right')
    
    def go_home(self):
        """Navigate to main screen"""
        return self.set_current('main_idle', direction='right')
    
    def start_authentication_flow(self):
        """Start the authentication process"""
        return self.set_current('auth_selection', direction='left')
    
    def handle_authentication_success(self, user_name, auth_method):
        """Handle successful authentication"""
        # Start user session
        app_state.start_session(user_name, auth_method)
        
        # Navigate to activity code entry
        return self.set_current('activity_code', direction='left')
    
    def handle_authentication_failure(self, reason='invalid_credentials'):
        """Handle authentication failure"""
        app_state.failed_attempts += 1
        
        # If too many failures, go back to auth selection
        if app_state.failed_attempts >= AppConfig.MAX_PIN_ATTEMPTS:
            app_state.failed_attempts = 0
            return self.set_current('auth_selection', direction='right')
        
        # Otherwise stay on current screen for retry
        return False
    
    def complete_activity_session(self):
        """Complete activity session and return to main"""
        # End user session
        session_summary = app_state.end_session()
        
        if session_summary:
            print(f"Session completed: {session_summary['session_id']}")
        
        # Return to main screen
        return self.set_current('main_idle', direction='right')
    
    def handle_emergency_access(self):
        """Handle emergency access request"""
        return self.set_current('emergency_access', direction='left')
    
    def handle_configuration_access(self):
        """Handle configuration access request"""
        return self.set_current('configuration', direction='left')
    
    def get_navigation_stats(self):
        """Get navigation statistics"""
        if not self.navigation_history:
            return {"total_navigations": 0}
        
        screen_visits = {}
        for nav in self.navigation_history:
            screen = nav['to']
            screen_visits[screen] = screen_visits.get(screen, 0) + 1
        
        return {
            "total_navigations": len(self.navigation_history),
            "screen_visits": screen_visits,
            "current_screen": self.get_current_screen_name(),
            "total_screens": len(self.screen_registry)
        }
    
    def set_transition_type(self, transition_type='slide', direction='left'):
        """Set screen transition type and direction"""
        if transition_type == 'slide':
            self.screen_manager.transition = SlideTransition(
                direction=direction,
                duration=AppConfig.TRANSITION_DURATION
            )
        elif transition_type == 'fade':
            self.screen_manager.transition = FadeTransition(
                duration=AppConfig.FADE_DURATION
            )
        else:
            print(f"Unknown transition type: {transition_type}")
    
    def refresh_current_screen(self):
        """Refresh the current screen layout"""
        current_screen = self.get_current_screen()
        if current_screen and hasattr(current_screen, 'refresh_layout'):
            Clock.schedule_once(lambda dt: current_screen.refresh_layout(), 0.1)
    
    def refresh_all_screens(self):
        """Refresh all registered screens (useful for theme changes)"""
        for screen_name, screen in self.screen_registry.items():
            if hasattr(screen, 'refresh_layout'):
                Clock.schedule_once(lambda dt, s=screen: s.refresh_layout(), 0.1)
    
    def cleanup(self):
        """Cleanup navigation manager"""
        # Clear navigation history
        self.navigation_history.clear()
        
        # Notify all screens of cleanup
        for screen_name, screen in self.screen_registry.items():
            if hasattr(screen, 'cleanup'):
                screen.cleanup()
        
        # Clear screen registry
        self.screen_registry.clear()
        
        print("NavigationManager cleaned up")
    
    def get_screen_hierarchy(self):
        """Get screen hierarchy for debugging"""
        hierarchy = {}
        for screen_name in self.screen_registry:
            hierarchy[screen_name] = {
                'class': self.screen_registry[screen_name].__class__.__name__,
                'allowed_destinations': self.navigation_rules.get(screen_name, [])
            }
        return hierarchy
    
    def validate_screen_integrity(self):
        """Validate screen manager integrity"""
        issues = []
        
        # Check if all registered screens are in screen manager
        sm_screens = {s.name for s in self.screen_manager.screens}
        reg_screens = set(self.screen_registry.keys())
        
        if sm_screens != reg_screens:
            issues.append("Screen manager and registry mismatch")
        
        # Check current screen validity
        current = self.get_current_screen_name()
        if current not in self.screen_registry:
            issues.append(f"Current screen '{current}' not in registry")
        
        # Check navigation rules consistency
        for screen, destinations in self.navigation_rules.items():
            for dest in destinations:
                if dest not in self.screen_registry:
                    issues.append(f"Navigation rule references non-existent screen: {dest}")
        
        if issues:
            print(f"Screen integrity issues found: {issues}")
            return False
        
        return True