#! /usr/bin/env python3

import socket
import struct

# UDP settings
UDP_IP = "0.0.0.0"       # Alle Interfaces
UDP_PORT = 4242          # opentrack standard port

# Socket erstellen
sock_ot = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_ot.bind((UDP_IP, UDP_PORT))

print(f"start udp receiver for opentrack on port {UDP_PORT}\n")

class Opentrack:
    def __init(self):
        x = 0
        y = 0
        z = 0
        yaw = 0
        pitch = 0
        roll = 0

# Enter IP and UDP port of sim computer here
XPLANE_IP="127.0.0.1"
XPLANE_PORT=49000 # 49000 is default

# Enter pilots_head DREF values here - can be found with Data Ref Editor plugin, search for pilot_head.
x_pos_offset = -0.5
y_pos_offset = 2
z_pos_offset = -12.05 - 0.15

# Set scaling factors according to your needs
headg_scale = 1.2
pitch_scale = 1.5

x_pos_scale = -0.0003
y_pos_scale = 0.0001
z_pos_scale = -0.0001

# Set endianness (byte order) of simulator computer
datafmt = "<5sf500s" # use this for little-endian machines (x86 type CPUs)
# datafmt = ">5sf500s" # use this for big-endian machines (PowerPC)

# DREF positions of pilots head relavite to CG.
x_pos = b"sim/graphics/view/pilots_head_x"
y_pos = b"sim/graphics/view/pilots_head_y"
z_pos = b"sim/graphics/view/pilots_head_z"

# heading of pilots head
headg = b"sim/graphics/view/pilots_head_psi"

# pitch of pilots head
pitch = b"sim/graphics/view/pilots_head_the"

# get the UDP socket and message header ready
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
msgtype = b"DREF0"

FT = Opentrack()

try:
    while True:
        data, addr = sock_ot.recvfrom(1024)
        [FT.x, FT.y, FT.z, FT.yaw, FT.pitch, FT.roll] = struct.unpack('dddddd', data)
        print(f"data: {FT.x, FT.y, FT.z, FT.yaw, FT.pitch, FT.roll}")
    
        xp_headg = FT.yaw * headg_scale
        xp_pitch = FT.pitch * pitch_scale
        xp_x_pos = FT.x * x_pos_scale + x_pos_offset
        xp_y_pos = FT.y * y_pos_scale + y_pos_offset
        xp_z_pos = FT.z * z_pos_scale + z_pos_offset
        MESSAGE = struct.pack(datafmt, msgtype, xp_headg, headg)
        sock.sendto( MESSAGE, (XPLANE_IP, XPLANE_PORT) )
        MESSAGE = struct.pack(datafmt, msgtype, xp_pitch, pitch)
        sock.sendto( MESSAGE, (XPLANE_IP, XPLANE_PORT) )
        MESSAGE = struct.pack(datafmt, msgtype, xp_x_pos, x_pos)
        sock.sendto( MESSAGE, (XPLANE_IP, XPLANE_PORT) )
        MESSAGE = struct.pack(datafmt, msgtype, xp_y_pos, y_pos)
        sock.sendto( MESSAGE, (XPLANE_IP, XPLANE_PORT) )
        MESSAGE = struct.pack(datafmt, msgtype, xp_z_pos, z_pos)
        sock.sendto( MESSAGE, (XPLANE_IP, XPLANE_PORT) )


except KeyboardInterrupt:
    print("\nBeendet durch Benutzer.")
finally:
    sock.close()

