select companies.name, revenue, count(location_id) NUM_offices from companies left join offices on companies.company_id = offices.company_id  
group by offices.company_id having NUM_offices < 5 order by NUM_offices