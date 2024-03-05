using Vbool = ROOT::VecOps::RVec<bool>;
using Vfloat = ROOT::VecOps::RVec<float>;
using Vint = ROOT::VecOps::RVec<int>;
#include <map>
#include "TString.h"
#include "TTree.h"
#include "TTreeFormula.h"



Vint selectionMask(
    TTree       *tree,
    char        *cutString
) {

    // Inicializamos las variables 
        TTreeFormula* formula = new TTreeFormula("selection",cutString,tree);
        Vint passingMu;
        unsigned int muSize = formula -> GetNdata();


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

    // Miramos si pasan el corte
        for (unsigned int i=0; i < passingMu.size(); ++i) {
            if ( passingMu[i] == 0 ) {
                //No hagas nada si no pasa el corte
            }else{
                //Guardar el índice del muon
                passingMu.push_back(i);
            }
        }
    

    return passingMu;
};



Vint selectionIdxFromCut(
    TTree       *tree,
    char        *cutString
) {

    // Inicializamos las variables 
        Vint passingMu  = selectionMask(tree,cutString);
        Vint passingIdx = selectionIdxFromMask(passingMu);
    
    return passingIdx;

};

int nPassing( 
    TTree       *tree,
    char        *cutString
) {
    // Cantidad de muones que pasan el corte
        int nPrompt = selectionMask(tree, cutString).size();
    return nPrompt;
};