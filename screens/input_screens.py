"""
AMS Touch Interface - Input Screens

Professional PIN entry and activity code input screens with enhanced
security, visual feedback, and user guidance.

Features:
- Secure PIN input with masked display
- Professional numeric keypad
- Activity code entry with validation
- Enhanced visual feedback
- Error handling and retry logic
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

from screens.base_screen import BaseScreen
from core.config import ResponsiveUtils, Theme, AppConfig, app_state
from components.widgets import (
    ResponsiveButton, ResponsiveLabel, SecureTextInput, ResponsiveKeypad
)

class PinEntryScreen(BaseScreen):
    """
    Professional PIN entry screen with enhanced security features
    
    Features:
    - Secure masked PIN display
    - Professional keypad layout
    - User context display
    - Retry logic and validation
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = "Unknown User"
        self.pin_value = ""
        self.user_label = None
        self.pin_display = None
        self.keypad = None
        self.failed_attempts = 0
        self.create_layout()
    
    def create_layout(self):
        """Create PIN entry interface"""
        self.clear_widgets()
        
        # Main container
        layout = BoxLayout(
            orientation='vertical',
            padding=ResponsiveUtils.spacing('large'),
            spacing=ResponsiveUtils.spacing('medium')
        )
        
        # Apply themed background
        self.create_background(layout)
        
        # Create header
        header = self.create_header(
            'Enter PIN',
            back_callback=self.handle_back_pressed
        )
        
        # User context section
        user_context_section = self._create_user_context_section()
        
        # PIN input section
        pin_input_section = self._create_pin_input_section()
        
        # Keypad section
        keypad_section = self._create_keypad_section()
        
        # Instructions section
        instructions_section = self._create_instructions_section()
        
        # Assemble layout
        layout.add_widget(header)
        layout.add_widget(self.create_spacer(0.1))
        layout.add_widget(user_context_section)
        layout.add_widget(pin_input_section)
        layout.add_widget(self.create_spacer(0.1))
        layout.add_widget(keypad_section)
        layout.add_widget(instructions_section)
        layout.add_widget(self.create_spacer(0.3))
        
        self.add_widget(layout)
        self.layout_created = True
    
    def _create_user_context_section(self):
        """Create user context display"""
        user_context_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(70),
            spacing=ResponsiveUtils.spacing('small')
        )
        
        # User identification
        self.user_label = ResponsiveLabel(
            text=f'User: {self.current_user}',
            size_type='medium',
            color=Theme.get('on_surface_variant'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(40)
        )
        self.user_label.text_size = (None, None)
        
        # Context information
        context_label = ResponsiveLabel(
            text='Enter your 5-digit security PIN',
            size_type='normal',
            color=Theme.get('on_surface'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(30)
        )
        context_label.text_size = (None, None)
        
        user_context_section.add_widget(self.user_label)
        user_context_section.add_widget(context_label)
        
        return user_context_section
    
    def _create_pin_input_section(self):
        """Create PIN input display section"""
        pin_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(90)
        )
        
        # Center the PIN display
        pin_container.add_widget(Widget())
        
        # Secure PIN display
        self.pin_display = SecureTextInput(max_length=AppConfig.PIN_LENGTH)
        
        pin_container.add_widget(self.pin_display)
        pin_container.add_widget(Widget())
        
        return pin_container
    
    def _create_keypad_section(self):
        """Create keypad section"""
        keypad_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(360)
        )
        
        # Center the keypad
        keypad_container.add_widget(Widget())
        
        self.keypad = ResponsiveKeypad(callback=self.on_key_press)
        
        keypad_container.add_widget(self.keypad)
        keypad_container.add_widget(Widget())
        
        return keypad_container
    
    def _create_instructions_section(self):
        """Create instructions section"""
        instructions_section = ResponsiveLabel(
            text='Enter your PIN and press ENTER to continue.\\nPress CLEAR to reset your entry.',
            size_type='small',
            color=Theme.get('on_surface_variant'),
            halign='center',
            text_size=(ResponsiveUtils.responsive_dp(500), None),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(50)
        )
        
        return instructions_section
    
    def set_user(self, username):
        """Set current user for PIN entry"""
        self.current_user = username
        if self.user_label:
            self.user_label.text = f'User: {username}'
        
        self.log_user_action('pin_entry_user_set', {'user': username})
    
    def handle_back_pressed(self, button):
        """Handle back button press"""
        self.log_user_action('pin_entry_back_pressed')
        
        # Determine which screen to go back to based on user type
        if "biometric" in self.current_user.lower():
            self.navigate_to('biometric_scan', direction='right')
        else:
            self.navigate_to('card_scan', direction='right')
    
    def on_key_press(self, key):
        """Handle keypad key press"""
        if key == 'Clear':
            self.pin_value = ""
            self.pin_display.clear()
            self.log_user_action('pin_entry_cleared')
            
        elif key == 'Enter':
            if len(self.pin_value) == AppConfig.PIN_LENGTH:
                self.validate_pin()
            else:
                self.show_message(
                    "Incomplete PIN",
                    f"Please enter all {AppConfig.PIN_LENGTH} digits",
                    'warning',
                    2
                )
                
        elif key.isdigit() and len(self.pin_value) < AppConfig.PIN_LENGTH:
            self.pin_value += key
            self.pin_display.update_display(self.pin_value)
            
            # Log entry progress (without actual digits for security)
            self.log_user_action('pin_digit_entered', {
                'digits_entered': len(self.pin_value),
                'max_length': AppConfig.PIN_LENGTH
            })
    
    def validate_pin(self):
        """Validate entered PIN"""
        self.log_user_action('pin_validation_attempted')
        
        if self.pin_value == AppConfig.DEFAULT_PIN:
            # PIN is correct
            self.log_user_action('pin_validation_success')
            
            # Start user session
            app_state.start_session(
                self.current_user,
                'biometric' if 'biometric' in self.current_user.lower() else 'card'
            )
            
            # Show success message
            self.show_message(
                "Authentication Successful",
                "PIN accepted. Proceeding to activity code entry...",
                'success',
                2
            )
            
            # Navigate to activity code
            self.navigate_to('activity_code', direction='left')
            
        else:
            # PIN is incorrect
            self.failed_attempts += 1
            app_state.failed_attempts = self.failed_attempts
            
            self.log_user_action('pin_validation_failed', {
                'attempt_number': self.failed_attempts
            })
            
            if self.failed_attempts >= AppConfig.MAX_PIN_ATTEMPTS:
                # Too many failed attempts
                self.show_message(
                    "Access Denied",
                    f"Too many failed attempts. Returning to authentication selection.",
                    'error',
                    3
                )
                
                # Reset and return to auth selection
                self.reset_pin_entry()
                self.navigate_to('auth_selection', direction='right')
            else:
                # Show retry message
                remaining = AppConfig.MAX_PIN_ATTEMPTS - self.failed_attempts
                self.show_message(
                    "Authentication Error",
                    f"Invalid PIN. {remaining} attempts remaining.",
                    'error',
                    3
                )
                
                # Clear PIN for retry
                self.pin_value = ""
                self.pin_display.clear()
    
    def reset_pin_entry(self):
        """Reset PIN entry state"""
        self.pin_value = ""
        self.failed_attempts = 0
        if self.pin_display:
            self.pin_display.clear()
        
        self.log_user_action('pin_entry_reset')
    
    def on_screen_enter(self):
        """Called when screen becomes active"""
        super().on_screen_enter()
        self.reset_pin_entry()
    
    def cleanup(self):
        """Clean up PIN entry resources"""
        self.pin_value = ""
        super().cleanup()

