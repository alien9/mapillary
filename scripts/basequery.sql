


-- distancia coberta em um ano rio
select sum(st_length(st_transform(l.geom, 32723))) as distance,
extract('year' from to_timestamp(p.captured_at/1000)) as ano
from logradouros_buf lb 
join  photos p on st_contains(lb.geom, p.geom)='t' 
join logradouros l on l.gid = lb.logradouro_id and st_linelocatepoint(st_geometryn(l.geom,1), p.geom) between 0.1 and 0.9
group by ano
order by ano

-- distancia coberta em um ano mexico
select sum(st_length(l.geom)) as distance,
extract('year' from to_timestamp(p.captured_at/1000)) as ano
from logradouros_buf_mex lb 
join  photos_mex p on st_contains(lb.geom, p.geom)='t' 
join logradouros_mex l on l.gid = lb.logradouro_id and st_linelocatepoint(st_geometryn(l.geom_p,1), p.geom) between 0.1 and 0.9
group by ano
order by ano

-- distancia adicionada ao mapa a cada ano rio
select sum(distance) as distance, first_appearance from 
(
select distance, min(ano)as first_appearance, gid from 
(
select numero_fotos, distance, ano, gid from 
(
select count(*) as numero_fotos, st_length(st_transform(l.geom, 32723)) as distance,
extract('year' from to_timestamp(p.captured_at/1000)) as ano, l.gid 
from logradouros_buf lb 
join  photos p on st_contains(lb.geom, p.geom)='t' 
join logradouros l on l.gid = lb.logradouro_id and st_linelocatepoint(st_geometryn(l.geom,1), p.geom) between 0.1 and 0.9
group by ano, gid, distance
) tt where numero_fotos>1 
) s
group by distance, gid
) q
group by first_appearance
order by first_appearance

-- distancia adicionada ao mapa a cada ano mexico
select sum(distance) as distance, first_appearance from 
(
select distance, min(ano)as first_appearance, gid from 
(
select numero_fotos, distance, ano, gid from 
(
select count(*) as numero_fotos, st_length(l.geom) as distance,
extract('year' from to_timestamp(p.captured_at/1000)) as ano, l.gid 
from logradouros_buf_mex lb 
join  photos_mex p on st_contains(lb.geom, p.geom)='t' 
join logradouros_mex l on l.gid = lb.logradouro_id and st_linelocatepoint(st_geometryn(l.geom_p,1), p.geom) between 0.1 and 0.9
group by ano, gid, distance
) tt where numero_fotos>1 
) s
group by distance, gid
) q
group by first_appearance
order by first_appearance




insert into logradouro_photos_osm(logradouro_id, numero_fotos, highway, geom) 
select logradouro_id, count(*) as numero_fotos, case when o.highway is null then '' else o.highway end as highway, o.geom from logradouros_buf_osm lb 
join  photos p on st_contains(lb.geom, p.geom)='t' 
join osm_rio o on o.gid = lb.logradouro_id  and st_linelocatepoint(st_linemerge(o.geom), p.geom) between 0.1 and 0.9
group by logradouro_id, o.highway, o.geom

select l.gid, p.captured_at, p.geom, st_linelocatepoint(st_linemerge(l.geom), p.geom)  from logradouros l join logradouros_buf lb on lb.gid =l.gid
join photos p on st_contains(lb.geom, p.geom)='t'
order by p.captured_at



select count(*), EXTRACT('year' FROM to_timestamp(p.captured_at/1000)) as ano from photos p group by ano order by ano 
select count(*), EXTRACT('year' FROM to_timestamp(p.captured_at/1000)) as ano from photos_mex p group by ano order by ano 
select count(*) as n, creator_id from photos p group by creator_id order by n desc 


delete 
from photos_mex p 
where st_contains((select b.wkb_geometry from boundary_mexico b), p.geom)='f'




