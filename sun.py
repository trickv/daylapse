#!/usr/bin/env python3

import subprocess

import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
import astropy.coordinates
import astropy.units as u

from astroplan import Observer, FixedTarget

home = EarthLocation(lat=41.87699*u.deg, lon=-88.0808*u.deg, height=234*u.m)
o = Observer(home)
utcoffset = -6*u.hour

start_time = Time('2023-02-18 12:00:00') - utcoffset

print("Scheduling: sun set snaps")
time = start_time
for x in range(0, 30):
    time += 1
    s = o.sun_set_time(time, which='next') # horizon=20
    print("ISO: {0.iso}, JD: {0.jd}".format(s))
    cmd="sudo systemd-run --uid=trick --unit=daylapse-sunset-{} --on-calendar='{}' --timer-property=AccuracySec=100ms /home/trick/daylapse/snap sunset".format(time.to_datetime().date().isoformat(), s.iso)
    #print(cmd)
    subprocess.run(cmd, shell=True)


def sun_setting_below_angle(start_time, angle, days, stream_name):
    print("Scheduling: snaps for SUN setting below {}° for {} days out".format(angle, days))
    above = angle * u.degree
    time = start_time
    for x in range(0, days):
        time += 1
        s = o.sun_set_time(time, which='next', horizon=above, n_grid_points=1500)
        print("ISO: {0.iso}, JD: {0.jd}".format(s))
        cmd="sudo systemd-run --uid=trick --unit=daylapse-{}-{} --on-calendar='{}' --timer-property=AccuracySec=100ms /home/trick/daylapse/snap {}".format(stream_name, time.to_datetime().date().isoformat(), s.iso, stream_name)
        #print(cmd)
        subprocess.run(cmd, shell=True)

for angle in (10,20,30,40,50):
    sun_setting_below_angle(start_time, angle, 30, "above{}".format(angle))
