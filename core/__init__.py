import datetime


class SystemInfo:
    def __init__(): 
        pass

    @staticmethod
    def get_time():
        now = datetime.datetime.now()
        answer ='São {} horas e {} minutos.'.format(now.hour, now.minute)
        return answer
    
    @staticmethod
    def get_date():
        now = datetime.datetime.now()
        answer = 'hoje é {} de {} de {}'.format(now.day, now.strftime("%B"), now.year)
        return answer