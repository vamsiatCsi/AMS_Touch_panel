"""
AMS Touch Interface - Main Idle Screen (Updated Layout)

Professional main idle screen providing the primary interface and
entry point for the Activity Monitoring System.

Features:
- Site identification and real-time clock
- System status indicators
- Primary action button for starting sessions
- Theme toggle and configuration access
- Emergency access (positioned at bottom)
- Professional layout matching target design
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock

from screens.base_screen import BaseScreen
from core.config import Theme, ResponsiveUtils, AppConfig, app_state
from components.widgets import (
    ResponsiveButton, ResponsiveLabel, StatusIndicator
)

class MainIdleScreen(BaseScreen):
    """
    Professional main idle screen
    
    Serves as the primary interface with enhanced layout design,
    real-time updates, and professional visual hierarchy.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.datetime_label = None
        self.main_layout = None
        self.create_layout()
        
        # Schedule real-time clock updates
        Clock.schedule_interval(self.update_datetime, 1)
    
    def create_layout(self):
        """Create enhanced main screen layout with professional design"""
        self.clear_widgets()
        
        # Main container
        main_layout = BoxLayout(
            orientation='vertical',
            padding=ResponsiveUtils.spacing('large'),
            spacing=ResponsiveUtils.spacing('medium')
        )
        
        # Apply themed background
        self.create_background(main_layout)
        
        # Build layout sections
        header_section = self._create_header_section()
        status_section = self._create_status_section()
        main_action_section = self._create_main_action_section()
        control_section = self._create_control_section()
        emergency_section = self._create_emergency_section()
        footer_section = self._create_footer_section()
        
        # Assemble layout with adjusted spacing to match target design
        main_layout.add_widget(self.create_spacer(0.1))  # Reduced top spacer
        main_layout.add_widget(header_section)
        main_layout.add_widget(self.create_spacer(0.15))
        main_layout.add_widget(status_section)
        main_layout.add_widget(self.create_spacer(0.1))  # Reduced spacer
        main_layout.add_widget(main_action_section)
        main_layout.add_widget(self.create_spacer(0.15))
        main_layout.add_widget(control_section)
        main_layout.add_widget(self.create_spacer(0.2))  # Reduced spacer
        main_layout.add_widget(emergency_section)
        main_layout.add_widget(self.create_spacer(0.05))  # Small spacer before footer
        main_layout.add_widget(footer_section)
        
        self.add_widget(main_layout)
        self.main_layout = main_layout
        self.layout_created = True
    
    def _create_header_section(self):
        """Create clean header with site info and real-time clock"""
        header_section = BoxLayout(
            orientation='vertical',
            spacing=ResponsiveUtils.spacing('small'),  # Reduced spacing
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(200)  # Reduced height
        )
        
        # Site identification - larger and more prominent
        site_label = ResponsiveLabel(
            text=AppConfig.SITE_NAME,
            size_type='hero',  # Keep large size
            bold=True,
            color=Theme.get('on_surface'),  # Use primary text color
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(80)  # Increased height for site name
        )
        site_label.text_size = (None, None)
        
        # Real-time clock display - smaller and more subdued
        self.datetime_label = ResponsiveLabel(
            text=AppConfig.get_datetime_string(),
            size_type='medium',  # Reduced from large
            color=Theme.get('on_surface_variant'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(50)  # Reduced height
        )
        self.datetime_label.text_size = (None, None)
        
        header_section.add_widget(site_label)
        header_section.add_widget(self.datetime_label)
        
        return header_section
    
    def _create_status_section(self):
        """Create enhanced system status display"""
        status_section = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=ResponsiveUtils.responsive_dp(60)  # Reduced height
        )
        
        # Center the status content
        status_section.add_widget(Widget())  # Left spacer
        
        status_content = BoxLayout(
            orientation='horizontal',
            spacing=ResponsiveUtils.spacing('small'),  # Reduced spacing
            size_hint=(None, None),
            size=(ResponsiveUtils.responsive_dp(200), ResponsiveUtils.responsive_dp(40))
        )
        
        # Status indicator - smaller
        status_indicator = StatusIndicator(
            status='active',
            size_type='tiny'
        )
        status_indicator.pos_hint = {'center_y': 0.5}
        
        # Status text
        status_label = ResponsiveLabel(
            text='System Ready',
            size_type='medium',  # Reduced from large
            color=Theme.get('success'),
            bold=True,
            valign='middle'
        )
        
        status_content.add_widget(status_indicator)
        status_content.add_widget(status_label)
        
        status_section.add_widget(status_content)
        status_section.add_widget(Widget())  # Right spacer
        
        return status_section
    
    def _create_main_action_section(self):
        """Create primary action button"""
        main_action_section = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(80)  # Reduced height
        )
        
        # Center the start button
        main_action_section.add_widget(Widget())
        
        start_button = ResponsiveButton(
            text='TAP TO START',
            button_type='primary',
            size_type='large',  # Reduced from xlarge
            font_size=ResponsiveUtils.font_size('medium')  # Reduced font size
        )
        start_button.bind(on_press=self.on_start_pressed)
        
        main_action_section.add_widget(start_button)
        main_action_section.add_widget(Widget())
        
        return main_action_section
    
    def _create_control_section(self):
        """Create control buttons section"""
        control_section = BoxLayout(
            orientation='horizontal',
            spacing=ResponsiveUtils.spacing('medium'),  # Reduced spacing
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(60)  # Reduced height
        )
        
        control_section.add_widget(Widget())  # Left spacer
        
        # Theme toggle button
        theme_icon = 'moon' if Theme.is_dark() else 'sun'
        theme_text = 'LIGHT' if Theme.is_dark() else 'DARK'  # Show what it will switch TO
        
        theme_button = ResponsiveButton(
            text=theme_text,
            icon=theme_icon,
            button_type='secondary',
            size_type='small'  # Reduced size
        )
        theme_button.bind(on_press=self.toggle_theme)
        
        # Configuration button
        config_button = ResponsiveButton(
            text='CONFIGURE',
            icon='config',
            button_type='secondary',
            size_type='small'  # Reduced size
        )
        config_button.bind(on_press=self.open_configuration)
        
        control_section.add_widget(theme_button)
        control_section.add_widget(config_button)
        control_section.add_widget(Widget())  # Right spacer
        
        return control_section
    
    def _create_emergency_section(self):
        """Create emergency access section (positioned at bottom)"""
        emergency_section = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(60)  # Reduced height
        )
        
        emergency_section.add_widget(Widget())  # Left spacer
        
        emergency_button = ResponsiveButton(
            text='EMERGENCY ACCESS',
            icon='emergency',
            button_type='error',
            size_type='medium'  # Reduced from large
        )
        emergency_button.bind(on_press=self.handle_emergency_access)
        
        emergency_section.add_widget(emergency_button)
        emergency_section.add_widget(Widget())  # Right spacer
        
        return emergency_section
    
    def _create_footer_section(self):
        """Create footer with clean version information"""
        # Clean footer text without the "AMS Touch Interface 3.0 Professional - Refactored" part
        footer_text = f"{AppConfig.APP_NAME} {AppConfig.APP_VERSION}"
        
        version_label = ResponsiveLabel(
            text=footer_text,
            size_type='tiny',  # Made even smaller
            color=Theme.get('on_surface_variant'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(25)  # Reduced height
        )
        version_label.text_size = (None, None)
        
        return version_label
    
    def update_datetime(self, dt):
        """Update real-time clock display"""
        if self.datetime_label:
            self.datetime_label.text = AppConfig.get_datetime_string()
            self.datetime_label.color = Theme.get('on_surface_variant')
    
    def on_start_pressed(self, button):
        """Handle start button press to begin authentication flow"""
        self.log_user_action('start_button_pressed')
        
        if self.navigation_manager:
            self.navigation_manager.start_authentication_flow()
        else:
            self.navigate_to('auth_selection')
    
    def toggle_theme(self, button):
        """Handle theme toggle with professional feedback"""
        self.log_user_action('theme_toggle_requested')
        
        # Toggle theme
        is_dark = Theme.toggle_theme()
        
        # Update button text to show what it will switch TO (not current state)
        button.text = 'LIGHT' if is_dark else 'DARK'
        
        # Refresh all screens for theme change
        if self.navigation_manager:
            self.navigation_manager.refresh_all_screens()
        else:
            # Fallback: refresh current layout
            self.handle_theme_change()
        
        # Show user feedback
        theme_name = "Dark" if is_dark else "Light"
        self.show_message(
            'Theme Changed',
            f'Switched to {theme_name} theme',
            'success',
            2
        )
        
        self.log_user_action('theme_changed', {'new_theme': theme_name})
    
    def open_configuration(self, button):
        """Handle configuration access"""
        self.log_user_action('configuration_requested')
        
        if self.navigation_manager:
            self.navigation_manager.handle_configuration_access()
        else:
            self.navigate_to('configuration')
    
    def handle_emergency_access(self, button):
        """Handle emergency access request"""
        self.log_user_action('emergency_access_requested')
        
        if self.navigation_manager:
            self.navigation_manager.handle_emergency_access()
        else:
            self.navigate_to('emergency_access')
    
    def on_screen_enter(self):
        """Called when returning to main screen"""
        super().on_screen_enter()
        
        # Check if returning from a completed session
        user_context = self.get_user_context()
        if not user_context['session_active']:
            self.log_user_action('returned_to_main_idle')
        
        # Ensure datetime is current
        if self.datetime_label:
            self.datetime_label.text = AppConfig.get_datetime_string()
    
    def on_screen_exit(self):
        """Called when leaving main screen"""
        super().on_screen_exit()
        self.log_user_action('left_main_idle')
    
    def refresh_layout(self):
        """Refresh layout for theme changes"""
        # Stop the clock updates temporarily
        Clock.unschedule(self.update_datetime)
        
        # Recreate the layout
        self.create_layout()
        
        # Restart clock updates
        Clock.schedule_interval(self.update_datetime, 1)
    
    def cleanup(self):
        """Clean up screen resources"""
        # Stop scheduled updates
        Clock.unschedule(self.update_datetime)
        
        # Call parent cleanup
        super().cleanup()
    
    def get_system_status(self):
        """Get current system status information"""
        return {
            'screen': 'main_idle',
            'system_ready': True,
            'current_time': AppConfig.get_datetime_string(),
            'theme': Theme.get_theme_name(),
            'active_session': getattr(app_state, 'session_active', False),
            'uptime': 'Ready for operation'
        }