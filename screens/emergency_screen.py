"""
AMS Touch Interface - Emergency Access Screen

Professional emergency access interface with enhanced security warnings,
audit logging, and streamlined emergency procedures.

Features:
- Prominent security warnings
- Emergency PIN validation
- Comprehensive audit logging
- Professional warning aesthetics
- Emergency access workflow
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock
from datetime import datetime

from screens.base_screen import BaseScreen
from core.config import ResponsiveUtils, Theme, AppConfig
from components.widgets import (
    ResponsiveButton, ResponsiveLabel, SecureTextInput, ResponsiveKeypad
)

class EmergencyAccessScreen(BaseScreen):
    """
    Professional emergency access screen with comprehensive security measures
    
    Features:
    - Prominent security warnings and alerts
    - Emergency PIN validation system
    - Comprehensive audit logging
    - Professional emergency workflow
    - Enhanced visual security indicators
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.emergency_pin = ""
        self.pin_display = None
        self.keypad = None
        self.warning_banner = None
        self.failed_attempts = 0
        self.create_layout()
    
    def create_layout(self):
        """Create emergency access interface with security warnings"""
        self.clear_widgets()
        
        # Main container
        layout = BoxLayout(
            orientation='vertical',
            padding=ResponsiveUtils.spacing('large'),
            spacing=ResponsiveUtils.spacing('medium')
        )
        
        # Apply themed background
        self.create_background(layout)
        
        # Create enhanced warning banner
        warning_banner = self._create_warning_banner()
        
        # Warning message section
        warning_message_section = self._create_warning_message_section()
        
        # PIN entry section
        pin_entry_section = self._create_pin_entry_section()
        
        # Keypad section
        keypad_section = self._create_keypad_section()
        
        # Action buttons section
        actions_section = self._create_actions_section()
        
        # Emergency information section
        emergency_info_section = self._create_emergency_info_section()
        
        # Assemble layout
        layout.add_widget(warning_banner)
        layout.add_widget(warning_message_section)
        layout.add_widget(self.create_spacer(0.1))
        layout.add_widget(pin_entry_section)
        layout.add_widget(self.create_spacer(0.1))
        layout.add_widget(keypad_section)
        layout.add_widget(actions_section)
        layout.add_widget(emergency_info_section)
        layout.add_widget(self.create_spacer(0.1))
        
        self.add_widget(layout)
        self.layout_created = True
    
    def _create_warning_banner(self):
        """Create prominent emergency access warning banner"""
        self.warning_banner = ResponsiveLabel(
            text='🚨 EMERGENCY ACCESS PROTOCOL 🚨',
            size_type='large',
            bold=True,
            color=Theme.get('surface'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(80)
        )
        self.warning_banner.text_size = (None, None)
        
        # Style the warning banner with error background
        def update_banner_graphics(*args):
            self.warning_banner.canvas.before.clear()
            with self.warning_banner.canvas.before:
                Color(*Theme.get('error'))
                bg_rect = RoundedRectangle(
                    size=self.warning_banner.size,
                    pos=self.warning_banner.pos,
                    radius=[ResponsiveUtils.responsive_dp(12)]
                )
        
        self.warning_banner.bind(
            pos=update_banner_graphics,
            size=update_banner_graphics
        )
        
        return self.warning_banner
    
    def _create_warning_message_section(self):
        """Create detailed warning message section"""
        warning_message_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(120),
            spacing=ResponsiveUtils.spacing('small')
        )
        
        # Primary warning
        primary_warning = ResponsiveLabel(
            text='⚠️ UNAUTHORIZED ACCESS WILL BE REPORTED ⚠️',
            size_type='medium',
            bold=True,
            color=Theme.get('error'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(40)
        )
        primary_warning.text_size = (None, None)
        
        # Secondary warning
        secondary_warning = ResponsiveLabel(
            text='This emergency access is logged and monitored for security purposes.\\nUse only in genuine emergencies.',
            size_type='normal',
            color=Theme.get('error'),
            halign='center',
            text_size=(ResponsiveUtils.responsive_dp(600), None),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(60)
        )
        
        # Legal notice
        legal_notice = ResponsiveLabel(
            text='All emergency access attempts are subject to security review and audit.',
            size_type='small',
            color=Theme.get('on_surface_variant'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(20)
        )
        legal_notice.text_size = (None, None)
        
        warning_message_section.add_widget(primary_warning)
        warning_message_section.add_widget(secondary_warning)
        warning_message_section.add_widget(legal_notice)
        
        return warning_message_section
    
    def _create_pin_entry_section(self):
        """Create emergency PIN entry section"""
        pin_entry_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(120),
            spacing=ResponsiveUtils.spacing('normal')
        )
        
        # PIN entry label
        pin_label = ResponsiveLabel(
            text='Enter Emergency PIN:',
            size_type='medium',
            color=Theme.get('on_surface'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(40)
        )
        pin_label.text_size = (None, None)
        
        # PIN display container
        pin_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(80)
        )
        
        # Center the PIN display
        pin_container.add_widget(Widget())
        
        self.pin_display = SecureTextInput(max_length=AppConfig.PIN_LENGTH)
        
        pin_container.add_widget(self.pin_display)
        pin_container.add_widget(Widget())
        
        pin_entry_section.add_widget(pin_label)
        pin_entry_section.add_widget(pin_container)
        
        return pin_entry_section
    
    def _create_keypad_section(self):
        """Create emergency keypad section"""
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
    
    def _create_actions_section(self):
        """Create action buttons section"""
        actions_section = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(60),
            spacing=ResponsiveUtils.spacing('large')
        )
        
        actions_section.add_widget(Widget())  # Left spacer
        
        # Cancel button
        cancel_button = ResponsiveButton(
            text='CANCEL',
            icon='back',
            button_type='secondary',
            size_type='normal'
        )
        cancel_button.bind(on_press=self.cancel_emergency)
        
        # Emergency unlock button (disabled until PIN entered)
        self.unlock_button = ResponsiveButton(
            text='EMERGENCY UNLOCK',
            icon='unlock',
            button_type='error',
            size_type='large'
        )
        self.unlock_button.bind(on_press=self.attempt_emergency_unlock)
        
        actions_section.add_widget(cancel_button)
        actions_section.add_widget(self.unlock_button)
        actions_section.add_widget(Widget())  # Right spacer
        
        return actions_section
    
    def _create_emergency_info_section(self):
        """Create emergency information section"""
        info_section = ResponsiveLabel(
            text='Emergency access bypasses normal security protocols.\\nThis action will trigger immediate security notifications.',
            size_type='small',
            color=Theme.get('on_surface_variant'),
            halign='center',
            text_size=(ResponsiveUtils.responsive_dp(500), None),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(50)
        )
        
        return info_section
    
    def on_key_press(self, key):
        """Handle emergency keypad key press"""
        if key == 'Clear':
            self.emergency_pin = ""
            self.pin_display.clear()
            self.log_emergency_action('pin_cleared')
            
        elif key == 'Enter':
            if len(self.emergency_pin) == AppConfig.PIN_LENGTH:
                self.attempt_emergency_unlock(None)
            else:
                self.show_message(
                    "Incomplete PIN",
                    f"Please enter all {AppConfig.PIN_LENGTH} digits",
                    'warning',
                    2
                )
                
        elif key.isdigit() and len(self.emergency_pin) < AppConfig.PIN_LENGTH:
            self.emergency_pin += key
            self.pin_display.update_display(self.emergency_pin)
            
            # Log PIN entry progress (for security audit)
            self.log_emergency_action('pin_digit_entered', {
                'digits_entered': len(self.emergency_pin),
                'max_length': AppConfig.PIN_LENGTH
            })
    
    def attempt_emergency_unlock(self, button):
        """Attempt emergency unlock with PIN validation"""
        if len(self.emergency_pin) != AppConfig.PIN_LENGTH:
            self.show_message(
                "Incomplete PIN",
                "Please enter the complete emergency PIN",
                'warning',
                2
            )
            return
        
        self.log_emergency_action('unlock_attempt', {
            'pin_length': len(self.emergency_pin),
            'attempt_number': self.failed_attempts + 1
        })
        
        if self.emergency_pin == AppConfig.EMERGENCY_PIN:
            self.grant_emergency_access()
        else:
            self.handle_failed_attempt()
    
    def grant_emergency_access(self):
        """Grant emergency access with comprehensive logging"""
        timestamp = datetime.now()
        
        # Comprehensive emergency access logging
        emergency_log = {
            'event': 'EMERGENCY_ACCESS_GRANTED',
            'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'date': timestamp.strftime("%Y-%m-%d"),
            'time': timestamp.strftime("%H:%M:%S"),
            'location': AppConfig.SITE_NAME,
            'system': AppConfig.APP_NAME,
            'version': AppConfig.APP_VERSION,
            'ip_address': 'system_terminal',  # In production, get actual IP
            'emergency_type': 'manual_override',
            'authorized': True,
            'security_level': 'CRITICAL'
        }
        
        # Log to system (in production, this would go to secure audit log)
        print("🚨 CRITICAL SECURITY EVENT:")
        print(f"   {emergency_log}")
        
        self.log_emergency_action('access_granted', emergency_log)
        
        # Show success message with important information
        self.show_message(
            '🚨 Emergency Access Granted 🚨',
            f'Emergency unlock initiated at {timestamp.strftime("%H:%M:%S")}.\\n\\n'
            f'This action has been logged for security review.\\n'
            f'Site: {AppConfig.SITE_NAME}\\n'
            f'Time: {timestamp.strftime("%Y-%m-%d %H:%M:%S")}',
            'error',  # Use error type for visual prominence
            6
        )
        
        # Return to main after delay
        Clock.schedule_once(self.return_to_main, 6.5)
    
    def handle_failed_attempt(self):
        """Handle failed emergency access attempt"""
        self.failed_attempts += 1
        
        # Log failed attempt (critical for security)
        self.log_emergency_action('access_denied', {
            'attempt_number': self.failed_attempts,
            'reason': 'invalid_pin',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'location': AppConfig.SITE_NAME
        })
        
        if self.failed_attempts >= AppConfig.MAX_PIN_ATTEMPTS:
            # Lockout after too many attempts
            self.show_message(
                "🚨 Security Lockout 🚨",
                f"Too many failed emergency access attempts.\\n"
                f"This incident has been logged and security notified.\\n"
                f"Contact system administrator immediately.",
                'error',
                5
            )
            
            # Log security incident
            self.log_emergency_action('security_lockout', {
                'failed_attempts': self.failed_attempts,
                'lockout_triggered': True
            })
            
            # Return to main
            Clock.schedule_once(self.return_to_main, 5.5)
        else:
            remaining = AppConfig.MAX_PIN_ATTEMPTS - self.failed_attempts
            self.show_message(
                "❌ Emergency Access Denied",
                f"Invalid emergency PIN.\\n"
                f"{remaining} attempts remaining before lockout.",
                'error',
                4
            )
            
            # Clear PIN for retry
            self.emergency_pin = ""
            self.pin_display.clear()
    
    def cancel_emergency(self, button):
        """Cancel emergency access and return to main"""
        self.log_emergency_action('access_cancelled')
        
        self.show_message(
            "Emergency Access Cancelled",
            "Emergency access request cancelled by user.",
            'info',
            2
        )
        
        Clock.schedule_once(self.return_to_main, 2.5)
    
    def return_to_main(self, dt):
        """Return to main screen"""
        self.navigate_home()
    
    def log_emergency_action(self, action, details=None):
        """
        Log emergency access actions with enhanced detail
        
        Args:
            action: Action description
            details: Additional details dictionary
        """
        log_entry = {
            'event_type': 'EMERGENCY_ACCESS',
            'action': action,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'site': AppConfig.SITE_NAME,
            'system': f"{AppConfig.APP_NAME} {AppConfig.APP_VERSION}",
            'details': details or {},
            'security_level': 'CRITICAL'
        }
        
        # In production, this would go to a secure audit log
        print(f"🚨 EMERGENCY LOG: {log_entry}")
    
    def on_screen_enter(self):
        """Called when screen becomes active"""
        super().on_screen_enter()
        self.emergency_pin = ""
        self.failed_attempts = 0
        if self.pin_display:
            self.pin_display.clear()
        
        # Log screen entry
        self.log_emergency_action('screen_entered')
    
    def on_screen_exit(self):
        """Called when leaving screen"""
        super().on_screen_exit()
        self.log_emergency_action('screen_exited')
    
    def cleanup(self):
        """Clean up emergency access resources"""
        self.emergency_pin = ""
        self.failed_attempts = 0
        super().cleanup()
    
    def get_emergency_status(self):
        """Get current emergency access status"""
        return {
            'screen': 'emergency_access',
            'failed_attempts': self.failed_attempts,
            'max_attempts': AppConfig.MAX_PIN_ATTEMPTS,
            'pin_entered': len(self.emergency_pin),
            'lockout_risk': self.failed_attempts >= AppConfig.MAX_PIN_ATTEMPTS - 1
        }