using Vbool  = ROOT::VecOps::RVec<bool>;
using Vfloat = ROOT::VecOps::RVec<float>;
using Vint   = ROOT::VecOps::RVec<int>;

int nMuons(
    Vint muonIdx
) {
    return muonIdx.size();
}