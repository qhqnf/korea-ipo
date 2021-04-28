from datetime import date

class Formatter:

    @staticmethod
    def change_date_string_format(date_:str, format:str="%Y-%m-%d"):
        dt = date(year=int(date_[:4]), month=int(date_[4:6]), day=int(date_[6:]))
        str_dt = dt.strftime(format)
        return str_dt
        