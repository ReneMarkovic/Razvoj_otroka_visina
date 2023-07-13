import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import markdown
import os
import json
import datetime

report_text=""



st.session_state["mati"] = 168
st.session_state["oce"] = 178
st.session_state["spol"] =  "M"
st.session_state["t_otrok"] = 5*12+8
st.session_state["h_otrok"] = 127
st.session_state["show_results"] = False


def get_variable_state():
    mati=st.session_state["mati"]
    oce=st.session_state["oce"] 
    spol=st.session_state["spol"] 
    t_otrok=st.session_state["t_otrok"]
    h_otrok=st.session_state["h_otrok"] 
    st.session_state["show_results"] = False
    return [mati,oce,spol,t_otrok,h_otrok]

def save_user_input():
    time_now = datetime.datetime.now()
    st.session_state["time_now"] = time_now
    filename = os.path.join("user_input.json")
    with open(filename, "a") as f:
        
        json.dump(st.session_state, f)

save_user_input()


def interval(x,seznam,p_values):
    seznam=sorted(seznam)
    for i,v in enumerate(seznam):
        if v>x:
            dy=p_values[i]-p_values[i-1]
            dx=seznam[i]-seznam[i-1]
            k=dy/dx
            pp=p_values[i-1]+k*(x-seznam[i-1])
            return (x,pp)


def napoved(x,seznam,p_values):
    seznam=sorted(seznam)
    for i,v in enumerate(p_values):
        if v>x:
            dx=p_values[i]-p_values[i-1]
            dy=seznam[i]-seznam[i-1]
            k=dy/dx
            y=seznam[i-1]+k*(x-p_values[i-1])
            return y
        

def figure_1(female_h, female_p, male_h, male_p):
    
    mati,oce,spol,t_otrok,h_otrok=get_variable_state()
    plt.figure(figsize=(12,6))
    x,y=interval(mati,female_h,female_p)
    y_f=y
    
    x,y=interval(oce,male_h,male_p)
    y_m=y
    
    
    y_cor=(y_m+y_f)/2.0
    
    aa=0.4

    if spol=="M":
        x_napoved=napoved(y_cor,male_h,male_p)
        h_pred=x_napoved
        plt.vlines(x_napoved,0,y_cor,ls="-.",color="navy")
        plt.hlines(y_cor,min(female_h),x_napoved,ls="-.",color="navy")
        plt.text(min(female_h)+15,y_cor + 1, f"Sin", ha='center', va='bottom', color="navy",size=12)
    plt.plot(male_h,male_p,color="navy",alpha=aa,lw=0.5)
    plt.scatter(male_h,male_p,color="navy",s=5)
    
    plt.scatter(x,y,color="navy",s=20)
    plt.scatter(x,0,color="navy",s=40)
    
    plt.text(min(female_h) + 1,y_m + 1, f"Oče", ha='center', va='bottom', color="navy",size=12)
    plt.hlines(y,min(female_h),x, ls="-.",color="navy",lw=0.5)
    plt.vlines(x,0,y,ls="-.",color="navy",lw=0.5)
        
    x, y = interval(mati,female_h,female_p)
    y_f = y
    
    aa=0.4
    if spol=="Ž":
        x_napoved=napoved(y_cor,female_h,female_p)
        h_pred=x_napoved
        plt.vlines(x_napoved,0,y_cor,ls="-.",color="hotpink")
        plt.hlines(y_cor,min(female_h),x_napoved,ls="-.",color="hotpink")
        plt.text(min(female_h)+15,y_cor + 1, f"Hči", ha='center', va='bottom', color="hotpink",size=12)
    
    plt.plot(female_h,female_p,marker="o",color="pink",alpha=aa,lw=0.5)
    plt.scatter(female_h,female_p,color="pink",s=5)
    
    plt.scatter(x,y,color="hotpink",s=20,alpha=aa)
    plt.scatter(x,0,color="hotpink",s=40,alpha=aa)
    plt.vlines(x,0,y,ls="-.",color="hotpink",alpha=aa,lw=0.5)
    plt.hlines(y,min(female_h),x,ls="-.",color="hotpink",alpha=aa,lw=0.5)
    plt.text(min(female_h)+1,y_f + 1, f"Mati", ha='center', va='bottom', color="hotpink",size=12)
    
    
    plt.hlines(50,min(female_h),200,ls="-.",color="gray",lw=0.5)
    plt.text(190,50 + 1, f"Povprečje", ha='center', va='bottom', color="gray")
    
    
    plt.title(f"Korekcija percentila -> {y_cor:.1f}")
    plt.ylabel("Percentili (%)")
    plt.xlabel("Višina [cm]")
    plt.xlim(min(female_h),200)
    plt.ylim(0,100)
    plt.savefig("Fig_1.jpg",dpi=150)
    st.pyplot(plt)
    return [y_cor,h_pred,y_m,y_f]


