import pandas as pd
import pickle

class Lancamento:
    def __init__(self, data, conta_debito, conta_credito, valor, descricao):
        self.data = data
        self.conta_debito = conta_debito
        self.conta_credito = conta_credito
        self.valor = valor
        self.descricao = descricao
    
    def __str__(self):
        return f'Data: {self.data}\nConta Débito: {self.conta_debito}\nConta Crédito: {self.conta_credito}\nValor: {self.valor}\nDescrição: {self.descricao}\n'

class ListaLancamentos:

    def __init__(self):
        self.lancamentos = []
    
    def __str__(self):
        texto = ''
        for i in range(len(self.lancamentos)):
            texto += f'Lançamento #{i}:\n{self.lancamentos[i]}\n'
        return texto

    def appendLancamento(self, lancamento):
        self.lancamentos.append(lancamento)
        return self.lancamentos

class Empresa:

    def __init__(self, nome, cnpj, nire, administradores, responsaveis):
        self.nome = nome
        self.cnpj = cnpj
        self.nire = nire
        self.administradores = administradores
        self.responsaveis = responsaveis
        self.plano_contas = None
        self.lancamentos = ListaLancamentos()
        self.diarios = []
        self.razoes = []

    def __str__(self):
        return f'Empresa: {self.nome}\nCNPJ: {self.cnpj}\nNIRE: {self.nire}\nAdministradores: {self.administradores}\nResponsáveis: {self.responsaveis}'

    def criarPlanoContas(self, contas):
        plano = PlanoContas(self, contas)
        self.plano_contas = plano
        return True

    def criarDiario(self, ano):
        diario = Diario(self, ano)
        self.diarios.append(diario)
        return True

    def criarRazao(self, ano):
        razao = Razao(self, ano)
        self.razoes.append(razao)
        return True

    def criaLancamento(self, data, conta_debito, conta_credito, valor, descricao):
        lancamento = Lancamento(data, conta_debito, conta_credito, valor, descricao)
        self.lancamentos.appendLancamento(lancamento)
        return True

    def save(self, arquivo):
        file_to_store = open(arquivo, 'wb')
        pickle.dump(self, file_to_store)
        file_to_store.close()
        print(f"Dados salvos com sucesso no arquivo {file_to_store.name}")
        return True


class Diario:

    def __init__(self, empresa, ano):
        self.empresa = empresa
        self.ano = ano
        self.conteudo = {'registros':[]}

    def __str__(self):
        return f"LIVRO DIÁRIO\nEmpresa: {self.empresa}\nAno: {self.ano}"

    def preencherDiario(self):
        lst_lancamentos = self.empresa.lancamentos.lancamentos
        for i in range(len(lst_lancamentos)):
            n_lancamento = i
            if(lst_lancamentos[i].data.year == self.ano):
                data_lancamento = lst_lancamentos[i].data
                conta_debito = lst_lancamentos[i].conta_debito
                conta_credito = lst_lancamentos[i].conta_credito
                valor = lst_lancamentos[i].valor
                descricao = lst_lancamentos[i].descricao
            
                self.conteudo['registros'].append({'data_lancamento':data_lancamento,\
                                                    'n_lancamento':n_lancamento,
                                                    'conta_debito':conta_debito,\
                                                        'conta_credito':conta_credito,\
                                                            'valor': valor,\
                                                                'descricao':descricao})
        return self.conteudo

    def retornaDiarioDF(self):
        diarioDF = pd.DataFrame(self.conteudo['registros'])
        return diarioDF


class Razao:

    def __init__(self, empresa, ano):

        self.empresa = empresa
        self.ano = ano
        self.conteudo = pd.DataFrame()
    
    def __str__(self):
        return f"LIVRO RAZAO\nEmpresa: {self.empresa}\nAno: {self.ano}\n"

    def preencherRazao(self, diario):
        if(len(empresa.diarios[0].conteudo['registros']) == 0):
            print("ERRO: Diário sem lançamentos.")
        else:
            df_diario = pd.DataFrame(diario.conteudo['registros'])
            df_razao = df_diario.melt(id_vars=['data_lancamento','n_lancamento','valor'], value_vars=['conta_debito','conta_credito'], var_name='d/c', value_name='conta')\
                .pivot_table(index=['conta', 'data_lancamento','n_lancamento'],columns='d/c').fillna(0)
            df_razao['liquido'] = df_razao['valor']['conta_debito'] - df_razao['valor']['conta_credito']
            df_razao['saldo_conta'] = df_razao['liquido'].groupby('conta').cumsum()
            self.conteudo = df_razao    
            return self.conteudo
    
    def retornaRazaoDF(self):
        return self.conteudo



class PlanoContas:
    def __init__(self, empresa, contas):
        self.empresa = empresa
        self.contas = contas

    def __str__(self):
        return f"Plano de Contas\nEmpresa: {self.empresa}\nContas: {self.contas}\n"



########################Testes##############################
############################################################

if __name__ == '__main__':

    import os
    os.system('cls')

    import datetime as dt    

    # dict_contas = {'1.1':"ATIVO CIRCULANTE", \
    #     '1.2': 'ATIVO NÃO CIRCULANTE', \
    #         '2.1':'PASSIVO CIRCULANTE', \
    #             '2.2': 'PASSIVO NÃO CIRCULANTE', \
    #                 '2.3': 'PATRIMÔNIO LÍQUIDO', \
    #                     '3': 'RECEITAS', \
    #                         '4' : 'DESPESAS' }

    # empresa = Empresa(nome='ABC Ltda.', cnpj='000000000001', nire='0001212', administradores='Zezinho', responsaveis='Luisinho')

    # empresa.criarPlanoContas(dict_contas)
 
    # empresa.criarDiario(ano=2021)
    # empresa.criarRazao(ano=2021)

    # empresa.criaLancamento(data=dt.date(year=2021, month=2, day=4), conta_debito='1.1',conta_credito='2.3', valor=3000, descricao='Integralização de capital inicial pelos sócios.')
    # empresa.criaLancamento(data=dt.date(year=2021, month=2, day=5), conta_debito='1.1',conta_credito='2.1', valor=5000, descricao='Compra de mercadorias a prazo para revenda.')
    # empresa.criaLancamento(data=dt.date(year=2021, month=2, day=6), conta_debito='1.1',conta_credito='3', valor=7000, descricao='Registro de receita por venda de mercadorias a vista.')
    # empresa.criaLancamento(data=dt.date(year=2021, month=2, day=6), conta_debito='4',conta_credito='1.1', valor=5000, descricao='Baixa do estoque por venda de mercadorias a vista.')

    # empresa.diarios[0].preencherDiario()
    # empresa.razoes[0].preencherRazao(empresa.diarios[0])
    #empresa.save(file_name)

    file_name = 'empresa1_dados.tutty'
    empresa = pickle.load(open(file_name,'rb'))
    print(empresa.razoes[0].retornaDiarioDF())
