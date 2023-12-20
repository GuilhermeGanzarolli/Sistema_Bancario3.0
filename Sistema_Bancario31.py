from abc import ABC, abstractclassmethod, abstractproperty

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = list()
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta) #Esta função registrar é uma função que tem na class Transacao
    
    def adicionar_conta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico() #Este histórico é uma classe do tipo histórico

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

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

    
    def sacar(self, valor):
        pode_sacar = valor <= self._saldo

        if valor <= 0:
            print("### Valor inválido para saque ###")
        
        elif pode_sacar:
            self._saldo -= valor
            print(f"=== Saque de R${valor:.2f} realizado com sucesso ===")
            return True
        else:
            print("### Saldo insuficiente para realizar saque ###")
        
        return False


    def depositar(self, valor):
        if valor <= 0:
            print("### Valor inválido para depósito ###")
            return False
        else:
            self._saldo+=valor
            print("=== Depósito de R${valor:.2f} realizado com sucesso!")
            return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_saque = 500, limite_saques_diarios = 3):
        super().__init__(numero, cliente)
        self.limite_saque = limite_saque
        self.limite_saques_diarios = limite_saques_diarios
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"]== "Saque"])
        excedeu_valor_max = valor > self.limite_saque
        excedeu_saques_diarios =  numero_saques >= self.limite_saques_diarios 

        if excedeu_valor_max:
            print("Saque máximo para conta corrente é de R$500,00")
        elif excedeu_saques_diarios:
            print("São apermitidos apenas 3 saques diários")
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transicoes = []

    @property
    def transacoes(self):
        return self._transicoes
    
    def adicionar_transacoes(self, transacao):
        self._transicoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor
        })

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao =  conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao =  conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