def analiza(df_male,df_female,y_corr):
    mati,oce,spol,otrok_t,otrok_h=get_variable_state()
    result_text=""
    st.markdown("## Specične karakteristike otroka")
    result_text+="## Specične karakteristike otroka\n\n"
    
    df=df_male
    if spol=="Ž":
        df=df_female
    
    cols=df.columns
    seznam=df[df["Month"]==otrok_t][cols[5::]].values[0]
    p_values=[p.replace("P","").replace("01","0.1").replace("999","99.9") for p in cols[5::]]
    p_values=[float(p) for p in p_values]
    x1,y1=interval(otrok_h,seznam,p_values)
    x_napoved=napoved(y_corr,seznam,p_values)
    
    delta_H=otrok_h-x_napoved
    
    h_mean=df[df["Month"]==otrok_t]["P50"].values[0]
    final_mean=df["P50"].max()
    
    scale=oce/final_mean
    if spol=="Ž":
        scale=mati/final_mean
    
    
    rezultat=f"Povprečen otrok starosti **{otrok_t/12:.1f}** let je visok **{h_mean:.1f}** cm. "
    rezultat+=f"Višina otroka je **{otrok_h} cm**, kar ustreza **{y1:.1f} percentilu**. "
    rezultat+=f"Ob upoštevanju, da je mid-parental centile **{y_corr:.1f}**, je pričakovana velikost otroka **{x_napoved:.1f}** cm. "
    rezultat+=f"Ralika med dejansko velikostjo in pričakovano je **{otrok_h-x_napoved:.1f}** cm oziroma **{delta_H/x_napoved*100:.1f}**% od pričakovane višine.\n\n"
    st.markdown(rezultat)
    result_text+=rezultat
    #display(df[df["Month"]==otrok_t][cols[5::]])
    
    plt.figure(figsize=(12,6))
    
    color=["red","orange","yellow","green","yellow","orange","red"]
    plt.subplot(121)
    plt.title("Normalni potek")
    for cc,c in enumerate([1,5,25,50,75,95,99]):
        plt.plot(df["L"],df[f"P{c}"],label=f"p = {c}",color=color[cc])
        
    plt.text(otrok_t/12,otrok_h + 3, f"Podatek", ha='center', va='bottom', color="black",size=12)
    plt.scatter(otrok_t/12,otrok_h)
    
    plt.text(otrok_t/12,x_napoved + 1, f"Predvideno", ha='center', va='bottom', color="black",size=12)
    plt.scatter(otrok_t/12,x_napoved,color="green")
    
    plt.xlim(0,int(otrok_t/12)+1)
    plt.ylim(40,otrok_h+5)
    plt.yticks(range(40,int(otrok_h+5),5))
    plt.ylabel("Višina (cm)")
    plt.xlabel("Starost (let)")
    plt.legend()
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    
    
    plt.subplot(122)
    plt.title("Prilagojen potek")
    for cc,c in enumerate([1,5,25,50,75,95,99]):
        plt.plot(df["L"],df[f"P{c}"]*scale,label=f"p = {c}",color=color[cc])
        
    plt.text(otrok_t/12,otrok_h + 3, f"Podatek", ha='center', va='bottom', color="black",size=12)
    plt.scatter(otrok_t/12,otrok_h)
    
    plt.text(otrok_t/12,x_napoved + 1, f"Predvideno", ha='center', va='bottom', color="black",size=12)
    plt.scatter(otrok_t/12,x_napoved,color="green")
    
    plt.xlim(0,int(otrok_t/12)+1)
    plt.ylim(40,otrok_h+5)
    plt.yticks(range(40,int(otrok_h+5),5))
    plt.ylabel("Višina (cm)")
    plt.xlabel("Starost (let)")
    plt.legend()
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.savefig("Fig_2.jpg",dpi=150)
    st.pyplot(plt)
    return result_text


