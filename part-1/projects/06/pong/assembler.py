class Code:
    REDUNDANT_BITS = '11'
    c_translation = {
        'dest': {
            'null': '000',
            'M': '001',
            'D': '010',
            'MD': '011',
            'A': '100',
            'AM': '101',
            'AD': '110',
            'AMD': '111',
        },
        'jmp': {
            'null': '000',
            'JGT': '001',
            'JEG': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        },
        'comp': {
            '0': '0101010',
            '1': '0111111',
            '-1': '0111010',
            'D': '0001100',
            'A': '0110000',
            'M': '1110000',
            '!D': '0001101',
            '!A': '0110001',
            '!M': '1110001',
            '-D': '0001111',
            '-A': '0110011',
            '-M': '1110011',
            'D+1': '0011111',
            'A+1': '0110111',
            'M+1': '1110111',
            'D-1': '0001110',
            'A-1': '0110010',
            'M-1': '1110010',
            'D+A': '0000010',
            'D+M': '1000010',
            'D-A': '0010011',
            'D-M': '1010011',
            'A-D': '0000111',
            'M-D': '1000111',
            'D&A': '0000000',
            'D&M': '1000000',
            'D|A': '0010101',
            'D|M': '1010101',
        }
    }

    def __init__(self, source_file):
        self.source_file = source_file

    def write_binary(self, binary):
            with open(self.source_file.split('.')[0] + '.hack', 'a+') as hack_file:
                hack_file.write(binary + '\n')

    def code_c_instruction(self, comp, jmp, dest):
        binary = '1' + Code.REDUNDANT_BITS + Code.c_translation['comp'][comp.strip()] + Code.c_translation['dest'][dest.strip()] + Code.c_translation['jmp'][jmp.strip()]
        self.write_binary(binary)
    
    def code_a_instruction(self, value):
        binary =  '0' + bin(value)[2:].zfill(15)
        self.write_binary(binary)
    
    

class Parser:

    symtab = {
        'R0': 0,
        'R1': 1,
        'R2': 2,
        'R3': 3,
        'R4': 4,
        'R5': 5,
        'R6': 6,
        'R7': 7,
        'R8': 8,
        'R9': 9,
        'R10': 10,
        'R11': 11,
        'R12': 12,
        'R13': 13,
        'R14': 14,
        'R15': 15,
        'SCREEN': 16384,
        'KBD': 24576,
        'SP': 0,
        'LLL': 1,
        'ARG': 2,
        'THIS': 3,
        'THAT': 4
    }

    def __init__(self, source_file):
        self.source_file = source_file

    def strip_comments_and_whitespaces(self, line):
        ''' removes comments, cleans whitespaces, returns only the instruction '''
        return line[:line.find('//')].strip()

    def pass1(self):
        instruction_no = 0
        with open(self.source_file, 'r') as source_code:
            for line in source_code:
                line = self.strip_comments_and_whitespaces(line)
                #continue if its a full-line comment or a whitespace
                if not line: continue

                if line.startswith('('):
                    label = line.strip('(').strip(')')
                    Parser.symtab[label] = instruction_no
                else:
                    instruction_no += 1
        print('Symtab after pass1', end='\n\n')
        print(Parser.symtab, end='\n\n')
    
    def pass2(self):
        code = Code(self.source_file)
        variable_addr = 16
        with open(self.source_file, 'r') as source_code:
            for line in source_code:
                line = self.strip_comments_and_whitespaces(line)
                #continue if its a full-line comment or a whitespace
                if not line: continue
                #A instruction
                if line.startswith('@'):
                    try:
                        symbol_value = int(line[1:])
                    except ValueError:
                        symbol = line[1:]
                        symbol_value = Parser.symtab.get(symbol)
                        if symbol_value is None:
                            Parser.symtab[symbol] = variable_addr
                            symbol_value = variable_addr
                            variable_addr += 1
                    code.code_a_instruction(symbol_value)
                #continue for labels
                elif line.startswith('('):
                    continue
                #C instruction
                else:
                    #dest
                    dest = line.split('=')[0] if '=' in line else 'null'
                    #jmp
                    jmp = line.split(';')[-1] if ';' in line else 'null'
                    #comp
                    comp = line.split(';')[0].split('=')[-1]
                    code.code_c_instruction(comp, jmp, dest)

if __name__ == '__main__':
    import sys
    try:
        source_file = sys.argv[1]
        if not source_file.endswith('.asm'):
            raise Exception('File must have .asm extension')
    except IndexError:
        raise Exception('Pass the file as an argument')

    parser = Parser(source_file)
    parser.pass1()
    parser.pass2()
    print('hack file for ' + source_file +  ' generated.')