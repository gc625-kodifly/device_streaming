import os
from nicegui import ui

mtx_path = os.environ.get("MTX_PATH", "cam")
port = int(os.environ.get("NICEGUI_PORT", "6969"))

print(f"mtx path: {mtx_path}")
ui.label("Camera (WebRTC via MediaMTX through Caddy)")

ui.html(f'''
<div style="width: 100%; max-width: 960px; aspect-ratio: 16/9; border: 1px solid #333;">
  <iframe src="/{mtx_path}/" style="width:100%; height:100%; border:0;" allow="autoplay; fullscreen"></iframe>
</div>
''', sanitize=False)

ui.run(host="0.0.0.0", port=port)
