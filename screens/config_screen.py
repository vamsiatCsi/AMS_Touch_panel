"""
AMS Touch Interface - Configuration Screen

Professional configuration management interface providing system settings,
user management, device configuration, and administrative functions.

Features:
- Comprehensive configuration options
- User management interface
- Device settings and calibration
- System information display
- Professional admin interface
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from datetime import datetime

from screens.base_screen import BaseScreen
from core.config import ResponsiveUtils, Theme, AppConfig, app_state
from components.widgets import ResponsiveButton, ResponsiveLabel, StatusIndicator

class ConfigurationScreen(BaseScreen):
    """
    Professional configuration screen for system administration
    
    Features:
    - System configuration options
    - User management interface
    - Device settings and diagnostics
    - Professional admin layout
    - Comprehensive system information
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config_sections = []
        self.create_layout()
    
    def create_layout(self):
        """Create configuration interface"""
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
            'System Configuration',
            back_callback=self.handle_back_pressed
        )
        
        # System status section
        status_section = self._create_system_status_section()
        
        # Configuration options (scrollable)
        config_scroll = self._create_configuration_scroll()
        
        # Admin actions section
        admin_actions_section = self._create_admin_actions_section()
        
        # Assemble layout
        layout.add_widget(header)
        layout.add_widget(status_section)
        layout.add_widget(self.create_section_divider())
        layout.add_widget(config_scroll)
        layout.add_widget(self.create_section_divider())
        layout.add_widget(admin_actions_section)
        
        self.add_widget(layout)
        self.layout_created = True
    
    def _create_system_status_section(self):
        """Create system status overview"""
        status_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(140),
            spacing=ResponsiveUtils.spacing('small')
        )
        
        # System info header
        info_header = ResponsiveLabel(
            text='System Information',
            size_type='medium',
            bold=True,
            color=Theme.get('primary'),
            halign='center',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(40)
        )
        info_header.text_size = (None, None)
        
        # System status grid
        status_grid = GridLayout(
            cols=2,
            spacing=ResponsiveUtils.spacing('normal'),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(100),
            row_default_height=ResponsiveUtils.responsive_dp(30)
        )
        
        # Status items
        status_items = [
            ('System Version:', AppConfig.get_version_info()),
            ('Site Location:', AppConfig.SITE_NAME),
            ('Current Time:', AppConfig.get_datetime_string()),
            ('Theme Mode:', Theme.get_theme_name()),
            ('System Status:', 'Operational'),
            ('Last Restart:', 'System Boot')
        ]
        
        for label, value in status_items:
            # Label
            label_widget = ResponsiveLabel(
                text=label,
                size_type='small',
                color=Theme.get('on_surface_variant'),
                size_hint_y=None,
                height=ResponsiveUtils.responsive_dp(25)
            )
            
            # Value with status indicator for some items
            if label == 'System Status:':
                value_container = BoxLayout(
                    orientation='horizontal',
                    spacing=ResponsiveUtils.spacing('small'),
                    size_hint_y=None,
                    height=ResponsiveUtils.responsive_dp(25)
                )
                
                status_indicator = StatusIndicator(
                    status='active',
                    size_type='small'
                )
                
                value_widget = ResponsiveLabel(
                    text=value,
                    size_type='small',
                    color=Theme.get('success'),
                    bold=True
                )
                
                value_container.add_widget(status_indicator)
                value_container.add_widget(value_widget)
                status_grid.add_widget(label_widget)
                status_grid.add_widget(value_container)
            else:
                value_widget = ResponsiveLabel(
                    text=value,
                    size_type='small',
                    color=Theme.get('on_surface')
                )
                status_grid.add_widget(label_widget)
                status_grid.add_widget(value_widget)
        
        status_section.add_widget(info_header)
        status_section.add_widget(status_grid)
        
        return status_section
    
    def _create_configuration_scroll(self):
        """Create scrollable configuration options"""
        # Scrollable container
        config_scroll = ScrollView(
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(300)
        )
        
        # Configuration content
        config_content = BoxLayout(
            orientation='vertical',
            spacing=ResponsiveUtils.spacing('medium'),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(500)  # Allow scrolling
        )
        
        # Configuration sections
        config_sections = [
            ('User Management', self._create_user_management_section()),
            ('Device Settings', self._create_device_settings_section()),
            ('Security Settings', self._create_security_settings_section()),
            ('System Settings', self._create_system_settings_section()),
            ('Maintenance', self._create_maintenance_section())
        ]
        
        for section_title, section_content in config_sections:
            # Section header
            section_header = ResponsiveLabel(
                text=section_title,
                size_type='medium',
                bold=True,
                color=Theme.get('secondary'),
                size_hint_y=None,
                height=ResponsiveUtils.responsive_dp(40)
            )
            
            config_content.add_widget(section_header)
            config_content.add_widget(section_content)
            config_content.add_widget(self.create_fixed_spacer(10))
        
        config_scroll.add_widget(config_content)
        return config_scroll
    
    def _create_user_management_section(self):
        """Create user management options"""
        user_section = GridLayout(
            cols=2,
            spacing=ResponsiveUtils.spacing('normal'),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(80),
            row_default_height=ResponsiveUtils.responsive_dp(35)
        )
        
        user_buttons = [
            ('Add User', self.add_user, 'user'),
            ('Edit Users', self.edit_users, 'config'),
            ('Card Registration', self.card_registration, 'card'),
            ('Biometric Setup', self.biometric_setup, 'fingerprint')
        ]
        
        for btn_text, callback, icon in user_buttons:
            btn = ResponsiveButton(
                text=btn_text,
                icon=icon,
                button_type='secondary',
                size_type='small'
            )
            btn.bind(on_press=callback)
            user_section.add_widget(btn)
        
        return user_section
    
    def _create_device_settings_section(self):
        """Create device configuration options"""
        device_section = GridLayout(
            cols=2,
            spacing=ResponsiveUtils.spacing('normal'),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(80),
            row_default_height=ResponsiveUtils.responsive_dp(35)
        )
        
        device_buttons = [
            ('Display Settings', self.display_settings, 'sun'),
            ('Network Config', self.network_config, 'network'),
            ('Scanner Setup', self.scanner_setup, 'scan'),
            ('Calibration', self.device_calibration, 'config')
        ]
        
        for btn_text, callback, icon in device_buttons:
            btn = ResponsiveButton(
                text=btn_text,
                icon=icon,
                button_type='secondary',
                size_type='small'
            )
            btn.bind(on_press=callback)
            device_section.add_widget(btn)
        
        return device_section
    
    def _create_security_settings_section(self):
        """Create security configuration options"""
        security_section = GridLayout(
            cols=2,
            spacing=ResponsiveUtils.spacing('normal'),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(80),
            row_default_height=ResponsiveUtils.responsive_dp(35)
        )
        
        security_buttons = [
            ('Change PINs', self.change_pins, 'lock'),
            ('Security Audit', self.security_audit, 'warning'),
            ('Access Logs', self.access_logs, 'time'),
            ('Backup Config', self.backup_config, 'success')
        ]
        
        for btn_text, callback, icon in security_buttons:
            btn = ResponsiveButton(
                text=btn_text,
                icon=icon,
                button_type='secondary',
                size_type='small'
            )
            btn.bind(on_press=callback)
            security_section.add_widget(btn)
        
        return security_section
    
    def _create_system_settings_section(self):
        """Create system configuration options"""
        system_section = GridLayout(
            cols=2,
            spacing=ResponsiveUtils.spacing('normal'),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(80),
            row_default_height=ResponsiveUtils.responsive_dp(35)
        )
        
        system_buttons = [
            ('Date/Time', self.datetime_settings, 'calendar'),
            ('Language', self.language_settings, 'config'),
            ('Timeouts', self.timeout_settings, 'time'),
            ('Diagnostics', self.system_diagnostics, 'scan')
        ]
        
        for btn_text, callback, icon in system_buttons:
            btn = ResponsiveButton(
                text=btn_text,
                icon=icon,
                button_type='secondary',
                size_type='small'
            )
            btn.bind(on_press=callback)
            system_section.add_widget(btn)
        
        return system_section
    
    def _create_maintenance_section(self):
        """Create maintenance options"""
        maintenance_section = GridLayout(
            cols=2,
            spacing=ResponsiveUtils.spacing('normal'),
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(40),
            row_default_height=ResponsiveUtils.responsive_dp(35)
        )
        
        maintenance_buttons = [
            ('System Logs', self.system_logs, 'scan'),
            ('Reset Settings', self.reset_settings, 'clear')
        ]
        
        for btn_text, callback, icon in maintenance_buttons:
            btn = ResponsiveButton(
                text=btn_text,
                icon=icon,
                button_type='warning' if 'reset' in btn_text.lower() else 'secondary',
                size_type='small'
            )
            btn.bind(on_press=callback)
            maintenance_section.add_widget(btn)
        
        return maintenance_section
    
    def _create_admin_actions_section(self):
        """Create administrative action buttons"""
        admin_actions = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(60),
            spacing=ResponsiveUtils.spacing('large')
        )
        
        admin_actions.add_widget(Widget())  # Left spacer
        
        # Restart system button
        restart_btn = ResponsiveButton(
            text='RESTART SYSTEM',
            icon='config',
            button_type='warning',
            size_type='normal'
        )
        restart_btn.bind(on_press=self.restart_system)
        
        # Factory reset button (dangerous)
        factory_reset_btn = ResponsiveButton(
            text='FACTORY RESET',
            icon='error',
            button_type='error',
            size_type='normal'
        )
        factory_reset_btn.bind(on_press=self.factory_reset)
        
        admin_actions.add_widget(restart_btn)
        admin_actions.add_widget(factory_reset_btn)
        admin_actions.add_widget(Widget())  # Right spacer
        
        return admin_actions
    
    def handle_back_pressed(self, button):
        """Handle back button press"""
        self.log_user_action('configuration_back_pressed')
        self.navigate_home()
    
    # Configuration action methods
    def add_user(self, button):
        self.log_user_action('add_user_requested')
        self.show_message('Add User', 'User management features coming soon...', 'info', 3)
    
    def edit_users(self, button):
        self.log_user_action('edit_users_requested')
        self.show_message('Edit Users', 'User editing features coming soon...', 'info', 3)
    
    def card_registration(self, button):
        self.log_user_action('card_registration_requested')
        self.show_message('Card Registration', 'Card registration wizard coming soon...', 'info', 3)
    
    def biometric_setup(self, button):
        self.log_user_action('biometric_setup_requested')
        self.show_message('Biometric Setup', 'Biometric enrollment features coming soon...', 'info', 3)
    
    def display_settings(self, button):
        self.log_user_action('display_settings_requested')
        self.show_message('Display Settings', 'Display configuration options coming soon...', 'info', 3)
    
    def network_config(self, button):
        self.log_user_action('network_config_requested')
        self.show_message('Network Configuration', 'Network settings interface coming soon...', 'info', 3)
    
    def scanner_setup(self, button):
        self.log_user_action('scanner_setup_requested')
        self.show_message('Scanner Setup', 'Scanner calibration tools coming soon...', 'info', 3)
    
    def device_calibration(self, button):
        self.log_user_action('device_calibration_requested')
        self.show_message('Device Calibration', 'Hardware calibration tools coming soon...', 'info', 3)
    
    def change_pins(self, button):
        self.log_user_action('change_pins_requested')
        self.show_message('Change PINs', 'PIN management interface coming soon...', 'info', 3)
    
    def security_audit(self, button):
        self.log_user_action('security_audit_requested')
        self.show_message('Security Audit', 'Security audit tools coming soon...', 'info', 3)
    
    def access_logs(self, button):
        self.log_user_action('access_logs_requested')
        self.show_message('Access Logs', 'Access log viewer coming soon...', 'info', 3)
    
    def backup_config(self, button):
        self.log_user_action('backup_config_requested')
        self.show_message('Backup Configuration', 'Configuration backup tools coming soon...', 'info', 3)
    
    def datetime_settings(self, button):
        self.log_user_action('datetime_settings_requested')
        self.show_message('Date/Time Settings', 'Date and time configuration coming soon...', 'info', 3)
    
    def language_settings(self, button):
        self.log_user_action('language_settings_requested')
        self.show_message('Language Settings', 'Multi-language support coming soon...', 'info', 3)
    
    def timeout_settings(self, button):
        self.log_user_action('timeout_settings_requested')
        self.show_message('Timeout Settings', 'Session timeout configuration coming soon...', 'info', 3)
    
    def system_diagnostics(self, button):
        self.log_user_action('system_diagnostics_requested')
        self.show_message('System Diagnostics', 'Diagnostic tools coming soon...', 'info', 3)
    
    def system_logs(self, button):
        self.log_user_action('system_logs_requested')
        self.show_message('System Logs', 'System log viewer coming soon...', 'info', 3)
    
    def reset_settings(self, button):
        """Handle settings reset with confirmation"""
        self.log_user_action('reset_settings_requested')
        
        def confirm_reset():
            self.log_user_action('reset_settings_confirmed')
            self.show_message(
                'Settings Reset',
                'Settings have been reset to defaults.\\nRestart required to take effect.',
                'success',
                4
            )
        
        def cancel_reset():
            self.log_user_action('reset_settings_cancelled')
        
        self.show_confirmation(
            '⚠️ Reset Settings',
            'Are you sure you want to reset all settings to defaults?\\n\\nThis action cannot be undone.',
            confirm_reset,
            cancel_reset
        )
    
    def restart_system(self, button):
        """Handle system restart with confirmation"""
        self.log_user_action('restart_system_requested')
        
        def confirm_restart():
            self.log_user_action('restart_system_confirmed')
            self.show_message(
                'System Restart',
                'System restart initiated...\\nPlease wait for system to reboot.',
                'warning',
                5
            )
            # In production, this would trigger an actual restart
        
        def cancel_restart():
            self.log_user_action('restart_system_cancelled')
        
        self.show_confirmation(
            '🔄 System Restart',
            'Are you sure you want to restart the system?\\n\\nAll active sessions will be terminated.',
            confirm_restart,
            cancel_restart
        )
    
    def factory_reset(self, button):
        """Handle factory reset with strong confirmation"""
        self.log_user_action('factory_reset_requested')
        
        def confirm_factory_reset():
            self.log_user_action('factory_reset_confirmed')
            self.show_message(
                '🚨 Factory Reset Initiated',
                'DANGER: Factory reset initiated!\\n\\n'
                'All data, settings, and users will be permanently deleted.\\n'
                'System will return to initial setup state.',
                'error',
                8
            )
            # In production, this would trigger actual factory reset
        
        def cancel_factory_reset():
            self.log_user_action('factory_reset_cancelled')
        
        self.show_confirmation(
            '🚨 FACTORY RESET WARNING',
            'DANGER: This will permanently delete ALL data!\\n\\n'
            '• All user accounts will be removed\\n'
            '• All settings will be lost\\n'
            '• All logs will be deleted\\n'
            '• System returns to factory state\\n\\n'
            'This action CANNOT be undone!\\n\\n'
            'Are you absolutely sure?',
            confirm_factory_reset,
            cancel_factory_reset
        )
    
    def on_screen_enter(self):
        """Called when screen becomes active"""
        super().on_screen_enter()
        self.log_user_action('configuration_screen_entered')
    
    def on_screen_exit(self):
        """Called when leaving screen"""
        super().on_screen_exit()
        self.log_user_action('configuration_screen_exited')
    
    def get_system_info(self):
        """Get comprehensive system information"""
        return {
            'app_name': AppConfig.APP_NAME,
            'app_version': AppConfig.APP_VERSION,
            'build_info': AppConfig.BUILD_INFO,
            'site_name': AppConfig.SITE_NAME,
            'current_time': AppConfig.get_datetime_string(),
            'theme_mode': Theme.get_theme_name(),
            'window_size': f"{Window.width}x{Window.height}",
            'active_session': getattr(app_state, 'session_active', False),
            'current_user': getattr(app_state, 'current_user', None),
            'configuration_screen': 'operational'
        }