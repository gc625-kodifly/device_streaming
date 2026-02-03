import os
from nicegui import ui
from sensor_msgs.msg import NavSatFix

mtx_path = os.environ.get("MTX_PATH", "cam")

# Default map settings
DEFAULT_MAP = {
    'default_lat': 22.42667,
    'default_lon': 114.198,
    'zoom': 16,
}


class DashboardTab:
    """Dashboard tab with video stream, map, and PTZ controls."""
    
    def __init__(self, gps_event):
        self.gps_event = gps_event
        self.marker = None
    
    def build(self, tab):
        """Build the dashboard panel."""
        with ui.tab_panel(tab):
            # Responsive row: stacks on mobile, side-by-side on desktop
            with ui.row().classes('w-full gap-4 flex-wrap'):
                self._build_video_stream()
                self._build_right_column()
            
            self._setup_gps_subscription()
    
    def _build_video_stream(self):
        """Build the video stream section."""
        # Full width on mobile, 65% on large screens
        with ui.element('div').classes('w-full lg:w-[65%]').style('aspect-ratio: 16/9; border: 1px solid #333;'):
            ui.element('iframe').props(
                f'src="/{mtx_path}/" allow="autoplay; fullscreen"'
            ).classes('w-full h-full border-0')
    
    def _build_right_column(self):
        """Build the right column with map and PTZ controls."""
        # Full width on mobile, ~33% on large screens (flex-1 takes remaining space)
        with ui.column().classes('w-full lg:flex-1 gap-2'):
            self._build_ptz_controls()
            self._build_map()
    
    def _build_map(self):
        """Build the map widget."""
        with ui.card().classes('w-full p-0 overflow-hidden'):
            m = ui.leaflet(
                center=(DEFAULT_MAP['default_lat'], DEFAULT_MAP['default_lon']),
                zoom=DEFAULT_MAP['zoom']
            ).classes('w-full').style('min-height: 300px;')
            
            m.tile_layer(
                url_template='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                options={'attribution': '&copy; OpenStreetMap contributors'},
            )
            
            self.marker = m.marker(latlng=(DEFAULT_MAP['default_lat'], DEFAULT_MAP['default_lon']))
    
    def _build_ptz_controls(self):
        """Build the PTZ joystick controls."""
        with ui.card().classes('w-full items-center text-center p-4'):
            ui.label('Pan-Tilt').classes('font-bold text-xs text-gray-500 mb-2')
            
            with ui.row().classes('items-center justify-center gap-4'):
                x_label = ui.label('X: 0.00')
                
                ui.joystick(
                    color='blue',
                    size=100,
                    on_move=lambda e: (
                        x_label.set_text(f'X: {e.x:.2f}'),
                        y_label.set_text(f'Y: {e.y:.2f}')
                    ),
                    on_end=lambda _: (
                        x_label.set_text('X: 0.00'),
                        y_label.set_text('Y: 0.00')
                    ),
                    mode='static',
                    shape='circle',
                    restOpacity=1
                )
                
                y_label = ui.label('Y: 0.00')
    
    def _setup_gps_subscription(self):
        """Setup GPS subscription to update marker position."""
        @self.gps_event.subscribe
        def update_gps(msg: NavSatFix):
            if self.marker:
                self.marker.move(lat=msg.latitude, lng=msg.longitude)
