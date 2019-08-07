class CompilationEngine:
    def __init__(self, tokenizer, output_file):
        self.output_file = open(output_file, 'w')
        self.tokenizer = tokenizer
        self.current_indent = 0
        self.first_idr = True
    
    def inc_indent(self):
        self.current_indent += 2

    def dec_indent(self):
        self.current_indent -= 2
    
    def indent_tag(self):
        indentation = ' '*self.current_indent
        self.output_file.write(indentation)
        print(indentation, end='')
    
    def spitTerminal(self):
        not_default = False
        if self.token_type == 'stringConst':
            self.token, self.token_type = self.token.strip('"'), 'stringConstant'
            not_default = True
        elif self.token_type == 'intConst':
            self.token_type = 'integerConstant'
            not_default = True
        elif self.token in ['&', '>', '<']:
            if self.token == '&': self.token = '&amp;'
            elif self.token == '<': self.token = '&lt;'
            elif self.token == '>': self.token = '&gt;'
        self.indent_tag()
        if not_default:
            self.output_file.write('<' + self.token_type + '>')
        else:
            self.output_file.write('<' + self.token_type.lower() + '>')
        print('<' + self.token_type.lower() + '>', end=' ')

        self.output_file.write(' ' + self.token + ' ')
        print(' ' + self.token + ' ', end=' ')

        if not_default:
            self.output_file.write('</' + self.token_type + '>\n')
        else:
            self.output_file.write('</' + self.token_type.lower() + '>\n')
        print('</' + self.token_type.lower() + '>')
    
    def spitNonTerminal(self, non_terminal_name, end=False):
        if not end:
            self.indent_tag()
            self.output_file.write('<' + non_terminal_name + '>\n')
            print('<' + non_terminal_name + '>')
            self.inc_indent()
        else:
            self.dec_indent()
            self.indent_tag()
            self.output_file.write('</' + non_terminal_name + '>\n')
            print('</' + non_terminal_name + '>')
    
    def get_comparison_list(self, rule):
        if rule == 'identifier':
            return ['identifier']
        elif rule == 'keywordConst':
            return ['this', 'null', 'true', 'false']
        elif rule == 'int':
            return ['intConst']
        elif rule == 'string':
            return ['stringConst']
        elif rule == 'unary':
            return ['-', '~']
    
    def match_grammar(self, rule):
        if rule in ['keywordConst', 'unary']:
            compare = self.token
        else:
            compare = self.token_type
        
        comparison_list = self.get_comparison_list(rule)
        
        if compare in comparison_list:
            self.spitTerminal()
            return True
        else:
            raise Exception(self.token)
    
    def eat(self, grammar_token):
        self.token, self.token_type = self.tokenizer.advance()
        self.grammar_token = grammar_token

        if grammar_token in ['identifier', 'string', 'int', 'keywordConst', 'unary'] and self.match_grammar(grammar_token):
            return True

        if '#' in grammar_token:
            if self.token in grammar_token.split('#'):
                self.spitTerminal()
                return True
            elif '0identifier' in grammar_token.split('#') and self.token_type == 'identifier':
                self.match_grammar('identifier')
                return True
            elif 'subroutineCall' in grammar_token.split('#') and self.token_type == 'identifier':
                self.compileSubroutineCall()
                return True
            elif 'keywordConst' in grammar_token.split('#') and self.token_type == 'keyword':
                self.match_grammar('keywordConst')
                return True
            elif 'int' in grammar_token.split('#') and self.token_type == 'intConst':
                self.match_grammar('int')
                return True
            elif 'unary' in grammar_token.split('#') and self.token_type == 'symbol':
                self.match_grammar('unary')
                return True
            elif 'string' in grammar_token.split('#') and self.token_type == 'stringConst':
                self.match_grammar('string')
                return True
            else:
                raise Exception(self.token)

        if self.token != grammar_token:
            raise Exception(self.token)
        self.spitTerminal()
        return True
    
    def compileTerm(self):
        self.spitNonTerminal('term')
        
        if self.tokenizer.look_ahead()[0] in ['-', '~']:
            self.eat('unary')
            self.compileTerm()
        elif self.tokenizer.look_ahead()[1] == 'identifier' and self.tokenizer.look_ahead(1)[0] == '.':
            self.compileSubroutineCall()
        elif self.tokenizer.look_ahead()[1] == 'identifier' and self.tokenizer.look_ahead(1)[0] == '[':
            self.eat('identifier')
            self.eat('[')
            self.compileExpression()
            self.eat(']')
        elif self.tokenizer.look_ahead()[1] in ['intConst', 'stringConst', 'identifier', 'keyword']:
            self.eat('int#unary#string#0identifier#keywordConst#subroutineCall')
        elif '(' in self.tokenizer.look_ahead()[0]:
            self.eat('(')
            self.compileExpression()
            self.eat(')')
        else:
            raise Exception(self.token)

        self.spitNonTerminal('term', end=True)
    
    def compileOp(self):
        self.eat('+#=#-#/#*#>#<#&#|')
    
    def compileExpression(self):
        self.spitNonTerminal('expression')

        self.compileTerm()
        if self.tokenizer.look_ahead()[0] in ['+', '=', '-', '/', '*', '>', '<', '&', '|']:
            self.compileOp()
            self.compileTerm()
        
        self.spitNonTerminal('expression', end=True)
    
    def compileExpressionList(self):
        if self.tokenizer.look_ahead()[1] in ['intConst', 'stringConst', 'identifier'] or \
            self.tokenizer.look_ahead()[0] in ['this', 'null', 'true', 'false', '(', ')', '-', '~']:
            self.compileExpression()

            while(self.tokenizer.look_ahead()[0] == ','):
                self.eat(',')
                self.compileExpression()

    def compileSubroutineCall(self):
        self.eat('identifier')
        if self.tokenizer.look_ahead()[0] == '.':
            self.eat('.')
            self.eat('identifier')
        self.eat('(')
        self.spitNonTerminal('expressionList')
        if self.tokenizer.look_ahead()[0] != ')':
            self.compileExpressionList()
        self.spitNonTerminal('expressionList', end=True)
        self.eat(')')
    
    def compileIfStatement(self):
        self.spitNonTerminal('ifStatement')

        self.eat('if')
        self.eat('(')
        self.compileExpression()
        self.eat(')')
        self.eat('{')

        self.compileStatements()

        self.eat('}')

        if self.tokenizer.look_ahead()[0] == 'else':
            self.eat('else')
            self.eat('{')
           
            self.compileStatements()

            self.eat('}')
        
        self.spitNonTerminal('ifStatement', end=True)

    def compileWhileStatement(self):
        self.spitNonTerminal('whileStatement')

        self.eat('while')
        self.eat('(')
        self.compileExpression()
        self.eat(')')
        self.eat('{')

        self.compileStatements()

        self.eat('}')

        self.spitNonTerminal('whileStatement', end=True)
    
    def compileLetStatement(self):
        self.spitNonTerminal('letStatement')

        self.eat('let')
        self.eat('identifier')

        if self.tokenizer.look_ahead()[0] == '[':
            self.eat('[')
            self.compileExpression()
            self.eat(']')
        
        self.eat('=')
        self.compileExpression()
        self.eat(';')

        self.spitNonTerminal('letStatement', end=True)
    
    def compileDoStatement(self):
        self.spitNonTerminal('doStatement')

        self.eat('do')
        self.compileSubroutineCall()
        self.eat(';')

        self.spitNonTerminal('doStatement', end=True)
    
    def compileReturnStatement(self):
        self.spitNonTerminal('returnStatement')

        self.eat('return')
        if self.tokenizer.look_ahead()[0] != ';':
            self.compileExpression()
        self.eat(';')
        
        self.spitNonTerminal('returnStatement', end=True)

    
    def _compileStatements(self, not_spit=False):
        if self.tokenizer.look_ahead()[0] not in ['let', 'if', 'while', 'do', 'return']:
            return
        
        if self.tokenizer.look_ahead()[0] == 'if':
            self.spitNonTerminal('statements')
            self.compileIfStatement()
            self.spitNonTerminal('statements', True)
        elif self.tokenizer.look_ahead()[0] == 'while':
            self.spitNonTerminal('statements')
            self.compileWhileStatement()
            self.spitNonTerminal('statements', True)
        elif self.tokenizer.look_ahead()[0] == 'let':
            self.compileLetStatement()
        elif self.tokenizer.look_ahead()[0] == 'do':
            self.compileDoStatement()
        elif self.tokenizer.look_ahead()[0] == 'return':
            self.compileReturnStatement()
        self.compileStatements()
    
    def compileStatement(self):
        if self.tokenizer.look_ahead()[0] == 'if':
            self.compileIfStatement()
        elif self.tokenizer.look_ahead()[0] == 'while':
            self.compileWhileStatement()
        elif self.tokenizer.look_ahead()[0] == 'let':
            self.compileLetStatement()
        elif self.tokenizer.look_ahead()[0] == 'do':
            self.compileDoStatement()
        elif self.tokenizer.look_ahead()[0] == 'return':
            self.compileReturnStatement()
    
    def compileStatements(self):
        if (self.tokenizer.look_ahead()[0] in ['let', 'do', 'return', 'if', 'while']):
            self.spitNonTerminal('statements')
            while (self.tokenizer.look_ahead()[0] in ['let', 'do', 'return', 'if', 'while']):
                self.compileStatement()
            self.spitNonTerminal('statements', True)
    
    def compileType(self):
        self.eat('int#char#boolean#0identifier')

    def compileClassVarDec(self):

        self.eat('static#field')
        self.compileType()
        self.eat('identifier')

        while(self.tokenizer.look_ahead()[0] == ','):
            self.eat(',')
            self.eat('identifier')
        
        self.eat(';')
    
    def compileParameterList(self):
        self.compileType()
        self.eat('identifier')

        while(self.tokenizer.look_ahead()[0] == ','):
            self.eat(',')
            self.compileType()
            self.eat('identifier')

    def compileVarDec(self):
        self.spitNonTerminal('varDec')

        self.eat('var')
        self.compileType()
        self.eat('identifier')

        while(self.tokenizer.look_ahead()[0] == ','):
            self.eat(',')
            self.eat('identifier')
        self.eat(';')

        self.spitNonTerminal('varDec', end=True)

    def compileSubroutineBody(self):
        self.spitNonTerminal('subroutineBody')

        self.eat('{')
        while (self.tokenizer.look_ahead()[0] == 'var'):
            self.compileVarDec()
        self.compileStatements()

        self.eat('}')

        self.spitNonTerminal('subroutineBody', end=True)

    def compileSubroutineDec(self):
        self.eat('constructor#function#method')
        if self.tokenizer.look_ahead()[0] == 'void':
            self.eat('void')
        else:
            self.compileType()
        self.eat('identifier')

        self.eat('(')

        self.spitNonTerminal('parameterList')
        if self.tokenizer.look_ahead()[0] != ')':
            self.compileParameterList()
        self.spitNonTerminal('parameterList', end=True)
        self.eat(')')

        self.compileSubroutineBody()

    def compileClass(self):
        self.spitNonTerminal('class')
    
        self.eat('class')
        self.eat('identifier')
        self.eat('{')

        while(self.tokenizer.look_ahead()[0] in ['static', 'field']):
            self.spitNonTerminal('classVarDec')
            self.compileClassVarDec()
            self.spitNonTerminal('classVarDec', end=True)
    
        while(self.tokenizer.look_ahead()[0] in ['constructor', 'function', 'method']):
            self.spitNonTerminal('subroutineDec')
            self.compileSubroutineDec()
            self.spitNonTerminal('subroutineDec', end=True)
        
        self.eat('}')
    
        self.spitNonTerminal('class', end=True)
    
    def run(self):
        self.compileClass()
