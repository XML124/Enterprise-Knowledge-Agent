import ast, operator
from app.rag.retrieval import retrieve

def search_documents(question: str, top_k: int = 4):
    return retrieve(question, top_k=top_k)

_ALLOWED = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow}

def _eval(node):
    if isinstance(node, ast.Expression): return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int,float)): return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.left), _eval(node.right))
    raise ValueError("Unsupported expression")

def calculator(expression: str) -> float:
    return float(_eval(ast.parse(expression, mode="eval")))
