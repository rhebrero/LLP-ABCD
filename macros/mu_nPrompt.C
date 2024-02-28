using Vbool = ROOT::VecOps::RVec<bool>;
using Vfloat = ROOT::VecOps::RVec<float>;
using Vint = ROOT::VecOps::RVec<int>;

int mu_nPrompt( 
    Vfloat  mu_d0_pv,
    float   d0_cut
) {
    
    // Cantidad de muones
        unsigned int n = mu_d0_pv.size();

    // Número de 
        int nPrompt;

    // Miramos si pasan el corte
        for (unsigned int i=0; i<n; ++i) {
            if (mu_d0_pv[i] <= d0_cut) {
                ++nPrompt;
            }
        }

    return nPrompt;
};