from .Database import Database

class DataRepository:

    @staticmethod
    def read_all_sensors():
        sql = "SELECT * FROM Sensor"
        params = []
        return Database.get_rows(sql,params)

    @staticmethod
    def read_all_readings_by_date(date):
        sql = "SELECT * FROM aquastats.Meetwaarden where date(datum) = %s and SensorID is not null order by Datum;"
        params = [date]
        return Database.get_rows(sql,params)
    
    @staticmethod
    def read_all_readings_by_date_limit5(date):
        sql = "SELECT * FROM aquastats.Meetwaarden where date(datum) = %s and SensorID is not null order by Datum limit 5;"
        params = [date]
        return Database.get_rows(sql,params)

    @staticmethod
    def get_pump_status():
        sql = "SELECT * FROM aquastats.Pomp;"
        params = []
        return Database.get_one_row(sql,params)