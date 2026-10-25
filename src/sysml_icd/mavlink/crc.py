"""MAVLink checksum (CRC-16/MCRF4XX) and CRC_EXTRA calculation."""


def crc_accumulate(crc, data):
    """Feed bytes into the 16-bit CRC state and return the new state."""
    for b in data:
        tmp = (b ^ (crc & 0xFF)) & 0xFF
        tmp = (tmp ^ (tmp << 4)) & 0xFF
        crc = ((crc >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF
    return crc


def crc_extra(msg_name, ordered_fields):
    """Compute CRC_EXTRA from a message name and its fields in wire order."""
    crc = crc_accumulate(0xFFFF, (msg_name + " ").encode())
    for typ, field_name in ordered_fields:
        crc = crc_accumulate(crc, (typ + " ").encode())
        crc = crc_accumulate(crc, (field_name + " ").encode())
    return (crc & 0xFF) ^ (crc >> 8)       # fold 16 bit into 8 bit
