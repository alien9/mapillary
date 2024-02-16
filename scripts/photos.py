import requests
import json, re,dotenv
import os
from vt2geojson.tools import vt_bytes_to_geojson

dotenv.read_dotenv()

import math
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)

MAP_ACCESS_TOKEN = os.environ.get("MAP_ACCESS_TOKEN")
outputfolder = "./download"

z = 14
ll_lon, ll_lat, ur_lon, ur_lat=list(map(lambda x: float(x), os.environ.get("BBOX").split(",")))
llx,lly = deg2num (ll_lat, ll_lon, z)
urx,ury = deg2num (ur_lat, ur_lon, z)
#uncomment the one layer you wish to use

#type="mly1_computed_public"
#type="mly_map_feature_point"
#type="mly_map_feature_traffic_sign"
type="mly1_computed_public"
#type="mly1_public"

#types = ["mly1_computed_public","mly_map_feature_point","mly_map_feature_traffic_sign","mly1_computed_public","mly1_public"]
types = ["mly_map_feature_traffic_sign"]
#types = ["mly1_computed_public"]
files=[]
for type in types:
    output = {"type":"FeatureCollection","features":[]}
    for x in range(min(llx,urx),max(llx,urx),1):
        for y in range(min(lly,ury),max(lly,ury),1):
            print (type,x,y)
            url = f"https://tiles.mapillary.com/maps/vtp/{type}/2/{z}/{x}/{y}?access_token={MAP_ACCESS_TOKEN}"
            r = requests.get(url)
            assert r.status_code == 200, r.content
            vt_content = r.content
            features = vt_bytes_to_geojson(vt_content, x, y, z)
            #print(features)
            #for f in features["features"]:
            #    output['features'].append(f)
            fu=outputfolder + os.path.sep + type + "_" + str(x) + "_" + str(y) + "_" + str(z) + "_" + str(llx) + "_" + str(urx) + "_" + str(lly) + "_" + str(ury) + ".geojson"
            with open(fu, "w") as fx:
                json.dump(features, fx)
            files.append(fu)
