#!/usr/bin/env python3
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
import astropy.coordinates
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

print("sun set")
time = Time('2023-01-18 12:00:00') - utcoffset
for x in range(0, 20):
    time += 1
    s = o.sun_set_time(time, which='next') # horizon=20
    print("ISO: {0.iso}, JD: {0.jd}".format(s))

print("sun 20°")
import astropy.units as u
above = 20 * u.degree
time = Time('2023-01-18 12:00:00') - utcoffset
for x in range(0, 20):
    time += 1
    s = o.sun_set_time(time, which='next', horizon=above, n_grid_points=1500) # horizon=20
    print("ISO: {0.iso}, JD: {0.jd}".format(s))
