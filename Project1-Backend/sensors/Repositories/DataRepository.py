from .Database import Database

class DataRepository:

    @staticmethod
    def read_all_sensors():
        sql = "SELECT * FROM Device"
        params = []
        return Database.get_rows(sql,params)

    @staticmethod
    def read_all_readings_by_date(date):
        sql = "SELECT * FROM aquastats.Meetwaarden where date(datum) = %s and DeviceID is not null and Waarde is not null order by Datum;"
        params = [date]
        return Database.get_rows(sql,params)
    
    @staticmethod
    def read_all_readings_by_date_limit5(date):
        sql = "SELECT * FROM Meetwaarden where date(datum) = %s and DeviceID is not null and Waarde is not null order by Datum limit 5;"
        params = [date]
        return Database.get_rows(sql,params)

    @staticmethod
    def get_pump_status():
        sql = "SELECT * FROM Meetwaarden where DeviceID = 7 order by Datum desc;"
        params = []
        return Database.get_one_row(sql,params)

    @staticmethod
    def post_new_reading(data, sensorID):
        params = [data[1],sensorID]
        sql = "INSERT into Meetwaarden ( Waarde, DeviceID) VALUES ( %s, %s)"
        Database.execute_sql(sql,params)

    @staticmethod
    def post_new_pump_change(status, pumpID):
        params = [pumpID,status]
        sql = "insert into Meetwaarden (DeviceID, Status) VALUES (%s, %s)"
        Database.execute_sql(sql,params)

    @staticmethod
    def get_dates():
        sql = "SELECT distinct Datum from Meetwaarden order by Datum Desc"
        return Database.get_rows(sql)

    @staticmethod
    def get_last_five_dates():
        sql = "SELECT distinct Datum from Meetwaarden order by Datum Desc limit 5"
        return Database.get_rows(sql)

    @staticmethod
    def get_last_five_readings  (sensorID):
        params = [sensorID]
        sql = "SELECT * from aquastats.Meetwaarden as M right join aquastats.Device as S on M.DeviceID = S.DeviceID where M.DeviceID = %s and S.Type = 'Sensor' order by Datum Desc limit 5"
        return Database.get_rows(sql, params)