"""
AMS Touch Interface - Professional UI Components

Enhanced UI widget system providing responsive, themeable components
for the Activity Monitoring System touch interface.

Features:
- Responsive design system
- Professional theming support  
- Touch-optimized interactions
- Icon-based visual design
- Animation and feedback systems
"""

import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse, Line
from kivy.animation import Animation
from kivy.clock import Clock

from core.config import Theme, ResponsiveUtils, IconManager, AppConfig

class ResponsiveButton(Button):
    """
    Professional responsive button with enhanced theming and touch feedback
    
    Features:
    - Multiple button types (primary, secondary, success, warning, error)
    - Icon support with fallback text
    - Responsive sizing and animations
    - Touch feedback and visual states
    """
    
    def __init__(self, button_type='primary', icon=None, size_type='normal', **kwargs):
        super().__init__(**kwargs)
        
        # Store button configuration
        self.button_type = button_type
        self.icon = icon
        self.size_type = size_type
        
        # Remove default Kivy button styling
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        
        # Set responsive sizing
        if not kwargs.get('size'):
            self.size_hint = (None, None)
            self.size = ResponsiveUtils.button_size(size_type)
        
        # Setup appearance and behavior
        self.setup_appearance()
        self.setup_animations()
        
        # Bind events for updates
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        Clock.schedule_once(lambda dt: self.update_graphics(), 0.1)
    
    def setup_appearance(self):
        """Configure button colors and text based on type"""
        # Define color schemes for different button types
        color_schemes = {
            'primary': (Theme.get('primary'), Theme.get('surface')),
            'secondary': (Theme.get('surface_variant'), Theme.get('primary')),
            'success': (Theme.get('success'), Theme.get('surface')),
            'warning': (Theme.get('warning'), Theme.get('surface')),
            'error': (Theme.get('error'), Theme.get('surface')),
            'surface': (Theme.get('surface'), Theme.get('on_surface')),
            'outline': (Theme.get('background'), Theme.get('primary'))
        }
        
        self.bg_color, self.text_color = color_schemes.get(
            self.button_type, color_schemes['primary']
        )
        self.color = self.text_color
        
        # Setup icon and text
        if self.icon:
            icon_path = IconManager.get_icon_path(self.icon)
            if not icon_path:
                # Use fallback text if icon not available
                fallback = IconManager.get_fallback_text(self.icon)
                if self.text:
                    self.text = f"{fallback} {self.text}"
                else:
                    self.text = fallback
        
        # Set responsive font size
        font_size_map = {
            'tiny': 'small',
            'small': 'small', 
            'normal': 'normal',
            'medium': 'medium',
            'large': 'large',
            'xlarge': 'large',
            'hero': 'xlarge'
        }
        self.font_size = ResponsiveUtils.font_size(
            font_size_map.get(self.size_type, 'normal')
        )
    
    def setup_animations(self):
        """Setup button animation callbacks"""
        self.bind(on_press=self.on_press_animation)
        self.bind(on_release=self.on_release_animation)
    
    def update_graphics(self, *args):
        """Update button graphics with professional styling"""
        self.canvas.before.clear()
        
        with self.canvas.before:
            # Enhanced shadow effect
            Color(*Theme.get('shadow'))
            shadow_offset = ResponsiveUtils.responsive_dp(3)
            shadow = RoundedRectangle(
                size=(self.size[0] + shadow_offset, self.size[1] + shadow_offset),
                pos=(self.pos[0] + shadow_offset/2, self.pos[1] - shadow_offset/2),
                radius=[ResponsiveUtils.responsive_dp(12)]
            )
            
            # Main button background
            Color(*self.bg_color)
            main_rect = RoundedRectangle(
                size=self.size,
                pos=self.pos,
                radius=[ResponsiveUtils.responsive_dp(12)]
            )
            
            # Subtle border for definition
            if self.button_type != 'outline':
                Color(*Theme.get('outline'))
                border = Line(
                    rounded_rectangle=(
                        self.x, self.y, self.width, self.height,
                        ResponsiveUtils.responsive_dp(12)
                    ),
                    width=ResponsiveUtils.responsive_dp(1)
                )
    
    def on_press_animation(self, *args):
        """Animate button press with scale effect"""
        anim = Animation(
            size=(self.size[0] * 0.95, self.size[1] * 0.95),
            duration=AppConfig.BUTTON_ANIMATION_DURATION
        )
        anim.start(self)
    
    def on_release_animation(self, *args):
        """Animate button release returning to normal size"""
        original_size = (self.size[0] / 0.95, self.size[1] / 0.95)
        anim = Animation(
            size=original_size,
            duration=AppConfig.BUTTON_ANIMATION_DURATION
        )
        anim.start(self)
    
    def refresh_theme(self):
        """Refresh button appearance for theme changes"""
        self.setup_appearance()
        self.update_graphics()

