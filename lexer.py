class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', Line: {self.line})"

class Lexer:
    # الكلمات المفتاحية 
    KEYWORDS = [
        "اطبع", "ثنائي", "نص", "حرف", "عشري", "صحيح",
        "اذا", "والا", "بينما", "كرر", "نهاية",
        "ارجع", "دالة", "صح", "خطأ",
        "من", "الى",
        "و", "او",
        "اختر", "حالة", "افتراضي"
    ]

    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.pos = 0
        self.line = 1

    def tokenize(self):
        self.pos = 0
        self.line = 1
        self.tokens = []

        while self.pos < len(self.code):
            char = self.code[self.pos]

            # تجاهل المسافات والاسطر
            if char.isspace():
                if char == '\n':
                    self.line += 1
                self.pos += 1
                continue

            # التعليقات ب !!
            if self.code[self.pos:self.pos+2] == '!!':
                while self.pos < len(self.code) and self.code[self.pos] != '\n':
                    self.pos += 1
                continue

            # النصوص بين " "
            if char == '"':
                self.pos += 1
                string_val = ""
                while self.pos < len(self.code) and self.code[self.pos] != '"':
                    string_val += self.code[self.pos]
                    self.pos += 1
                self.pos += 1
                self.tokens.append(Token("STRING", string_val, self.line))
                continue

            # الحرف الواحد بين ' '
            if char == "'":
                self.pos += 1
                char_val = ""
                if self.pos < len(self.code) and self.code[self.pos] != "'":
                    char_val = self.code[self.pos]
                    self.pos += 1
                if self.pos < len(self.code) and self.code[self.pos] == "'":
                    self.pos += 1
                    self.tokens.append(Token("CHAR", char_val, self.line))
                else:
                    raise Exception(f"خطا في السطر {self.line}: حرف مفتوح بدون اغلاق، اضف ' في النهاية")
                continue

            # الارقام الصحيحة والعشرية
            if char.isdigit():
                num_str = ""
                while self.pos < len(self.code):
                    current_char = self.code[self.pos]
                    if current_char.isdigit():
                        num_str += current_char
                        self.pos += 1
                    elif current_char == ".":
                        next_pos = self.pos + 1
                        if next_pos < len(self.code) and self.code[next_pos].isdigit():
                            num_str += current_char
                            self.pos += 1
                        else:
                            break
                    else:
                        break
                if "." in num_str:
                    self.tokens.append(Token("FLOAT", float(num_str), self.line))
                else:
                    self.tokens.append(Token("INT", int(num_str), self.line))
                continue

            # الكلمات المفتاحية والمعرفات
            if char.isalpha() or char == '_' or '\u0600' <= char <= '\u06ff':
                id_str = ""
                while self.pos < len(self.code) and (
                    self.code[self.pos].isalnum() or
                    self.code[self.pos] == '_' or
                    '\u0600' <= self.code[self.pos] <= '\u06ff'
                ):
                    id_str += self.code[self.pos]
                    self.pos += 1
                if id_str in self.KEYWORDS:
                    self.tokens.append(Token("KEYWORD", id_str, self.line))
                else:
                    self.tokens.append(Token("IDENTIFIER", id_str, self.line))
                continue

            # الرموز والعمليات
            if char in "+-*/><=!":
                two = self.code[self.pos:self.pos+2]
                if two == "==":
                    self.tokens.append(Token("EQUALS", "==", self.line))
                    self.pos += 2
                elif two == "!=":
                    self.tokens.append(Token("NEQ", "!=", self.line))
                    self.pos += 2
                elif two == "<=":
                    self.tokens.append(Token("LTE", "<=", self.line))
                    self.pos += 2
                elif two == ">=":
                    self.tokens.append(Token("GTE", ">=", self.line))
                    self.pos += 2
                else:
                    type_map = {
                        "+": "PLUS", "-": "MINUS", "*": "MUL", "/": "DIV",
                        ">": "GT", "<": "LT", "=": "ASSIGN"
                    }
                    if char in type_map:
                        self.tokens.append(Token(type_map[char], char, self.line))
                    self.pos += 1
                continue

            # نقطة نهاية السطر
            if char == ".":
                self.tokens.append(Token("DOT_END", ".", self.line))
                self.pos += 1
                continue

            # تخطي اي رمز غير معروف
            self.pos += 1

        return self.tokens