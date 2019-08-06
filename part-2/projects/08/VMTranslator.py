class Parser:

    command_types = {
        'C_ARITHMETIC': {'sub', 'add', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'},
        'C_PUSH': {'push'},
        'C_POP': {'pop'},
        'C_LABEL': {'label'},
        'C_IF': {'if-goto'},
        'C_GOTO': {'goto'},
        'C_RETURN': {'return'},
        'C_CALL': {'call'},
        'C_FUNCTION': {'function'},
    }


    def __init__(self, source_file):
        # self.pending_functions = {}
        self.source_files = source_files
    
    def strip_comments_and_whitespaces(self, line):
        ''' removes comments, cleans whitespaces, returns only the instruction '''
        return line[:line.find('//')].strip()
    
    def get_command(self, line):
        return line.split()[0].strip()
    
    def get_command_type(self, current_command, line):
        for command_type, command in Parser.command_types.items():
            if current_command in command: return command_type
        raise Exception(current_command + ': Invalid command')
    
    def get_arg1(self, current_command, command_type, line):
        if command_type == 'C_RETURN': return None
        if command_type == 'C_ARITHMETIC': return current_command
        return line.split()[1].strip()

    def get_arg2(self, current_command, command_type, line):
        if command_type in {'C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL'}:
            return line.split()[2].strip()
        return None
    
    def get_lexical_elements(self, line, vm_file):
        current_command = self.get_command(line)
        command_type = self.get_command_type(current_command, line)
        arg1, arg2 = self.get_arg1(current_command, command_type, line), self.get_arg2(current_command, command_type, line)
        lexical_elements = {'command': current_command, 'command_type': command_type,
                            'arg1': arg1, 'arg2': arg2, 'line': line, 'vm_filename': vm_file.name.split('/')[-1].split('.')[0]
                            }
        return lexical_elements

    def parse_line(self):
        # function_line = ''
        for source_file in self.source_files:
            with open(source_file, 'r') as vm_file:
                for line in vm_file:
                    line = self.strip_comments_and_whitespaces(line)
                    if not line: continue
                    #handle lexical_elements for function
                    # if line.startswith('function'):
                    #     self.pending_functions[line] = []
                    #     function_line = line
                    #     continue
                    # if function_line:
                    #     self.pending_functions[function_line].append(self.get_lexical_elements(line, vm_file))
                    #     if line.startswith('return'): function_line = ''
                    #     continue
                    #end
                    yield self.get_lexical_elements(line, vm_file)

class CodeWriter:
    RAM = {'stack': 'SP', 'local': 'LCL', 'this': 'THIS', 'pointer': 'POINTER',
           'that': 'THAT', 'argument': 'ARG', 'constant': 'CONSTANT'}

    label_counter = 1

    def __init__(self, output_file):
        self.asm_file = open(output_file, 'w')
    
    def inc_stack_pointer(self):
        asm_commands = [f'@{CodeWriter.RAM["stack"]}', f'M=M+1']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def dec_stack_pointer(self):
        asm_commands = [f'@{CodeWriter.RAM["stack"]}', 'M=M-1']
        self.asm_file.writelines(command+'\n' for command in asm_commands)

    def star_pointer_to_D(self, pointer='stack', offset='0'):
        ''' copies the value from the starred variable to register D '''
        if offset=='0':
            asm_commands = [f'@{CodeWriter.RAM[pointer]}', f'A=M', f'D=M']
        else:
            asm_commands = [f'@{offset}', f'D=A', f'@{CodeWriter.RAM[pointer]}', f'A=M+D', f'D=M']
        self.asm_file.writelines(command+'\n' for command in asm_commands)

    def star_pointer_to_register(self, register, pointer='stack'):
        ''' copies the value from the starred variable to register D '''
        asm_commands = [f'@{CodeWriter.RAM[pointer]}', f'A=M', f'D=M', f'@{register}', f'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def D_to_star_pointer(self, pointer='stack'):
        ''' copies the value in register D to the starred variable '''
        asm_commands = [f'@{CodeWriter.RAM[pointer]}',  f'A=M', f'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def offset_for_temp(self, offset, register='R15'):
        asm_commands = ['@5', 'D=A', f'@{offset}', 'D=D+A', f'@{register}', 'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def star_register_to_D(self, register='R15'):
        asm_commands = [f'@{register}', 'A=M', 'D=M']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def offset_to_register(self, segment_pointer, offset, register):
        asm_commands = [f'@{offset}', f'D=A', f'@{CodeWriter.RAM[segment_pointer]}', f'D=D+M', f'@{register}', f'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def D_to_star_register(self, register):
        asm_commands = [f'@{register}', f'A=M', f'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def push_const_to_stack(self, const):
        asm_commands = [f'@{const}', f'D=A', f'@{CodeWriter.RAM["stack"]}', f'A=M', f'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def push_pointer_to_stack(self, segment):
        asm_commands = [f'@{CodeWriter.RAM[segment]}', f'D=M', f'@{CodeWriter.RAM["stack"]}', f'A=M', f'M=D']
        # self.offset_to_register(segment_pointer=segment, offset=offset, register='R15')
        # self.star_pointer_to_D()
        # self.D_to_star_register(register='R15') 
        self.asm_file.writelines(command+'\n' for command in asm_commands)

    def pop_pointer_from_stack(self, segment):
        self.star_pointer_to_D()
        asm_commands = [f'@{CodeWriter.RAM[segment]}', f'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def push_static_variable_to_stack(self, offset, lexical_elements):
        asm_commands = [f'@{lexical_elements.get("vm_filename")}.{offset}', f'D=M']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
        self.D_to_star_pointer()

    def pop_static_variable_from_stack(self, offset, lexical_elements):
        self.star_pointer_to_D()
        asm_commands = [f'@{lexical_elements.get("vm_filename")}.{offset}', f'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def write_push(self, lexical_elements):
        segment = lexical_elements.get('arg1')
        offset = lexical_elements.get('arg2')
        if segment == 'pointer':
            segment = 'this' if offset == '0' else 'that'
            # push pointer 1 --->  *SP=that, SP++
            self.push_pointer_to_stack(segment)
        elif segment == 'constant':
            # push const 200 ---> *SP=const, SP++
            self.push_const_to_stack(offset)
        elif segment == 'static':
            # push static 2 --> *SP = static+2, SP++
            self.push_static_variable_to_stack(offset, lexical_elements)
        elif segment == 'temp':
            #push temp 2 --> *SP = temp[2], SP++
            self.offset_for_temp(offset)
            self.star_register_to_D()
            self.D_to_star_pointer()
        else:
            # push argument 2 ---> *SP = *(ARG + 2); SP++
            # push this 6 ---> *SP = *(THIS + 6); SP++
            self.star_pointer_to_D(pointer=segment, offset=offset)
            self.D_to_star_pointer()
        self.inc_stack_pointer()
    
    def write_pop(self, lexical_elements):
        segment = lexical_elements.get('arg1')
        offset = lexical_elements.get('arg2')
        self.dec_stack_pointer()
        if segment == 'pointer':
            #pop pointer 0 ---> SP--; this=*SP
            segment = 'this' if offset == '0' else 'that'
            self.pop_pointer_from_stack(segment)
        elif segment == 'static':
            # pop static 2 --> SP--, static+2 = *SP
            self.pop_static_variable_from_stack(offset, lexical_elements)
        elif segment == 'temp':
            # pop temp 2 --> SP--, temp[2] = *SP
            self.offset_for_temp(offset)
            self.star_pointer_to_D()
            self.D_to_star_register(register='R15') 
        else:
            #pop that 2 --->  SP--; *(that+2) = *SP
            self.offset_to_register(segment_pointer=segment, offset=offset, register='R15')
            self.star_pointer_to_D()
            self.D_to_star_register(register='R15') 

    def add_registers(self):
        asm_commands = ['@R13', 'D=M', '@R14', 'D=D+M', f'@{CodeWriter.RAM["stack"]}', 'A=M', 'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def sub_registers(self):
        # R14-R13
        asm_commands = ['@R13', 'D=M', '@R14', 'D=M-D', f'@{CodeWriter.RAM["stack"]}', 'A=M', 'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def gt_registers(self):
        #r14 > r13
        asm_commands = ['@R13', 'D=M', '@R14', 'D=M-D', f'@R14GT{CodeWriter.label_counter}',
                        'D;JGT', '@SP', 'A=M', 'M=0', f'@NEXT{CodeWriter.label_counter}', '0;JMP',
                        f'(R14GT{CodeWriter.label_counter})', '@SP', 'A=M', 'M=-1', f'(NEXT{CodeWriter.label_counter})']
        CodeWriter.label_counter += 1
        self.asm_file.writelines(command+'\n' for command in asm_commands)

    def lt_registers(self):
        #r14 < r13
        asm_commands = ['@R13', 'D=M', '@R14', 'D=M-D', f'@R14LT{CodeWriter.label_counter}',
                        'D;JLT', '@SP', 'A=M', 'M=0', f'@NEXT{CodeWriter.label_counter}', '0;JMP',
                        f'(R14LT{CodeWriter.label_counter})', '@SP', 'A=M', 'M=-1', f'(NEXT{CodeWriter.label_counter})']
        CodeWriter.label_counter += 1
        self.asm_file.writelines(command+'\n' for command in asm_commands)

    def eq_register(self):
        asm_commands = ['@R13', 'D=M','@R14', 'D=D-M',f'@EQ{CodeWriter.label_counter}', 'D;JEQ',
                        '@SP', 'A=M', 'M=0', f'@NEXT{CodeWriter.label_counter}', '0;JMP',
                        f'(EQ{CodeWriter.label_counter})', '@SP', 'A=M', 'M=-1', f'(NEXT{CodeWriter.label_counter})']
        CodeWriter.label_counter += 1
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def and_registers(self):
        asm_commands = ['@R13', 'D=M', '@R14', 'D=D&M', '@SP', 'A=M', 'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)

    def or_registers(self):
        asm_commands = ['@R13', 'D=M', '@R14', 'D=D|M', '@SP', 'A=M', 'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def not_register(self):
        asm_commands = ['@R13', 'D=!M', '@SP', 'A=M','M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)

    def neg_register(self):
        asm_commands = ['@R13', 'D=-M', '@SP', 'A=M', 'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)

    def perform_arithmetic(self, lexical_elements):
        self.dec_stack_pointer()
        self.star_pointer_to_register(register='R13')

        if lexical_elements.get('command') not in {'neg', 'not'}:
            self.dec_stack_pointer()
            self.star_pointer_to_register(register='R14')

        if lexical_elements.get('command') == 'add':
            self.add_registers()
        elif lexical_elements.get('command') == 'sub':
            self.sub_registers()
        elif lexical_elements.get('command') == 'gt':
            self.gt_registers()
        elif lexical_elements.get('command') == 'lt':
            self.lt_registers()
        elif lexical_elements.get('command') == 'or':
            self.or_registers()
        elif lexical_elements.get('command') == 'and':
            self.and_registers()
        elif lexical_elements.get('command') == 'not':
            self.not_register()
        elif lexical_elements.get('command') == 'eq':
            self.eq_register()
        elif lexical_elements.get('command') == 'neg':
            self.neg_register()
        self.inc_stack_pointer()
    
    def write_label(self, lexical_elements):
        asm_commands = [f'({lexical_elements.get("arg1")})']
        self.asm_file.writelines(command+'\n' for command in asm_commands)

    def write_goto(self, lexical_elements):
        asm_commands = [f'@{lexical_elements.get("arg1")}', '0;JMP']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def write_if_goto(self, lexical_elements):
        self.dec_stack_pointer()
        self.star_pointer_to_D()
        asm_commands = [f'@{lexical_elements.get("arg1")}', 'D;JNE']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def store_frame(self, pointer):
        self.asm_file.write(f'// saving {pointer}\n')
        if pointer not in ['LCL', 'ARG', 'THIS', 'THAT']:
            asm_commands = [f'@{pointer}', 'D=A']
        else:
            asm_commands = [f'@{pointer}', 'D=M']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
        self.D_to_star_pointer()
    
    def reinitialize_arg(self, n_args):
        self.asm_file.write(f'// reinitializing ARG\n')
        asm_commands = ['@5', 'D=A', '@R13', 'M=D', f'@{n_args}', 'D=A', '@R14', 'M=D', '@SP', 'D=M', '@R13', 'D=D-M', '@R14', 'D=D-M', '@ARG', 'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def reinitialize_lcl(self):
        self.asm_file.write(f'// reinitializing LCL\n')
        asm_commands = ['@SP', 'D=M', '@LCL', 'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)

    def save_current_stack_frame(self, lexical_elements):
        return_address = lexical_elements.get('arg1') + 'ret$' + str(CodeWriter.label_counter)
        CodeWriter.label_counter += 1
        #store return address
        self.store_frame(return_address)
        self.inc_stack_pointer()
        #store LCL
        self.store_frame('LCL')
        self.inc_stack_pointer()
        #store ARG
        self.store_frame('ARG')
        self.inc_stack_pointer()
        #store THIS
        self.store_frame('THIS')
        self.inc_stack_pointer()
        #store THAT
        self.store_frame('THAT')
        self.inc_stack_pointer()
        return return_address
    
    def jump_to_function(self, lexical_elements):
        asm_commands = [f'@{lexical_elements.get("arg1")}', '0;JMP']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def reinitialize_pointers(self, lexical_elements):
        n_args = lexical_elements.get('arg2')
        self.reinitialize_arg(n_args)
        self.reinitialize_lcl()
    
    def handle_stack_frame(self, lexical_elements):
        return_address = self.save_current_stack_frame(lexical_elements)
        self.reinitialize_pointers(lexical_elements)
        self.jump_to_function(lexical_elements)
        self.asm_file.write(f'// returning point f{lexical_elements.get("arg1")}\n')
        self.write_label({'arg1': return_address})
    
    def initialize_locals(self):
        asm_commands = ['@LCL']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def label_function_and_initialize_locals(self, lexical_elements):
        self.write_label(lexical_elements)
        n_locals = lexical_elements.get('arg2')
        for i in range(int(n_locals)):
            self.write_push({'arg1': 'constant', 'arg2': '0'})
    
    def set_endframe(self):
        #R13 has endframe
        asm_commands = ['@LCL', 'D=M', '@R13', 'M=D']
        self.asm_file.writelines(['// ' + 'set endframe' + '\n'])
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def save_return_addr_r14(self):
        asm_commands = ['@5', 'D=A', '@R13', 'D=M-D', 'A=D', 'D=M', '@R14', 'M=D']
        self.asm_file.writelines(command+'\n' for command in asm_commands)

    def return_to_caller(self):
        #R15 has return address
        self.asm_file.writelines(['// ' + 'return to caller' + '\n'])
        asm_commands = ['@R14', 'A=M', '0;JMP']
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def push_return_value(self):
        self.write_pop({'arg1': 'argument', 'arg2': '0'})
    
    def reposition_pointer(self, pointer):
        offset = {'THIS': '2', 'THAT': '1', 'ARG': '3', 'LCL': '4'}
        if pointer == 'SP':
            asm_commands = ['@ARG', 'D=M+1', '@SP', 'M=D']
        else:
            asm_commands = [f'@{offset.get(pointer)}', 'D=A', '@R13', 'D=M-D', 'A=D', 'D=M', f'@{pointer}', 'M=D']
        self.asm_file.writelines(['// ' + f'reposition {pointer}' + '\n'])
        self.asm_file.writelines(command+'\n' for command in asm_commands)
    
    def recycle_and_return(self):
        self.set_endframe()
        # self.store_ret_addr()
        self.asm_file.writelines(['// saving return addr to temp' + '\n'])
        self.save_return_addr_r14()
        self.asm_file.writelines(['// return value to arg' + '\n'])
        self.push_return_value()
        self.reposition_pointer('SP')
        self.reposition_pointer('THIS')
        self.reposition_pointer('THAT')
        self.reposition_pointer('ARG')
        self.reposition_pointer('LCL')
        self.return_to_caller()
    
    def lexical_elements_to_assembly(self, lexical_elements):
        #writing command before generating assembly
        self.asm_file.writelines(['// ' + lexical_elements.get('line') + '\n'])
        if lexical_elements.get('command_type') == 'C_ARITHMETIC':
            self.perform_arithmetic(lexical_elements)
        elif lexical_elements.get('command_type') == 'C_PUSH':
            self.write_push(lexical_elements)
        elif lexical_elements.get('command_type') == 'C_POP':
            self.write_pop(lexical_elements)
        elif lexical_elements.get('command_type') == 'C_LABEL':
            self.write_label(lexical_elements)
        elif lexical_elements.get('command_type') == 'C_GOTO':
            self.write_goto(lexical_elements)
        elif lexical_elements.get('command_type') == 'C_IF':
            self.write_if_goto(lexical_elements)
        elif lexical_elements.get('command_type') == 'C_CALL':
            self.handle_stack_frame(lexical_elements)
        elif lexical_elements.get('command_type') == 'C_FUNCTION':
            self.label_function_and_initialize_locals(lexical_elements)
        elif lexical_elements.get('command_type') == 'C_RETURN':
            self.recycle_and_return()
        self.asm_file.write('\n')
    
    def initialize_pointers(self):
        asm_commands = ['@261', 'D=A', '@SP', 'M=D',
                        # '@300', 'D=A', '@LCL', 'M=D',
                        # '@400', 'D=A', '@ARG', 'M=D',
                        # '@3000', 'D=A', '@THIS', 'M=D',
                        # '@4000', 'D=A', '@THAT', 'M=D'
                        ]
        self.asm_file.writelines(['// ' + 'Initialization' + '\n'])
        self.asm_file.writelines(command+'\n' for command in asm_commands)
        
    def write_assembly(self, parser):
        if not parser.source_files[0].lower().endswith('basicloop.vm'):
            self.initialize_pointers()
        for lexical_elements in parser.parse_line():
            self.lexical_elements_to_assembly(lexical_elements)
        self.asm_file.close()

if __name__ == '__main__':
    import sys, os, glob
    source= sys.argv[1]
    if os.path.isfile(source):
        output_file = source.split('.')[0] + '.asm'
        source_files = [source]
    else:
        os.chdir(source)
        output_file = [x for x in source.split('/') if x][-1] + '.asm'
        source_files = glob.glob('*.vm')
    #make sure Sys.vm if exists, is at the top
    if 'Sys.vm' in source_files:
        del source_files[source_files.index('Sys.vm')]
        source_files.append('Sys.vm')
        source_files.reverse()

    parser = Parser(source_files)
    codewriter = CodeWriter(output_file)
    codewriter.write_assembly(parser)
