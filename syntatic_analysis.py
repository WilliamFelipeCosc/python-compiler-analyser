import ast
import astpretty
from graphviz import Digraph

def gerar_ast(codigo_fonte):
    try:
        arvore = ast.parse(codigo_fonte)
        return arvore
    except SyntaxError as e:
        print("❌ Erro de sintaxe encontrado:")
        linha_erro = e.text.strip() if e.text is not None else ""
        print(f"Linha {e.lineno}, coluna {e.offset}: {linha_erro}")
        print(f"Detalhes: {e.msg}")
        return None

def ast_para_graphviz(node, dot=None, parent=None):
    if dot is None:
        dot = Digraph()
        dot.attr('node', shape='box')
    node_id = str(id(node))
    label = type(node).__name__
    dot.node(node_id, label)
    if parent:
        dot.edge(str(id(parent)), node_id)
    for child in ast.iter_child_nodes(node):
        ast_para_graphviz(child, dot, node)
    return dot

# Exemplo de uso
if __name__ == "__main__":
    with open("main.py", "r", encoding="utf-8") as f:
        codigo = f.read()

    ast_gerada = gerar_ast(codigo)
    if ast_gerada:
        print("✅ Código sintaticamente correto!\n")
        print("🌳 Árvore Sintática Abstrata (AST):\n")
        astpretty.pprint(ast_gerada)
        # Gerar imagem da AST
        dot = ast_para_graphviz(ast_gerada)
        dot.render("./images/ast_tree", format="png", cleanup=True)
        print("🖼️ Imagem da AST salva como 'ast_tree.png'")