class ResponsiveLabel(Label):
    """
    Professional responsive label with enhanced typography
    
    Features:
    - Responsive font sizing
    - Professional typography scale
    - Theme-aware coloring
    - Text alignment and wrapping options
    """
    
    def __init__(self, size_type='normal', **kwargs):
        super().__init__(**kwargs)
        
        self.size_type = size_type
        
        # Set responsive font size if not specified
        if not kwargs.get('font_size'):
            self.font_size = ResponsiveUtils.font_size(size_type)
        
        # Set theme-appropriate color
        self.color = Theme.get('on_surface')
        
        # Enable text wrapping by default
        self.text_size = kwargs.get('text_size', (None, None))
    
    def refresh_theme(self):
        """Refresh label appearance for theme changes"""
        self.color = Theme.get('on_surface')

class StatusIndicator(Widget):
    """
    Professional status indicator with animations
    
    Features:
    - Multiple status types (active, warning, error, scanning)
    - Animated pulse effects
    - Responsive sizing
    - Theme-aware coloring
    """
    
    def __init__(self, status='active', size_type='normal', **kwargs):
        super().__init__(**kwargs)
        
        self.status = status
        self.size_hint = (None, None)
        
        # Set responsive size
        size = ResponsiveUtils.icon_size(size_type)
        self.size = (size, size)
        
        # Setup graphics and animations
        self.update_graphics()
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.animate_pulse()
    
    def get_status_color(self):
        """Get color based on status type"""
        status_colors = {
            'active': Theme.get('success'),
            'warning': Theme.get('warning'),
            'error': Theme.get('error'),
            'inactive': Theme.get('on_surface_variant'),
            'scanning': Theme.get('secondary'),
            'connecting': Theme.get('primary')
        }
        return status_colors.get(self.status, Theme.get('primary'))
    
    def update_graphics(self, *args):
        """Update status indicator graphics"""
        self.canvas.clear()
        
        with self.canvas:
            Color(*self.get_status_color())
            self.circle = Ellipse(pos=self.pos, size=self.size)
    
    def animate_pulse(self):
        """Animate pulsing effect for active status"""
        if self.status in ['active', 'scanning', 'connecting']:
            # pulse_size = self.size[0] * 1.3
            pulse_size = self.size[0] * 0
            normal_size = self.size[0]
            
            # Create pulsing animation
            anim = (
                Animation(size=(pulse_size, pulse_size), duration=1.0) +
                Animation(size=(normal_size, normal_size), duration=1.0)
            )
            anim.repeat = True
            anim.start(self)
    
    def set_status(self, new_status):
        """Change indicator status"""
        self.status = new_status
        self.update_graphics()
        # Restart animation with new status
        Animation.cancel_all(self)
        self.animate_pulse()

