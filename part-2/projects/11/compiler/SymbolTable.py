class Table(list):
    name, type, kind, number = 0, 1, 2, 3

    def __init__(self, name):
        self._running_numbers = {}
        self.name = name
    
    def _get_running_number(self, kind):
        return self._running_numbers[(kind)]

    def _inc_running_number(self, kind):
        self._running_numbers[(kind)] = self._running_numbers.get((kind), -1) + 1
        return self._running_numbers[kind]
    
    def define(self, name, type, kind):
        if kind not in ['arg', 'field', 'static', 'local']:
            raise Exception('Invalid keyword')
        number = self._inc_running_number(kind)
        self.append((name, type, kind, number))
    
    def variable_count(self, kind):
        count = 0
        for variable in self:
            if variable[Table.kind] == kind:
                count += 1
        return count

    def kind_of(self, name):
        for variable in self:
            if variable[Table.name] == name: return variable[Table.kind]
    
    def type_of(self, name):
        for variable in self:
            if variable[Table.name] == name: return variable[Table.type]

    def index_of(self, name):
        for variable in self:
            if variable[Table.name] == name: return variable[Table.number]
    
    def __str__(self):
        if not self:
            return "<EMPTY TABLE>"
        return '\n'.join(str(coll) for coll in self)


class SubroutineTable(Table):

    def __init__(self, name, class_table):
        self.class_table = class_table
        super().__init__(name)

    def kind_of(self, name):
        found = super().kind_of(name) 
        if found is None:
            for variable in self.class_table:
                if variable[Table.name] == name: return variable[Table.kind]
        else:
            return found

    def type_of(self, name):
        found = super().type_of(name) 
        if found is None:
            for variable in self.class_table:
                if variable[Table.name] == name: return variable[Table.type]
        else:
            return found

    def index_of(self, name):
        found = super().index_of(name) 
        if found is None:
            for variable in self.class_table:
                if variable[Table.name] == name: return variable[Table.number]
        else:
            return found

    # def start_subroutine(self):
    #     breakpoint()
    #     new = SubroutineTable(self.name, self.class_table)
    #     del self
    #     self = new


class SymbolTable:

    def __init__(self):
        self.class_level = Table('class')
        self.sub_level = SubroutineTable('sub', self.class_level)
        