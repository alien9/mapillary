import requests
import json, re,dotenv
import os, psycopg2
from vt2geojson.tools import vt_bytes_to_geojson
import math
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)

dotenv.read_dotenv()
z=14
ll_lon, ll_lat, ur_lon, ur_lat=list(map(lambda x: float(x), os.environ.get("BBOX").split(",")))
llx,lly = deg2num (ll_lat, ll_lon, z)
urx,ury = deg2num (ur_lat, ur_lon, z)


conn=None
try:
    conn = psycopg2.connect("dbname='mapillary' user='driver' host='localhost' password='driver'")
except:
    print("I am unable to connect to the database")
    exit()
cur=conn.cursor()
query=f"select count(*) as n, organization_id from photos_mex p group by organization_id order by n desc limit 5"
print(query)
cur.execute(query)
rows=cur.fetchall()
for row in rows:
    if row[1] is not None:
        url=f"https://graph.mapillary.com/{row[1]}?access_token={os.environ.get('MAP_ACCESS_TOKEN')}&fields=description,name"
        r = requests.get(url)
        assert r.status_code == 200, r.content
        j=r.json()
        print(f"{j['name']}\t{row[0]}")        