class SecureTextInput(BoxLayout):
    """
    Professional secure text input display for PIN entry
    
    Features:
    - Secure bullet point display
    - Responsive sizing and layout
    - Visual feedback for input
    - Professional styling with borders
    """
    
    def __init__(self, max_length=5, **kwargs):
        super().__init__(**kwargs)
        
        self.orientation = 'horizontal'
        self.max_length = max_length
        self.current_value = ""
        self.input_boxes = []
        
        # Calculate responsive dimensions
        spacing_value = ResponsiveUtils.spacing('normal')
        self.spacing = spacing_value
        self.size_hint = (None, None)
        
        box_size = ResponsiveUtils.responsive_dp(65)
        total_width = max_length * box_size + (max_length - 1) * spacing_value
        self.size = (total_width, ResponsiveUtils.responsive_dp(75))
        
        # Create input boxes
        self._create_input_boxes(box_size)
    
    def _create_input_boxes(self, box_size):
        """Create individual input display boxes"""
        for i in range(self.max_length):
            box = ResponsiveLabel(
                text='',
                font_size=ResponsiveUtils.font_size('large'),
                size_hint=(None, None),
                size=(box_size, ResponsiveUtils.responsive_dp(75)),
                halign='center',
                valign='middle'
            )
            
            # Enable text size binding for proper centering
            box.bind(texture_size=box.setter('text_size'))
            
            # Setup box styling
            self._update_box_graphics(box)
            box.bind(
                pos=lambda instance, value, b=box: self._update_box_graphics(b),
                size=lambda instance, value, b=box: self._update_box_graphics(b)
            )
            
            self.input_boxes.append(box)
            self.add_widget(box)
    
    def _update_box_graphics(self, box, *args):
        """Update individual box graphics"""
        box.canvas.before.clear()
        
        with box.canvas.before:
            # Background
            Color(*Theme.get('surface'))
            bg_rect = RoundedRectangle(
                size=box.size,
                pos=box.pos,
                radius=[ResponsiveUtils.responsive_dp(12)]
            )
            
            # Border
            Color(*Theme.get('outline'))
            border = Line(
                rounded_rectangle=(
                    box.x, box.y, box.width, box.height,
                    ResponsiveUtils.responsive_dp(12)
                ),
                width=ResponsiveUtils.responsive_dp(2)
            )
    
    def update_display(self, value):
        """Update secure display with bullet points"""
        self.current_value = value
        
        for i, box in enumerate(self.input_boxes):
            if i < len(value):
                box.text = '●'  # Secure bullet point
                # Highlight active box
                box.canvas.before.clear()
                with box.canvas.before:
                    Color(*Theme.get('primary'))
                    bg_rect = RoundedRectangle(
                        size=box.size,
                        pos=box.pos,
                        radius=[ResponsiveUtils.responsive_dp(12)]
                    )
                box.color = Theme.get('surface')
            else:
                box.text = ''
                self._update_box_graphics(box)
                box.color = Theme.get('on_surface')
    
    def clear(self):
        """Clear all input displays"""
        self.current_value = ""
        self.update_display("")

class ResponsiveKeypad(GridLayout):
    """
    Professional responsive numeric keypad
    
    Features:
    - Touch-optimized button layout
    - Responsive sizing and spacing
    - Professional button styling
    - Callback system for key presses
    """
    
    def __init__(self, callback=None, **kwargs):
        super().__init__(**kwargs)
        
        self.cols = 3
        self.rows = 4
        self.callback = callback
        
        # Calculate responsive dimensions
        button_spacing = ResponsiveUtils.spacing('normal')
        self.spacing = button_spacing
        self.size_hint = (None, None)
        
        button_size = ResponsiveUtils.responsive_dp(85)
        total_width = 3 * button_size + 2 * button_spacing
        total_height = 4 * button_size + 3 * button_spacing
        self.size = (total_width, total_height)
        
        # Create keypad buttons
        self._create_keypad_buttons(button_size)
    
    def _create_keypad_buttons(self, button_size):
        """Create keypad button layout"""
        button_config = [
            ('1', 'secondary'), ('2', 'secondary'), ('3', 'secondary'),
            ('4', 'secondary'), ('5', 'secondary'), ('6', 'secondary'),
            ('7', 'secondary'), ('8', 'secondary'), ('9', 'secondary'),
            ('CLEAR', 'warning'), ('0', 'secondary'), ('ENTER', 'success')
        ]
        
        for btn_text, btn_type in button_config:
            btn = ResponsiveButton(
                text=btn_text,
                button_type=btn_type,
                font_size=ResponsiveUtils.font_size('medium'),
                size_hint=(None, None),
                size=(button_size, button_size)
            )
            btn.bind(on_press=self._on_key_press)
            self.add_widget(btn)
    
    def _on_key_press(self, button):
        """Handle keypad button press"""
        if self.callback:
            # Standardize button text
            text = button.text.strip()
            if text == 'CLEAR':
                text = 'Clear'
            elif text == 'ENTER':
                text = 'Enter'
            
            self.callback(text)