def potek_visine(df_male,df_female,y_corr):
    mati,oce,spol,otrok_t,otrok_h=get_variable_state()
    result_text=""
    result_text+="## Napoved nadaljne rasti otroka\n\n"
    st.markdown("## Napoved nadaljne rasti otroka")
    df=df_male
    if spol=="Ž":
        df=df_female
    
    cols=df.columns
    seznam=df[df["Month"]==otrok_t][cols[5::]].values[0]
    p_values=[p.replace("P","").replace("01","0.1").replace("999","99.9") for p in cols[5::]]
    p_values=[float(p) for p in p_values]
    x1,y1=interval(otrok_h,seznam,p_values)
    x_napoved=napoved(y_corr,seznam,p_values)
    
    delta_H=otrok_h-x_napoved
    
    h_mean=df[df["Month"]==otrok_t]["P50"].values[0]
    final_mean=df["P50"].max()
    
    scale=otrok_h/h_mean
    h_final=scale*final_mean
    
    rezultat=f"V kolikor bo otrok nadaljeval z rastjo v isti percentilni skupini, se bo njegova višina z leti spreminjala kot to prikazuje spodnja slika. Iz napovedi pa je razvidno, da bi lahko otrok, dosegel končno višino **{h_final:.1f} cm**.\n\n"
    result_text+=rezultat
    st.markdown(rezultat)
    #display(df[df["Month"]==otrok_t][cols[5::]])
    
    plt.figure(figsize=(12,6))
    
    color=["red","orange","yellow","green","yellow","orange","red"]
    plt.title("Normalni potek")
    for cc,c in enumerate([1,5,25,50,75,95,99]):
        plt.plot(df[df["Month"]<otrok_t]["L"],df[df["Month"]<otrok_t][f"P{c}"],label=f"p = {c}",color=color[cc])
    plt.plot(df[df["Month"]>otrok_t]["L"],df[df["Month"]>otrok_t][f"P50"]*scale,label=f" Napoved",color="black")
    plt.legend()
    for cc,c in enumerate([1,5,25,50,75,95,99]):
        y0=df[df["Month"]>otrok_t]["P50"]
        dy=y0+(df[df["Month"]>otrok_t][f"P{c}"]-y0)*(1-np.exp(-0.01*(df[df["Month"] > otrok_t]["Month"] - otrok_t)))
        
        plt.plot(df[df["Month"]>otrok_t]["L"],dy*scale,label=f"p = {c}",color=color[cc],ls="-.",lw=0.5)
    plt.text(otrok_t/12,otrok_h + 3, f"Podatek", ha='center', va='bottom', color="black",size=12)
    plt.scatter(otrok_t/12,otrok_h)
    
    plt.text(otrok_t/12,x_napoved + 1, f"Predvideno", ha='center', va='bottom', color="black",size=12)
    plt.scatter(otrok_t/12,x_napoved,color="green")
    
    plt.xlim(0,19)
    plt.ylim(40,200)
    plt.yticks(range(40,201,5))
    plt.xticks(range(0,20,1))
    plt.ylabel("Višina (cm)")
    plt.xlabel("Starost (let)")
    
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.savefig("Fig_3.jpg",dpi=150)
    st.pyplot(plt)
    st.markdown("**Vir:**")
    result_text+="\n\n {FIGURE_3} \n\n"
    result_text+="**Vir:**\n\n"
    result_text+="[https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1071029/](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1071029/)\n\n"
    
    link="https://geekymedics.com/paediatric-growth-chart-documentation-osce-guide/"
    st.markdown(f"- [tolmačenje grafov]({link})")
    return result_text
    

