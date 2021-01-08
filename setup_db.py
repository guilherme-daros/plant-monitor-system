'''Setup database for first System initialization '''
from sqlite_commands import create_db, create_table

create_db('watering_system_data')
create_table('watering_system_data', 'all_watering_history',
             'plant_id', 'date_time')
