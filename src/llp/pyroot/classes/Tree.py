from genericpath import isfile
import ROOT as rt
import pathlib, inspect
from collections.abc import Iterable
from array import array
import numpy as np
import pdb

from llp.utils.paths import data_directory, check_root_file

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
        nentries = -1,
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
        
        self.new_branches = {}
        self.entry = {}
        
        self.nentries = nentries
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
        
        self._branches  = branches
        self._tree_path = tree_path
        self._tree = None
        
        
        # TFile y TTree temporales para poder crear nuevas ramas
        self._file = None
        self._tree = None
        
        self.load_files()
        
        
        # branch_name : branch_def for branch_name, branch_def in branches.items()
                        
    
    def load_files(self):
        
        src_tree = rt.TChain(self.tree_path)
        for i, file_path in enumerate(self.files):
            if self.debug: print(f'Adding file {file_path}...')
            src_tree.Add(file_path, self.nentries)
        
        
        output_path = check_root_file(self.output_path)
        if output_path.exists() & (not self.overwrite):
            raise RuntimeError("File already exists! To overwrite the file"
                          "please set 'self.overwrite' to True, i.e. Tree(...,overwrite=True).")
        # else:
        #     output_path.unlink()
        if self.debug: print(f'Cloning file to {output_path}...')
        
        
        # Antes de clonar, tenemos que crear el archivo root al que va a estar ligado el TTree.
        self._file = file = rt.TFile(str(output_path),"RECREATE")
        
        # Hay que recrear la estructura del archivo original
        for folder in self.tree_path.split('/')[:-1]:
            file.mkdir(folder)
            file.cd(folder)
            
        self.activate_branches(src_tree, verbose = False)
        self._tree = tree = src_tree.CloneTree(self.nentries,'fast')
        
        self.activate_branches(tree)
        del src_tree
    
        
        
    def activate_branches(self, tree, verbose = True):
        tree.SetBranchStatus('*',0)
        if self.debug & verbose:
            print("Activating branches:")
            [print(f" - {branch}") for branch in self.branch_names]
        if isinstance(self.branches,dict):
            [tree.SetBranchStatus(branch,1) for branch in self.branch_names]
        else:
            raise TypeError(f'Type of "branches" is not valid: type is {type(self.branches)} and dict(str : Rtype) was expected.')
        return       
        
        
    
    @property
    def branches(self):
        return self._branches
    
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
    def tree(self):
        return self._tree
    
    @property
    def files(self):
        return self._files
    
    @property
    def file(self):
        return self._file
    
    @property
    def branch_names(self):
        if isinstance(self.branches,(tuple, list)):
            return list(self.branches)
        elif isinstance(self.branches, dict):
            return list(self.branches.keys())
        else:
            raise ValueError("Invalid type of self.branches.")
    
    def add_branch(
        self,
        branch_name,
        f,
        fType,
        default_value,
        vectorial,
        **kwargs
    ):
        self.entry[branch_name] = default_value
        
        # pdb.set_trace()
        self.tree.Branch(branch_name, self.entry[branch_name], f'{branch_name}/{fType}')

        self.new_branches[branch_name] = self.branch_updater(branch_name,f,vectorial,**kwargs)
    
    def branch_updater(self,branch_name,f,vectorial,**kwargs):
        if vectorial:
            def update_vectorial_branch(entry):
                result = f(entry,**kwargs)
                self.entry[branch_name].clear()
                
                for i in range(len(result)):
                    self.entry[branch_name][i] = result[i] 
                 
            return update_vectorial_branch
        else:
            def update_vectorial_branch(entry):
                result = f(entry,**kwargs)
                self.entry[branch_name].clear()
                
                self.entry[branch_name][0] = result
                 
            return update_vectorial_branch
            
    
    
    
        
    def process_branches(self):
        self.set_branches()
                
        for i, n_entry in enumerate(range(self.tree.GetEntries())):
            
            if (not (i+1) % self.debug_step) & (self.debug): print(f'Filling entry #{i+1}...')
            self.tree.GetEntry(n_entry)
            
            print('\n Before update Entry fill')
            for branch_name in self.new_branches.keys():
                print(f'{branch_name}: {self.entry[branch_name]} -> {getattr(self.tree,branch_name)}',)

            
            for branch_name, f in self.new_branches.items(): # Update each branch using the updater.
                f(self.tree)
            
            print('\n Before TTree fill')
            for branch_name in self.new_branches.keys():
                print(f'{branch_name}: {self.entry[branch_name]} -> {getattr(self.tree,branch_name)}',)

            
            
            self.tree.Fill()
            print('\n After TTree fill')
            for branch_name in self.new_branches.keys():
                print(f'{branch_name}: {self.entry[branch_name]} -> {getattr(self.tree,branch_name)}',)
            exit()
        
        self.write()
        return
        
    
    def write(self):
        print(f'Guardando cambios...')
        self.tree.Write()
        self.is_written = True
        return
    
    def close(self):
        print(f'Cerrando archivo: {self.output_path}')
        # if not self.is_written: self.write()
        
        self.file.Close('R')
    
    def set_branches(self):
        self.tree.SetBranchStatus('*',1)    
        for branch_name, branch_value in self.entry.items():            
            if branch_name in self.new_branches.keys():
                continue
            else:
                self.tree.SetBranchAddress(branch_name, rt.AddressOf(branch_value))
    
    def get_tree(self):
        print(f'Abriendo archivo: {self.output_path}')
        self._file = file = rt.TFile.Open(self.output_path)
        self._tree = tree =  file.Get(self.tree_path)
        
        self.set_branches()
        
        if self.debug:
            print(type(file), file)
            print(type(tree), tree)
        
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
    t1.close()


# trigger_list = ['a','b','c']

# trig = ' || '.join([f'trig_hlt_path == {trigger_path}' for trigger_path in trigger_list])

# selection = []
# selection.append('1')
# selection.append('2')

# selection = [' && '.join([selection_i,trigger]) for selection_i in selection]


