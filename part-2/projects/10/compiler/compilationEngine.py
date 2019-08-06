class CompilationEngine:
    def __init__(self, tokenizer, output_file):
        self.output_file = open(output_file, 'w')
        self.tokenizer = tokenizer
        self.current_indent = 0
    
    def inc_indent(self):
        self.current_indent += 4

    def dec_indent(self):
        self.current_indent -= 4
    
    def indent_tag(self):
        indentation = ' '*self.current_indent
        self.output_file.write(indentation)
        print(indentation, end='')
    
    def spitTerminal(self):
        self.output_file.write('<' + self.token_type.lower() + '>')
        print('<' + self.token_type.lower() + '>', end=' ')
        self.output_file.write(' ' + self.token + ' ')
        print(' ' + self.token + ' ', end=' ')
        self.output_file.write('</' + self.token_type.lower() + '>\n')
        print('</' + self.token_type.lower() + '>')

        self.indent_tag()
    
    def spitNonTerminal(self, non_terminal_name, end=False):

        if not end:
            self.output_file.write('<' + non_terminal_name + '>\n')
            print('<' + non_terminal_name + '>')
        else:
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
            for possible_match in grammar_token.split('#'):
                if possible_match in ['identifier', 'string', 'int', 'keywordConst', 'unary'] and self.match_grammar(grammar_token):
                    break
                elif possible_match == 'subroutineCall':
                    self.compileSubroutineCall()
                    break
                elif possible_match != grammar_token:
                    raise Exception(possible_match)
                else:
                    self.spitTerminal()

        if self.token != grammar_token:
            raise Exception(self.token)
        self.spitTerminal()
        return True
    
    def compileTerm(self):
        self.spitNonTerminal('term')
        self.inc_indent()
        
        self.compileTerm()
    
    def compileOp(self):
        self.spitNonTerminal('op')
        self.inc_indent()

        self.eat('+#=#-#/#*#>#<#&#|')

        self.dec_indent()
        self.spitNonTerminal('op', end=True)
    
    def compileExpression(self):
        self.spitNonTerminal('expression')
        self.inc_indent()

        self.compileTerm()
        if self.tokenizer.look_ahead()[0] in ['+', '=', '-', '/', '*', '>', '<', '&', '|']:
            self.compileOp()
            self.compileTerm()
        
        self.dec_indent()
        self.spitNonTerminal('expression', end=True)
    
    def compileExpressionList(self):
        self.spitNonTerminal('expressionList')
        self.inc_indent()

        if self.tokenizer.look_ahead()[1] in ['intConst', 'stringConst', 'identifier'] or \
            self.tokenizer.look_ahead()[0] in ['this', 'null', 'true', 'false']:
            self.compileExpression()

            while(self.tokenizer.look_ahead()[0] == ','):
                self.compileExpression()
        
        self.dec_indent()
        self.spitNonTerminal('expressionList', end=True)


    def compileSubroutineCall(self):
        self.spitNonTerminal('subroutineCall')
        self.inc_indent()

        self.eat('identifier')
        if self.tokenizer.look_ahead()[0] == '.':
            self.eat('.')
            self.eat('identifier')
        self.eat('(')
        self.compileExpressionList()
        self.eat(')')

        self.dec_indent()
        self.spitNonTerminal('subroutineCall', end=True)
    
    def compileIfStatement(self):
        self.spitNonTerminal('ifStatement')
        self.inc_indent()

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
        
        self.dec_indent()
        self.spitNonTerminal('ifStatement', end=True)

    def compileWhileStatement(self):
        self.spitNonTerminal('whileStatement')
        self.inc_indent()

        self.eat('while')
        self.eat('(')
        self.compileExpression()
        self.eat(')')
        self.eat('{')
        self.compileStatements()
        self.eat('}')

        self.dec_indent()
        self.spitNonTerminal('whileStatement', end=True)
    
    def compileLetStatement(self):
        self.spitNonTerminal('letStatement')
        self.inc_indent()

        self.eat('let')
        self.eat('identifier')

        if self.tokenizer.look_ahead()[0] == '[':
            self.eat('[')
            self.compileExpression()
            self.eat(']')
        
        self.eat('=')
        self.compileExpression()
        self.eat(';')

        self.dec_indent()
        self.spitNonTerminal('letStatement', end=True)
    
    def compileDoStatement(self):
        self.spitNonTerminal('doStatement')
        self.inc_indent()

        self.eat('do')
        self.compileSubroutineCall()
        self.eat(';')

        self.dec_indent()
        self.spitNonTerminal('doStatement', end=True)
    
    def compileReturnStatement(self):
        self.spitNonTerminal('returnStatement')
        self.inc_indent()

        self.eat('return')
        if self.tokenizer.look_ahead()[0] != ';':
            self.compileExpression()
        
        self.dec_indent()
        self.spitNonTerminal('returnStatement', end=True)

    
    def compileStatements(self):
        if self.tokenizer.look_ahead()[0] not in ['let', 'if', 'while', 'do', 'return']:
            return
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

    def compileType(self):
        self.spitNonTerminal('type')
        self.inc_indent()
        self.eat('int|char|boolean|identifier')
        self.dec_indent()
        self.spitNonTerminal('type', end=True)

    def compileClassVarDec(self):
        self.inc_indent()

        self.eat('static|field')
        self.compileType()
        self.eat('identifier')

        while(self.tokenizer.look_ahead()[0] == ','):
            self.eat(',')
            self.eat('identifier')
        
        self.eat(';')
    
    def compileParameterList(self):
        self.spitNonTerminal('parameterList')
        self.inc_indent()

        self.compileType()
        self.eat('identifier')

        while(self.tokenizer.look_ahead()[0] == ','):
            self.eat(',')
            self.compileType()
            self.eat('identifier')
        
        self.dec_indent()
        self.spitNonTerminal('parameterList', end=True)
    
    def compileVarDec(self):
        self.spitNonTerminal('varDec')
        self.inc_indent()

        self.eat('var')
        self.compileType()
        self.eat('identifier')

        while(self.tokenizer.look_ahead()[0] == ','):
            self.eat(',')
            self.eat('identifier')
        self.eat(';')

        self.dec_indent()
        self.spitNonTerminal('varDec', end=True)
    
    def compileSubroutineBody(self):
        self.spitNonTerminal('subroutineBody')
        self.inc_indent()

        self.eat('{')
        while (self.tokenizer.look_ahead()[0] == 'var'):
            self.compileVarDec()
        
        self.compileStatements()
        self.eat('}')

        self.dec_indent()
        self.spitNonTerminal('subroutineBody', end=True)

    def compileSubroutineDec(self):
        self.spitNonTerminal('subroutineDec')
        self.inc_indent()

        self.eat('constructor|function|method')
        if self.tokenizer.look_ahead()[0] == 'void':
            self.eat('void')
        else:
            self.compileType()
        self.eat('identifier')

        self.eat('(')

        if self.tokenizer.look_ahead()[0] != ')':
            self.compileParameterList()
        self.eat(')')

        self.compileSubroutineBody()

        self.dec_indent()
        self.spitNonTerminal('subroutine', end=True)

    def compileClass(self):
        self.spitNonTerminal('class')
        self.inc_indent()
        self.indent_tag()

        self.eat('identifier')
        self.eat('{')

        if self.tokenizer.look_ahead()[0] in ['static', 'field']:
            self.spitNonTerminal('classVarDec')

            while(self.tokenizer.look_ahead()[0] in ['static', 'field']):
                self.compileClassVarDec()
            
            self.spitNonTerminal('classVarDec', end=True)
        
        if self.tokenizer.look_ahead()[0] in ['constructor', 'function', 'method']:
            self.spitNonTerminal('subroutineDec')

            while(self.tokenizer.look_ahead()[0] in ['constructor', 'function', 'method']):
                self.compileSubroutineDec()
            
            self.spitNonTerminal('subroutineDec', end=True)
        
        self.eat('}')
    
        self.dec_indent()
        self.indent_tag()
        self.spitNonTerminal('class', end=True)
    
    def run(self):
        self.compileClass()
