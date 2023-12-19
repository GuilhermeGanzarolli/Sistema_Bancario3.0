from abc import ABC, abstractclassmethod, abstractproperty

##### CONTA #####
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()


    @property
    def saldo(self):
        return self._saldo


    @property
    def numero(self):
        return self._numero


    @property
    def agencia(self):
        return self._agencia


    @property
    def cliente(self):
        return self._cliente


    @property
    def historico(self):
        return self._historico


    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)


    ###Operações###
    
    def sacar(self, valor):
        saldo = self._saldo
        ultrapassou_saldo = valor > saldo

        if ultrapassou_saldo:
            print("### Saldo insuficiente para continuar operação")
        
        elif valor > 0:
            self._saldo -= valor
            print(f"=== Saque de {valor} realizado com sucesso ===")
            return True
        
        else:
            print("### Valor inválido para continuar operação ###")
    

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Saque realizado coms sucesso")
            return True
        
        else:
            print("### Valor inválido para continuar operação ###")
            return False

        
##### CONTA CORRENTE #####
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, saques_diarios = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.saques_diarios = saques_diarios


##### CLIENTE #####
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


##### PESSOA FÍSICA #####
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


##### TRANSACAO #####
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass


    @abstractclassmethod
    def registrar(self, conta):
        pass


##### HISTORICO #####
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": "Data atual"
            }
        )


##### SAQUE #####
class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    @property
    def valor(self):
        return self.valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


##### DEPOSITO #####
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    @property
    def valor(self):
        return self.valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)