"""
AMS Touch Interface - Base Screen Class

Professional base screen providing consistent functionality and theming
for all screens in the Activity Monitoring System.

Features:
- Consistent background and theming
- Standard header creation
- Message popup system
- Navigation management integration
- Screen lifecycle management
- Theme refresh capabilities
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

from core.config import Theme, ResponsiveUtils, AppConfig
from components.widgets import ResponsiveButton, ResponsiveLabel, EnhancedPopup

class BaseScreen(Screen):
    """
    Professional base screen class for consistent functionality
    
    Provides common functionality for all screens including:
    - Theme management and background creation
    - Standard header generation
    - Message popup system  
    - Navigation manager integration
    - Screen lifecycle hooks
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Navigation manager reference (set by navigation manager)
        self.navigation_manager = None
        
        # Screen state tracking
        self.is_active = False
        self.layout_created = False
        
        # Background graphics reference
        self.bg_rect = None
    
    def set_navigation_manager(self, nav_manager):
        """Set navigation manager reference"""
        self.navigation_manager = nav_manager
    
    def create_background(self, layout):
        """
        Create consistent themed background for screen layouts
        
        Args:
            layout: The main layout widget to apply background to
        """
        if not layout:
            return
            
        layout.canvas.before.clear()
        with layout.canvas.before:
            Color(*Theme.get('background'))
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)
        
        # Bind to update background on layout changes
        layout.bind(size=self.update_background, pos=self.update_background)
    
    def update_background(self, instance, value):
        """Update background rectangle when layout changes"""
        if self.bg_rect:
            self.bg_rect.size = instance.size
            self.bg_rect.pos = instance.pos
    
    def create_header(self, title, back_button=True, back_callback=None):
        """
        Create consistent header section for screens
        
        Args:
            title: Header title text
            back_button: Whether to include back button
            back_callback: Custom callback for back button (optional)
            
        Returns:
            BoxLayout containing header elements
        """
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(80),
            spacing=ResponsiveUtils.spacing('normal')
        )
        
        # Add back button if requested
        if back_button:
            back_btn = ResponsiveButton(
                text='BACK',
                icon='back',
                button_type='secondary',
                size_type='normal'
            )
            
            # Use custom callback or default navigation
            if back_callback:
                back_btn.bind(on_press=back_callback)
            else:
                back_btn.bind(on_press=self.handle_back_navigation)
            
            header.add_widget(back_btn)
        
        # Add title label
        title_label = ResponsiveLabel(
            text=title,
            size_type='title',
            bold=True,
            color=Theme.get('primary')
        )
        header.add_widget(title_label)
        
        # Add spacer
        header.add_widget(Widget())
        
        return header
    
    def show_message(self, title, message, msg_type='info', auto_dismiss=3):
        """
        Show professional message popup with consistent styling
        
        Args:
            title: Popup title
            message: Message content
            msg_type: Message type (info, success, warning, error)
            auto_dismiss: Auto dismiss time in seconds (0 to disable)
            
        Returns:
            EnhancedPopup instance
        """
        # Create message content
        content = ResponsiveLabel(
            text=message,
            size_type='normal',
            color=Theme.get('on_surface'),
            text_size=(ResponsiveUtils.responsive_dp(400), None),
            halign='center',
            valign='middle'
        )
        
        # Create and show popup
        popup = EnhancedPopup(
            title=title,
            content=content,
            popup_type=msg_type,
            auto_dismiss_time=auto_dismiss
        )
        popup.open()
        return popup
    
    def show_confirmation(self, title, message, confirm_callback, cancel_callback=None):
        """
        Show confirmation dialog with Yes/No buttons
        
        Args:
            title: Dialog title
            message: Confirmation message
            confirm_callback: Callback for confirm button
            cancel_callback: Callback for cancel button (optional)
        """
        # Create content with buttons
        content_layout = BoxLayout(
            orientation='vertical',
            spacing=ResponsiveUtils.spacing('large')
        )
        
        # Message label
        msg_label = ResponsiveLabel(
            text=message,
            size_type='normal',
            color=Theme.get('on_surface'),
            text_size=(ResponsiveUtils.responsive_dp(400), None),
            halign='center'
        )
        content_layout.add_widget(msg_label)
        
        # Button layout
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(60),
            spacing=ResponsiveUtils.spacing('normal')
        )
        
        # Cancel button
        cancel_btn = ResponsiveButton(
            text='CANCEL',
            button_type='secondary',
            size_type='normal'
        )
        
        # Confirm button
        confirm_btn = ResponsiveButton(
            text='CONFIRM',
            button_type='success',
            size_type='normal'
        )
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(confirm_btn)
        content_layout.add_widget(button_layout)
        
        # Create popup
        popup = EnhancedPopup(
            title=title,
            content=content_layout,
            popup_type='warning',
            auto_dismiss_time=0,
            size_hint=(0.6, 0.4)
        )
        
        # Button callbacks
        def on_cancel(btn):
            popup.dismiss()
            if cancel_callback:
                cancel_callback()
        
        def on_confirm(btn):
            popup.dismiss()
            if confirm_callback:
                confirm_callback()
        
        cancel_btn.bind(on_press=on_cancel)
        confirm_btn.bind(on_press=on_confirm)
        
        popup.open()
        return popup
    
    def handle_back_navigation(self, button):
        """Handle back button press with navigation manager"""
        if self.navigation_manager:
            self.navigation_manager.go_back()
        else:
            print("Warning: No navigation manager available")
    
    def navigate_to(self, screen_name, direction='left'):
        """
        Navigate to another screen
        
        Args:
            screen_name: Target screen name
            direction: Transition direction
        """
        if self.navigation_manager:
            self.navigation_manager.set_current(screen_name, direction)
        else:
            print(f"Warning: Cannot navigate to {screen_name} - no navigation manager")
    
    def navigate_home(self):
        """Navigate to main screen"""
        self.navigate_to('main_idle', 'right')
    
    def refresh_layout(self):
        """
        Refresh screen layout (called on theme changes or window resize)
        Subclasses should override this method to recreate their layout
        """
        if hasattr(self, 'create_layout'):
            self.create_layout()
        else:
            print(f"Warning: {self.__class__.__name__} should implement create_layout() method")
    
    def on_screen_enter(self):
        """
        Called when screen becomes active
        Subclasses can override for screen-specific entry logic
        """
        self.is_active = True
        print(f"Screen activated: {self.name}")
    
    def on_screen_exit(self):
        """
        Called when screen becomes inactive  
        Subclasses can override for screen-specific exit logic
        """
        self.is_active = False
        print(f"Screen deactivated: {self.name}")
    
    def cleanup(self):
        """
        Cleanup screen resources
        Subclasses can override for custom cleanup
        """
        # Cancel any scheduled events
        Clock.unschedule(self.update_background)
        
        # Clear graphics
        if hasattr(self, 'bg_rect'):
            self.bg_rect = None
        
        print(f"Screen cleaned up: {self.name}")
    
    def get_screen_info(self):
        """Get screen information for debugging"""
        return {
            'name': self.name,
            'class': self.__class__.__name__,
            'is_active': self.is_active,
            'layout_created': self.layout_created,
            'has_navigation_manager': self.navigation_manager is not None
        }
    
    def handle_theme_change(self):
        """Handle theme change by refreshing layout"""
        Clock.schedule_once(lambda dt: self.refresh_layout(), 0.1)
    
    def create_spacer(self, size_hint_y=1.0):
        """Create a flexible spacer widget"""
        return Widget(size_hint_y=size_hint_y)
    
    def create_fixed_spacer(self, height):
        """Create a fixed-height spacer widget"""
        return Widget(
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(height)
        )
    
    def create_centered_container(self, widget):
        """Create a container that centers a widget horizontally"""
        container = BoxLayout(orientation='horizontal')
        container.add_widget(Widget())  # Left spacer
        container.add_widget(widget)
        container.add_widget(Widget())  # Right spacer
        return container
    
    def create_section_divider(self):
        """Create a visual section divider"""
        divider = Widget(
            size_hint_y=None,
            height=ResponsiveUtils.responsive_dp(1)
        )
        
        def draw_divider(widget, *args):
            widget.canvas.clear()
            with widget.canvas:
                Color(*Theme.get('outline'))
                Rectangle(size=widget.size, pos=widget.pos)
        
        divider.bind(size=draw_divider, pos=draw_divider)
        Clock.schedule_once(lambda dt: draw_divider(divider), 0.1)
        
        return divider
    
    def log_user_action(self, action, details=None):
        """
        Log user action for audit purposes
        
        Args:
            action: Action description
            details: Additional details dictionary
        """
        from core.config import app_state
        
        log_entry = {
            'screen': self.name,
            'action': action,
            'user': getattr(app_state, 'current_user', 'unknown'),
            'timestamp': AppConfig.get_datetime_string(),
            'details': details or {}
        }
        
        # In production, this would write to a proper log file
        print(f"User Action: {log_entry}")
    
    def get_user_context(self):
        """Get current user context information"""
        from core.config import app_state
        
        return {
            'user': getattr(app_state, 'current_user', None),
            'session_active': getattr(app_state, 'session_active', False),
            'login_time': getattr(app_state, 'login_time', None),
            'authentication_method': getattr(app_state, 'authentication_method', None)
        }