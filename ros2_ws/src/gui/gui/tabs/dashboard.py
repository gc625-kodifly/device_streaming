import os
from nicegui import ui
from sensor_msgs.msg import NavSatFix

from ..settings import settings

mtx_path = os.environ.get("MTX_PATH", "cam")


class DashboardTab:
    """Dashboard tab with video stream, map, and PTZ controls."""
    
    def __init__(self, gps_event):
        self.gps_event = gps_event
        self.marker = None
    
    def build(self, tab):
        """Build the dashboard panel."""
        map_settings = settings.map
        
        with ui.tab_panel(tab):
            with ui.row().classes('w-full gap-4'):
                self._build_video_stream()
                self._build_right_column(map_settings)
            
            self._setup_gps_subscription()
    
    def _build_video_stream(self):
        """Build the video stream section."""
        with ui.element('div').classes('w-[65%]').style('aspect-ratio: 16/9; border: 1px solid #333;'):
            ui.element('iframe').props(
                f'src="/{mtx_path}/" allow="autoplay; fullscreen"'
            ).classes('w-full h-full border-0')
    
    def _build_right_column(self, map_settings):
        """Build the right column with map and PTZ controls."""
        with ui.column().classes('w-1/3 gap-2'):
            self._build_map(map_settings)
            self._build_ptz_controls()
    
    def _build_map(self, map_settings):
        """Build the map widget."""
        with ui.card().classes('w-full p-0 overflow-hidden flex-grow'):
            m = ui.leaflet(
                center=(map_settings['default_lat'], map_settings['default_lon']),
                zoom=map_settings['zoom']
            ).classes('w-full h-full').style('min-height: 300px;')
            
            m.tile_layer(
                url_template='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                options={'attribution': '&copy; OpenStreetMap contributors'},
            )
            
            self.marker = m.marker(latlng=(map_settings['default_lat'], map_settings['default_lon']))
    
    def _build_ptz_controls(self):
        """Build the PTZ joystick controls."""
        with ui.card().classes('w-full items-center text-center p-2'):
            ui.label('Pan-Tilt').classes('font-bold text-xs text-gray-500 mb-1')
            
            with ui.row().classes('items-center gap-4'):
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

