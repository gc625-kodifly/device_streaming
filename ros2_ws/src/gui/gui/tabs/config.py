from nicegui import ui
import os

mtx_path = os.environ.get("MTX_PATH", "cam")
class ConfigTab:
    """Configuration tab - placeholder for future settings."""
    
    def __init__(self):
        
        pass
    
    def build(self, tab):
        """Build the configuration panel."""
        with ui.tab_panel(tab):
            ui.label('Configuration').classes('text-2xl font-bold mb-4')
            ui.label('Settings coming soon...').classes('text-gray-500')


class ConfigCameraTab:
    
    def __init__(self, node, param_fetcher) -> None:
        self.node = node
        self.param_fetcher = param_fetcher
        self.exposure = None
        self.brightness = None
        self.param_fields = {}
        self.param_types = {}  # Track original types for casting
    def _on_reset_defaults(self):
        """Reset parameters to default values."""
        pass

    def _on_save_apply(self):
        """Save and apply parameter changes."""
        # Extract current values from UI fields, casting to original types
        params_to_set = {}
        for name, field in self.param_fields.items():
            value = field.value
            # Cast back to original type (ui.number always returns float)
            original_type = self.param_types.get(name)
            if original_type == int and isinstance(value, float):
                value = int(value)
            params_to_set[name] = value
        try:
            results = self.param_fetcher.set_all(params_to_set)
            if all(results):
                self.node.get_logger().info(f"Successfully set params: {params_to_set}")
                ui.notify("Parameters saved successfully", type="positive")
            else:
                failed = [name for name, ok in zip(params_to_set.keys(), results) if not ok]
                self.node.get_logger().warning(f"Failed to set some params: {failed}")
                ui.notify(f"Failed to set: {failed}", type="warning")
        except Exception as e:
            self.node.get_logger().error(f"Failed to set params: {e}")
            ui.notify(f"Error: {e}", type="negative")

    def build(self, tab):
        # Fetch actual params from the remote node
        try:
            params = self.param_fetcher.fetch_all(timeout_sec=5.0)
            self.node.get_logger().info(f"Camera params: {params}")
        except Exception as e:
            self.node.get_logger().error(f"Failed to fetch params: {e}")
            params = {}

    
        with ui.tab_panel(tab):
            with ui.row().classes('w-full gap-4'):
                # Left side - Camera iframe (2/3 width)
                with ui.element('div').classes('w-[65%]').style('aspect-ratio: 16/9; border: 1px solid #333;'):
                    ui.element('iframe').props(
                        f'src="/{mtx_path}/" allow="autoplay; fullscreen"'
                    ).classes('w-full h-full border-0')
                
                # Right side - Parameters panel (1/3 width)
                with ui.card().classes('w-1/3 p-4'):
                    ui.label('Camera Parameters').classes('text-xl font-bold mb-4')
                    
                    # Parameter fields
                    with ui.column().classes('w-full gap-4'):
                        for param, value in params.items():
                            self.param_types[param] = type(value)  # Store original type
                            if isinstance(value, bool):
                                self.param_fields[param] = ui.switch(param, value=value)
                            elif isinstance(value, float):
                                self.param_fields[param] = ui.number(label=param, value=value, step=0.01)
                            elif isinstance(value, int):
                                self.param_fields[param] = ui.number(label=param, value=value, step=1)
                            elif isinstance(value, str):
                                self.param_fields[param] = ui.input(label=param, value=value)
                            
                            
                        # self.exposure = ui.number(
                        #     label='Exposure',
                        #     value=int(time.time()),
                        #     step=1
                        # ).classes('w-full')
                        
                        # self.brightness = ui.number(
                        #     label='Brightness', 
                        #     value=0,
                        #     step=1
                        # ).classes('w-full')
                    
                    # Spacer
                    ui.space()
                    
                    # Buttons
                    with ui.row().classes('w-full gap-2 mt-auto pt-4'):
                        ui.button(
                            'Reset to Default',
                            on_click=self._on_reset_defaults
                        ).props('outline').classes('flex-1')
                        
                        ui.button(
                            'Save and Apply',
                            on_click=self._on_save_apply
                        ).props('color=primary').classes('flex-1')