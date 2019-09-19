import SymbolTable
import glob
import vmwriter
import os

void_subroutines = ['Output.printInt', 'Output.printOutput', 'Memory.poke',
                    'Output.printString', 'Memory.deAlloc', 'Output.moveCursor', 
                    'Screen.clearScreen', 'Screen.setColor', 'Output.println',
                    'Screen.drawRectangle']

class CompilationEngine:
    def __init__(self, tokenizer, output_file):
        self.vm_writer = vmwriter.VMWriter(output_file)
        self.tokenizer = tokenizer
        self.current_indent = 0
        self.first_idr = True
        self.nArgs = 0

        self.symbol_table = SymbolTable.SymbolTable()
    
    @staticmethod
    def set_void_subroutines(source_files):
        for file in source_files:
            with open(file, 'r') as f:
                for line in f:
                    if 'void' in line:
                        void_subroutines.append(os.path.abspath(file).split('.')[-2].split('/')[-1]+'.'+line[line.find('void')+5 : line.find('(')])
                        if void_subroutines[-1] == 'move':
                            a=2
        # print(void_subroutines)

    
    def inc_indent(self):
        self.current_indent += 2

    def dec_indent(self):
        self.current_indent -= 2
    
    def indent_tag(self):
        indentation = ' '*self.current_indent
        # self.output_file.write(indentation)
    
    def spitTerminal(self):
        not_default = False
        if self.token_type == 'stringConst':
            self.token, self.token_type = self.token.strip('"'), 'stringConstant'
            not_default = True
        elif self.token_type == 'intConst':
            self.token_type = 'integerConstant'
            not_default = True
        elif self.token in ['&', '>', '<']:
            # if self.token == '&': self.token = '&amp;'
            # elif self.token == '<': self.token = '&lt;'
            # elif self.token == '>': self.token = '&gt;'
            pass
        self.indent_tag()
        if not_default:
            # self.output_file.write('<' + self.token_type + '>')
            pass
        else:
            # self.output_file.write('<' + self.token_type.lower() + '>')
            pass

        # self.output_file.write(' ' + self.token + ' ')

        if not_default:
            pass
            # self.output_file.write('</' + self.token_type + '>\n')
        else:
            pass
            # self.output_file.write('</' + self.token_type.lower() + '>\n')
    
    def spitNonTerminal(self, non_terminal_name, end=False):
        if not end:
            self.indent_tag()
            # self.output_file.write('<' + non_terminal_name + '>\n')
            self.inc_indent()
        else:
            self.dec_indent()
            self.indent_tag()
            # self.output_file.write('</' + non_terminal_name + '>\n')
    
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
            operation = self.token
            if operation == '-':
                operation = '--'
            self.compileTerm()
            # print(f'{operation}')
            self.vm_writer.writeArithmetic(operation)

        elif self.tokenizer.look_ahead()[1] == 'identifier' and self.tokenizer.look_ahead(1)[0] == '.':
            self.compileSubroutineCall()
            
        elif self.tokenizer.look_ahead()[1] == 'identifier' and self.tokenizer.look_ahead(1)[0] == '(':
            self.compileSubroutineCall()

        elif self.tokenizer.look_ahead()[1] == 'identifier' and self.tokenizer.look_ahead(1)[0] == '[':
            self.eat('identifier')
            dest_kind, dest_index = self.symbol_table.sub_level.kind_of(self.token), \
                                    self.symbol_table.sub_level.index_of(self.token)
            self.eat('[')
            self.compileExpression()
            self.eat(']')
            self.vm_writer.writeArrayPushForSource(dest_kind, dest_index)
            
        elif self.tokenizer.look_ahead()[1] in ['intConst', 'stringConst', 'identifier', 'keyword']:
            self.eat('int#unary#string#0identifier#keywordConst#subroutineCall')
            if self.token_type == 'integerConstant':
                # print(f'push const {self.token}')
                self.vm_writer.writePush('constant', self.token)
            if self.token_type == 'identifier':
                segment = self.symbol_table.sub_level.kind_of(self.token)
                offset = self.symbol_table.sub_level.index_of(self.token)
                # print(f'push {segment} {offset} {self.token}')
                self.vm_writer.writePush(segment, offset)
            if self.token_type == 'keyword':
                if self.token in ['false', 'null']:
                    self.vm_writer.writePush('constant', '0')
                if self.token == 'true':
                    self.vm_writer.writePush('constant', '0')
                    self.vm_writer.writeArithmetic('~')
                if self.token == 'this':
                    self.vm_writer.writePush('pointer', '0')
            if self.token_type == 'stringConstant':
                string_length = len(self.token)
                self.vm_writer.writePush('constant', string_length)
                self.vm_writer.writeCall('String.new', 1)
                for char in self.token:
                    self.vm_writer.writePush('constant', ord(char))
                    self.vm_writer.writeCall('String.appendChar', 2)
                
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
        while (self.tokenizer.look_ahead()[0] in ['+', '=', '-', '/', '*', '>', '<', '&', '|']):
            self.compileOp()
            operation = self.token
            self.compileTerm()
            # print(f'{operation}')
            self.vm_writer.writeArithmetic(operation)

        
        self.spitNonTerminal('expression', end=True)
    
    def compileExpressionList(self):
        if self.tokenizer.look_ahead()[1] in ['intConst', 'stringConst', 'identifier'] or \
            self.tokenizer.look_ahead()[0] in ['this', 'null', 'true', 'false', '(', ')', '-', '~']:
            self.compileExpression()
            self.nArgs += 1

            while(self.tokenizer.look_ahead()[0] == ','):
                self.eat(',')
                self.compileExpression()
                self.nArgs += 1
        

    def compileSubroutineCall(self):
        self.eat('identifier')
        own_method = True
        dest, dest2 = self.token, ''
        if self.tokenizer.look_ahead()[0] == '.':
            self.eat('.')
            self.eat('identifier')
            dest2 = self.token
            own_method = False

        #handle methods
        if dest2 != 'new' and dest[0].islower():
            # push current object as first argument
            if not own_method:
                dest_kind = self.symbol_table.sub_level.kind_of(dest)
                dest_index = self.symbol_table.sub_level.index_of(dest)
            else:
                dest_kind = 'pointer'
                dest_index = '0'
            self.vm_writer.writePush(dest_kind, dest_index )
            self.nArgs += 1

        self.eat('(')
        self.spitNonTerminal('expressionList')
        try:
            if self.tokenizer.look_ahead()[0] != ')':
                self.compileExpressionList()
        except:
            a=2
        self.spitNonTerminal('expressionList', end=True)
        self.eat(')')
        
        if not own_method:
            calling_class = self.symbol_table.sub_level.type_of(dest)
            calling_class = calling_class if calling_class else dest
        else:
            calling_class = self.current_class

        dest = calling_class +'.' + (dest2 or dest)
        self.vm_writer.writeCall(dest, self.nArgs)
        if dest == 'Screen.drawRectangle':
            a=2
        if dest in void_subroutines:
            self.vm_writer.writePop('temp', '0')
        self.nArgs = 0
    
    def compileIfStatement(self):
        self.spitNonTerminal('ifStatement')

        self.eat('if')
        self.eat('(')
        self.compileExpression()
        self.eat(')')
        label_true, label_false = self.vm_writer.generateLabels('IF', self.current_subroutine)
        self.eat('{')
        self.vm_writer.writeIf(label_true)

        self.compileStatements()
        self.vm_writer.writeGoto(label_false)

        self.eat('}')
        self.vm_writer.writeLabel(label_true)

        if self.tokenizer.look_ahead()[0] == 'else':
            self.eat('else')
            self.eat('{')
           
            self.compileStatements()

            self.eat('}')
        
        self.vm_writer.writeLabel(label_false)
        
        self.spitNonTerminal('ifStatement', end=True)

    def compileWhileStatement(self):
        self.spitNonTerminal('whileStatement')

        self.eat('while')
        self.eat('(')
        label_true, label_false = self.vm_writer.generateLabels('WHILE', self.current_subroutine)
        self.vm_writer.writeLabel(label_true)
        self.compileExpression()
        self.vm_writer.writeIf(label_false)
        self.eat(')')
        self.eat('{')

        self.compileStatements()
        self.vm_writer.writeGoto(label_true)
        self.vm_writer.writeLabel(label_false)

        self.eat('}')

        self.spitNonTerminal('whileStatement', end=True)
    
    def compileLetStatement(self):
        arr_dest = False
        self.spitNonTerminal('letStatement')

        self.eat('let')
        self.eat('identifier')
        dest = self.token
        dest_kind, dest_index = self.symbol_table.sub_level.kind_of(self.token), \
                                self.symbol_table.sub_level.index_of(self.token)

        if self.tokenizer.look_ahead()[0] == '[':
            arr_dest = True
            self.eat('[')
            self.compileExpression()
            self.eat(']')
            self.vm_writer.writeArrayPush(dest_kind, dest_index)
        
        self.eat('=')
        self.compileExpression()
        # print(f'pop {self.symbol_table.sub_level.kind_of(dest)} {self.symbol_table.sub_level.index_of(dest)}')
        if not arr_dest:
            self.vm_writer.writePop(self.symbol_table.sub_level.kind_of(dest),
                                    self.symbol_table.sub_level.index_of(dest)
                                    )
        else:
            self.vm_writer.writeArrayPop()

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
            if self.tokenizer.look_ahead()[0] == 'this':
                self.vm_writer.writePush('pointer', '0')
                self.eat('this')
                self.vm_writer.writeReturn()
            else:
                self.compileExpression()
                self.vm_writer.writeReturn()
        else:
            self.vm_writer.writeReturn(is_void=True)

        self.eat(';')
        
        self.spitNonTerminal('returnStatement', end=True)
    
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
        kind = self.token
        self.compileType()
        type = self.token
        self.eat('identifier')
        name = self.token
        self.symbol_table.class_level.define(name, type, kind)

        while(self.tokenizer.look_ahead()[0] == ','):
            self.eat(',')
            self.eat('identifier')
            name = self.token
            self.symbol_table.class_level.define(name, type, kind)
        
        self.eat(';')
    
    def compileParameterList(self):
        kind = 'arg'
        self.compileType()
        type = self.token
        self.eat('identifier')
        name = self.token
        self.symbol_table.sub_level.define(name, type, kind)

        while(self.tokenizer.look_ahead()[0] == ','):
            self.eat(',')
            self.compileType()
            type = self.token
            self.eat('identifier')
            name = self.token
            self.symbol_table.sub_level.define(name, type, kind)

    def compileVarDec(self):
        self.spitNonTerminal('varDec')

        kind = 'local'
        self.eat('var')
        self.compileType()
        type = self.token

        self.eat('identifier')
        name = self.token
        self.symbol_table.sub_level.define(name, type, kind)
        
        while(self.tokenizer.look_ahead()[0] == ','):
            self.eat(',')
            self.eat('identifier')
            name = self.token
            self.symbol_table.sub_level.define(name, type, kind)
        self.eat(';')

        self.spitNonTerminal('varDec', end=True)

    def compileSubroutineBody(self, is_constructor=False, is_method=True):
        self.spitNonTerminal('subroutineBody')

        self.eat('{')
        while (self.tokenizer.look_ahead()[0] == 'var'):
            self.compileVarDec()
        no_of_locals = self.symbol_table.sub_level.variable_count('local')
        self.vm_writer.writeFunction(self.current_class, self.current_subroutine, no_of_locals)
        
        if is_constructor:
            field_space = self.symbol_table.class_level.variable_count('field')
            self.vm_writer.writePush('constant', field_space)
            self.vm_writer.writeCall('Memory.alloc', 1)
            self.vm_writer.writePop('pointer', '0')
        if is_method:
            # set this
            self.vm_writer.writePush('argument', '0')
            self.vm_writer.writePop('pointer', '0')
        self.compileStatements()

        self.eat('}')

        # self.symtab_file.writelines([ '-'*100 + '\n', self.current_class + '\n',
        #                                 self.symbol_table.class_level.__str__() + '\n',
        #                                self.current_subroutine + '\n' ,
        #                                 self.symbol_table.sub_level.__str__() + '\n',
        #                                 '-'*100 + '\n', '\n'*5]
        #                             )
        self.symbol_table.sub_level = SymbolTable.SubroutineTable('sub', self.symbol_table.class_level)

        self.spitNonTerminal('subroutineBody', end=True)

    def compileSubroutineDec(self):
        self.eat('constructor#function#method')
        is_method, is_constructor = False, False
        if self.token == 'method':
            is_method = True
        if self.token == 'constructor':
            is_constructor = True
        if self.tokenizer.look_ahead()[0] == 'void':
            self.eat('void')
        else:
            self.compileType()
        self.eat('identifier')
        self.current_subroutine = self.token
        if is_method:
            self.symbol_table.sub_level.define('this', self.current_class, 'arg')

        self.eat('(')

        self.spitNonTerminal('parameterList')
        if self.tokenizer.look_ahead()[0] != ')':
            self.compileParameterList()
        self.spitNonTerminal('parameterList', end=True)
        self.eat(')')


        self.compileSubroutineBody(is_constructor, is_method)

    def compileClass(self):
        self.spitNonTerminal('class')
    
        self.eat('class')
        self.eat('identifier')
        self.current_class = self.token
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
