"""Print what mavgen derived for the three reference messages.

Run mavgen first:
    python -m pymavlink.tools.mavgen --lang=Python3 --wire-protocol=2.0 \
        --output=generated/mini.py fixtures/mini.xml
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "generated"))
import mini  # noqa: E402  (generated module, path set above)

for cls in (mini.MAVLink_heartbeat_message,
            mini.MAVLink_attitude_message,
            mini.MAVLink_global_position_int_message):
    print(cls.msgname, "id", cls.id)
    print("  definition order:", cls.fieldnames)
    print("  wire order:      ", cls.ordered_fieldnames)
    print("  format:          ", cls.unpacker.format, "| bytes:", cls.unpacker.size)
    print("  crc_extra:       ", cls.crc_extra)

mav = mini.MAVLink(None)
msg = mini.MAVLink_heartbeat_message(type=2, autopilot=12, base_mode=145,
                                     custom_mode=0, system_status=4,
                                     mavlink_version=3)
data = msg.pack(mav)                     # bytes as sent over the link
print(mav.decode(bytearray(data)))       # decoded back into an object
print(data)