def result():
    mati,oce,spol,t_otrok,h_otrok=get_variable_state()
    report_text=""
    report_text+="## Vneseni podatki\n\n"
    report_text+="### Starši\n\n"
    report_text+=f"Oče: {oce} cm\n\n"
    report_text+=f"Mati: {mati} cm\n\n"
    report_text+="### Otrok\n\n"
    report_text+=f"Starost: {t_otrok} mesecev\n\n"
    report_text+=f"Starost: {(t_otrok/12):.1f} letih\n\n"
    report_text+=f"Višina: {h_otrok} cm\n\n"
    report_text+=f"Spol: {spol}\n\n"

    female_h, female_p, male_h, male_p,df_male,df_female=load_data()
    
    rezultat="### Predvidevanja glede na velikost staršev\n\n"
    report_text+=rezultat
    report_text+="\n\n {FIGURE_1} \n\n"
    st.markdown(rezultat)
    otrok_p,otrok_h,y_m,y_f=figure_1(female_h, female_p, male_h, male_p)
    y_corr=(y_m+y_f)/2
    
    
    rezultat=f"Višina matere ustreza {y_f:.1f} percenilu. Višina očeta ustreza {y_m:.1f} percenilu. "
    rezultat+=f"Ob upoštevanju velikosti staršev, je srednja percentilna krivulja {y_corr:.1f}. "
    rezultat+=f"Če bi otrok sledil percentilni krivulji, bi pričakocali, da bi dosegel višino v odrasli dobi **{otrok_h:.1f} cm.**\n\n"
    st.markdown(rezultat)
    report_text+=rezultat

    rezultat="### Analiza dejanske višine otroka\n\n"
    rezultat+="Graf na levi prikazuje normalni potek razvijanja višine ob upoštevanju različnih percentilnih skupin. "
    rezultat+="Druga točka pa prikazuje dejansko višino otroka. S tem lahko ocenimo v kateri percentilni skupini je otrok glede na vso populacijo. "
    rezultat+="Graf na desni pa prikazuje prilagojene percentilne krivulje, ki upoštevajo višino otroka. "
    rezultat+="V kolikor pride glede na normalni razvoj do odstopanj, lahko ta odstopanje še analiziramo z vidika višine staršev."
    st.markdown(rezultat)
    report_text+=rezultat
    
    report_text+=analiza(df_male,df_female,y_corr)
    report_text+="\n\n {FIGURE_2} \n\n"
    
    
    report_text+=potek_visine(df_male,df_female,y_corr)
    return report_text


def load_data():
    file_path = "Višina.xlsx"
    xls = pd.ExcelFile(file_path)
    male,female = xls.sheet_names

    df_male = pd.read_excel(file_path, sheet_name=male)
    df_female = pd.read_excel(file_path, sheet_name=female)

    cols=df_male.columns

    male_h=df_male.iloc[-1,5::].tolist()
    male_p=[p.replace("P","").replace("01","0.1").replace("999","99.9") for p in cols[5::]]
    male_p=[float(p) for p in male_p]

    cols=df_female.columns

    female_h=df_female.iloc[-1,5::].tolist()
    female_p=[p.replace("P","").replace("01","0.1").replace("999","99.9") for p in cols[5::]]
    female_p=[float(p) for p in female_p]
    return [female_h, female_p, male_h, male_p,df_male,df_female]


