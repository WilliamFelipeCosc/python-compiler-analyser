import tokenize
from io import BytesIO
import token
import re

TOKENS = [
    # F-strings e strings comuns
    ('FSTRING', r'f"(?:[^"\\]|\\.)*"|f\'(?:[^\'\\]|\\.)*\''),
    ('STRING',  r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\''),
    # Palavras-chave
    ('DEF',         r'\bdef\b'),
    ('RETURN',      r'\breturn\b'),
    ('WHILE',       r'\bwhile\b'),
    ('TRUE',        r'\bTrue\b'),
    ('TRY',         r'\btry\b'),
    ('EXCEPT',      r'\bexcept\b'),
    ('IF',          r'\bif\b'),
    ('ELSE',        r'\belse\b'),
    ('ELIF',        r'\belif\b'),
    ('BREAK',       r'\bbreak\b'),
    ('CONTINUE',    r'\bcontinue\b'),
    ('RAISE',       r'\braise\b'),
    ('PRINT',       r'\bprint\b'),
    ('INPUT',       r'\binput\b'),
    ('NOTINLIST',   r'not\s+in'),
    ('NOT',         r'\bnot\b'),
    ('IN',          r'\bin\b'),
    ('AS',          r'\bas\b'),
    ('OR',          r'\bor\b'),
    # Operadores e delimitadores
    ('EQEQUAL',     r'=='),
    ('NOTEQUAL',    r'!='),
    ('LESSEQUAL',   r'<='),
    ('GREATEREQUAL',r'>='),
    ('EQUAL',       r'='),
    ('LESS',        r'<'),
    ('GREATER',     r'>'),
    ('PLUS',        r'\+'),
    ('MINUS',       r'-'),
    ('DOUBLESTAR',  r'\*\*'),
    ('STAR',        r'\*'),
    ('SLASH',       r'/'),
    ('COLON',       r':'),
    ('COMMA',       r','),
    ('LSQB',        r'\['),
    ('RSQB',        r'\]'),
    ('LPAR',        r'\('),
    ('RPAR',        r'\)'),
    # Outros
    ('NUMBER',      r'\b\d+(\.\d+)?\b'),
    ('IDENT',       r'\b[_a-zA-Z][_a-zA-Z0-9]*\b'),
    ('NEWLINE',     r'\n'),
    ('SKIP',        r'[ \t]+'),
    ('COMMENT',     r'\#.*'),
]

def analisar_lexico(codigo_fonte):
    tokens_resultantes = []

    # Transformar o código-fonte em bytes para o tokenize funcionar
    bytes_code = BytesIO(codigo_fonte.encode('utf-8'))

    for tok in tokenize.tokenize(bytes_code.readline):
        tipo = token.tok_name.get(tok.type)
        linha = tok.start[0]
        lexema = tok.string
        # Tenta encontrar o nome do token definido em TOKENS com base no lexema
        token_nome = None
        for nome, padrao in TOKENS:
            if re.fullmatch(padrao, lexema):
                token_nome = nome
                break

        # Ignorar tokens de espaço em branco, indentação e comentários
        if tipo in ['ENCODING', 'NL', 'NEWLINE', 'INDENT', 'DEDENT', 'ENDMARKER']:
            continue

        tokens_resultantes.append({
            'Token': lexema,
            'Tipo': tipo,
            'Descrição': descrever_token(tipo, lexema),
            'Linha': linha,
            'Nome': token_nome if token_nome else '-'
        })

    return tokens_resultantes


def descrever_token(tipo, lexema):
    """Retorna uma descrição textual com base no tipo e lexema"""
    if tipo == 'NAME':
        if lexema in [
            'def', 'return', 'if', 'else', 'elif', 'while', 'try', 'except', 'raise', 'continue', 'break', 'as', 'print', 'input', 'float', 'int'
        ]:
            return 'Palavra-chave'
        else:
            return 'Identificador (variável ou função)'
    elif tipo == 'STRING':
        return 'Literal de string'
    elif tipo == 'NUMBER':
        return 'Literal numérico'
    elif tipo == 'OP':
        return 'Operador ou delimitador'
    elif tipo == 'ERRORTOKEN':
        return 'Caractere inválido ou especial'
    else:
        return 'Outro'

def retorno_analise_lexica_formatado(codigo_fonte):
    """
    Retorna a análise léxica no formato de tokens agrupados por linha:
    (TOKEN)(VALOR)
    """
    resultado = []
    bytes_code = BytesIO(codigo_fonte.encode('utf-8'))
    tokens = list(tokenize.tokenize(bytes_code.readline))

    linha_atual = 1
    linha_tokens = []

    for tok in tokens:
        tipo = token.tok_name.get(tok.type)
        lexema = tok.string
        if tipo in ['ENCODING', 'NL', 'NEWLINE', 'INDENT', 'DEDENT', 'ENDMARKER']:
            if linha_tokens:
                resultado.append(''.join(linha_tokens))
                linha_tokens = []
            linha_atual = tok.end[0]
            continue

        # Formatação do token
        if tipo == 'NAME':
            linha_tokens.append(f'({lexema.upper()})')
        elif tipo == 'STRING':
            linha_tokens.append(f'(STRING, {repr(lexema)})')
        elif tipo == 'NUMBER':
            linha_tokens.append(f'(NUMBER, {lexema})')
        elif tipo == 'OP':
            linha_tokens.append(f'({lexema})')
        elif tipo == 'ERRORTOKEN':
            linha_tokens.append(f'(ERRORTOKEN, {repr(lexema)})')
        else:
            linha_tokens.append(f'({tipo})')

        # Quebra de linha se o token está em uma nova linha
        if tok.end[0] != linha_atual:
            if linha_tokens:
                resultado.append(''.join(linha_tokens))
                linha_tokens = []
            linha_atual = tok.end[0]

    if linha_tokens:
        resultado.append(''.join(linha_tokens))

    return '\n'.join(resultado)

# Exemplo de uso:
if __name__ == "__main__":
    with open("main.py", "r", encoding="utf-8") as f:
        codigo = f.read()

    print("=== Análise Léxica Formatada ===")
    print(retorno_analise_lexica_formatado(codigo))
    print("\n=== Tabela de Tokens ===")
    tokens = analisar_lexico(codigo)
    print(f"{'Nome':<20} {'Token':<40} {'Tipo':<20} {'Descrição':<40} {'Linha':<5}")
    print('-' * 125)
    for t in tokens:
        print(f"{t['Nome']:<20} {t['Token']:<40} {t['Tipo']:<20} {t['Descrição']:<40} {t['Linha']:<5}")

