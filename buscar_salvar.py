from bs4 import BeautifulSoup
import pandas as pd
import requests
from html.parser import HTMLParser

pd.set_option('display.float_format', lambda x: '%.3f' % x)

#Acessa a tabela de todas as ações
url = "http://www.fundamentus.com.br/resultado.php"
r = requests.get(url)
soup = BeautifulSoup(r.content, "lxml")

#Guarda os códigos das ações em tabela_a
tabela_a = []
for text in soup.find_all('td', attrs={'ckass':'res_papel'}):
    b = text.get_text()
    tabela_a.append([b])

#Cria um DataFrame para armazenar as info das ações
nomes_col = ["codigo",
             "empresa",
             "cotacao",
             "num_acoes",
             "p/l",
             "p/vp",
             "p/ebit",
             "psr",
             "p/ativos",
             "p/giro",
             "p/ativ_circ_liq",
             "dy",
             "ev/ebitda",
             "ev/ebit",
             "cresc_rec_5a",
             "lpa",
             "vpa",
             "marg_bruta",
             "marg_ebit",
             "marg_liq",
             "ebit_ativ",
             "roic",
             "roe",
             "liq_corr",
             "div_br/patrim",
             "giro_ativ",
             "ativo",
             "ativ_cirq",
             "div_bruta",
             "div_liq",
             "patrim_liq",
             "setor",
             "subsetor"]
info_a = pd.DataFrame(columns = nomes_col)

#Função para puxar as info
tt_var = "a"
def proc_valor(t_sopa, titul):
    global tt_var
    for t_var in t_sopa.find_all('span', string=titul):
        tt_var = t_var.parent.next_sibling.next_sibling.text.replace(" ", "").replace("\n", "").replace(".", "").replace(",", ".")
        tt_var = pd.to_numeric(tt_var, errors='ignore')
    return tt_var
    
#Acessa as páginas de cada ação e armazena as info no info_a
for pp in tabela_a:
    for pcod in pp:
        urll = "http://www.fundamentus.com.br/detalhes.php?papel=" + str(pcod)
        rr = requests.get(urll)
        soupp = BeautifulSoup(rr.content, "lxml")
        print(proc_valor(soupp, "Empresa"))
        info_a.append([proc_valor(soupp, "Papel"),
                       proc_valor(soupp, "Empresa"),
                       proc_valor(soupp, "Cotação"),
                       proc_valor(soupp, "Nro. Ações"),
                       proc_valor(soupp, "P/L"),
                       proc_valor(soupp, "P/VP"),
                       proc_valor(soupp, "P/EBIT"),
                       proc_valor(soupp, "PSR"),
                       proc_valor(soupp, "P/Ativos"),
                       proc_valor(soupp, "P/Cap. Giro"),
                       proc_valor(soupp, "P/Ativ Circ Liq"),
                       proc_valor(soupp, "Div. Yeld"),
                       proc_valor(soupp, "EV/EBITDA"),
                       proc_valor(soupp, "EV/EBIT"),
                       proc_valor(soupp, "Cresc. Rec (5a)"),
                       proc_valor(soupp, "LPA"),
                       proc_valor(soupp, "VPA"),
                       proc_valor(soupp, "Marg. Bruta"),
                       proc_valor(soupp, "Marg. Ebit"),
                       proc_valor(soupp, "Marg. Líquida"),
                       proc_valor(soupp, "EBIT / Ativo"),
                       proc_valor(soupp, "ROIC"),
                       proc_valor(soupp, "ROE"),
                       proc_valor(soupp, "Liquidez Corr"),
                       proc_valor(soupp, "Div Br/ Patrim"),
                       proc_valor(soupp, "Giro Ativos"),
                       proc_valor(soupp, "Ativo"),
                       proc_valor(soupp, "Ativo Circulante"),
                       proc_valor(soupp, "Dív. Bruta"),
                       proc_valor(soupp, "Dív. Líquida"),
                       proc_valor(soupp, "Patrim. Líq"),
                       proc_valor(soupp, "Setor"),
                       proc_valor(soupp, "Subsetor")])
        print(info_a)
