from ast_nodes import *

# استثناء خاص لتنفيذ ارجع داخل الدوال
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.output_lines = []

    def run(self, ast):
        try:
            for node in ast:

                # طباعة
                if isinstance(node, PrintNode):
                    parts = []
                    for val in node.values:
                        result = self.evaluate(val)
                        if result is True:
                            parts.append("صح")
                        elif result is False:
                            parts.append("خطا")
                        else:
                            parts.append(str(result))
                    self.output_lines.append("".join(parts))

                # تعريف متغير
                elif isinstance(node, VarAssignNode):
                    self.variables[node.var_name] = self.evaluate(node.value_node)

                # اعادة اسناد
                elif isinstance(node, VarReassignNode):
                    if node.var_name not in self.variables:
                        raise Exception(
                            f"خطا: المتغير '{node.var_name}' غير معرف، عرفه اولا قبل تغيير قيمته"
                        )
                    self.variables[node.var_name] = self.evaluate(node.value_node)

                # اذا  والا
                elif isinstance(node, IfNode):
                    condition = self.evaluate(node.condition)
                    target = node.body if condition else (node.else_body or [])
                    self.run(target)

                # بينما
                elif isinstance(node, WhileNode):
                    loop_count = 0
                    while self.evaluate(node.condition):
                        loop_count += 1
                        if loop_count > 10000:
                            raise Exception("خطا: حلقة لا نهائية — تاكد من الشرط داخل الحلقة")
                        self.run(node.body)

                # كرر
                elif isinstance(node, ForNode):
                    start = self.evaluate(node.start)
                    end = self.evaluate(node.end)
                    old_val = self.variables.get(node.var_name)
                    for i in range(int(start), int(end) + 1):
                        self.variables[node.var_name] = i
                        self.run(node.body)
                    # استرجاع القيمة القديمة او حذف المتغير
                    if old_val is not None:
                        self.variables[node.var_name] = old_val
                    else:
                        if node.var_name in self.variables:
                            del self.variables[node.var_name]

                # اختر 
                elif isinstance(node, SwitchNode):
                    value = self.evaluate(node.value)
                    matched = False
                    for case_val, case_body in node.cases:
                        if self.evaluate(case_val) == value:
                            self.run(case_body)
                            matched = True
                            break
                    if not matched and node.default:
                        self.run(node.default)

                # تعريف دالة
                elif isinstance(node, FunctionDefNode):
                    self.variables[node.name] = node

                # استدعاء دالة
                elif isinstance(node, FunctionCallNode):
                    self.call_function(node.name, node.args)

                # ارجع
                elif isinstance(node, ReturnNode):
                    value = self.evaluate(node.value_node)
                    raise ReturnException(value)

                else:
                    raise Exception(f"خطا داخلي: نوع العقدة '{type(node).__name__}' غير مدعوم")

        except ReturnException:
            raise
        except Exception as e:
            self.output_lines.append(str(e))

        return "\n".join(self.output_lines)

    def evaluate(self, node):
        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, StringNode):
            return node.value

        if isinstance(node, CharNode):
            return node.value

        if isinstance(node, BoolNode):
            return node.value

        if isinstance(node, IdentifierNode):
            if node.name in self.variables:
                return self.variables[node.name]
            raise Exception(f"خطا: المتغير '{node.name}' غير معرف، ")

        if isinstance(node, FunctionCallNode):
            return self.call_function(node.name, node.args)

        if isinstance(node, BinaryOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            try:
                if node.op == "+":
                    #   نص +رقم
                    if isinstance(left, str) or isinstance(right, str):
                        return str(left) + str(right)  
                    return left + right
                if node.op == "-":  return left - right
                if node.op == "*":  return left * right
                if node.op == "/":
                    if right == 0:
                        raise Exception("خطأ: لا يمكن القسمة على صفر")
                    return left / right
                if node.op == "==": return left == right
                if node.op == "!=": return left != right
                if node.op == ">":  return left > right
                if node.op == "<":  return left < right
                if node.op == ">=": return left >= right
                if node.op == "<=": return left <= right
                if node.op == "و":  return left and right
                if node.op == "او": return left or right
            except TypeError:
                raise Exception(
                    f"خطا: لا يمكن اجراء العملية '{node.op}' "
                    f"بين '{type(left).__name__}' و'{type(right).__name__}'"
                )

        raise Exception(f"خطا داخلي: نوع العقدة '{type(node).__name__}' غير متوقع")

    def call_function(self, name, args):
        if name not in self.variables:
            raise Exception(f"خطا: الدالة '{name}' غير معرفة،")

        func = self.variables[name]
        if not isinstance(func, FunctionDefNode):
            raise Exception(f"خطا: '{name}' متغير وليس دالة")

        if len(args) != len(func.params):
            raise Exception(
                f"خطا: الدالة '{name}' تتوقع {len(func.params)} معاملات "
                f"لكن اعطيت {len(args)}"
            )

        old_variables = self.variables.copy()

        for param, arg in zip(func.params, args):
            self.variables[param] = self.evaluate(arg)

        return_value = None
        try:
            self.run(func.body)
        except ReturnException as r:
            return_value = r.value
        finally:
            self.variables = old_variables

        return return_value