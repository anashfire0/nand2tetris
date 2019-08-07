import re

class Tokenizer:

    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var',
                'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let',
                'do', 'if', 'else', 'while', 'return']
    
    symbols = ['(', ')', '[', ']', '{', '}', ',', ';', '+', '-', '*', '/', '.', '>', '<', '&', '|', '=', '~']
    symbols_split = r'([\(\)\[\]\{\}\,\;\+\-\*\/\.\>\<\&\|\=\~])'
    identifier = re.compile(r'[a-zA-Z_][a-zA-Z_\d]*')
    string = re.compile(r'".*"')
    whitespace = re.compile(r'\s*')

    def __init__(self, input_file):
        self.input_file_name = input_file
        self.all_tokens = []
        self.set_all_tokens()
        self.current_token_pointer = 0

    @classmethod
    def is_string(cls, token):
        return Tokenizer.string.match(token)
    
    @classmethod
    def is_identifier(cls, token):
        return Tokenizer.identifier.match(token)
    
    @classmethod
    def is_symbol(cls, token):
        return token in Tokenizer.symbols
    
    @classmethod
    def is_int(cls, token):
        try:
            return -1 < int(token) < 2**15
        except ValueError:
            return False
    
    @classmethod
    def split_symbols(cls, line):
        return filter(lambda y: y, map(lambda x: x.strip(), re.split(Tokenizer.symbols_split, line)))
    
    @classmethod
    def is_keyword(cls, token):
        return token in Tokenizer.keywords
    
    def token_type(self, token):
        if token in Tokenizer.keywords: return token, 'keyword'
        elif Tokenizer.is_identifier(token): return token, 'identifier'
        elif Tokenizer.is_string(token): return token, 'stringConst'
        elif Tokenizer.is_int(token): return token, 'intConst'
        elif Tokenizer.is_symbol(token): return token, 'symbol'
    
    def strip_comments_and_whitespaces(self, line, input_file):
        multiple_line_comment, single_line_comment = line.find(r'/*'), line.find(r'//')
        if multiple_line_comment == -1:
            if single_line_comment == -1:
                return line.strip()
            else:
                return line[:single_line_comment].strip()
        else:
            if line.find(r'*/') != -1: return ''
            line = line[:multiple_line_comment].strip()
            if line.find(r'*/') == -1:
                for next_line in input_file:
                    if next_line.find(r'*/') != -1: break
            return line.strip()
    
    def look_ahead(self, ahead=0):
        try:
            return self.all_tokens[self.current_token_pointer+ahead]
        except IndexError:
            return 'END'
    
    def advance(self):
        try:
            to_ret = self.all_tokens[self.current_token_pointer]
            self.current_token_pointer += 1
            return to_ret
        except IndexError:
            return 'END'
    
    def set_all_tokens(self):
        with open(self.input_file_name, 'r') as input_file:
            for line in input_file:
                line = self.strip_comments_and_whitespaces(line, input_file)
                if not line: continue
                for possible_token in Tokenizer.split_symbols(line):
                    if Tokenizer.is_string(possible_token):
                        self.all_tokens.append(self.token_type(possible_token.strip()))
                        continue
                    tokens = possible_token.split()
                    for token in tokens:
                        self.all_tokens.append(self.token_type(token.strip()))
                        

if __name__ == '__main__':
    tok = Tokenizer('test.txt')
    for i in range(10):
        print(tok.advance())
    print(tok.current_token_pointer)
    for i in range(3):
        print(tok.look_ahead())
    print(tok.current_token_pointer)
    for i in range(5):
        print(tok.advance())
    print(tok.current_token_pointer)

                        