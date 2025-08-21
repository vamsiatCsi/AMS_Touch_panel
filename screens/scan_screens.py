"""
AMS Touch Interface - Scanning Screens

Professional card and biometric scanning interfaces with enhanced
visual feedback, animations, and user guidance.

Features:
- Card reader simulation with visual feedback
- Biometric scanner with fingerprint visualization  
- Animated scanning indicators
- Professional device imagery
- Status feedback and error handling
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock

from screens.base_screen import BaseScreen
from core.config import ResponsiveUtils, Theme, AppConfig
from components.widgets import (
    ResponsiveButton, ResponsiveLabel, ScanningBar, ScannerImage
)

class CardScanScreen(BaseScreen):
    """
    Professional card scanning screen with enhanced animations
    
    Features:
    - Visual card reader representation
    - Animated scanning feedback
    - Clear user instructions
    - Professional status updates
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scanning = False
        self.scanner_image = None
        self.scanning_bar = None
        self.instruction_label = None
        self.status_label = None
        self.create_layout()
    
    def create_layout(self):
        """Create card scanning interface"""
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
            'Card Authentication',
            back_callback=self.handle_back_pressed
        )
        
        # Scanning section
        scan_section = self._create_scan_section()
        
        # Action section
        action_section = self._create_action_section()
        
        # Assemble layout
        layout.add_widget(header)
        layout.add_widget(self.create_spacer(0.1))
        layout.add_widget(scan_section)
        layout.add_widget(self.create_spacer(0.2))
        layout.add_widget(action_section)
        layout.add_widget(self.create_spacer(0.3))
        
        self.add_widget(layout)
        self.layout_created = True
    
    def _create_scan_section(self):
        """Create card scanning visualization section"""
        scan_section = BoxLayout(
            orientation='vertical',
            spacing=ResponsiveUtils.spacing('large'),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(450)
        )
        
        # Scanner container with device visualization
        scanner_container = FloatLayout(
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(280)
        )
        
        # Scanner device image
        self.scanner_image = ScannerImage(
            scan_type='card',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        scanner_container.add_widget(self.scanner_image)
        
        # Scanning overlay animation
        self.scanning_bar = ScanningBar(
            scan_type='card',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        scanner_container.add_widget(self.scanning_bar)
        
        # User instructions
        self.instruction_label = ResponsiveLabel(
            text='Hold card near the reader',
            size_type='large',
            color=Theme.get('on_surface'),
            bold=True,
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(50)
        )
        self.instruction_label.text_size = (None, None)
        
        # Status display
        self.status_label = ResponsiveLabel(
            text='Ready to scan card...',
            size_type='normal',
            color=Theme.get('on_surface_variant'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(40)
        )
        self.status_label.text_size = (None, None)
        
        # Additional instructions
        help_label = ResponsiveLabel(
            text='Present your authorized access card or badge to the reader.\\nEnsure the card is clean and properly oriented.',
            size_type='small',
            color=Theme.get('on_surface_variant'),
            halign='center',
            text_size=(ResponsiveUtils.responsive_dp(500), None),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(60)
        )
        
        scan_section.add_widget(scanner_container)
        scan_section.add_widget(self.instruction_label)
        scan_section.add_widget(self.status_label)
        scan_section.add_widget(help_label)
        
        return scan_section
    
    def _create_action_section(self):
        """Create action buttons section"""
        action_section = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(70)
        )
        
        action_section.add_widget(Widget())  # Left spacer
        
        # Simulate scan button (for demonstration)
        simulate_button = ResponsiveButton(
            text='SIMULATE SCAN',
            icon='scan',
            button_type='success',
            size_type='medium'
        )
        simulate_button.bind(on_press=self.simulate_card_scan)
        
        action_section.add_widget(simulate_button)
        action_section.add_widget(Widget())  # Right spacer
        
        return action_section
    
    def handle_back_pressed(self, button):
        """Handle back button press"""
        self.log_user_action('card_scan_back_pressed')
        self.navigate_to('auth_selection', direction='right')
    
    def simulate_card_scan(self, button):
        """Simulate card scanning process"""
        if not self.scanning:
            self.log_user_action('card_scan_simulated')
            self.start_scanning()
    
    def start_scanning(self):
        """Start card scanning animation and process"""
        self.scanning = True
        
        # Update UI state
        self.status_label.text = 'Scanning card...'
        self.status_label.color = Theme.get('warning')
        self.instruction_label.text = 'Please wait...'
        
        # Start scanning animation
        self.scanning_bar.start_scanning()
        
        # Schedule scan completion
        Clock.schedule_once(self.complete_scan, AppConfig.SCAN_ANIMATION_SECONDS)
    
    def complete_scan(self, dt):
        """Complete card scanning process"""
        # Stop scanning animation
        self.scanning_bar.stop_scanning()
        
        # Update UI with success
        self.status_label.text = 'Card recognized: Authorized User'
        self.status_label.color = Theme.get('success')
        self.instruction_label.text = 'Card accepted'
        
        self.log_user_action('card_scan_completed', {'result': 'success'})
        
        # Proceed to PIN entry
        Clock.schedule_once(self.proceed_to_pin, 1.5)
    
    def proceed_to_pin(self, dt):
        """Proceed to PIN entry screen"""
        # Set user context for PIN screen
        if self.navigation_manager:
            pin_screen = self.navigation_manager.get_screen('pin_entry')
            if pin_screen and hasattr(pin_screen, 'set_user'):
                pin_screen.set_user('Card User')
        
        self.navigate_to('pin_entry', direction='left')
    
    def on_screen_enter(self):
        """Called when screen becomes active"""
        super().on_screen_enter()
        self.scanning = False
        if self.status_label:
            self.status_label.text = 'Ready to scan card...'
            self.status_label.color = Theme.get('on_surface_variant')
        if self.instruction_label:
            self.instruction_label.text = 'Hold card near the reader'
    
    def cleanup(self):
        """Clean up scanning resources"""
        if self.scanning_bar:
            self.scanning_bar.stop_scanning()
        self.scanning = False
        super().cleanup()

class BiometricScanScreen(BaseScreen):
    """
    Professional biometric scanning screen with fingerprint visualization
    
    Features:
    - Fingerprint scanner representation
    - Animated biometric scanning
    - Professional visual feedback
    - Status updates and guidance
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scanning = False
        self.scanner_image = None
        self.scanning_bar = None
        self.instruction_label = None
        self.status_label = None
        self.create_layout()
    
    def create_layout(self):
        """Create biometric scanning interface"""
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
            'Biometric Authentication',
            back_callback=self.handle_back_pressed
        )
        
        # Scanning section
        scan_section = self._create_scan_section()
        
        # Action section
        action_section = self._create_action_section()
        
        # Assemble layout
        layout.add_widget(header)
        layout.add_widget(self.create_spacer(0.05))
        layout.add_widget(scan_section)
        layout.add_widget(self.create_spacer(0.15))
        layout.add_widget(action_section)
        layout.add_widget(self.create_spacer(0.25))
        
        self.add_widget(layout)
        self.layout_created = True
    
    def _create_scan_section(self):
        """Create biometric scanning visualization section"""
        scan_section = BoxLayout(
            orientation='vertical',
            spacing=ResponsiveUtils.spacing('large'),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(500)
        )
        
        # Scanner container with fingerprint visualization
        scanner_container = FloatLayout(
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(320)
        )
        
        # Fingerprint scanner image
        self.scanner_image = ScannerImage(
            scan_type='fingerprint',
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        scanner_container.add_widget(self.scanner_image)
        
        # Scanning overlay animation
        self.scanning_bar = ScanningBar(
            scan_type='biometric',
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        scanner_container.add_widget(self.scanning_bar)
        
        # User instructions
        self.instruction_label = ResponsiveLabel(
            text='Place finger on scanner',
            size_type='large',
            color=Theme.get('on_surface'),
            bold=True,
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(50)
        )
        self.instruction_label.text_size = (None, None)
        
        # Status display
        self.status_label = ResponsiveLabel(
            text='Ready to scan fingerprint...',
            size_type='normal',
            color=Theme.get('on_surface_variant'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(40)
        )
        self.status_label.text_size = (None, None)
        
        # Detailed instructions
        help_label = ResponsiveLabel(
            text='Place your finger firmly on the biometric scanner.\\nEnsure your finger is clean and dry for optimal scanning.',
            size_type='small',
            color=Theme.get('on_surface_variant'),
            halign='center',
            text_size=(ResponsiveUtils.responsive_dp(500), None),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(60)
        )
        
        scan_section.add_widget(scanner_container)
        scan_section.add_widget(self.instruction_label)
        scan_section.add_widget(self.status_label)
        scan_section.add_widget(help_label)
        
        return scan_section
    
    def _create_action_section(self):
        """Create action buttons section"""
        action_section = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(70)
        )
        
        action_section.add_widget(Widget())  # Left spacer
        
        # Simulate scan button (for demonstration)
        simulate_button = ResponsiveButton(
            text='SIMULATE SCAN',
            icon='fingerprint',
            button_type='success',
            size_type='medium'
        )
        simulate_button.bind(on_press=self.simulate_biometric_scan)
        
        action_section.add_widget(simulate_button)
        action_section.add_widget(Widget())  # Right spacer
        
        return action_section
    
    def handle_back_pressed(self, button):
        """Handle back button press"""
        self.log_user_action('biometric_scan_back_pressed')
        self.navigate_to('auth_selection', direction='right')
    
    def simulate_biometric_scan(self, button):
        """Simulate biometric scanning process"""
        if not self.scanning:
            self.log_user_action('biometric_scan_simulated')
            self.start_scanning()
    
    def start_scanning(self):
        """Start biometric scanning animation and process"""
        self.scanning = True
        
        # Update UI state
        self.status_label.text = 'Scanning fingerprint...'
        self.status_label.color = Theme.get('warning')
        self.instruction_label.text = 'Keep finger steady...'
        
        # Start scanning animation
        self.scanning_bar.start_scanning()
        
        # Schedule scan completion (biometric takes slightly longer)
        Clock.schedule_once(self.complete_scan, AppConfig.SCAN_ANIMATION_SECONDS + 1)
    
    def complete_scan(self, dt):
        """Complete biometric scanning process"""
        # Stop scanning animation
        self.scanning_bar.stop_scanning()
        
        # Update UI with success
        self.status_label.text = 'Fingerprint recognized: Authorized User'
        self.status_label.color = Theme.get('success')
        self.instruction_label.text = 'Biometric accepted'
        
        self.log_user_action('biometric_scan_completed', {'result': 'success'})
        
        # Proceed to PIN entry
        Clock.schedule_once(self.proceed_to_pin, 1.5)
    
    def proceed_to_pin(self, dt):
        """Proceed to PIN entry screen"""
        # Set user context for PIN screen
        if self.navigation_manager:
            pin_screen = self.navigation_manager.get_screen('pin_entry')
            if pin_screen and hasattr(pin_screen, 'set_user'):
                pin_screen.set_user('Biometric User')
        
        self.navigate_to('pin_entry', direction='left')
    
    def on_screen_enter(self):
        """Called when screen becomes active"""
        super().on_screen_enter()
        self.scanning = False
        if self.status_label:
            self.status_label.text = 'Ready to scan fingerprint...'
            self.status_label.color = Theme.get('on_surface_variant')
        if self.instruction_label:
            self.instruction_label.text = 'Place finger on scanner'
    
    def cleanup(self):
        """Clean up scanning resources"""
        if self.scanning_bar:
            self.scanning_bar.stop_scanning()
        self.scanning = False
        super().cleanup()