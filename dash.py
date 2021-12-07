import streamlit as st
import numpy as np

from atomizationModel import AtomizationModel as model

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

st.sidebar.header('Configuration')
noz = st.sidebar.selectbox('Select Nozzle', model.nozzles)
orif = st.sidebar.selectbox('Select Orifice', noz_orif_ang(noz)[0])
defl = st.sidebar.selectbox('Select Deflection', noz_orif_ang(noz)[1])
press = st.sidebar.slider('Select Pressure', 10, 90, 40)
airspeed = st.sidebar.slider('Select Airspeed', 50, 180, 140)

st.title('USDA Atomization Model')
a = model(noz, orif, airspeed, press, defl)
col1, col2, col3 = st.columns(3)
with col1:  
    st.latex(f'D_{{V0.1}} = {a.dv01()}\\ \mu m')
with col2:
    st.latex(f'D_{{V0.5}} = {a.dv05()}\\ \mu m')
with col3:
    st.latex(f'D_{{V0.9}} = {a.dv09()}\\ \mu m')
    
st.latex(f'Relative\\ Span = {a.rs():.2f}')
st.latex(f'Percent\\  Volume\\  < 100\mu m = {a.p_lt_100():.2f}\%')
st.latex(f'Percent\\  Volume\\  < 200\mu m = {a.p_lt_200():.2f}\%')
st.latex(f'Relative\\ Span = \t{{{a.rs():.2f}}}')
st.latex(f'Droplet\\  Spectrum\\  Category = {a.dsc()}')