from copy import deepcopy
from llp.pyroot.macros import evalFormula
import ROOT

class Branch(object):
    def __init__(
        self,
        tree,
        branch_name,
        value,
        fType = None,
        alias = None,           # Will set an alias
        f = None,
        vector = False,
        priority = 0,
        **kwargs
    ):
        self.f = f
        self.kwargs = kwargs
        self.value = value
        self.name = branch_name
        self.tree = tree
        self.alias = alias
        self.vector = vector
        self.priority = priority
        
        if fType:
            if self.vector:
                self.fType = f'[{vector}]/{fType}'
            else:
                self.fType = f'/{fType}'
        else:
            self.fType = None
        
        
        
    def set_branches(self):
        
        if self.fType:
            self.tree.Branch(self.name, self.value, self.name + self.fType)
        else:
            self.tree.Branch(self.name, self.value)
        
        self.tree.SetBranchAddress(self.name, self.value)

    
    def __call__(self):
        if self.f:
            try:
                self.value.clear()  
                if not self.vector:
                    self.value.push_back(self.f(self.tree,**self.kwargs))
                else:
                        [self.value.push_back(e) for e in self.f(self.tree,**self.kwargs)]
            except Exception as e:
                print(self.name,self.value,self.f)
                raise e
            
    def __str__(self):
        return f'{self.name}: {self.value} -> {getattr(self.tree,self.name)}'

class BranchCollection(Branch):
    def __init__(
        self,
        tree,
        branch_name,
        value,
        n,
        fType = None,
        alias = None,           # Will set an alias
        f = None,
        vector = False,
        priority = 0,
        **kwargs
    ):
        #TODO: Terminar esto para poder producir N branches a partir del nombre con *
        super().__init__(tree,branch_name,value,fType,alias,f,vector,priority,**kwargs)
        
        
        self.multiplicity = n
        self.names  = [branch_name.replace('*',str(i+1)) for i in range(n)]
        self.values = {branch_name : deepcopy(value) for branch_name in self.names}
        self.value = None
            
    @property
    def n(self):
        return self.multiplicity

    def set_branches(self):
        for name in self.names:
            if self.fType:
                self.tree.Branch(name, self.values[name], self.fType)
            else:
                self.tree.Branch(name, self.values[name])
            
            self.tree.SetBranchAddress(name, self.values[name])
            self.tree.SetBranchStatus(name, 1)

        return
    
    def __call__(self):
        if self.f:
            results = self.f(self.tree,**self.kwargs)
            # print(results)
            for branch_name,result in zip(self.names,results):
                # print(f'\nSetting {branch_name}: {result}')
                self.values[branch_name].clear()
                if not self.vector:
                    self.values[branch_name].push_back(result)
                else:
                    [self.values[branch_name].push_back(e) for e in result]
            #     print(f'Set {branch_name}: {self.values[branch_name]}')
            #     [print(name,value) for name, value in self.values.items()]
            # print('\nFinally:')
            # [print(name,value) for name, value in self.values.items()]
    def __str__(self):
        return '\n'.join([
            f'{branch_name}: {value} -> {getattr(self.tree,branch_name)}'
            for branch_name, value in self.values.items()
        ])


class Formula(Branch):
    def __init__(
        self,
        tree,
        branch_name,
        value,
        formula,
        alias = None,
        vector = False,
        priority = 0,
        **kwargs
    ):
        #TODO: Terminar esto para poder producir N branches a partir del nombre con *
        super().__init__(tree,branch_name,value,None,alias,evalFormula,vector,priority,**kwargs)
        self.formula = formula
        
                    
    def set_branches(self):
        # Función dummy, porque no se necesita para la TTreeFormula
        super().set_branches()
        self.formula = ROOT.TTreeFormula(f'{self.name}_formula',self.formula,self.tree)
        # self.formula.Compile()
        return
    
    def __call__(self):
        if self.f:
            # print(self.name, self.value)
            self.value.clear()  
            if not self.vector:
                self.value.push_back(self.f(self.formula))
            else:
                # PyROOT RVec
                try:
                    # print(self.name, self.value)
                    [self.value.push_back(e) for e in self.f(self.formula)]
                    # print(self.name, self.value)
                except Exception as e:
                    print(self.name,self.value,self.f)
                    raise e
    def __str__(self):
        return f'{self.name}: {self.value} -> {getattr(self.tree,self.name)}'
