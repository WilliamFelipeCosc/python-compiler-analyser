import ast
from graphviz import Digraph

def analisar_variaveis_nao_utilizadas(tree):
    atribuicoes = set()
    usos = set()

    class VarVisitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    atribuicoes.add(target.id)
            self.generic_visit(node)
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Load):
                usos.add(node.id)
            self.generic_visit(node)

    VarVisitor().visit(tree)
    return atribuicoes - usos

def analisar_funcoes_nao_chamadas(tree):
    definidas = set()
    chamadas = set()

    class FuncVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            definidas.add(node.name)
            self.generic_visit(node)
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                chamadas.add(node.func.id)
            self.generic_visit(node)

    FuncVisitor().visit(tree)
    return definidas - chamadas

def analisar_tipos_e_operacoes(tree):
    erros = []

    class TypeVisitor(ast.NodeVisitor):
        def visit_BinOp(self, node):
            # Verifica se operações são feitas entre tipos compatíveis
            if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
                left = node.left
                right = node.right
                # Apenas verifica se são literais numéricos
                if isinstance(left, ast.Constant) and isinstance(right, ast.Constant):
                    if not (isinstance(left.value, (int, float)) and isinstance(right.value, (int, float))):
                        erros.append(f"Operação aritmética entre tipos incompatíveis: {type(left.value)} e {type(right.value)} na linha {node.lineno}")
            self.generic_visit(node)
        def visit_Compare(self, node):
            # Verifica se comparações são feitas entre tipos compatíveis
            left = node.left
            for comparator in node.comparators:
                if isinstance(left, ast.Constant) and isinstance(comparator, ast.Constant):
                    if type(left.value) != type(comparator.value):
                        erros.append(f"Comparação entre tipos diferentes: {type(left.value)} e {type(comparator.value)} na linha {node.lineno}")
            self.generic_visit(node)

    TypeVisitor().visit(tree)
    return erros

def analisar_escopo(tree):
    erros = []

    class EscopoVisitor(ast.NodeVisitor):
        def __init__(self):
            self.escopo = set()
        def visit_FunctionDef(self, node):
            # Adiciona argumentos ao escopo local
            local_escopo = set(arg.arg for arg in node.args.args)
            for n in ast.walk(node):
                if isinstance(n, ast.Assign):
                    for target in n.targets:
                        if isinstance(target, ast.Name):
                            local_escopo.add(target.id)
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                    if n.id not in local_escopo and n.id not in dir(__builtins__):
                        erros.append(f"Variável '{n.id}' usada fora do escopo na função '{node.name}' (linha {n.lineno})")
            self.generic_visit(node)

    EscopoVisitor().visit(tree)
    return erros

def analisar_fluxo_de_controle(tree):
    avisos = []

    class FluxoVisitor(ast.NodeVisitor):
        def visit_If(self, node):
            # Verifica se há bloco if vazio
            if not node.body:
                avisos.append(f"Bloco if vazio na linha {node.lineno}")
            self.generic_visit(node)
        def visit_While(self, node):
            if not node.body:
                avisos.append(f"Bloco while vazio na linha {node.lineno}")
            self.generic_visit(node)
        def visit_For(self, node):
            if not node.body:
                avisos.append(f"Bloco for vazio na linha {node.lineno}")
            self.generic_visit(node)

    FluxoVisitor().visit(tree)
    return avisos

def analisar_codigo(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)

    variaveis_nao_usadas = analisar_variaveis_nao_utilizadas(tree)
    funcoes_nao_chamadas = analisar_funcoes_nao_chamadas(tree)
    erros_tipos = analisar_tipos_e_operacoes(tree)
    erros_escopo = analisar_escopo(tree)
    avisos_fluxo = analisar_fluxo_de_controle(tree)

    print("Análise semântica de", filepath)
    if variaveis_nao_usadas:
        print("Variáveis atribuídas mas não utilizadas:", variaveis_nao_usadas)
    else:
        print("Nenhuma variável atribuída sem uso.")

    if funcoes_nao_chamadas:
        print("Funções definidas mas não chamadas:", funcoes_nao_chamadas)
    else:
        print("Todas as funções definidas foram chamadas.")

    if erros_tipos:
        print("Erros de tipos e operações:", erros_tipos)
    else:
        print("Nenhum erro de tipo ou operação encontrado.")

    if erros_escopo:
        print("Erros de escopo:", erros_escopo)
    else:
        print("Nenhum erro de escopo encontrado.")

    if avisos_fluxo:
        print("Avisos de fluxo de controle:", avisos_fluxo)
    else:
        print("Nenhum problema de fluxo de controle encontrado.")

def exibir_arvore_semantica(tree, nivel=0):
    """
    Exibe uma árvore semântica simplificada do código Python analisado.
    Mostra funções, variáveis e estruturas de controle.
    """
    prefixo = "  " * nivel

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            print(f"{prefixo}Função: {node.name} (linha {node.lineno})")
            exibir_arvore_semantica(node, nivel + 1)
        elif isinstance(node, ast.Assign):
            nomes = [t.id for t in node.targets if isinstance(t, ast.Name)]
            print(f"{prefixo}Atribuição: {', '.join(nomes)} (linha {node.lineno})")
        elif isinstance(node, ast.If):
            print(f"{prefixo}If (linha {node.lineno})")
            exibir_arvore_semantica(node, nivel + 1)
            if node.orelse:
                print(f"{prefixo}else (linha {node.lineno})")
                for n in node.orelse:
                    exibir_arvore_semantica(n, nivel + 2)
        elif isinstance(node, ast.For):
            print(f"{prefixo}For (linha {node.lineno})")
            exibir_arvore_semantica(node, nivel + 1)
        elif isinstance(node, ast.While):
            print(f"{prefixo}While (linha {node.lineno})")
            exibir_arvore_semantica(node, nivel + 1)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                print(f"{prefixo}Chamada de função: {node.func.id} (linha {node.lineno})")
        # Recursivamente para outros nós
        else:
            exibir_arvore_semantica(node, nivel)

