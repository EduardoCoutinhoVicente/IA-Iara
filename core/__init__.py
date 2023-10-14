import datetime  # Importa o módulo datetime para trabalhar com datas e horas.
import locale    # Importa o módulo locale para configurar o idioma e a região.

class SystemInfo:
    def __init__(self): 
        pass# não faz nada(usado para quando se quer ter um metodo vazio)

    @staticmethod
    def get_time():
        """
        Retorna a hora atual no formato 'São HH horas e MM minutos'.
        """
        now = datetime.datetime.now() # Obtém a data e hora atuais.
        answer ='São {} horas e {} minutos.'.format(now.hour, now.minute)
        return answer
    
    @staticmethod
    def get_date():
        """
        Retorna a data atual no formato 'Hoje é dia DD de Mês de AAAA'.
        """
        locale.setlocale(locale.LC_TIME, "pt_BR.utf8")  # Define a configuração regional para Português (Brasil).
        now = datetime.datetime.now()  # Obtém a data e hora atuais.
        resposta = 'Hoje é dia {} de {} de {}'.format(now.day, now.strftime("%B"), now.year) # Formata as informações de data.
        return resposta
    
    @staticmethod
    def gethello():
        """
        Retorna uma mensagem de saudação.
        """
        resposta = 'Olá, meu nome é Iara, como posso te ajudar' # Retorna uma mensagem de saudação.
        return resposta
    
    @staticmethod
    def getlingua():
        """
        Retorna uma mensagem sobre a linguagem que ela foi feita.
        """
        resposta = 'Eu fui desenvolvida com a linguagem python'  
        return resposta
    
    @staticmethod
    def getbonita():
        """
        Retorna uma mensagem sobre ela ser bonita
        """
        resposta = 'obrigada, você e mais ainda!!' # Retorna uma mensagem de agardecimento.
        return resposta