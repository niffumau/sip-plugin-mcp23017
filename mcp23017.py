# mcp23017.py
# MCP23017 16-channel relay plugin for SIP
from sip import template_render
from webpages import ProtectedPage
from urls import urls
from helpers import run_program
from blinker import signal
import gv
import json
import smbus
import web
bus = smbus.SMBus(1)
plugin_data = {
    "boards": [
        {"address": 0x20, "active_level": "low"},
    ]
}
# MCP23017 Registers
IODIRA = 0x00
IODIRB = 0x01
GPIOA = 0x12
GPIOB = 0x13
OLATA = 0x14
OLATB = 0x15
def init_board(address, active_level="low"):
    try:
        # Set initial state based on active level
        # For active-low: HIGH (0xFF) = relays OFF
        # For active-high: LOW (0x00) = relays OFF
        initial_state = 0xFF if active_level == "low" else 0x00
        
        bus.write_byte_data(address, OLATA, initial_state)
        bus.write_byte_data(address, OLATB, initial_state)
        # Then set all pins as outputs (0x00)
        bus.write_byte_data(address, IODIRA, 0x00)
        bus.write_byte_data(address, IODIRB, 0x00)
        print(f"[MCP23017] Board at {hex(address)} initialized successfully (active-{active_level})")
    except OSError as e:
        print(f"[MCP23017] Error initializing board at {hex(address)}: {e}")
def load_settings():
    global plugin_data
    default = {
        "boards": [
            {"address": 0x20, "active_level": "low"}
        ]
    }
    try:
        with open("./data/mcp23017.json") as f:
            plugin_data = json.load(f)
        # Ensure key exists and migrate old format
        if "boards" not in plugin_data:
            plugin_data = default
            save_settings()
        else:
            # Migrate boards without active_level
            for board in plugin_data["boards"]:
                if "active_level" not in board:
                    board["active_level"] = "low"
            save_settings()
    except Exception:
        plugin_data = default
        save_settings()
def save_settings():
    with open("./data/mcp23017.json", "w") as f:
        json.dump(plugin_data, f)
def update_stations(name, **kw):
    load_settings()
    if "boards" not in plugin_data:
        return
    stations = gv.srvals
    total_channels = 0
    for board in plugin_data["boards"]:
        address = board["address"]
        active_level = board.get("active_level", "low")
        
        # Build full 8-bit port values
        portA = 0x00
        portB = 0x00
        for ch in range(16):
            if total_channels >= len(stations):
                break
            state = stations[total_channels]  # True = ON, False = OFF
            
            # Logic based on active level
            if active_level == "low":
                # Active-low logic: LOW = ON, HIGH = OFF
                bit_val = 0 if state else 1
            else:
                # Active-high logic: HIGH = ON, LOW = OFF
                bit_val = 1 if state else 0
            
            if ch < 8:
                if bit_val:
                    portA |= (1 << ch)
            else:
                if bit_val:
                    portB |= (1 << (ch - 8))
            total_channels += 1
        # Write both ports once
        try:
            bus.write_byte_data(address, OLATA, portA)
            bus.write_byte_data(address, OLATB, portB)
        except OSError:
            print(f"[MCP23017] Cannot write to board {hex(address)}")
# Initialize all boards on plugin load
def initialize_all_boards():
    load_settings()
    if "boards" in plugin_data:
        for board in plugin_data["boards"]:
            active_level = board.get("active_level", "low")
            init_board(board["address"], active_level)
    print("[MCP23017] Plugin loaded and boards initialized")
gv.plugin_menu.append(['MCP23017', '/mcp23017'])
signal('zone_change').connect(update_stations)
class settings(ProtectedPage):
    def GET(self):
        load_settings()
        return template_render.mcp23017(settings=plugin_data)
class save_settings_page(ProtectedPage):
    def GET(self):
        qdict = web.input()
        boards = []
        for key in qdict:
            if key.startswith("addr"):
                index = key.replace("addr", "")
                # Skip if marked for deletion
                if f"del{index}" in qdict:
                    continue
                try:
                    addr = int(qdict[key], 16)
                    active_level = qdict.get(f"active{index}", "low")
                    boards.append({
                        "address": addr,
                        "active_level": active_level
                    })
                except:
                    pass
        # Add new board if provided
        if "newaddr" in qdict and qdict["newaddr"]:
            try:
                addr = int(qdict["newaddr"], 16)
                active_level = qdict.get("newactive", "low")
                boards.append({
                    "address": addr,
                    "active_level": active_level
                })
            except:
                pass
        plugin_data["boards"] = boards
        save_settings()
        # Re-initialize all boards after settings change
        initialize_all_boards()
        raise web.seeother("/mcp23017")
urls.extend([
    '/mcp23017', 'plugins.mcp23017.settings',
    '/mcp23017-save', 'plugins.mcp23017.save_settings_page'
])
# Initialize boards when plugin loads
initialize_all_boards()
