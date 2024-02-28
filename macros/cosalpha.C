#include "TLorentzVector.h"
#include "TMath.h"
#include <vector>

double cosalpha(double pt1, double eta1,double phi1, double pt2, double eta2, double phi2){
    float muMass = 0.105658375;

    //Calculates the dimuon mass given 4-vector components of both muons
    TLorentzVector mu1;
    TLorentzVector mu2;

    mu1.SetPtEtaPhiM(pt1,eta1,phi1,muMass);
    mu2.SetPtEtaPhiM(pt2,eta2,phi2,muMass);

    return mu1.Vect().Dot(mu2.Vect())/mu1.P()/mu2.P();
}