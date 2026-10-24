import sys
sys.path.insert(0, "generated")
import mini

for cls in (mini.MAVLink_heartbeat_message,
            mini.MAVLink_attitude_message,
            mini.MAVLink_global_position_int_message):
    print(cls.msgname, "id", cls.id)
    print("  Definition:", cls.fieldnames)
    print("  Leitung:   ", cls.ordered_fieldnames)
    print("  Format:    ", cls.unpacker.format, "| Bytes:", cls.unpacker.size)
    print("  crc_extra: ", cls.crc_extra)

mav = mini.MAVLink(None)
msg = mini.MAVLink_heartbeat_message(type=2, autopilot=12, base_mode=145,
                                     custom_mode=0, system_status=4,
                                     mavlink_version=3)
data = msg.pack(mav)          # → bytes, die über Funk gehen
print(mav.decode(bytearray(data)))   # → wieder ein Objekt
print(data)