class ScanningBar(Widget):
    """
    Professional animated scanning indicator
    
    Features:
    - Multiple scan types (card, biometric)
    - Smooth animations
    - Professional styling
    - Configurable animation parameters
    """
    
    def __init__(self, scan_type='card', **kwargs):
        super().__init__(**kwargs)
        
        self.scan_type = scan_type
        self.scanning = False
        self.scan_position = 0
        self.scan_direction = 1
        
        # Set responsive size based on scan type
        self.size_hint = (None, None)
        if scan_type == 'card':
            self.size = (
                ResponsiveUtils.responsive_dp(350),
                ResponsiveUtils.responsive_dp(250)
            )
        else:  # biometric
            self.size = (
                ResponsiveUtils.responsive_dp(250),
                ResponsiveUtils.responsive_dp(250)
            )
        
        # Setup graphics
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        self.update_graphics()
    
    def update_graphics(self, *args):
        """Update scanning bar graphics"""
        self.canvas.clear()
        
        with self.canvas:
            # Background
            Color(*Theme.get('scan_bar_bg'))
            if self.scan_type == 'card':
                bg_rect = RoundedRectangle(
                    size=self.size,
                    pos=self.pos,
                    radius=[ResponsiveUtils.responsive_dp(16)]
                )
            else:
                bg_circle = Ellipse(size=self.size, pos=self.pos)
            
            # Border
            Color(*Theme.get('outline'))
            border_width = ResponsiveUtils.responsive_dp(3)
            if self.scan_type == 'card':
                border = Line(
                    rounded_rectangle=(
                        self.x, self.y, self.width, self.height,
                        ResponsiveUtils.responsive_dp(16)
                    ),
                    width=border_width
                )
            else:
                border = Line(
                    ellipse=(self.x, self.y, self.width, self.height),
                    width=border_width
                )
            
            # Scanning animation
            if self.scanning:
                Color(*Theme.get('scan_bar'))
                if self.scan_type == 'card':
                    self._draw_card_scan()
                else:
                    self._draw_biometric_scan()
    
    def _draw_card_scan(self):
        """Draw card scanning line"""
        line_height = ResponsiveUtils.responsive_dp(4)
        line_y = self.y + (self.height * self.scan_position) - line_height/2
        
        scan_line = RoundedRectangle(
            pos=(self.x + ResponsiveUtils.responsive_dp(20), line_y),
            size=(self.width - ResponsiveUtils.responsive_dp(40), line_height),
            radius=[ResponsiveUtils.responsive_dp(2)]
        )
    
    def _draw_biometric_scan(self):
        """Draw biometric scanning circle"""
        circle_size = self.width * self.scan_position * 0.8
        circle_pos_x = self.center_x - circle_size/2
        circle_pos_y = self.center_y - circle_size/2
        
        scan_circle = Line(
            ellipse=(circle_pos_x, circle_pos_y, circle_size, circle_size),
            width=ResponsiveUtils.responsive_dp(4)
        )
    
    def start_scanning(self):
        """Start scanning animation"""
        self.scanning = True
        self.scan_position = 0
        self.scan_direction = 1
        Clock.schedule_interval(self._animate_scan, 1/AppConfig.SCAN_FPS)
    
    def stop_scanning(self):
        """Stop scanning animation"""
        self.scanning = False
        Clock.unschedule(self._animate_scan)
        self.update_graphics()
    
    def _animate_scan(self, dt):
        """Animate scanning effect"""
        if not self.scanning:
            return False
        
        if self.scan_type == 'card':
            # Bouncing line animation
            self.scan_position += self.scan_direction * 0.015
            if self.scan_position >= 1.0:
                self.scan_position = 1.0
                self.scan_direction = -1
            elif self.scan_position <= 0.0:
                self.scan_position = 0.0
                self.scan_direction = 1
        else:
            # Expanding circle animation
            self.scan_position += 0.025
            if self.scan_position >= 1.0:
                self.scan_position = 0.0
        
        self.update_graphics()
        return True