class ActivityCodeScreen(BaseScreen):
    """
    Professional activity code entry screen
    
    Features:
    - Activity code input and validation
    - Professional keypad interface
    - Code length validation
    - Clear user guidance
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.activity_code = ""
        self.code_display = None
        self.keypad = None
        self.create_layout()
    
    def create_layout(self):
        """Create activity code entry interface"""
        self.clear_widgets()
        
        # Main container
        layout = BoxLayout(
            orientation='vertical',
            padding=ResponsiveUtils.spacing('large'),
            spacing=ResponsiveUtils.spacing('large')
        )
        
        # Apply themed background
        self.create_background(layout)
        
        # Create header
        header = self.create_header(
            'Activity Code',
            back_callback=self.handle_back_pressed
        )
        
        # Code input section
        code_section = self._create_code_input_section()
        
        # Keypad section
        keypad_section = self._create_keypad_section()
        
        # Instructions section
        instructions_section = self._create_instructions_section()
        
        # Assemble layout
        layout.add_widget(header)
        layout.add_widget(self.create_spacer(0.1))
        layout.add_widget(code_section)
        layout.add_widget(self.create_spacer(0.1))
        layout.add_widget(keypad_section)
        layout.add_widget(instructions_section)
        layout.add_widget(self.create_spacer(0.3))
        
        self.add_widget(layout)
        self.layout_created = True
    
    def _create_code_input_section(self):
        """Create activity code input section"""
        code_section = BoxLayout(
            orientation='vertical',
            spacing=ResponsiveUtils.spacing('medium'),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(140)
        )
        
        # Code input label
        code_label = ResponsiveLabel(
            text='Enter Activity Code:',
            size_type='medium',
            color=Theme.get('on_surface'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(40)
        )
        code_label.text_size = (None, None)
        
        # Code display container
        input_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(80)
        )
        
        # Center the code display
        input_container.add_widget(Widget())
        
        self.code_display = ResponsiveLabel(
            text='',
            size_type='xlarge',
            color=Theme.get('on_surface'),
            size_hint=(None, None),
            size=(ResponsiveUtils.responsive_dp(300), ResponsiveUtils.responsive_dp(70)),
            halign='center',
            valign='middle'
        )
        
        # Style the code display with background
        self._style_code_display()
        
        input_container.add_widget(self.code_display)
        input_container.add_widget(Widget())
        
        code_section.add_widget(code_label)
        code_section.add_widget(input_container)
        
        return code_section
    
    def _style_code_display(self):
        """Style the activity code display"""
        def update_display_graphics(*args):
            self.code_display.canvas.before.clear()
            with self.code_display.canvas.before:
                Color(*Theme.get('surface'))
                bg_rect = RoundedRectangle(
                    size=self.code_display.size,
                    pos=self.code_display.pos,
                    radius=[ResponsiveUtils.responsive_dp(12)]
                )
        
        self.code_display.bind(pos=update_display_graphics, size=update_display_graphics)
    
    def _create_keypad_section(self):
        """Create keypad section"""
        keypad_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(360)
        )
        
        # Center the keypad
        keypad_container.add_widget(Widget())
        
        self.keypad = ResponsiveKeypad(callback=self.on_key_press)
        
        keypad_container.add_widget(self.keypad)
        keypad_container.add_widget(Widget())
        
        return keypad_container
    
    def _create_instructions_section(self):
        """Create instructions section"""
        instructions_section = ResponsiveLabel(
            text=f'Enter your activity code ({AppConfig.MIN_ACTIVITY_CODE_LENGTH}-{AppConfig.MAX_ACTIVITY_CODE_LENGTH} digits) and press ENTER.\\nThis identifies your work order or activity.',
            size_type='small',
            color=Theme.get('on_surface_variant'),
            halign='center',
            text_size=(ResponsiveUtils.responsive_dp(500), None),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(60)
        )
        
        return instructions_section
    
    def handle_back_pressed(self, button):
        """Handle back button press"""
        self.log_user_action('activity_code_back_pressed')
        self.navigate_to('pin_entry', direction='right')
    
    def on_key_press(self, key):
        """Handle keypad key press"""
        if key == 'Clear':
            self.activity_code = ""
            self.code_display.text = ""
            self.log_user_action('activity_code_cleared')
            
        elif key == 'Enter':
            if self.activity_code:
                self.validate_activity_code()
            else:
                self.show_message(
                    "Missing Activity Code",
                    "Please enter an activity code before proceeding.",
                    'warning',
                    2
                )
                
        elif key.isdigit() and len(self.activity_code) < AppConfig.MAX_ACTIVITY_CODE_LENGTH:
            self.activity_code += key
            self.code_display.text = self.activity_code
            
            self.log_user_action('activity_code_digit_entered', {
                'code_length': len(self.activity_code),
                'max_length': AppConfig.MAX_ACTIVITY_CODE_LENGTH
            })
    
    def validate_activity_code(self):
        """Validate and process activity code"""
        code_length = len(self.activity_code)
        
        if code_length < AppConfig.MIN_ACTIVITY_CODE_LENGTH:
            self.show_message(
                "Code Too Short",
                f"Activity code must be at least {AppConfig.MIN_ACTIVITY_CODE_LENGTH} digits",
                'error',
                3
            )
            return
        
        # Code is valid
        app_state.activity_code = self.activity_code
        
        self.log_user_action('activity_code_accepted', {
            'code_length': code_length,
            'code': self.activity_code  # In production, consider not logging the actual code
        })
        
        # Show success and proceed
        self.show_message(
            "Activity Code Accepted",
            "Code validated. Accessing key cabinet system...",
            'success',
            2
        )
        
        # Complete the authentication flow
        if self.navigation_manager:
            self.navigation_manager.complete_activity_session()
        else:
            # Fallback: return to main
            self.navigate_home()
    
    def on_screen_enter(self):
        """Called when screen becomes active"""
        super().on_screen_enter()
        self.activity_code = ""
        if self.code_display:
            self.code_display.text = ""
    
    def cleanup(self):
        """Clean up activity code resources"""
        self.activity_code = ""
        super().cleanup()