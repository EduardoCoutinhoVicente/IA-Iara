import datetime
import locale

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
        locale.setlocale(locale.LC_TIME, "pt_BR.utf8")
        now = datetime.datetime.now()
        resposta = 'Hoje é dia {} de {} de {}'.format(now.day, now.strftime("%B"), now.year)
        return resposta
    
    @staticmethod
    def gethello():
        resposta = 'Olá, meu nome é Iara, como posso te ajudar' 
        return resposta