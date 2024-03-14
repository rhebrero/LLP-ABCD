using Vfloat    = ROOT::VecOps::RVec<float>;
using Vdouble   = ROOT::VecOps::RVec<double>;

#include "TLorentzVector.h"
#include "TMath.h"
#include <vector>

double invMass(float pt1, float eta1,float phi1, float pt2, float eta2, float phi2){
    float muMass = 0.105658375;

    //Calculates the dimuon mass given 4-vector components of both muons
    TLorentzVector mu1;
    TLorentzVector mu2;

    mu1.SetPtEtaPhiM(pt1,eta1,phi1,muMass);
    mu2.SetPtEtaPhiM(pt2,eta2,phi2,muMass);
    TLorentzVector dim = mu1+mu2;
    return dim.M();
}

double invMass_fromIdx(int idx1, int idx2,Vfloat pt, Vfloat eta,Vfloat phi){
    
    double mass;

    if ((idx1 < 0) || (idx2 < 0) || (idx1 ==idx2)) {
        mass = 0; // defaults
    } else{
        //Calculates the dimuon mass given 4-vector components of both muons
            mass = invMass(pt[idx1],eta[idx1],phi[idx1],pt[idx2],eta[idx2],phi[idx2]);
    }

    return mass;
}