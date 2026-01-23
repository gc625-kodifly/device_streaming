import threading
from pathlib import Path
import os
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from nicegui import Event, app, ui, ui_run

from .tabs import DashboardTab, ConfigTab

port = int(os.environ.get("NICEGUI_PORT", "6969"))


class NiceGuiNode(Node):

    def __init__(self) -> None:
        super().__init__('nicegui')
        self.gps_update = Event()
        self.gps_sub = self.create_subscription(NavSatFix, "gps/fix", self.gps_update.emit, 1)

        @ui.page('/')
        def page():
            self._build_page()

    def _build_page(self):
        """Build the main page UI."""
        # Header with logo and tabs
        with ui.header().classes('items-center gap-4 px-4').style('background-color: rgb(46, 110, 255);'):
            ui.icon('smart_toy', size='32px').classes('text-white')
            ui.label('Device Streaming').classes('text-white text-xl font-bold')
            
            with ui.tabs().classes('text-white') as tabs:
                dashboard_tab = ui.tab('Dashboard', icon='dashboard')
                config_tab = ui.tab('Config', icon='settings')
        
        # Tab panels
        with ui.tab_panels(tabs, value=dashboard_tab).classes('w-full bg-gray-100 min-h-screen'):
            DashboardTab(self.gps_update).build(dashboard_tab)
            ConfigTab().build(config_tab)


def main() -> None:
    # NOTE: This function is defined as the ROS entry point in setup.py, but it's empty to enable NiceGUI auto-reloading
    pass


def ros_main() -> None:
    rclpy.init()
    node = NiceGuiNode()
    try:
        rclpy.spin(node)
    except ExternalShutdownException:
        pass


app.on_startup(lambda: threading.Thread(target=ros_main).start())
ui_run.APP_IMPORT_STRING = f'{__name__}:app'  # ROS2 uses a non-standard module name, so we need to specify it here
ui.run(uvicorn_reload_dirs=str(Path(__file__).parent.resolve()), favicon='🤖', host="0.0.0.0", port=port)