def ui():
    st.title("Podatki o višini otroka in staršev")
    mati = st.number_input("Višina matere [cm]:",value=168)
    oce = st.number_input("Višina očeta [cm]:",value=178)
    h_otrok = st.number_input("Višina otroka. [cm]:",value=127)
    
    spol_options = ("M", "Ž")
    spol_default_index = spol_options.index("M")
    spol = st.selectbox("Spol otroka", options=spol_options, index=spol_default_index)
    #spol = st.text_input("Spol otroka (M ali Ž):",value="M")
    st.write("Vnesite starost otroka v letih in mesecih.")
    t_otrok = 12 * st.number_input("Vnesite dopolnjena leta otroka:",value=5)
    t_otrok += st.number_input("Vnesite število mesecev:",value=8)
    
    st.session_state["mati"] = mati
    st.session_state["oce"] = oce
    st.session_state["spol"] = spol
    st.session_state["t_otrok"] = t_otrok
    st.session_state["h_otrok"] = h_otrok
    st.session_state["show_results"] = False
    
    if mati < 100:
        mati *= 100
    if oce < 100:
        oce *= 100.0
    if h_otrok < 100:
        h_otrok *= 100.0

    st.write()
    st.markdown("Povzetek vnesenih podatkov:")
    st.markdown(f"   - Višina matere = {mati} cm.")
    st.markdown(f"   - Višina očeta = {oce} cm.")
    st.markdown(f"   - Višina otroka = {h_otrok} cm.")
    st.markdown(f"   - Spol otroka = {spol}.")
    st.markdown(f"   - Starost otroka = {t_otrok/12:.1f} let.")
    vnos = 1 - st.checkbox("Ali so podatki pravilni?")
    page="Vnos podatkov"
    if vnos == 0:
        st.write("Hvala za pregled podatkov. S pritiskom na gumb začnite z analizo.")
        if st.button("Prični z analizo"):
            st.session_state["mati"] = mati
            st.session_state["oce"] = oce
            st.session_state["spol"] = spol
            st.session_state["t_otrok"] = t_otrok
            st.session_state["h_otrok"] = h_otrok
            st.session_state["show_results"] = True
            st.write("Analiza se izvaja. Prosim če ob strani izberete zavihek **Rezultati** in si ogledate  pripravljeno poročilo.")
            return [mati, oce, spol, t_otrok, h_otrok, page]
    else:
        st.write("Potrdite pravilnost podatkov")
    return [mati, oce, spol, t_otrok, h_otrok, page]


def page_results():
    report_text=""
    report_text+="### Rezutlati\n\n"
    report_text+="V nadaljevnaju so prikazani rezultati analize"
    
    st.title("Rezultati")
    st.markdown("V nadaljevnaju so prikazani rezultati analize")
    report_text=result()
    return report_text

def main():
    page = st.sidebar.selectbox("Izberite stran", ["Uvod", "Vnos podatkov", "Rezultati"])
    mati, oce, spol, t_otrok, h_otrok=[168,178,"M",68,127]
    if page == "Uvod":
        page_intro()
    elif page == "Vnos podatkov":
        mati, oce, spol, t_otrok, h_otrok, page=ui()
    elif page == "Rezultati":
        report_text=page_results()
        report_text=report_text.replace(" {FIGURE_1} ","![Fig_1](Fig_1.jpg)")
        report_text=report_text.replace(" {FIGURE_2} ","![Fig_2](Fig_2.jpg)")
        report_text=report_text.replace(" {FIGURE_3} ","![Fig_3](Fig_3.jpg)")
        
        with open('report.md', 'w+',encoding="utf8") as f:
            f.write(report_text)
        markdown.markdownFromFile(input='report.md', output='report.html')
        mime_type = "text/html"
        encoding = "utf-8"
        with open('report.html', 'r',encoding="utf8") as f:
            st.download_button(label="Prenesite poročilo",
                           data=f,
                           file_name="report.html",
                           mime=mime_type,
                           key=None)

def page_intro():
    st.markdown("## Analiza")
    st.markdown("V nadaljevanju so povzeti podatki o starših in predstavljeni z vidika statističnih lasntosti.Za višino matere in očeta je določena vrednost percentila. Ta vrednost je tudi uporavljena za določitev predvidene velikosti otraoka v odrasli dobi. Velikost očeta in matere je tudi uporabljena za pravilno tolmačenje velikosti otroka v različnih staornih obdobjih. Vsi tukaj uporabljeni podatki podatki za izvedbo analize so pridobljeni s strani Svetovne zdravstvene organizacije (ang. WHO). Te podatke uporalbjajo tudi drugi strokovnjaki.")
    st.markdown("## viri")
    st.markdown("- [Podatki 5-19 let](https://www.who.int/tools/growth-reference-data-for-5to19-years/indicators/height-for-age)")
    st.markdown("- [Podatki 0-5 let](https://www.who.int/tools/child-growth-standards/standards/length-height-for-age)")