#!/usr/bin/env python3
from demo_opts import get_device
from luma.core.render import canvas
from PIL import Image, ImageFont
import netifaces as ni
import socket
import shmgpsd
import time

def get_shm():
  return shmgpsd.SHM()

def get_visible_sats(shm_gpsd):
  return shm_gpsd.satellites_visible

def get_used_sats(shm_gpsd):
  return shm_gpsd.satellites_used

def get_fix(shm_gpsd):
  return shm_gpsd.fix.mode

def get_satellites(shm_gpsd):
  sat_dict = {}
  for sat_i in range(0, shmgpsd.MAXCHANNELS):
    if shm_gpsd.skyview[sat_i].PRN != 0:
      sat_dict.update({shm_gpsd.skyview[sat_i].PRN : { 'snr':  shm_gpsd.skyview[sat_i].ss }})
  return sat_dict

def main():
    # Load default font.
    font = ImageFont.load_default()
    font2 = ImageFont.truetype(font="Quicksand-Regular.ttf", size=14)
    while True:
      with canvas(device) as draw:
        # Get GPS info
        shm_gpsd  = get_shm()
        sats      = get_visible_sats(shm_gpsd)
        sats_used = get_used_sats(shm_gpsd)
        fix       = get_fix(shm_gpsd)
        # Draw Some Text
        draw.text((30,0), "GPS Monitor", font=font2, fill=255)
        draw.text((0,15), socket.gethostname(), font=font, fill=255)
        draw.text((0,25), ni.ifaddresses('eth0')[ni.AF_INET][0]['addr'], font=font, fill=256)
        print(f"Fix: {fix}")
        draw.text((0,35), f"Fix: {fix}", font=font, fill=255)
        print(f"Sats:: {sats}")
        draw.text((0,45), f"Sats visible: {sats}", font=font, fill=255)
        print(f"Sats used: {sats_used}")
        draw.text((0,55), f"Sats used: {sats_used}", font=font, fill=255)
        small = Image.open("./sat.bmp")
        draw.bitmap((0,0), small, fill=255)

      time.sleep(1)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
