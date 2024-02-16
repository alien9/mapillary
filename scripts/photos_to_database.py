import os, json, psycopg2, dotenv
env=dotenv.read_dotenv()
print(env)


conn=None
try:
    conn = psycopg2.connect("dbname='mapillary' user='driver' host='localhost' password='driver'")
except:
    print("I am unable to connect to the database")


conn.autocommit = True
with conn.cursor() as cur:
    try:
        cur.execute("CREATE DATABASE dbtest")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

for filename in os.listdir("./download/"):
    print(f"./download/{filename}")
    with open(f"./download/{filename}") as fu:
        things=json.loads(fu.read())
        
        print(things["type"])
        for feat in things["features"]:
            if feat["geometry"]["type"]=="Point":
                with conn.cursor() as cur:
                    fu='f'
                    if feat['properties']['is_pano']!='False':
                        fu='t'
                    query=f"INSERT INTO public.photos_mex  (id, captured_at, compass_angle, creator_id, is_pano, organization_id, sequence_id, geom) VALUES({feat['properties']['id']}, {feat['properties']['captured_at']}, {feat['properties']['compass_angle']}, {feat['properties']['creator_id']},'{fu}', {feat['properties'].get('organization_id', 'NULL')}, '{feat['properties']['sequence_id']}', geomfromewkt('SRID=4326; POINT({feat['geometry']['coordinates'][0]} {feat['geometry']['coordinates'][1]})'));"
                    print(query)
                    try:
                        cur.execute(query)
                    except:
                        print("no way")