class EnhancedPopup(Popup):
    """
    Professional popup with enhanced theming and auto-dismiss
    
    Features:
    - Multiple popup types (info, success, warning, error)
    - Auto-dismiss functionality
    - Responsive sizing
    - Professional styling
    """
    
    def __init__(self, popup_type='info', auto_dismiss_time=0, **kwargs):
        super().__init__(**kwargs)
        
        self.popup_type = popup_type
        self.auto_dismiss_time = auto_dismiss_time
        
        # Set responsive size
        self.size_hint = (0.8, 0.6)
        
        # Apply theming
        self._setup_appearance()
        
        # Setup auto-dismiss
        if auto_dismiss_time > 0:
            Clock.schedule_once(self._auto_dismiss, auto_dismiss_time)
    
    def _setup_appearance(self):
        """Setup popup appearance based on type"""
        color_map = {
            'info': Theme.get('surface'),
            'success': Theme.get('success'),
            'warning': Theme.get('warning'),
            'error': Theme.get('error')
        }
        
        self.background_color = color_map.get(
            self.popup_type, Theme.get('surface')
        )
        
        # Enhanced title styling
        if hasattr(self, 'title'):
            self.title_size = ResponsiveUtils.font_size('large')
    
    def _auto_dismiss(self, dt):
        """Auto-dismiss popup after timeout"""
        self.dismiss()

class ImageIcon(Widget):
    """
    Professional image-based icon with fallback support
    
    Features:
    - Image icon loading with fallback text
    - Responsive sizing
    - Theme-aware styling
    - Multiple icon formats support
    """
    
    def __init__(self, icon_name, size_type='normal', **kwargs):
        super().__init__(**kwargs)
        
        self.icon_name = icon_name
        self.size_hint = (None, None)
        
        # Set responsive size
        icon_size = ResponsiveUtils.icon_size(size_type)
        self.size = (icon_size, icon_size)
        
        # Create icon
        self.create_icon()
    
    def create_icon(self):
        """Create icon from image or fallback to text"""
        icon_path = IconManager.get_icon_path(self.icon_name)
        
        if icon_path:
            # Use image icon
            self.image_widget = Image(
                source=icon_path,
                size=self.size,
                pos=self.pos
            )
            self.bind(
                pos=self._update_image_pos,
                size=self._update_image_size
            )
            self.add_widget(self.image_widget)
        else:
            # Use fallback text
            fallback_text = IconManager.get_fallback_text(self.icon_name)
            self.label_widget = ResponsiveLabel(
                text=fallback_text,
                size_type='small',
                bold=True,
                size=self.size,
                pos=self.pos,
                halign='center',
                valign='middle'
            )
            self.bind(
                pos=self._update_label_pos,
                size=self._update_label_size
            )
            self.add_widget(self.label_widget)
    
    def _update_image_pos(self, instance, pos):
        """Update image position"""
        if hasattr(self, 'image_widget'):
            self.image_widget.pos = pos
    
    def _update_image_size(self, instance, size):
        """Update image size"""
        if hasattr(self, 'image_widget'):
            self.image_widget.size = size
    
    def _update_label_pos(self, instance, pos):
        """Update label position"""
        if hasattr(self, 'label_widget'):
            self.label_widget.pos = pos
    
    def _update_label_size(self, instance, size):
        """Update label size"""
        if hasattr(self, 'label_widget'):
            self.label_widget.size = size

