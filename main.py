from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem
from ipaddress import IPv4Network, AddressValueError

def tela_calc():
    segunda_tela.show()  # Exibe a segunda tela
    num_ip = primeira_tela.num_ip.text().strip()  # Captura o IP e remove espaços desnecessários
    
    # Completa para /24 se o usuário não fornecer um prefixo
    if not '/' in num_ip:
        num_ip += '/24'
    
    # Captura o número de sub-redes selecionado
    if primeira_tela.num_rede.currentText():
        num_redes = int(primeira_tela.num_rede.currentText())
        print(f"Número de sub-redes selecionado: {num_redes}")  # Debug
    else:
        print("Por favor, selecione um número de sub-redes válido.")
        return

    try:
        # Converte o IP inserido para um objeto IPv4Network
        rede = IPv4Network(num_ip, strict=False)
        print(f"Rede base: {rede}")  # Debug

        # Calcula o novo prefixo para as sub-redes
        bits_necessarios = (num_redes - 1).bit_length()
        new_prefix = rede.prefixlen + bits_necessarios
        print(f"Novo prefixo: {new_prefix}")  # Debug

        # Verifica se o novo prefixo é válido
        if new_prefix > 30:
            print("Não é possível criar tantas sub-redes com o IP fornecido.")
            return

        # Gera as sub-redes
        subredes = list(rede.subnets(new_prefix=new_prefix))
        print(f"Sub-redes geradas: {subredes}")  # Debug

        # Configura a tabela na segunda tela para exibir os resultados
        segunda_tela.table_subredes.setRowCount(len(subredes))  # Define o número de linhas
        segunda_tela.table_subredes.setColumnCount(4)  # Define o número de colunas
        headers = ["Endereço de Rede", "Primeiro IP", "Último IP", "Broadcast"]
        segunda_tela.table_subredes.setHorizontalHeaderLabels(headers)  # Define os cabeçalhos da tabela
        
        # Preenche a tabela com os dados das sub-redes
        for row_num, subrede in enumerate(subredes):
            segunda_tela.table_subredes.setItem(row_num, 0, QTableWidgetItem(str(subrede.network_address)))  # Endereço de Rede
            primeira_ip = subrede[1]  # Primeiro IP utilizável
            ultima_ip = subrede[-2]  # Último IP utilizável
            segunda_tela.table_subredes.setItem(row_num, 1, QTableWidgetItem(str(primeira_ip)))  # Primeiro IP
            segunda_tela.table_subredes.setItem(row_num, 2, QTableWidgetItem(str(ultima_ip)))  # Último IP
            segunda_tela.table_subredes.setItem(row_num, 3, QTableWidgetItem(str(subrede.broadcast_address)))  # Endereço de Broadcast

        # Fecha a primeira tela
        primeira_tela.close()

    except AddressValueError:
        print("Endereço IP inválido")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Inicializando o aplicativo
app = QtWidgets.QApplication([])

# Carregando as telas
primeira_tela = uic.loadUi("primeira_tela.ui")
segunda_tela = uic.loadUi("segunda_tela.ui")

# Configurando o botão da primeira tela para chamar a função de cálculo
primeira_tela.botao_tela_principal.clicked.connect(tela_calc)

# Exibindo a primeira tela
primeira_tela.show()

# Executa o loop do aplicativo
app.exec()
