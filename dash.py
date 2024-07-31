import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from atomizationModel import AtomizationModel as model
from plots import Plots as plot

gpm = 0

def noz_orif_ang (nozzle):
    #Check ls
        orif_a = []
        def_a = []
        if nozzle in model.ls_dict.keys():
            orif_a = model.ls_dict[nozzle]['Orifice']
            def_a = model.ls_dict[nozzle]['Angle']
        #Check hs
        orif_b = []
        def_b = []
        if nozzle in model.hs_dict.keys():
            orif_b = model.hs_dict[nozzle]['Orifice']
            def_b = model.hs_dict[nozzle]['Angle']
        #combine and remove duplicates
        orif_c = sorted(np.unique(orif_a+orif_b))
        def_c = sorted(np.unique(def_a+def_b))
        return orif_c, def_c

def get_gpm():
    if solve_for=='Number of Nozzles':
        return model(noz, orif, airspeed, press, defl).calc_gpm()
    else:
        return (gpa * airspeed * sw) / (num_noz * 495)

def solve_for_callback():
    if solve_for=='Number of Nozzles':
        st.session_state.num_noz = (gpa * airspeed * sw) / (get_gpm() * 495)
    else:
        gpm_40 = model(noz, orif, airspeed, 40, defl).calc_gpm()
        st.session_state.press = 40 * (get_gpm() / gpm_40)**2
    return gpm

solve_for = st.sidebar.radio(
     'Solve for:',
     ['Number of Nozzles', 'Pressure'],
     on_change=solve_for_callback
)

st.sidebar.header('Atomization Model')
noz = st.sidebar.selectbox('Select Nozzle', model.nozzles, on_change=solve_for_callback)
orif = st.sidebar.selectbox('Select Orifice', noz_orif_ang(noz)[0], on_change=solve_for_callback)
defl = st.sidebar.selectbox('Select Deflection', noz_orif_ang(noz)[1], on_change=solve_for_callback)
press = st.sidebar.slider('Select Pressure', 10, 90, 40, disabled=(solve_for=='Pressure'), key='press', on_change=solve_for_callback)
airspeed = st.sidebar.slider('Select Airspeed', 50, 180, 140, on_change=solve_for_callback)
st.sidebar.header('Calibration')
gpa = st.sidebar.slider('Select Application Rate (GPA)', 1, 10, 2, on_change=solve_for_callback)
sw = st.sidebar.slider('Select Swath Width (FT)', 30, 100, 55, on_change=solve_for_callback)
num_noz = st.sidebar.slider('Select Number of Nozzles', 10, 100, 35, disabled=(solve_for=='Number of Nozzles'), key='num_noz', on_change=solve_for_callback)


st.title('USDA Atomization Model')
a = model(noz, orif, airspeed, press, defl)
col1, col2 = st.columns(2)
with col1:  
    st.markdown(f'$D_{{V0.1}}$ = {a.dv01()} microns - {a.dsc_name_dv01()}')
    st.markdown(f'$D_{{V0.5}}$ = {a.dv05()} microns - {a.dsc_name_dv05()}')
    st.markdown(f'$D_{{V0.9}}$ = {a.dv09()} microns - {a.dsc_name_dv09()}')
with col2:
    st.markdown(f'Droplet Spectrum Category = {a.dsc_name()}')
    st.markdown(f'Relative Span = {a.rs():.2f}')
    st.markdown(f'Percent Volume < 100 microns = {a.p_lt_100():.2f}\%')

st.pyplot(fig=plot.plot2D([('Test',a)]))

st.markdown(f'Required Total Boom Flow Rate = {(get_gpm()*num_noz):.2f} GPM')
st.markdown(f'Required Single Nozzle Flow Rate (GPM) = {get_gpm():.2f} GPM')
st.markdown(f'{round(press)} PSI required for desired {round(num_noz)} nozzles' if solve_for=='Pressure' else f'{round(num_noz)} nozzles required for desired {round(press)} PSI')