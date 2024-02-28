using namespace ROOT::VecOps;
using Vfloat = ROOT::VecOps::RVec<float>;


Vfloat pt(
    Vfloat px,
    Vfloat py
) {
    return sqrt(pow(px,2) + pow(py,2));
}