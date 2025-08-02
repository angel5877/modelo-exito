/*Creación de tablas*/
-- 1. Agregar el "mes de lanzamiento" (mes en el que el producto se vendió por primera vez)
drop table t_VarsA;
create table t_VarsA as
select p.P_ID,p.P_Name,p.Category,p.Specs,p.Price,
date_format(o.Fec_Ven1,'%Y%m') as Per_VenL,
date_format(date_add(o.Fec_Ven1, INTERVAL 1 MONTH),'%Y%m') as Per_VenM1,
date_format(date_add(o.Fec_Ven1, INTERVAL 2 MONTH),'%Y%m') as Per_VenM2,
date_format(date_add(o.Fec_Ven1, INTERVAL 3 MONTH),'%Y%m') as Per_VenM3,
date_format(date_add(o.Fec_Ven1, INTERVAL 4 MONTH),'%Y%m') as Per_VenM4,
date_format(date_add(o.Fec_Ven1, INTERVAL 5 MONTH),'%Y%m') as Per_VenM5
from product p left join
(select P_ID,MIN(Order_Date) as Fec_Ven1 from orders GROUP BY P_ID) o on (p.P_ID=o.P_ID)
-- ----------------------------------------------------------------------------
-- 2. Obtener las cantidades vendidas por mes
drop table t_VarsB;
create table t_VarsB as
select a.P_ID,a.P_Name,a.Category,a.Specs,a.Price,
a.Per_VenL,a.Per_VenM1,a.Per_VenM2,a.Per_VenM3,
SUM(case when m0.P_ID is null then 0 else m0.Qty end) as Und_ML,
SUM(case when m1.P_ID is null then 0 else m1.Qty end) as Und_M1,
SUM(case when m2.P_ID is null then 0 else m2.Qty end) as Und_M2,
SUM(case when m3.P_ID is null then 0 else m3.Qty end) as Und_M3,
SUM(case when m4.P_ID is null then 0 else m4.Qty end) as Und_M4,
SUM(case when m5.P_ID is null then 0 else m5.Qty end) as Und_M5
from t_VarsA a 
left join orders m0 on (a.P_ID=m0.P_ID and a.Per_VenL=date_format(m0.Order_Date,'%Y%m'))
left join orders m1 on (a.P_ID=m1.P_ID and a.Per_VenM1=date_format(m1.Order_Date,'%Y%m'))
left join orders m2 on (a.P_ID=m2.P_ID and a.Per_VenM2=date_format(m2.Order_Date,'%Y%m'))
left join orders m3 on (a.P_ID=m3.P_ID and a.Per_VenM3=date_format(m3.Order_Date,'%Y%m'))
left join orders m4 on (a.P_ID=m4.P_ID and a.Per_VenM4=date_format(m4.Order_Date,'%Y%m'))
left join orders m5 on (a.P_ID=m5.P_ID and a.Per_VenM5=date_format(m5.Order_Date,'%Y%m'))
group by a.P_ID,a.P_Name,a.Category,a.Specs,a.Price,
a.Per_VenL,a.Per_VenM1,a.Per_VenM2,a.Per_VenM3,a.Per_VenM4,a.Per_VenM5
-- ----------------------------------------------------------------------------
-- 3. Crear tabla de puntajes por categoria y mes de lanzamiento
create table temp_mesl_catl as
select category,per_venl, 
sum(Und_M1) as Und_M1,sum(Und_M2) as Und_M2,
sum(Und_M3) as Und_M3,sum(Und_M4) as Und_M4,
sum(Und_M5) as Und_M5
from t_VarsB where (Und_ML+Und_M1+Und_M2+Und_M3+Und_M4+Und_M5)>0
group by category,per_venl

select * from temp_mesl_catl2
create table temp_mesl_catl2 as
select category,per_venl, 
comparar_valores(Und_M1, Und_M2) as pts_m2,
comparar_valores(Und_M2, Und_M3) as pts_m3,
comparar_valores(Und_M3, Und_M4) as pts_m4,
comparar_valores(Und_M4, Und_M5) as pts_m5
from temp_mesl_catl;

