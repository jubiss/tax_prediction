def convert_valor_bad_format_to_float(valor):
    if type(valor) == str:
        reais = valor[:-3]
        reais = reais.replace("'","").replace(".", "").replace(",","")
        centavos = valor[-3:].replace(",", ".")
        return float(reais+centavos)
    else:
        return valor

def format_cnpj_to_int(cnpj):
    """
    Transform CNPJ format to integer representation
    """
    cnpj = cnpj.replace('.', '').replace('/', '').replace('-', '')
    return cnpj