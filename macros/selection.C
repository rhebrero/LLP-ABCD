using Vbool = ROOT::VecOps::RVec<bool>;
using Vfloat = ROOT::VecOps::RVec<float>;
using Vint = ROOT::VecOps::RVec<int>;
#include <map>
#include "TString.h"
#include "TTree.h"
#include "TTreeFormula.h"
#include <iostream>



Vint selectionMask(
    TTree       *tree,
    char        *cutString,
    int muSize
) {

    // Inicializamos las variables 
        TTreeFormula* formula = new TTreeFormula("selection",cutString,tree);
        Vint passingMu;
        
    
    // Almacenamos el valor lógico de cada uno
        for (unsigned int i=0; i < muSize; ++i) {
                passingMu.push_back(formula -> EvalInstance(i));

        }

    delete formula;

    return passingMu;
};

Vint selectionIdxFromMask(
    Vint  passingMu
) {
    int muSize = passingMu.size();
    Vint passingIdx;
    // Miramos si pasan el corte
        for (auto i=0; i < muSize; ++i) {
            if ( passingMu[i] == 0 ) {
                //No hagas nada si no pasa el corte
            }else{
                //Guardar el índice del muon
                passingIdx.push_back(i);
            }
        }
    

    return passingIdx;
};



Vint selectionIdxFromCut(
    TTree       *tree,
    char        *cutString,
    int muSize
) {

    // Inicializamos las variables 
        Vint passingMu  = selectionMask(tree,cutString,muSize);
        Vint passingIdx = selectionIdxFromMask(passingMu);
    
    return passingIdx;

};

int nPassing( 
    TTree       *tree,
    char        *cutString,
    int muSize
) {
    // Cantidad de muones que pasan el corte
        int nPrompt = selectionMask(tree, cutString, muSize).size();
    return nPrompt;
};