create table DE_PTS_MESL_CAT as
select category,per_venl,
cast(right(per_venl, 2) as unsigned) as Mes_Lanza,
(pts_m2+pts_m3+pts_m4+pts_m5) as Pts_Lanza
from temp_mesl_catl2 where per_venl>=202308 and per_venl<=202407
-- ----------------------------------------------------------------------------
-- 3. Calcular variables de ventana de 6 meses
drop table t_VarsC;
create table t_VarsC as
select P_ID,P_Name,Category,Specs,Price,Per_VenL,
cast(right(Per_VenL, 2) as unsigned) as Mes_Lanza,
case when (Und_M1+Und_M2+Und_M3+Und_M4+Und_M5)>0 then 1 else 0 end as flg_M5_post, -- Criterio 2
(Und_ML+Und_M1+Und_M2+Und_M3+Und_M4+Und_M5) as Und_M6 -- Criterio 3
from t_VarsB where (Und_ML+Und_M1+Und_M2+Und_M3+Und_M4+Und_M5)>0
-- ----------------------------------------------------------------------------
-- 4. Agregar Rating
drop table t_VarsD;
create table t_VarsD as
select p.P_ID,p.P_Name,p.Category,p.Specs,p.Price,p.Per_VenL,p.Mes_Lanza,
ROUND(AVG(case when r.Or_ID is null then 0 else r.Prod_Rating end),2) as Prod_Rat,
p.Flg_M5_post,p.Und_M6,
SUM(case when o.P_ID is null then 0 else 1 end) as Nro_Ope,
SUM(case when o.P_ID is null then 0 else o.Qty end) as Und_Ven
from t_VarsC p left join orders o on (p.P_ID=o.P_ID)
left join rating r on (o.Or_ID=r.Or_ID)
group by p.P_ID,p.P_Name,p.Category,p.Specs,p.Price,p.Per_VenL,p.Mes_Lanza,p.Flg_M5_post,p.Und_M6
-- ----------------------------------------------------------------------
-- Agregar edad promedio
drop table t_VarsE;
create table t_VarsE as
select t.*,les.Edad_Prom from t_VarsD t left join
(select P_ID,round(avg(age),0) as Edad_Prom
from orders o left join customer c on (o.C_ID=c.C_ID)
group by P_ID) les on (t.P_ID=les.P_ID)
-- ----------------------------------------------------------------------
-- 4. Variables de perfil de cliente
-- El cliente selecciona un rango de edad
create table tmp_edad_cat as
select category,min_edad,max_edad,ran_edad,sum(qty) as cantV
from orders o left join
(select c_id,
case when age<=25 then 18
	 when age<=34 then 26
     when age<=41 then 35
     when age<=48 then 42
     when age<=55 then 49
     when age<=62 then 56 else 63 end as min_edad,
case when age<=25 then 25
	 when age<=34 then 34
     when age<=41 then 41
     when age<=48 then 48
     when age<=55 then 55
     when age<=62 then 62 else 70 end as max_edad,
case when age<=25 then '1. Hasta 25'
	 when age<=34 then '2. De 26 a 34'
     when age<=41 then '3. De 35 a 41'
     when age<=48 then '4. De 42 a 48'
     when age<=55 then '5. De 49 a 55' 
     when age<=62 then '6. De 56 a 62' else '7. Más de 62' end as ran_edad
from customer) c on (o.c_id=c.c_id)
left join product p on (o.p_id=p.p_id)
group by category,min_edad,max_edad,ran_edad;

CREATE TABLE DE_PTS_EDAD_CAT AS
SELECT category,ran_edad,min_edad,max_edad,
    (8 - RANK() OVER (
        PARTITION BY category 
        ORDER BY cantV DESC
    )) AS puntaje
FROM tmp_edad_cat;
-- ----------------------------------------------------------------------
-- Género (Crear tabla de porcentajes por categoria y distribución)
drop table tmp_cat_gen1;
create table tmp_cat_gen1 as
select o.C_ID,p.Category,c.Gender,o.Qty
from orders o left join customer c on (o.C_ID=c.C_ID)
left join product p on (o.P_ID=p.P_ID)

drop table DE_RAT_GEN_CAT;
create table DE_RAT_GEN_CAT as
select Category,
sum(case when Gender='Male' then Qty else 0 end)/sum(Qty) as Afin_Hombre,
sum(case when Gender='Female' then Qty else 0 end)/sum(Qty) as Afin_Mujer
from tmp_cat_gen1 group by Category
-- ----------------------------------------------------------------------
-- Agregar proporción por género (Crear variables de afinidad)
create table tmp_prod_gen as
select p.P_ID,
sum(case when c.Gender='Male' then 1 else 0 end) as Nro_Hombre,
sum(case when c.Gender='Female' then 1 else 0 end) as Nro_Mujer
from orders o left join customer c on (o.C_ID=c.C_ID)
left join product p on (o.P_ID=p.P_ID)
group by p.P_ID

create table t_VarsF as
select t.*,
case when Nro_Hombre>0 then 1 else 0 end as Flg_Hombre,
case when Nro_Mujer>0 then 1 else 0 end as Flg_Mujer 
from t_VarsE t left join tmp_prod_gen tmp on (t.P_ID=tmp.P_ID)

-- Tabla final de variables
create table T_PROD_VARS as
select 
t.P_ID, t.P_Name, t.Category, t.Specs, t.Price, t.Nro_Ope, t.Edad_Prom, t.Flg_Hombre, t.Flg_Mujer,
t.Per_VenL, t.Mes_Lanza, t.Prod_Rat, t.Flg_M5_post, t.Und_M6, t.Und_Ven,
(Flg_Hombre*Afin_hombre) as Afin_Hombre,
(Flg_Mujer*Afin_hombre) as Afin_Mujer,
D2.puntaje as Edad_Pts,D3.Pts_Lanza as MesL_Pts
from t_VarsF t 
left join DE_RAT_GEN_CAT D1 on (t.Category=D1.Category)
left join DE_PTS_EDAD_CAT D2 
on (t.Category=D2.Category and (t.Edad_Prom>=D2.min_edad and t.Edad_Prom<=D2.max_edad))
left join DE_PTS_MESL_CAT D3 on (t.Category=D3.Category and t.Mes_Lanza=D3.Mes_Lanza)
-- ------------------------------------------------------------------
-- Tablas finales
select * from T_PROD_VARS -- LIMIT 6266; -- Variables por producto
select * from DE_RAT_GEN_CAT -- Ratios por género y categoría
select * from DE_PTS_EDAD_CAT -- Puntaje por edad y categoría
select * from DE_PTS_MESL_CAT -- Puntaje por mes de lanzamiento y categoría
-- ------------------------------------------------------------------
