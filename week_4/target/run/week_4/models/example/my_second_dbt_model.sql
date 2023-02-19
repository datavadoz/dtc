

  create or replace view `dtc-de-375513`.`dezoomcamp`.`my_second_dbt_model`
  OPTIONS()
  as -- Use the `ref` function to select from other models

select *
from `dtc-de-375513`.`dezoomcamp`.`my_first_dbt_model`
where id = 1;

