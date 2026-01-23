from nicegui import ui

from ..settings import settings, DEFAULT_SETTINGS


class ConfigTab:
    """Configuration tab with camera, stream, PTZ, and SLAM settings."""
    
    def __init__(self):
        self.ui_elements = {}
    
    def build(self, tab):
        """Build the configuration panel."""
        with ui.tab_panel(tab):
            ui.label('Configuration').classes('text-2xl font-bold mb-4')
            
            with ui.row().classes('w-full gap-4 flex-wrap'):
                self._build_camera_panel()
                self._build_stream_panel()
                self._build_ptz_panel()
                self._build_slam_panel()
            
            self._build_action_buttons()
    
    def _build_camera_panel(self):
        """Build camera panel."""
        cam = settings.camera
        
        with ui.card().classes('w-96'):
            ui.label('Camera').classes('text-lg font-bold mb-2')
            ui.separator()
            
            with ui.column().classes('w-full gap-3 mt-2'):
                self.ui_elements['camera.exposure'] = ui.number(
                    label='Exposure (µs)', value=cam['exposure'], min=100, max=100000, step=100
                ).classes('w-full')
                
                self.ui_elements['camera.gain'] = ui.number(
                    label='Gain (dB)', value=cam['gain'], min=0, max=48, step=1
                ).classes('w-full')
                
                self.ui_elements['camera.brightness'] = ui.slider(
                    min=0, max=100, value=cam['brightness']
                ).props('label')
                ui.label('Brightness').classes('text-xs text-gray-500 -mt-2')
                
                self.ui_elements['camera.contrast'] = ui.slider(
                    min=0, max=100, value=cam['contrast']
                ).props('label')
                ui.label('Contrast').classes('text-xs text-gray-500 -mt-2')
                
                self.ui_elements['camera.trigger_mode'] = ui.select(
                    label='Trigger Mode',
                    options=['Continuous', 'Software', 'Hardware'],
                    value=cam['trigger_mode']
                ).classes('w-full')
                
                self.ui_elements['camera.auto_exposure'] = ui.switch(
                    'Auto Exposure', value=cam['auto_exposure']
                )
                self.ui_elements['camera.auto_white_balance'] = ui.switch(
                    'Auto White Balance', value=cam['auto_white_balance']
                )
    
    def _build_stream_panel(self):
        """Build stream panel."""
        stream = settings.stream
        
        with ui.card().classes('w-96'):
            ui.label('Stream').classes('text-lg font-bold mb-2')
            ui.separator()
            
            with ui.column().classes('w-full gap-3 mt-2'):
                self.ui_elements['stream.resolution'] = ui.select(
                    label='Resolution',
                    options=['1920x1080', '1280x720', '640x480'],
                    value=stream['resolution']
                ).classes('w-full')
                
                self.ui_elements['stream.framerate'] = ui.number(
                    label='Framerate (fps)', value=stream['framerate'], min=1, max=60, step=1
                ).classes('w-full')
                
                self.ui_elements['stream.bitrate'] = ui.number(
                    label='Bitrate (kbps)', value=stream['bitrate'], min=500, max=20000, step=100
                ).classes('w-full')
                
                self.ui_elements['stream.codec'] = ui.select(
                    label='Codec',
                    options=['H.264', 'H.265', 'MJPEG'],
                    value=stream['codec']
                ).classes('w-full')
    
    def _build_ptz_panel(self):
        """Build PTZ panel."""
        ptz = settings.ptz
        
        with ui.card().classes('w-96'):
            ui.label('PTZ').classes('text-lg font-bold mb-2')
            ui.separator()
            
            with ui.column().classes('w-full gap-3 mt-2'):
                self.ui_elements['ptz.pan_speed'] = ui.number(
                    label='Pan Speed', value=ptz['pan_speed'], min=0, max=63, step=1
                ).classes('w-full')
                
                self.ui_elements['ptz.tilt_speed'] = ui.number(
                    label='Tilt Speed', value=ptz['tilt_speed'], min=0, max=63, step=1
                ).classes('w-full')
                
                self.ui_elements['ptz.invert_pan'] = ui.switch(
                    'Invert Pan', value=ptz['invert_pan']
                )
                self.ui_elements['ptz.invert_tilt'] = ui.switch(
                    'Invert Tilt', value=ptz['invert_tilt']
                )
    
    def _build_slam_panel(self):
        """Build SLAM panel."""
        slam = settings.slam
        
        with ui.card().classes('w-96'):
            ui.label('SLAM').classes('text-lg font-bold mb-2')
            ui.separator()
            
            with ui.column().classes('w-full gap-3 mt-2'):
                self.ui_elements['slam.enabled'] = ui.switch(
                    'Enabled', value=slam['enabled']
                )
                
                self.ui_elements['slam.algorithm'] = ui.select(
                    label='Algorithm',
                    options=['ORB-SLAM3', 'RTAB-Map', 'LSD-SLAM', 'DSO'],
                    value=slam['algorithm']
                ).classes('w-full')
                
                self.ui_elements['slam.max_features'] = ui.number(
                    label='Max Features', value=slam['max_features'], min=100, max=5000, step=100
                ).classes('w-full')
                
                self.ui_elements['slam.scale_factor'] = ui.number(
                    label='Scale Factor', value=slam['scale_factor'], min=1.0, max=2.0, step=0.1, format='%.1f'
                ).classes('w-full')
                
                self.ui_elements['slam.num_levels'] = ui.number(
                    label='Pyramid Levels', value=slam['num_levels'], min=1, max=16, step=1
                ).classes('w-full')
                
                self.ui_elements['slam.loop_closure'] = ui.switch(
                    'Loop Closure', value=slam['loop_closure']
                )
                self.ui_elements['slam.relocalization'] = ui.switch(
                    'Relocalization', value=slam['relocalization']
                )
                self.ui_elements['slam.save_map'] = ui.switch(
                    'Save Map on Exit', value=slam['save_map']
                )
    
    def _build_action_buttons(self):
        """Build save and reset buttons."""
        with ui.row().classes('w-full justify-end mt-4'):
            ui.button(
                'Reset to Defaults',
                icon='restore',
                on_click=self._reset_settings
            ).props('flat')
            
            ui.button(
                'Save',
                icon='save',
                on_click=self._save_settings
            ).props('color=primary')
    
    def _save_settings(self):
        """Save settings from UI to JSON."""
        for key, element in self.ui_elements.items():
            category, setting = key.split('.')
            settings.set(category, setting, element.value)
        
        if settings.save():
            ui.notify('Settings saved!', type='positive')
        else:
            ui.notify('Failed to save settings', type='negative')
    
    def _reset_settings(self):
        """Reset UI elements to default values."""
        settings.reset()
        
        for key, element in self.ui_elements.items():
            category, setting = key.split('.')
            default_value = DEFAULT_SETTINGS[category][setting]
            element.value = default_value
        
        ui.notify('Settings reset to defaults', type='info')
