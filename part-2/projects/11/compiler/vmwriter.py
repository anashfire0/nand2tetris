class VMWriter:
    def __init__(self, vm_file):
        self.vm_file = open(vm_file, 'w')
        self.running_label = 0
        self.labels = []

    def writePush(self, segment, offset):
        if segment == 'arg':
            segment = 'argument'
        if segment == 'field':
            segment = 'this'
        self.vm_file.writelines([f'push {segment} {offset}\n'])

    def writePop(self, segment, offset):
        if segment == 'arg':
            segment = 'argument'
        if segment == 'field':
            segment = 'this'
        self.vm_file.writelines([f'pop {segment} {offset}\n'])

    def writeArithmetic(self, operation):
        operations = { '+': 'add',
                       '-': 'sub',
                       '~': 'not',
                       '--': 'neg',
                       '=': 'eq',
                       '>': 'gt',
                       '<': 'lt',
                       '&': 'and',
                       '|': 'or',
                       '*': 'call Math.multiply 2',
                       '/': 'call Math.divide 2',
        }
        operation = operations[operation]
        self.vm_file.writelines([operation + '\n'])
    
    def writeArrayPush(self, segment, offset):
        # self.vm_file.writelines(['push constant dest\n',
        #                           'add\n', 
        #                           'pop temp 3\n'
        #                         ])
        if segment == 'arg':
            segment = 'argument'
        if segment == 'field':
            segment = 'this'
        self.vm_file.writelines([f'push {segment} {offset}\n',
                                  'add\n', 
                                  'pop temp 1\n'
                                ])
    
    def writeArrayPop(self):
        self.vm_file.writelines(['push temp 1\n', 'pop pointer 1\n',
                                'pop that 0\n'])
    
    def writeArrayPushForSource(self, segment, offset):
        if segment == 'arg':
            segment = 'argument'
        if segment == 'field':
            segment = 'this'
        # self.vm_file.writelines(['push constant dest\n',
        #                           'add\n', 
        #                           'pop pointer 1\n',
        #                           'push that 0\n'
        #                         ])
        self.vm_file.writelines([f'push {segment} {offset}\n',
                                  'add\n', 
                                  'pop pointer 1\n',
                                  'push that 0\n'
                                ])

    
    def clearLabels(self):
        self.labels.clear()
    
    def generateLabels(self, label_name, subroutine=''):
        self.running_label += 1
        label_true = f'{label_name}_{subroutine}_TRUE_{self.running_label}'
        label_false = f'{label_name}_{subroutine}_FALSE_{self.running_label}'
        return label_true, label_false

        # self.labels.append('L'+ str(self.running_label))
    
    def writeLabel(self, label):
        self.vm_file.writelines([f'label {label}\n'])

    def writeGoto(self, label):
        self.vm_file.writelines([f'goto {label}\n'])

    def writeIf(self, label, negate=True):
        if negate:
            self.vm_file.writelines(['not\n', f'if-goto {label}\n'])
        else:
            self.vm_file.writelines([f'if-goto {label}\n'])

    def writeCall(self, call, nArgs):
        calls = {
                    '*': 'call Math.multiply 2',
                    '/': 'call Math.divide 2',
                  }
        self.vm_file.writelines([calls.get(call, 'call ' + call + f' {nArgs}') + '\n'])

    def writeFunction(self, class_name, function_name, nLocals):
        self.vm_file.writelines(['function ' + class_name + '.' + function_name + f' {nLocals}\n'])
        pass

    def writeReturn(self, is_void=False):
        if is_void:
            self.vm_file.writelines(['push constant 0\n'])
        self.vm_file.writelines(['return\n'])
        
        
