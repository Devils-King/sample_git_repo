
select make,model,safe_cast(car_age as int64) as car_age,count(registration_number) as demand, count(case when is_sale = 1 then 1 end) as sales
from AnalyticsCommon.GARDashboard_Sim_select_updated a
left join AnalyticsCommon.newcitymapping2 as z on cast(z.pincode as string) = a.pincode
where is_new = 'false'
and (city_group_new = 'Top 8'
or lower(growth_city_name) in ('lucknow','chandigarh','goa','jaipur'))
and quote_date between '2023-07-01' - 60 and '2023-07-01'
and is_renewal is null
and registration_number is not null
and safe_cast(car_age as int64) > 0
and z.city_grouping in ('Top 8','Next 16')
and case when z.city = 'Delhi' then safe_cast(car_age as int64) < 8 else 1 = 1 end
-- and safe_cast(car_age as int64) >= 3
and (model like 'XUV 700'
or model like 'Punch'
or model like 'Carens'
)
group by 1,2,3
order by 1,2,3