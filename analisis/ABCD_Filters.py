import ROOT as rt
import pdb


class ABCD_Filters:
        
    def __init__(self):
            
        self.all_triggers = [
            'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v2',
            'HLT_DoubleL2Mu23NoVtx_2Cha_v2',
            'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v3',
            'HLT_DoubleL2Mu23NoVtx_2Cha_v3',
            'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v1',
            'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v1'
        ]

        self.triggers = self._join_triggers()

        self.sel_All =   self._sel_All()  + [self.triggers]        
        self.sel_D6D6 =   self._sel_D6D6() + [self.triggers]
        self.sel_D2D2 =   self._sel_D2D2() + [self.triggers]
        self.sel_D2D6 =   self._sel_D2D6() + [self.triggers]
        self.sel_PD2 =    self._sel_PD2()  + [self.triggers]
        self.sel_PP =     self._sel_PP()   + [self.triggers]
        self.sel_PD6 =    self._sel_PD6()  + [self.triggers]

        self.sels = [self.sel_PP, self.sel_D2D2, self.sel_D6D6, self.sel_PD2, self.sel_PD6, self.sel_D2D6]

        self.dim_params = [
                {'dim': 'PP',   'dim1': 'PP',   'dim2': 'PP',   'num1': '1', 'num2': '2'},
                {'dim': 'D2D2', 'dim1': 'D2D2', 'dim2': 'D2D2', 'num1': '1', 'num2': '2'},
                {'dim': 'D6D6', 'dim1': 'D6D6', 'dim2': 'D6D6', 'num1': '1', 'num2': '2'},
                {'dim': 'PD2',  'dim1': 'PP',   'dim2': 'D2D2', 'num1': '1', 'num2': '1'},
                {'dim': 'PD6',  'dim1': 'PP',   'dim2': 'D6D6', 'num1': '1', 'num2': '1'},
                {'dim': 'D2D6', 'dim1': 'D2D2', 'dim2': 'D6D6', 'num1': '1', 'num2': '1'},
                ]


    def _join_triggers(self):
            return '(trig_hlt_idx>=0) && ('+'||'.join([f'trig_hlt_path == \"{trigger}\"' for trigger in self.all_triggers])+')'
            
            
    def _sel_All(self):
         return [
              'patmu_nGood>1'
         ]

    def _sel_D6D6(self):
        return [
    #     Region basics
            'patmu_nPrompt==0',
            'patmu_nDisplaced6>1',
            
            # 'dimD6D6_isOS==1',
    
        ]

    def _sel_D2D2(self):
        return [
    #     Region basics
            'patmu_nPrompt==0',
            'patmu_nDisplaced2>1',

            # 'dimD2D2_isOS==1',

        ]

    def _sel_D2D6(self):
        return [
    #     Region basics
            'patmu_nDisplaced2>0',
            'patmu_nDisplaced6>0', 

            # 'dimPD_isOS==1',

        ]

    def _sel_PD2(self):
        return [
    #     Region basics
            'patmu_nDisplaced2>0',
            'patmu_nPrompt>0', 

        ]

    def _sel_PP(self):
        return [
    #     Region basics
            'patmu_nPrompt>1',
            'patmu_nDisplaced2==0',
            'patmu_nDisplaced6==0',

            # 'dimPP_isOS==1',

        ]

    def _sel_PD6(self):
        return [
    #     Region basics
            'patmu_nPrompt>0',
            'patmu_nDisplaced6>0', 
            # 'dimPD_isOS==1',

    ]

    def search_cuts(self): 
        return [
                'patmu_pt[dim{dim1}_mu{num1}_idx]>10',
                'patmu_pt[dim{dim2}_mu{num2}_idx]>10',
                'dim{dim}_mass>15',
                'dim{dim}_mass>110 || dim{dim}_mass<70',
                'dim{dim}_isOS==1',
                ]
    
    def more_cuts(self):
         return [
                # 'dim{dim}_hasVtx==0',
                'max(patmu_trackIso[dim{dim1}_mu{num1}_idx]/patmu_pt[dim{dim1}_mu{num1}_idx], patmu_trackIso[dim{dim2}_mu{num2}_idx]/patmu_pt[dim{dim2}_mu{num2}_idx])<0.1',
                # 'dim{dim}_mass>70',
                # 'patmu_pt[dim{dim1}_mu{num1}_idx]>40',
                # 'patmu_pt[dim{dim2}_mu{num2}_idx]>40',
         ]
    
    def Smuon100_cuts(self, ptCut100='37.5', massCut100='15'):
            return [
                    'dim{dim}_mass>' + massCut100,
                    'patmu_pt[dim{dim1}_mu{num1}_idx]>' + ptCut100,
                    'patmu_pt[dim{dim2}_mu{num2}_idx]>' + ptCut100,
            ]

    def Smuon500_cuts(self, ptCut500='55', massCut500='70'):
            return [
                    'dim{dim}_mass>' + massCut500,
                    'patmu_pt[dim{dim1}_mu{num1}_idx]>' + ptCut500, 
                    'patmu_pt[dim{dim2}_mu{num2}_idx]>' + ptCut500,
            ]

    def Zmass_validation_cuts(self):
        return  [
                'patmu_pt[dim{dim1}_mu{num1}_idx]>10',
                'patmu_pt[dim{dim2}_mu{num2}_idx]>10',
                # 'dim{dim}_mass>15',
                'dim{dim}_mass<110 && dim{dim}_mass>70',
                'dim{dim}_isOS==1',
                ]

    def SS_validation_cuts(self):
         return [
                'patmu_pt[dim{dim1}_mu{num1}_idx]>10',
                'patmu_pt[dim{dim2}_mu{num2}_idx]>10',
                'dim{dim}_mass>15',
                'dim{dim}_mass>110 || dim{dim}_mass<70',
                'dim{dim}_isOS==0',
                ]
    
    def d0sig_for_cuts(self):
         return [
                'patmu_pt[dim{dim1}_mu{num1}_idx]>10',
                'patmu_pt[dim{dim2}_mu{num2}_idx]>10',
                'dim{dim}_mass>15',
                'dim{dim}_mass<110 && dim{dim}_mass>70',
                'min(patmu_trackIso[dim{dim1}_mu{num1}_idx]/patmu_pt[dim{dim1}_mu{num1}_idx], patmu_trackIso[dim{dim2}_mu{num2}_idx]/patmu_pt[dim{dim2}_mu{num2}_idx])<0.5'
                ]


    # def dim_params(self):
    #     return [
    #             {'dim': 'PP',   'dim1': 'PP',   'dim2': 'PP',   'num1': '1', 'num2': '2'},
    #             {'dim': 'D2D2', 'dim1': 'D2D2', 'dim2': 'D2D2', 'num1': '1', 'num2': '2'},
    #             {'dim': 'D6D6', 'dim1': 'D6D6', 'dim2': 'D6D6', 'num1': '1', 'num2': '2'},
    #             {'dim': 'PD2',  'dim1': 'PP',   'dim2': 'D2D2', 'num1': '1', 'num2': '1'},
    #             {'dim': 'PD6',  'dim1': 'PP',   'dim2': 'D6D6', 'num1': '1', 'num2': '1'},
    #             {'dim': 'D2D6', 'dim1': 'D2D2', 'dim2': 'D6D6', 'num1': '1', 'num2': '1'},
    #             ]

    def add_cuts(self, additional_cuts):
                
        for sel, param in zip(self.sels, self.dim_params):
                
                sel.extend([branch_cut.format(**param) for branch_cut in additional_cuts])

