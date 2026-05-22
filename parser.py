from ast_nodes import (
    VarAssignNode, VarReassignNode, PrintNode,
    NumberNode, StringNode, CharNode, BoolNode, IdentifierNode,
    BinaryOpNode, IfNode, WhileNode, ForNode, SwitchNode,
    FunctionDefNode, FunctionCallNode, ReturnNode
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        token = self.current_token()
        if token is None:
            raise Exception("خطا: وصلنا لنهاية الكود بشكل غير متوقع، ربما ناقصة نقطة في اخر سطر")
        if token.type != token_type:
            raise Exception(
                f"خطا في السطر {token.line}: توقعت '{token_type}' لكن وجدت '{token.value}'"
            )
        self.pos += 1
        return token

    def parse(self):
        nodes = []
        while self.pos < len(self.tokens):
            stmt = self.statement()
            if stmt:
                nodes.append(stmt)
        return nodes

    def statement(self):
        token = self.current_token()
        if token is None:
            return None

        # تعريف متغير
        if token.type == "KEYWORD" and token.value in ["صحيح", "عشري", "نص", "حرف", "ثنائي"]:
            return self.var_assignment()

        # طباعة
        elif token.type == "KEYWORD" and token.value == "اطبع":
            return self.print_statement()

        # شرط
        elif token.type == "KEYWORD" and token.value == "اذا":
            return self.if_statement()

        # بينما
        elif token.type == "KEYWORD" and token.value == "بينما":
            return self.while_statement()

        #كرر
        elif token.type == "KEYWORD" and token.value == "كرر":
            return self.for_statement()

        # اختر
        elif token.type == "KEYWORD" and token.value == "اختر":
            return self.switch_statement()

        # تعريف دالة
        elif token.type == "KEYWORD" and token.value == "دالة":
            return self.function_def()

        # ارجع
        elif token.type == "KEYWORD" and token.value == "ارجع":
            return self.return_statement()

        # معرف اعادة اسناد او استدعاء دالة
        elif token.type == "IDENTIFIER":
            next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_token and next_token.type == "ASSIGN":
                return self.var_reassign()
            else:
                return self.function_call_statement()

        else:
            raise Exception(
                f"خطا في السطر {token.line}: الكلمة '{token.value}' غير معروفة او غير مدعومة حاليا"
            )

    def var_assignment(self):
        try:
            var_type = self.eat("KEYWORD").value
            var_name = self.eat("IDENTIFIER").value
            self.eat("ASSIGN")
            value_node = self.comparison()
            self.eat("DOT_END")
            return VarAssignNode(var_type, var_name, value_node)
        except Exception as e:
            raise Exception(f"خطا في تعريف المتغير — {str(e)}")

    def var_reassign(self):
        try:
            var_name = self.eat("IDENTIFIER").value
            self.eat("ASSIGN")
            value_node = self.comparison()
            self.eat("DOT_END")
            return VarReassignNode(var_name, value_node)
        except Exception as e:
            raise Exception(f"خطا في اسناد المتغير — {str(e)}")

    def print_statement(self):
        try:
            self.eat("KEYWORD")  # اطبع
            values = [self.comparison()]
            while self.current_token() and self.current_token().type == "PLUS":
                self.pos += 1
                values.append(self.comparison())
            self.eat("DOT_END")
            return PrintNode(values)
        except Exception as e:
            raise Exception(f"خطا في جملة الطباعة — {str(e)}")

    def if_statement(self):
        try:
            self.eat("KEYWORD")  # اذا
            condition = self.comparison()
            self.eat("DOT_END")

            body = []
            while self.current_token() and not (
                self.current_token().type == "KEYWORD" and
                self.current_token().value in ("نهاية", "والا")
            ):
                body.append(self.statement())

            else_body = None
            if self.current_token() and self.current_token().value == "والا":
                self.eat("KEYWORD")  # والا
                self.eat("DOT_END")
                else_body = []
                while self.current_token() and not (
                    self.current_token().type == "KEYWORD" and
                    self.current_token().value == "نهاية"
                ):
                    else_body.append(self.statement())

            if self.current_token() is None:
                raise Exception("خطا: جملة 'اذا' بدون 'نهاية' في الاخر")
            self.eat("KEYWORD")  # نهاية
            self.eat("DOT_END")
            return IfNode(condition, body, else_body)
        except Exception as e:
            raise Exception(f"خطا في جملة الشرط — {str(e)}")

    def while_statement(self):
        try:
            self.eat("KEYWORD")  # بينما
            condition = self.comparison()
            self.eat("DOT_END")

            body = []
            while self.current_token() and not (
                self.current_token().type == "KEYWORD" and
                self.current_token().value == "نهاية"
            ):
                body.append(self.statement())

            if self.current_token() is None:
                raise Exception("خطا: جملة 'بينما' بدون 'نهاية' في الاخر")
            self.eat("KEYWORD")  # نهاية
            self.eat("DOT_END")
            return WhileNode(condition, body)
        except Exception as e:
            raise Exception(f"خطا في جملة التكرار — {str(e)}")

    def for_statement(self):
        try:
            self.eat("KEYWORD")                     # كرر
            var_name = self.eat("IDENTIFIER").value  # اسم المتغير
            self.eat("KEYWORD")                     # من
            start = self.expression()               # قيمة البداية
            self.eat("KEYWORD")                     # الى
            end = self.expression()                 # قيمة النهاية
            self.eat("DOT_END")                     # .

            body = []
            while self.current_token() and not (
                self.current_token().type == "KEYWORD" and
                self.current_token().value == "نهاية"
            ):
                body.append(self.statement())

            if self.current_token() is None:
                raise Exception("خطا: جملة 'كرر' بدون 'نهاية' في الاخر")
            self.eat("KEYWORD")  # نهاية
            self.eat("DOT_END")
            return ForNode(var_name, start, end, body)
        except Exception as e:
            raise Exception(f"خطا في جملة التكرار — {str(e)}")

    def switch_statement(self):
        try:
            self.eat("KEYWORD")   # اختر
            value = self.expression()
            self.eat("DOT_END")   # .

            cases = []            
            default = None

            while self.current_token() and not (
                self.current_token().type == "KEYWORD" and
                self.current_token().value == "نهاية"
            ):
                if self.current_token().value == "حالة":  
                    self.eat("KEYWORD")       # حالة
                    case_val = self.expression()
                    self.eat("DOT_END")       # .
                    case_body = []
                    while self.current_token() and not (
                        self.current_token().type == "KEYWORD" and
                        self.current_token().value in ("نهاية", "افتراضي", "حالة")
                    ):
                        case_body.append(self.statement())
                    cases.append((case_val, case_body))

                elif self.current_token().value == "افتراضي":
                    self.eat("KEYWORD")       # افتراضي
                    self.eat("DOT_END")       # .
                    default = []
                    while self.current_token() and not (
                        self.current_token().type == "KEYWORD" and
                        self.current_token().value == "نهاية"
                    ):
                        default.append(self.statement())
                else:
                    break

            if self.current_token() is None:
                raise Exception("خطا: جملة 'اختر' بدون 'نهاية' في الاخر")
            self.eat("KEYWORD")   # نهاية
            self.eat("DOT_END")
            return SwitchNode(value, cases, default)
        except Exception as e:
            raise Exception(f"خطا في جملة الاختيار — {str(e)}")

    def function_def(self):
        try:
            self.eat("KEYWORD")  # دالة
            name = self.eat("IDENTIFIER").value
            params = []
            while self.current_token() and self.current_token().type != "DOT_END":
                params.append(self.eat("IDENTIFIER").value)
            self.eat("DOT_END")

            body = []
            while self.current_token() and not (
                self.current_token().type == "KEYWORD" and
                self.current_token().value == "نهاية"
            ):
                body.append(self.statement())

            if self.current_token() is None:
                raise Exception("خطا: دالة بدون 'نهاية' في الاخر")
            self.eat("KEYWORD")  # نهاية
            self.eat("DOT_END")
            return FunctionDefNode(name, params, body)
        except Exception as e:
            raise Exception(f"خطا في تعريف الدالة — {str(e)}")

    def function_call_statement(self):
        try:
            name = self.eat("IDENTIFIER").value
            args = []
            while self.current_token() and self.current_token().type != "DOT_END":
                args.append(self.expression())
            self.eat("DOT_END")
            return FunctionCallNode(name, args)
        except Exception as e:
            raise Exception(f"خطا في استدعاء الدالة — {str(e)}")

    def return_statement(self):
        try:
            self.eat("KEYWORD")  # ارجع
            value_node = self.expression()
            self.eat("DOT_END")
            return ReturnNode(value_node)
        except Exception as e:
            raise Exception(f"خطا في جملة الإرجاع — {str(e)}")

    def expression(self):
        # عمليات حسابية فقط
        left = self.primary()
        while self.current_token() and self.current_token().type in ("PLUS", "MINUS", "MUL", "DIV"):
            op = self.current_token().value
            self.pos += 1
            right = self.primary()
            left = BinaryOpNode(left, op, right)
        return left

    def comparison(self):
        # مقارنة   
        left = self.expression()
        comp_types = ("EQUALS", "NEQ", "GT", "LT", "GTE", "LTE")
        if self.current_token() and self.current_token().type in comp_types:
            op = self.current_token().value
            self.pos += 1
            right = self.expression()
            left = BinaryOpNode(left, op, right)

        #  بعد المقارنة
        while self.current_token() and (
            self.current_token().type == "KEYWORD" and
            self.current_token().value in ("و", "او")
        ):
            logic_op = self.current_token().value
            self.pos += 1
            right = self.comparison()
            left = BinaryOpNode(left, logic_op, right)

        return left

    def primary(self):
        token = self.current_token()
        if token is None:
            raise Exception("خطا: توقعت قيمة لكن وصلنا لنهاية الكود")

        if token.type == "INT":
            self.eat("INT")
            return NumberNode(token.value)

        elif token.type == "FLOAT":
            self.eat("FLOAT")
            return NumberNode(token.value)

        elif token.type == "STRING":
            self.eat("STRING")
            return StringNode(token.value)

        elif token.type == "CHAR":
            self.eat("CHAR")
            return CharNode(token.value)

        elif token.type == "KEYWORD" and token.value in ("صح", "خطا"):
            self.eat("KEYWORD")
            return BoolNode(token.value == "صح")

        elif token.type == "IDENTIFIER":
            name = self.eat("IDENTIFIER").value
            next_tok = self.current_token()
            if next_tok and next_tok.type not in (
                "DOT_END", "PLUS", "MINUS", "MUL", "DIV",
                "EQUALS", "NEQ", "GT", "LT", "GTE", "LTE", "ASSIGN"
            ) and not (next_tok.type == "KEYWORD" and next_tok.value in ("و", "او", "من", "الى", "نهاية", "والا", "افتراضي", "حالة")):
                args = []
                while self.current_token() and self.current_token().type not in (
                    "DOT_END", "PLUS", "MINUS", "MUL", "DIV",
                    "EQUALS", "NEQ", "GT", "LT", "GTE", "LTE"
                ):
                    args.append(self.primary())
                return FunctionCallNode(name, args)
            return IdentifierNode(name)

        else:
            raise Exception(
                f"خطا في السطر {token.line}: القيمة '{token.value}' غير مفهومة — "
                f"المقبول: ارقام، نصوص، احرف، اسماء متغيرات"
            )