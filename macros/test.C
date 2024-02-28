using Vbool = ROOT::VecOps::RVec<bool>;
using Vfloat = ROOT::VecOps::RVec<float>;
using Vint = ROOT::VecOps::RVec<int>;

bool test(
    float test
) {
    return true;
}

bool Vtest(
    Vfloat vector_var
) {
    // Longitud del vector
    return vector_var[0] > 0;
}