# add_cuts(Zmass_validation_branches_cuts)

    def make_SS_filters(self):

        # Filters for D6D6 dimuons, which has A, B, C and D components

        self.filters_D6D6 = '(' + ') && ('.join (self.sel_D6D6) + ')'

        self.filters_D6D6_over_limit =  self.filters_D6D6 + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimD6D6_mu2_idx]>{signal_limit})'
        self.filters_D6D6_over_limit_posmu1 = self.filters_D6D6_over_limit + ' && (int(patmu_pt[dimD6D6_mu1_idx])%2==0)'
        self.filters_D6D6_over_limit_negmu1 = self.filters_D6D6_over_limit + ' && (int(patmu_pt[dimD6D6_mu1_idx])%2==1)'

        self.filters_D6D6_under_limit_C = self.filters_D6D6 + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]<= {signal_limit}) && (patmu_d0sig_pv[dimD6D6_mu2_idx]<= {signal_limit})'
        self.filters_D6D6_under_limit_C_posmu1 = self.filters_D6D6_under_limit_C + ' && (int(patmu_pt[dimD6D6_mu1_idx])%2==0)'
        self.filters_D6D6_under_limit_C_negmu1 = self.filters_D6D6_under_limit_C + ' && (int(patmu_pt[dimD6D6_mu1_idx])%2==1)'

        self.filters_D6D6_under_limit_B = self.filters_D6D6 + ' && (int(patmu_pt[dimD6D6_mu1_idx])%2==0)  && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimD6D6_mu2_idx]<={signal_limit})'
        self.filters_D6D6_under_limit_D = self.filters_D6D6 + ' && (int(patmu_pt[dimD6D6_mu1_idx])%2==1)  && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimD6D6_mu2_idx]<={signal_limit})'


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Filters for D2D2 dimuons, which has just C component 

        self.filters_D2D2 = '(' + ') && ('.join (self.sel_D2D2) + ')'
        self.filters_D2D2_C = self.filters_D2D2 + ' && (patmu_d0sig_pv[dimD2D2_mu1_idx]>{signal_inf}) && (patmu_d0sig_pv[dimD2D2_mu2_idx]>{signal_inf}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]<{signal_limit}) && (patmu_d0sig_pv[dimD2D2_mu2_idx]<{signal_limit})'
        self.filters_D2D2_C_posmu1 = self.filters_D2D2_C + ' && (int(patmu_pt[dimD2D2_mu1_idx])%2==0)'
        self.filters_D2D2_C_negmu1 = self.filters_D2D2_C + ' && (int(patmu_pt[dimD2D2_mu1_idx])%2==1)'


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Filters for D2D6 dimuons, which has B, C and D components

        self.filters_D2D6_B = '(' + ') && ('.join (self.sel_D2D6) + ')' + ' && (int(patmu_pt[dimD6D6_mu1_idx])%2==0)' #&& (int(patmu_pt[dimD2D2_mu1_idx])%2==1)' 
        self.filters_D2D6_D = '(' + ') && ('.join (self.sel_D2D6) + ')' + ' && (int(patmu_pt[dimD6D6_mu1_idx])%2==1)' #&& (int(patmu_pt[dimD2D2_mu1_idx])%2==0)'

        self.filters_D2D6_over_limit_B = self.filters_D2D6_B + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]>{signal_inf})'
        self.filters_D2D6_over_limit_D = self.filters_D2D6_D + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]>{signal_inf})'

        self.filters_D2D6_under_limit_B_C = self.filters_D2D6_B + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]<{signal_limit}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]>{signal_inf})'
        self.filters_D2D6_under_limit_D_C = self.filters_D2D6_D + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]<{signal_limit}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]>{signal_inf})'


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Filters for PD2 dimuons, which, whith used defs of displaced, actually don't contribute

        self.filters_PD2_B = '(' + ') && ('.join (self.sel_PD2) + ')' + ' && (int(patmu_pt[dimD2D2_mu1_idx])%2==0)'# && (int(patmu_pt[dimPP_mu1_idx])%2==1)'
        self.filters_PD2_D = '(' + ') && ('.join (self.sel_PD2) + ')' + ' && (int(patmu_pt[dimD2D2_mu1_idx])%2==1)'# && (int(patmu_pt[dimPP_mu1_idx])%2==0)'

        self.filters_PD2_B_C = self.filters_PD2_B + ' && (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]<{signal_limit})'
        self.filters_PD2_D_C = self.filters_PD2_D + ' && (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]<{signal_limit})'


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Filters for PP dimuons, which, whith used defs of displaced, actually don't contribute

        self.filters_PP = '(' + ') && ('.join (self.sel_PP) + ')' + '&&  (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf}) && (patmu_d0sig_pv[dimPP_mu2_idx]>{signal_inf})'
        self.filters_PP_posmu1 = self.filters_PP + ' && (int(patmu_pt[dimPP_mu1_idx])%2==1)'
        self.filters_PP_negmu1 = self.filters_PP + ' && (int(patmu_pt[dimPP_mu1_idx])%2==0)'


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Filters for PD6 dimuons, which, whith used defs of displaced, actually don't contribute

        self.filters_PD6_B = '(' + ') && ('.join (self.sel_PD6) + ')' + ' && (int(patmu_pt[dimD6D6_mu1_idx])%2==0) '#&& (int(patmu_pt[dimPP_mu1_idx])%2==1)'
        self.filters_PD6_D = '(' + ') && ('.join (self.sel_PD6) + ')' + ' && (int(patmu_pt[dimD6D6_mu1_idx])%2==1) '#&& (int(patmu_pt[dimPP_mu1_idx])%2==0)'

        self.filters_PD6_over_limit_B = self.filters_PD6_B + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf})'
        self.filters_PD6_over_limit_D = self.filters_PD6_D + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf})'

        self.filters_PD6_under_limit_B_C = self.filters_PD6_B + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]<{signal_limit}) && (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf})'
        self.filters_PD6_under_limit_D_C = self.filters_PD6_D + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]<{signal_limit}) && (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf})'


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # The union of all self.filters which constitute each region, must only be used for plotting variables involving some dimuon index (not for invMass, hasVtx, etc.)

        
        self.total_filters_DD = self.filters_D6D6_over_limit
        
        self.total_filters_PD_B = '(' + self.filters_D6D6_under_limit_B + ') || (' +  self.filters_D2D6_over_limit_B + ') || (' + self.filters_PD6_over_limit_B + ')'
        
        self.total_filters_PD_D = '(' + self.filters_D6D6_under_limit_D + ') || (' + self.filters_D2D6_over_limit_D + ') || (' + self.filters_PD6_over_limit_D + ')'
        
        self.total_filters_PP = '('+ self.filters_D6D6_under_limit_C + ') ||' + '('+ self.filters_PP + ') ||' + '(' + self.filters_D2D2_C + ') || (' + self.filters_PD2_B_C + ') || (' + self.filters_PD2_D_C + ') || (' + self.filters_D2D6_under_limit_B_C + ') || (' +self.filters_D2D6_under_limit_D_C + ') || (' + self.filters_PD6_under_limit_B_C + ') || (' + self.filters_PD6_under_limit_D_C + ')'


  


    def make_filters(self):
        '''
        Makes final filters used in 2D ABCD and predictions plots by adding muons charge and d0sig limits specifications to Martin's d0sig definitions
        One must join and split different parts of this d0sig defs in order to obtain the final used ABCD regions
        '''

        # Filters for all events with >1 good muons
        self.Filters_All_muons = '(' + ') && ('.join (self.sel_All) + ')'


        # Make an extra filter for SS validation, it's the only needed since it's the only one I can't make directly with SS_validation_cuts due to the way PD filters defs are implemented  
        self.filters_D2D6_over_limit_SS = '(' + ') && ('.join (self.sel_D2D6) + ')' + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]>{signal_inf})'
        self.filters_D2D6_under_limit_SS = '(' + ') && ('.join (self.sel_D2D6) + ')' + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]<{signal_limit}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]>{signal_inf})'

        self.filters_D6D6_over_limit_SS = '(' + ') && ('.join (self.sel_D6D6) + ')' + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimD6D6_mu2_idx]<={signal_limit})'


        # Filters for D6D6 dimuons, which has A, B, C and D components

        self.filters_D6D6 = '(' + ') && ('.join (self.sel_D6D6) + ')'

        self.filters_D6D6_over_limit =  self.filters_D6D6 + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimD6D6_mu2_idx]>{signal_limit})'
        self.filters_D6D6_over_limit_posmu1 = self.filters_D6D6_over_limit + ' && (patmu_charge[dimD6D6_mu1_idx]==1 )'
        self.filters_D6D6_over_limit_negmu1 = self.filters_D6D6_over_limit + ' && (patmu_charge[dimD6D6_mu1_idx]==-1)'

        self.filters_D6D6_under_limit_C = self.filters_D6D6 + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]<= {signal_limit}) && (patmu_d0sig_pv[dimD6D6_mu2_idx]<= {signal_limit}) && (patmu_d0sig_pv[dimD6D6_mu2_idx]>={signal_inf}) && (patmu_d0sig_pv[dimD6D6_mu1_idx]>={signal_inf})'
        self.filters_D6D6_under_limit_C_posmu1 = self.filters_D6D6_under_limit_C + ' && (patmu_charge[dimD6D6_mu1_idx]==1)'
        self.filters_D6D6_under_limit_C_negmu1 = self.filters_D6D6_under_limit_C + ' && (patmu_charge[dimD6D6_mu1_idx]==-1)'

        self.filters_D6D6_under_limit_B = self.filters_D6D6 + ' && (patmu_charge[dimD6D6_mu1_idx]==-1)  && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimD6D6_mu2_idx]<={signal_limit}) && (patmu_d0sig_pv[dimD6D6_mu2_idx]>={signal_inf}) && (patmu_d0sig_pv[dimD6D6_mu1_idx]>={signal_inf})'
        self.filters_D6D6_under_limit_D = self.filters_D6D6 + ' && (patmu_charge[dimD6D6_mu1_idx]==1)   && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimD6D6_mu2_idx]<={signal_limit}) && (patmu_d0sig_pv[dimD6D6_mu2_idx]>={signal_inf}) && (patmu_d0sig_pv[dimD6D6_mu1_idx]>={signal_inf})'


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Filters for D2D2 dimuons, which has just C component 

        self.filters_D2D2 = '(' + ') && ('.join (self.sel_D2D2) + ')'
        self.filters_D2D2_C = self.filters_D2D2 + ' && (patmu_d0sig_pv[dimD2D2_mu1_idx]>{signal_inf}) && (patmu_d0sig_pv[dimD2D2_mu2_idx]>{signal_inf}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]<{signal_limit}) && (patmu_d0sig_pv[dimD2D2_mu2_idx]<{signal_limit})'
        self.filters_D2D2_C_posmu1 = self.filters_D2D2_C + ' && (patmu_charge[dimD2D2_mu1_idx]==1)'
        self.filters_D2D2_C_negmu1 = self.filters_D2D2_C + ' && (patmu_charge[dimD2D2_mu1_idx]==-1)'


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Filters for D2D6 dimuons, which has B, C and D components

        self.filters_D2D6_B = '(' + ') && ('.join (self.sel_D2D6) + ')' + ' && patmu_charge[dimD6D6_mu1_idx]==-1 && patmu_charge[dimD2D2_mu1_idx]==1' 
        self.filters_D2D6_D = '(' + ') && ('.join (self.sel_D2D6) + ')' + ' && patmu_charge[dimD6D6_mu1_idx]==1 && patmu_charge[dimD2D2_mu1_idx]==-1'

        self.filters_D2D6_over_limit_B = self.filters_D2D6_B + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]>{signal_inf})'
        self.filters_D2D6_over_limit_D = self.filters_D2D6_D + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]>{signal_inf})'

        self.filters_D2D6_under_limit_B_C = self.filters_D2D6_B + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]<{signal_limit}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]>{signal_inf})'
        self.filters_D2D6_under_limit_D_C = self.filters_D2D6_D + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]<{signal_limit}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]>{signal_inf})'


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Filters for PD2 dimuons, which, whith used defs of displaced, actually don't contribute

        self.filters_PD2_B = '(' + ') && ('.join (self.sel_PD2) + ')' + ' && patmu_charge[dimD2D2_mu1_idx]==-1 && patmu_charge[dimPP_mu1_idx]==1'
        self.filters_PD2_D = '(' + ') && ('.join (self.sel_PD2) + ')' + ' && patmu_charge[dimD2D2_mu1_idx]==1 && patmu_charge[dimPP_mu1_idx]==-1'

        self.filters_PD2_B_C = self.filters_PD2_B + ' && (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]<{signal_limit})'
        self.filters_PD2_D_C = self.filters_PD2_D + ' && (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf}) && (patmu_d0sig_pv[dimD2D2_mu1_idx]<{signal_limit})'


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Filters for PP dimuons, which, whith used defs of displaced, actually don't contribute

        self.filters_PP = '(' + ') && ('.join (self.sel_PP) + ')' + '&&  (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf}) && (patmu_d0sig_pv[dimPP_mu2_idx]>{signal_inf})'
        self.filters_PP_posmu1 = self.filters_PP + ' && (patmu_charge[dimPP_mu1_idx]==1)'
        self.filters_PP_negmu1 = self.filters_PP + ' && (patmu_charge[dimPP_mu1_idx]==-1)'


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # Filters for PD6 dimuons, which, whith used defs of displaced, actually don't contribute

        self.filters_PD6_B = '(' + ') && ('.join (self.sel_PD6) + ')' + ' && patmu_charge[dimD6D6_mu1_idx]==-1 && patmu_charge[dimPP_mu1_idx]==1'
        self.filters_PD6_D = '(' + ') && ('.join (self.sel_PD6) + ')' + ' && patmu_charge[dimD6D6_mu1_idx]==1 && patmu_charge[dimPP_mu1_idx]==-1'

        self.filters_PD6_over_limit_B = self.filters_PD6_B + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf})'
        self.filters_PD6_over_limit_D = self.filters_PD6_D + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]>{signal_limit}) && (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf})'

        self.filters_PD6_under_limit_B_C = self.filters_PD6_B + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]<{signal_limit}) && (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf})'
        self.filters_PD6_under_limit_D_C = self.filters_PD6_D + ' && (patmu_d0sig_pv[dimD6D6_mu1_idx]<{signal_limit}) && (patmu_d0sig_pv[dimPP_mu1_idx]>{signal_inf})'


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # The union of all self.filters which constitute each region, must only be used for plotting variables involving some dimuon index (not for invMass, hasVtx, etc.)

        
        self.total_filters_DD = self.filters_D6D6_over_limit
        
        self.total_filters_PD_B = '(' + self.filters_D6D6_under_limit_B + ') || (' +  self.filters_D2D6_over_limit_B + ') || (' + self.filters_PD6_over_limit_B + ')'
        
        self.total_filters_PD_D = '(' + self.filters_D6D6_under_limit_D + ') || (' + self.filters_D2D6_over_limit_D + ') || (' + self.filters_PD6_over_limit_D + ')'
        
        self.total_filters_PP = '('+ self.filters_D6D6_under_limit_C + ') ||' + '('+ self.filters_PP + ') ||' + '(' + self.filters_D2D2_C + ') || (' + self.filters_PD2_B_C + ') || (' + self.filters_PD2_D_C + ') || (' + self.filters_D2D6_under_limit_B_C + ') || (' +self.filters_D2D6_under_limit_D_C + ') || (' + self.filters_PD6_under_limit_B_C + ') || (' + self.filters_PD6_under_limit_D_C + ')'