class ScannerImage(FloatLayout):
    """
    Professional scanner device visualization
    
    Features:
    - Device-specific imagery
    - Fallback graphics generation
    - Responsive scaling
    - Professional styling
    """
    
    def __init__(self, scan_type='card', **kwargs):
        super().__init__(**kwargs)
        
        self.scan_type = scan_type
        self.size_hint = (None, None)
        
        # Set responsive size based on scanner type
        if scan_type == 'card':
            self.size = (
                ResponsiveUtils.responsive_dp(350),
                ResponsiveUtils.responsive_dp(250)
            )
        else:
            self.size = (
                ResponsiveUtils.responsive_dp(250),
                ResponsiveUtils.responsive_dp(250)
            )
        
        # Create scanner visual
        self.create_scanner_visual()
    
    def create_scanner_visual(self):
        """Create scanner visual from image or fallback"""
        scanner_path = IconManager.get_scanner_image(self.scan_type)
        
        if scanner_path:
            # Use actual scanner device image
            self.image_widget = Image(
                source=scanner_path,
                size_hint=(1, 1),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.add_widget(self.image_widget)
        else:
            # Create professional fallback graphics
            self._create_fallback_scanner()
    
    def _create_fallback_scanner(self):
        """Create professional fallback scanner graphics"""
        scanner_widget = Widget(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        def draw_scanner(widget, *args):
            widget.canvas.clear()
            with widget.canvas:
                if self.scan_type == 'card':
                    self._draw_card_reader(widget)
                else:
                    self._draw_fingerprint_scanner(widget)
        
        scanner_widget.bind(size=draw_scanner, pos=draw_scanner)
        self.add_widget(scanner_widget)
        Clock.schedule_once(lambda dt: draw_scanner(scanner_widget), 0.1)
    
    def _draw_card_reader(self, widget):
        """Draw professional card reader graphics"""
        # Main body
        Color(*Theme.get('surface_variant'))
        main_body = RoundedRectangle(
            size=(widget.width * 0.8, widget.height * 0.6),
            pos=(widget.center_x - widget.width * 0.4,
                 widget.center_y - widget.height * 0.3),
            radius=[ResponsiveUtils.responsive_dp(12)]
        )
        
        # Card slot
        Color(*Theme.get('outline'))
        slot = Rectangle(
            size=(widget.width * 0.6, ResponsiveUtils.responsive_dp(8)),
            pos=(widget.center_x - widget.width * 0.3,
                 widget.center_y - ResponsiveUtils.responsive_dp(4))
        )
    
    def _draw_fingerprint_scanner(self, widget):
        """Draw professional fingerprint scanner graphics"""
        # Scanner base
        Color(*Theme.get('surface_variant'))
        base = Ellipse(
            size=(widget.width * 0.9, widget.height * 0.9),
            pos=(widget.center_x - widget.width * 0.45,
                 widget.center_y - widget.height * 0.45)
        )
        
        # Fingerprint pattern
        Color(*Theme.get('outline'))
        for i in range(4):
            size_factor = 0.2 + i * 0.15
            Line(
                ellipse=(
                    widget.center_x - widget.width * size_factor/2,
                    widget.center_y - widget.height * size_factor/2,
                    widget.width * size_factor,
                    widget.height * size_factor
                ),
                width=ResponsiveUtils.responsive_dp(2)
            )