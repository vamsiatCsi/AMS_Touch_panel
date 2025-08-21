"""
AMS Touch Interface - Authentication Selection Screen

Professional authentication selection interface allowing users to choose
between card-based and biometric authentication methods.

Features:
- Visual authentication method selection
- Large touch-friendly buttons
- Professional layout and theming
- Clear navigation flow
- User guidance and instructions
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from screens.base_screen import BaseScreen
from core.config import ResponsiveUtils, Theme
from components.widgets import ResponsiveButton, ResponsiveLabel

class AuthSelectionScreen(BaseScreen):
    """
    Professional authentication selection screen
    
    Provides an intuitive interface for users to select their preferred
    authentication method with clear visual hierarchy and guidance.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_layout()
    
    def create_layout(self):
        """Create authentication selection layout"""
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
            'Authentication Method',
            back_callback=self.handle_back_pressed
        )
        
        # Instructions section
        instructions_section = self._create_instructions_section()
        
        # Authentication options
        options_section = self._create_options_section()
        
        # Assemble layout
        layout.add_widget(header)
        layout.add_widget(self.create_spacer(0.1))
        layout.add_widget(instructions_section)
        layout.add_widget(self.create_spacer(0.2))
        layout.add_widget(options_section)
        layout.add_widget(self.create_spacer(0.7))
        
        self.add_widget(layout)
        self.layout_created = True
    
    def _create_instructions_section(self):
        """Create instructions for authentication selection"""
        instructions_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(80),
            spacing=ResponsiveUtils.spacing('small')
        )
        
        # Main instruction
        main_instruction = ResponsiveLabel(
            text='Please select your authentication method:',
            size_type='medium',
            color=Theme.get('on_surface'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(40)
        )
        main_instruction.text_size = (None, None)
        
        # Secondary instruction
        secondary_instruction = ResponsiveLabel(
            text='Choose the method you have been authorized to use',
            size_type='normal',
            color=Theme.get('on_surface_variant'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(30)
        )
        secondary_instruction.text_size = (None, None)
        
        instructions_section.add_widget(main_instruction)
        instructions_section.add_widget(secondary_instruction)
        
        return instructions_section
    
    def _create_options_section(self):
        """Create authentication method options"""
        options_section = BoxLayout(
            orientation='horizontal',
            spacing=ResponsiveUtils.spacing('xlarge'),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(350)
        )
        
        # Center the options
        options_section.add_widget(Widget())
        
        # Card authentication option
        card_option = self._create_card_option()
        
        # Biometric authentication option
        biometric_option = self._create_biometric_option()
        
        options_section.add_widget(card_option)
        options_section.add_widget(biometric_option)
        options_section.add_widget(Widget())
        
        return options_section
    
    def _create_card_option(self):
        """Create card authentication option"""
        card_option = BoxLayout(
            orientation='vertical',
            spacing=ResponsiveUtils.spacing('medium'),
            size_hint_x=None,
            width=ResponsiveUtils.responsive_dp(280)
        )
        
        # Card button
        card_button = ResponsiveButton(
            text='CARD',
            icon='card',
            button_type='primary',
            size_type='xlarge',
            size=(ResponsiveUtils.responsive_dp(250), ResponsiveUtils.responsive_dp(200))
        )
        card_button.bind(on_press=self.select_card_auth)
        
        # Card label
        card_label = ResponsiveLabel(
            text='Card Access',
            size_type='large',
            bold=True,
            color=Theme.get('on_surface'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(40)
        )
        card_label.text_size = (None, None)
        
        # Card description
        card_description = ResponsiveLabel(
            text='Use your authorized\\naccess card or badge',
            size_type='normal',
            color=Theme.get('on_surface_variant'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(60)
        )
        card_description.text_size = (ResponsiveUtils.responsive_dp(250), None)
        
        # Center the button
        button_container = self.create_centered_container(card_button)
        
        card_option.add_widget(button_container)
        card_option.add_widget(card_label)
        card_option.add_widget(card_description)
        
        return card_option
    
    def _create_biometric_option(self):
        """Create biometric authentication option"""
        biometric_option = BoxLayout(
            orientation='vertical',
            spacing=ResponsiveUtils.spacing('medium'),
            size_hint_x=None,
            width=ResponsiveUtils.responsive_dp(280)
        )
        
        # Biometric button
        biometric_button = ResponsiveButton(
            text='SCAN',
            icon='fingerprint',
            button_type='primary',
            size_type='xlarge',
            size=(ResponsiveUtils.responsive_dp(250), ResponsiveUtils.responsive_dp(200))
        )
        biometric_button.bind(on_press=self.select_biometric_auth)
        
        # Biometric label
        biometric_label = ResponsiveLabel(
            text='Biometric Access',
            size_type='large',
            bold=True,
            color=Theme.get('on_surface'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(40)
        )
        biometric_label.text_size = (None, None)
        
        # Biometric description
        biometric_description = ResponsiveLabel(
            text='Use your fingerprint\\nor biometric scanner',
            size_type='normal',
            color=Theme.get('on_surface_variant'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(60)
        )
        biometric_description.text_size = (ResponsiveUtils.responsive_dp(250), None)
        
        # Center the button
        button_container = self.create_centered_container(biometric_button)
        
        biometric_option.add_widget(button_container)
        biometric_option.add_widget(biometric_label)
        biometric_option.add_widget(biometric_description)
        
        return biometric_option
    
    def handle_back_pressed(self, button):
        """Handle back button press"""
        self.log_user_action('auth_selection_back_pressed')
        self.navigate_home()
    
    def select_card_auth(self, button):
        """Handle card authentication selection"""
        self.log_user_action('card_auth_selected')
        
        # Show selection feedback
        self.show_message(
            'Card Authentication',
            'Proceeding to card scanner...',
            'info',
            1
        )
        
        # Navigate to card scanning
        self.navigate_to('card_scan', direction='left')
    
    def select_biometric_auth(self, button):
        """Handle biometric authentication selection"""
        self.log_user_action('biometric_auth_selected')
        
        # Show selection feedback
        self.show_message(
            'Biometric Authentication',
            'Proceeding to biometric scanner...',
            'info',
            1
        )
        
        # Navigate to biometric scanning
        self.navigate_to('biometric_scan', direction='left')
    
    def on_screen_enter(self):
        """Called when screen becomes active"""
        super().on_screen_enter()
        self.log_user_action('auth_selection_entered')
    
    def on_screen_exit(self):
        """Called when leaving screen"""
        super().on_screen_exit()
        self.log_user_action('auth_selection_exited')
    
    def get_available_methods(self):
        """Get list of available authentication methods"""
        return [
            {
                'method': 'card',
                'display_name': 'Card Access',
                'description': 'Use authorized access card or badge',
                'icon': 'card',
                'enabled': True
            },
            {
                'method': 'biometric',
                'display_name': 'Biometric Access', 
                'description': 'Use fingerprint or biometric scanner',
                'icon': 'fingerprint',
                'enabled': True
            }
        ]
    
    def show_method_info(self, method):
        """Show detailed information about authentication method"""
        methods_info = {
            'card': {
                'title': 'Card Authentication',
                'message': 'Present your authorized access card or badge to the card reader. Ensure the card is valid and not damaged.',
                'type': 'info'
            },
            'biometric': {
                'title': 'Biometric Authentication',
                'message': 'Place your finger firmly on the biometric scanner. Ensure your finger is clean and dry for best results.',
                'type': 'info'
            }
        }
        
        if method in methods_info:
            info = methods_info[method]
            self.show_message(info['title'], info['message'], info['type'], 4)