class Node:
    # الصنف الاساسي لجميع العقد
    pass

class PrintNode(Node):
    def __init__(self, values):
        self.values = values
    def __repr__(self):
        return f"PrintNode({self.values})"

class VarAssignNode(Node):
    def __init__(self, var_type, var_name, value_node):
        self.var_type = var_type
        self.var_name = var_name
        self.value_node = value_node
    def __repr__(self):
        return f"VarAssignNode({self.var_type} {self.var_name} = {self.value_node})"

class VarReassignNode(Node):
    #اعادة اسناد متغير موجود مثل  .
    def __init__(self, var_name, value_node):
        self.var_name = var_name
        self.value_node = value_node
    def __repr__(self):
        return f"VarReassignNode({self.var_name} = {self.value_node})"

class NumberNode(Node):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NumberNode({self.value})"

class StringNode(Node):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"StringNode(\"{self.value}\")"

class CharNode(Node):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"CharNode('{self.value}')"

class BoolNode(Node):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"BoolNode({self.value})"

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"IdentifierNode({self.name})"

class BinaryOpNode(Node):
    # عمليات حسابية ومقارنة ومنطقية
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinaryOpNode({self.left} {self.op} {self.right})"

class IfNode(Node):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
    def __repr__(self):
        return f"IfNode({self.condition}, body={self.body}, else={self.else_body})"

class WhileNode(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self):
        return f"WhileNode({self.condition}, {self.body})"

class ForNode(Node):
    # كرر عداد من 1 الى 5 .
    def __init__(self, var_name, start, end, body):
        self.var_name = var_name
        self.start = start      
        self.end = end
        self.body = body
    def __repr__(self):
        return f"ForNode({self.var_name}, {self.start}, {self.end})"

class SwitchNode(Node):
    # اختر قيمة  .
    def __init__(self, value, cases, default=None):
        self.value = value
        self.cases = cases
        self.default = default
    def __repr__(self):
        return f"SwitchNode({self.value})"  

class FunctionDefNode(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def __repr__(self):
        return f"FunctionDefNode({self.name}, {self.params})"

class FunctionCallNode(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def __repr__(self):
        return f"FunctionCallNode({self.name}, {self.args})"

class ReturnNode(Node):
    def __init__(self, value_node):
        self.value_node = value_node
    def __repr__(self):
        return f"ReturnNode({self.value_node})"