def gerar_grafo_arvore_semantica(tree):
    dot = Digraph(comment='Árvore Semântica')
    contador = {'id': 0}

    def adicionar_no(node, parent_id=None):
        node_id = str(contador['id'])
        contador['id'] += 1

        if isinstance(node, ast.FunctionDef):
            label = f"Função: {node.name}\n(linha {node.lineno})"
        elif isinstance(node, ast.Assign):
            nomes = [t.id for t in node.targets if isinstance(t, ast.Name)]
            label = f"Atribuição: {', '.join(nomes)}\n(linha {node.lineno})"
        elif isinstance(node, ast.If):
            label = f"If\n(linha {node.lineno})"
        elif isinstance(node, ast.For):
            label = f"For\n(linha {node.lineno})"
        elif isinstance(node, ast.While):
            label = f"While\n(linha {node.lineno})"
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            label = f"Chamada: {node.func.id}\n(linha {node.lineno})"
        else:
            label = type(node).__name__

        dot.node(node_id, label)

        if parent_id is not None:
            dot.edge(parent_id, node_id)

        # Recursivamente adiciona filhos relevantes
        if isinstance(node, ast.If):
            for n in node.body:
                adicionar_no(n, node_id)
            if node.orelse:
                else_id = str(contador['id'])
                dot.node(else_id, "else")
                dot.edge(node_id, else_id)
                contador['id'] += 1
                for n in node.orelse:
                    adicionar_no(n, else_id)
        elif hasattr(node, 'body') and isinstance(node.body, list): # type: ignore
            for n in node.body: # type: ignore
                adicionar_no(n, node_id)
        elif isinstance(node, ast.Module):
            for n in node.body:
                adicionar_no(n, node_id)
        elif isinstance(node, ast.FunctionDef):
            for n in node.body:
                adicionar_no(n, node_id)

    adicionar_no(tree)
    dot.render('./images/arvore_semantica.png', cleanup=True, format='png')

def gerar_grafo_fluxo_de_controle(tree):
    """
    Gera um grafo de fluxo de controle simplificado do código Python analisado.
    """
    dot = Digraph(comment='Fluxo de Controle')
    contador = {'id': 0}

    def adicionar_bloco(node, parent_id=None):
        node_id = str(contador['id'])
        contador['id'] += 1

        if isinstance(node, ast.If):
            label = f"If (linha {node.lineno})"
        elif isinstance(node, ast.For):
            label = f"For (linha {node.lineno})"
        elif isinstance(node, ast.While):
            label = f"While (linha {node.lineno})"
        elif isinstance(node, ast.FunctionDef):
            label = f"Função: {node.name} (linha {node.lineno})"
        elif isinstance(node, ast.Return):
            label = f"Return (linha {node.lineno})"
        elif isinstance(node, ast.Break):
            label = f"Break (linha {node.lineno})"
        elif isinstance(node, ast.Continue):
            label = f"Continue (linha {node.lineno})"
        else:
            label = type(node).__name__

        dot.node(node_id, label)
        if parent_id is not None:
            dot.edge(parent_id, node_id)

        # Fluxo para blocos de controle
        if isinstance(node, ast.If):
            # Corpo do if
            last_id = node_id
            for n in node.body:
                last_id = adicionar_bloco(n, last_id)
            # Else
            if node.orelse:
                else_id = str(contador['id'])
                dot.node(else_id, "else")
                dot.edge(node_id, else_id)
                contador['id'] += 1
                last_else_id = else_id
                for n in node.orelse:
                    last_else_id = adicionar_bloco(n, last_else_id)
            return node_id
        elif isinstance(node, (ast.For, ast.While)):
            last_id = node_id
            for n in node.body:
                last_id = adicionar_bloco(n, last_id)
            # Orelse do for/while
            if hasattr(node, 'orelse') and node.orelse:
                orelse_id = str(contador['id'])
                dot.node(orelse_id, "orelse")
                dot.edge(node_id, orelse_id)
                contador['id'] += 1
                last_orelse_id = orelse_id
                for n in node.orelse:
                    last_orelse_id = adicionar_bloco(n, last_orelse_id)
            return node_id
        elif hasattr(node, 'body') and isinstance(node.body, list):
            last_id = node_id
            for n in node.body:
                last_id = adicionar_bloco(n, last_id)
            return last_id
        return node_id

    adicionar_bloco(tree)
    dot.render('./images/fluxo_de_controle.png', cleanup=True, format='png')

# No bloco principal, adicione:
if __name__ == "__main__":
    analisar_codigo("main.py")
    print("\nÁrvore semântica simplificada de main.py:")
    with open("main.py", "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    exibir_arvore_semantica(tree)
    print("\nGerando gráfico da árvore semântica...")
    gerar_grafo_arvore_semantica(tree)
    print("\nGerando gráfico do fluxo de controle...")
    gerar_grafo_fluxo_de_controle(tree)