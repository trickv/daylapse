#!/usr/bin/env python3

import subprocess

import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
import astropy.coordinates
import astropy.units as u

home = EarthLocation(lat=41.87699*u.deg, lon=-88.0808*u.deg, height=234*u.m)
print(home)
utcoffset = -6*u.hour
time = Time('2023-01-18 07:15:00') - utcoffset
print(time)
astropy.coordinates.get_sun(time)
sc = astropy.coordinates.get_sun(time)
print(sc)
sc.transform_to(AltAz(obstime=time,location=home))
a = sc.transform_to(AltAz(obstime=time,location=home))
print("sun position at approx sunrise time")
print(a)
print(a.alt)
print(a.az)

print()
#import astroplan
from astroplan import Observer, FixedTarget
o = Observer(home)

start_time = Time('2023-01-31 12:00:00') - utcoffset

print("Scheduling: sun set snaps")
time = start_time
for x in range(0, 20):
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

sun_setting_below_angle(start_time, 20, 20, 'above20')
