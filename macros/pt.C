using namespace ROOT::VecOps;
using Vfloat = ROOT::VecOps::RVec<float>;
using Vdouble = ROOT::VecOps::RVec<double>;

// #include <vector>


Vfloat pt(
    Vfloat px,
    Vfloat py
) {

    Vfloat pt;

    for (unsigned int i = 0; i < px.size(); ++i) {
        
        pt.push_back(sqrt(pow(px[i],2) + pow(py[i],2)));
    }

    return pt;
}