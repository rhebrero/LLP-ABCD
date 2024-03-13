import ROOT as rt
import pathlib, inspect
from collections.abc import Iterable
from numbers import Number
from array import array
import numpy as np
import pdb
from copy import deepcopy
from llp.utils.paths import data_directory, check_root_file
from torch import Value
from .Branch import Branch, BranchCollection
import os, sys

  
        
class Tree(object):
    active_trees = 0
    known_alias = set()
    def __init__(
        self,
        tree_path,
        branches = {},
        files = [],
        alias = None,
        debug = False,
        entries = 0,
        debug_step = 10000,
        output_path = None,
        overwrite = False
    ):
        if not alias:
            self._alias = f't{self.active_trees}'
        else:
            self._alias = alias
        
        
            
        Tree.active_trees += 1
        self.is_written = False
        self.overwrite = overwrite
        self.are_branches_set = False
        
        self.src_branches = branches
        self.new_branches = {}
        self.new_collections = {}
        self._branch_priority = None
        self._min_entry = 0
        self._max_entry = None
        
        
        
        if isinstance(entries, Number):
            self._max_entry = int(entries-1)
            
        elif isinstance(entries,Iterable):
            try:
                assert len(entries) == 2
                self._min_entry, self._max_entry = [int(entry) for entry in entries]
            except AssertionError:
                raise ValueError('"entries" iterable must have only 2 values, min entry and max entry')
        else:
            raise ValueError('"entries" must be int or iterable of length 2')
        
        
        self.debug_step = debug_step
        self.debug = debug
        
        
        # Inicializamos datos sobre el tree
        if isinstance(files, str):
            self._files = [files]
        elif isinstance(files,Iterable):
            self._files = files
        
        if not output_path:
            self.output_path = str(data_directory / pathlib.Path(f'{self.alias}.root'))
        else:
            self.output_path = output_path
        
        
        
        self._tree_path = tree_path
        self._src_tree = None
        self._new_file = None
        self._new_tree = None
        
                
        self.load_files()
        
                        
    
    def load_files(self):
        
        self._src_tree = src_tree = rt.TChain(self.tree_path)
        for i, file_path in enumerate(self.files):
            if self.debug: print(f'Adding file {file_path}...')
            src_tree.Add(file_path)
        
        
        output_path = check_root_file(self.output_path)
        if output_path.exists() & (not self.overwrite):
            raise RuntimeError("File already exists! To overwrite the file"
                          "please set 'self.overwrite' to True, i.e. Tree(...,overwrite=True).")
        # else:
        #     output_path.unlink()
        if self.debug: print(f'Cloning file to {output_path}...')
        
        
        # Antes de clonar, tenemos que crear el archivo root al que va a estar ligado el TTree.
        self._new_file = new_file = rt.TFile(str(output_path),"RECREATE")
        
        # Hay que recrear la estructura del archivo original
        for folder in self.tree_path.split('/')[:-1]:
            new_file.mkdir(folder)
            new_file.cd(folder)
        
        
        if self.nentries == 0: self.max_entry = src_tree.GetEntries()-1
        
        self.activate_branches(src_tree, self.src_branches, verbose = False)
        self._new_tree = new_tree = src_tree.CloneTree(0)
        
        self.new_tree.AddFriend(self.src_tree)
        
        self.activate_branches(new_tree, self.total_branches)
        
            
    def activate_branches(self, tree, branches, verbose = True):
        tree.SetBranchStatus('*',0)
        
        if self.debug & verbose:
            print("Activating branches:")
            [print(f" - {branch}") for branch in branches.keys()]
            
        [tree.SetBranchStatus(branch,1) for branch in branches.keys()]
        
        return       
    
    
    @property
    def nentries(self):
        return self.max_entry - self.min_entry + 1 # +1 porque el 0 cuenta también
    
    @property
    def max_entry(self):
        return self._max_entry
    
    @property
    def min_entry(self):
        return self._min_entry
    
    @property
    def src_tree(self):
        return self._src_tree  
    
    @property
    def total_new_branches(self):
        return self.new_branches | self.new_collections
    
    @property
    def total_branches(self):
        return self.total_new_branches | self.src_branches
    
    @property
    def branches(self):
        return self._src_branches
    
    @property
    def tree_path(self) -> str:
        return self._tree_path
    @property
    def alias(self):
        return self._alias
    @alias.setter
    def alias(self,new_alias):
        try:
            assert new_alias not in Tree.known_alias
        except AssertionError:
            raise ValueError(f'"{new_alias}" already exists as a Tree alias, please, choose one that is not in {Tree.known_alias}.')
        
        if self.alias in Tree.known_alias:
            Tree.known_alias.remove(self.alias)
        
        
        self._alias = new_alias
        Tree.known_alias.add(new_alias)
    
    @property
    def new_tree(self):
        return self._new_tree

    
    @property
    def files(self):
        return self._files
    
    @property
    def file(self):
        return self._new_file
    
    @property
    def branch_names(self):
        if isinstance(self.branches,(tuple, list)):
            return list(self.branches)
        elif isinstance(self.branches, dict):
            return list(self.branches.keys())
        else:
            raise ValueError("Invalid type of self.branches.")
    
    @property
    def new_branch_names(self):
        return [branch.name for branch in self.new_branches.values()] + [collection.names for collection in self.new_collections.values()]
    
    def add_branch(
        self,
        branch_name,
        f,
        default_value,
        fType = None,
        vector = None,
        n = None,
        **kwargs
    ):
        if "*" not in branch_name:
            self.new_branches[branch_name] = Branch(
                                                self.new_tree                   ,
                                                branch_name                 ,
                                                value       = default_value ,
                                                fType       = fType         ,
                                                f           = f             ,
                                                vector      = vector        ,
                                                **kwargs
                                            )
        else:
            self.new_collections[branch_name] = BranchCollection(
                                                self.new_tree                   ,
                                                branch_name                 ,
                                                n           = n             ,
                                                value       = default_value ,
                                                fType       = fType         ,
                                                f           = f             ,
                                                vector      = vector        ,
                                                **kwargs
                                            )
    
    @property
    def branch_priority(self):
        return self._branch_priority
    
    def set_branch_priority(self):
        
        p_set = sorted(set([branch.priority for branch in self.total_new_branches.values()]),reverse=True)
        self._branch_priority = {p : {name : branch for name, branch in self.total_new_branches.items() if branch.priority == p} for p in p_set}
    
    def get_entry(self,n_entry):
        self.src_tree.GetEntry(n_entry)
        if self.new_tree: self.new_tree.GetEntry(n_entry)
    
    def print_entry(self,n_entry):
        self.get_entry(n_entry)
        
        for branch_name, branch in self.total_branches:
            if isinstance(branch,BranchCollection):
                for branch_name_i, branch_i in branch.values:
                    print(f' - {branch_name_i}: {branch_i.value}')
            else:
                print(f' - {branch_name}: {branch.value}')
    
    
    
    
    
    
    def process_branches(self,verbose = False):
        self.set_branches()
        
        for i, n_entry in enumerate(range(self.min_entry,self.max_entry+1)):
            
            if (not (i+1) % self.debug_step) & (self.debug): print(f'Filling entry #{i+1}...')
            self.new_tree.GetEntry(n_entry)
            self.src_tree.GetEntry(n_entry)
            
            # for branch_name in self.
            
            if verbose:
                
                print(
                    '\n'
                    '======================================\n'
                    f'        EVENT {n_entry}\n'
                    '======================================'
                )
            
                print('\n Before Branch update')
            # Actualizamos los valores de cada branch según su prioridad
            for p, branch_dict in self.branch_priority.items():
                for branch_name, branch in branch_dict.items():
                    if verbose: print(branch)
                    branch()
            
            
            if verbose:
                print('\n After Branch update')
                for branch_name, branch in self.total_new_branches.items():
                    print(branch)
                print(f'patmu_d0_pv: {self.new_tree.patmu_d0_pv}')

            self.new_tree.Fill()

        self.write()
        return
        
    
    def write(self):
        print(f'Guardando cambios...')
        self.is_written = True
        self.new_tree.Write()
        return
    
    def close(self):
        print(f'Cerrando archivo: {self.output_path}')
        # if not self.is_written: self.write()
        # self.new_tree.Close()
        self.file.Close()
    
    def set_branches(self):
        
        if not self.are_branches_set:
            for branch in self.total_new_branches.values():
                branch.set_branches()
        self.are_branches_set = True

        self.set_branch_priority()
        # self.activate_branches(self.new_tree)
        
        # for branch_name, branch_value in self.branches.items():
        #     self.src_tree.SetBranchStatus(branch_name, 1)
        
        # for branch_name, branch_value in self.new.items():            
        #     self.new_tree.SetBranchStatus(branch_name, 1)
        return
            


    
if __name__ == '__main__':
    from llp.pyroot.macros import mu_nPrompt
    from llp.utils.macros import load_macro
    
    
    
    files = [
        '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022B-ReReco-v2.root',
        '/pnfs/ciemat.es/data/cms/store/user/escalant/displacedMuons/NTuples/May2023-v1/ntuple_2022_DoubleMuonRun2022C-ReReco-v2.root'
    ]
    
    t1 = Tree(
        'SimpleNTupler/DDTree',
        files = files,
        branches = {
                'patmu_d0_pv' : rt.VecOps.RVec('float')((0)),
                'dsamu_d0_pv' : rt.VecOps.RVec('float')((0)),
                'dsamu_px'    : rt.VecOps.RVec('float')((0)),
                'dsamu_py'    : rt.VecOps.RVec('float')((0)),
            },
        debug = True,
        nentries = int(1e3),
        debug_step = int(1e2),
        output_path='test_nPrompt_1e3'
    )
    
    t1.add_branch(
        'patmu_nPrompt',
        mu_nPrompt,
        fType='I',
        d0_cut = 0.1,
        mu_type = 'pat'
    )
    
    t1.add_branch(
        'dsamu_nPrompt',
        mu_nPrompt,
        fType='I',
        d0_cut = 1,
        mu_type = 'dsa'
    )
    t1.process_branches()


# trigger_list = ['a','b','c']

# trig = ' || '.join([f'trig_hlt_path == {trigger_path}' for trigger_path in trigger_list])

# selection = []
# selection.append('1')
# selection.append('2')

# selection = [' && '.join([selection_i,trigger]) for selection_i in selection]

