# Python Portfolio RAROC Model

## Import all necessary packages, and Set your Working Directory.
"""

from IPython.display import HTML
import random

def hide_toggle(text_dets,for_next=False):
    this_cell = """$('div.cell.code_cell.rendered.selected')"""
    next_cell = this_cell + '.next()'
    toggle_text = text_dets  # text shown on toggle link
    target_cell = this_cell  # target cell to control with toggle
    js_hide_current = ''  # bit of JS to permanently hide code in current cell (only when toggling next cell)

    if for_next:
        target_cell = next_cell
        toggle_text += ' next cell'
        js_hide_current = this_cell + '.find("div.input").hide();'

    js_f_name = 'code_toggle_{}'.format(str(random.randint(1,2**64)))

    html = """
        <script>
            function {f_name}() {{
                {cell_selector}.find('div.input').toggle();
            }}

            {js_hide_current}
        </script>

        <a href="javascript:{f_name}()">{toggle_text}</a>
    """.format(
        f_name=js_f_name,
        cell_selector=target_cell,
        js_hide_current=js_hide_current,
        toggle_text=toggle_text
    )

    return HTML(html)

hide_toggle('...')

import os

#Set your working directory here (aka the address where you will be saving your work)
os.chdir(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files')

from tqdm import tqdm

import pandas as pd

import datetime

import numpy as np

# from pandas.core.common import SettingWithCopyWarning

import warnings

warnings.filterwarnings('ignore')

import time

from scipy.stats import norm

from math import *

from dateutil.relativedelta import *

import matplotlib.pyplot as plt

from threading import *

# from sqlalchemy import create_engine

import pymysql

import numpy_financial as npf

import seaborn as sns

import plotly.express as px

import plotly.graph_objects as go

hide_toggle("Installing Packages and Setting Working Directory")

"""## Loading Functions"""

def mod_db(db,date_ref):
    new_db=db.copy()

    new_enddate=[]

    for i in range(len(new_db)):
        new_enddate.append(min(list(new_db['EndDate'])[i],date_ref))

    new_db['EndDate']=new_enddate

    return new_db

hide_toggle("Database Modification Function")

def adj_factor_lognormal(mu, sigma, z):
    if z > 1:
        return exp(mu+sigma*norm.ppf(np.random.rand()))
    else:
        return exp(mu+sigma*norm.ppf(z))

def adj_factor_normal(mu, sigma, z):
    if z > 1:
        return norm.ppf(np.random.rand(),loc=mu,scale=sigma)
    else:
        return norm.ppf(z,loc = mu,scale = sigma)

def final_cashflow_counter1(y,list_node):
    if list_node[12]==0:
        return 1
    else:
        return 0

def final_cashflow_counter2(y,list_node):
    if not list_node[12]==0 and y > list_node[12]:
        return 1
    else:
        return 0

def final_cashflow_counter3(y,list_node):
    if not list_node[12]==0 and not y > list_node[12]:
        return 1
    else:
        return 0

def final_cashflow_counter_supp1(y,list_node):
    if list_node[10]==0:
        return 1
    else:
        return 0

def final_cashflow_counter_supp2(y,list_node):
    if not list_node[10]==0 and y < list_node[10]:
        return 1
    else:
        return 0

def final_cashflow_counter_supp3(y,list_node):
    if not list_node[10]==0 and not y < list_node[10]:
        return 1
    else:
        return 0

def billing_month_dummy(y):
    if y.day+6 > 31 and y.day+6 <= 37:
        return y.month+1
    else:
        return y.month

def billing_year(y):
    if y.month == 12 and y.day > 25:
        return y.year+1
    else:
        return y.year

def billing_month(y):
    if y == 13:
        return 1
    else:
        return y

def qtr(y):
    if y >= 10:
        return 4
    elif y >= 7:
        return 3
    elif y >= 4:
        return 2
    else:
        return 1

def pos_neg_dif(y):
    if y < 0:
        return 0
    else:
        return y

def pos_neg_dif_two_val(x,y):
    if x > 0:
        return 0
    elif y > 0:
        return y
    else:
        return 0



hide_toggle('Necessary Statistical Functions')

def load_profile_simulator(name_cc,january,february,march,april,may_load,june,july,august,september,october,november,december,
                           january_lf, february_lf, march_lf, april_lf, may_lf, june_lf, july_lf, august_lf, september_lf,
                          october_lf, november_lf, december_lf):

    name=name_cc

    jan = january
    feb = february
    mar = march
    apr = april
    may = may_load
    jun = june
    jul = july
    aug = august
    sep = september
    octo = october
    nov = november
    dec = december

    janlf = january_lf
    feblf = february_lf
    marlf = march_lf
    aprlf = april_lf
    maylf = may_lf
    junlf = june_lf
    jullf = july_lf
    auglf = august_lf
    seplf = september_lf
    octolf = october_lf
    novlf = november_lf
    declf = december_lf


    sim_input = pd.DataFrame()

    sim_input['Billing Month'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    sim_input['Days'] = [31,31,28,31,30,31,30,31,31,30,31,30]
    sim_input['Monthly Consumption'] = [jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec]
    sim_input['Daily Consumption'] = sim_input['Monthly Consumption']/sim_input['Days']
    sim_input['Hourly Consumption'] = sim_input['Daily Consumption']/24
    sim_input['Load Factors'] = [janlf/100, feblf/100, marlf/100, aprlf/100, maylf/100, junlf/100, jullf/100, auglf/100, seplf/100, octolf/100, novlf/100, declf/100]
    sim_input['Max Hourly Consumption'] = sim_input['Hourly Consumption']/sim_input['Load Factors']

    sim_hourly = pd.DataFrame()
    sim_hourly['Interval'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]

    sim_lf=[]
    sim_total=[]

    for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
        sim_hourly_index = list(sim_input['Billing Month']).index(month)
        sim_hourly[month]=[list(sim_input['Hourly Consumption'])[sim_hourly_index]]*11 + [list(sim_input['Max Hourly Consumption'])[sim_hourly_index]] + [list(sim_input['Hourly Consumption'])[sim_hourly_index]]*12
        resulting_sim_lf = np.mean(sim_hourly[month])/max(sim_hourly[month])
        sim_lf.append(resulting_sim_lf)
        sim_total.append(sum(sim_hourly[month]))

    sim_hourly_new=sim_hourly.transpose()
    sim_hourly_new.columns = sim_hourly_new.iloc[0]
    sim_hourly_new = sim_hourly_new[1:]


    sim_hourly_new['Simulated Daily Load'] = sim_total
    sim_hourly_new['Actual Daily Load'] = list(sim_input['Daily Consumption'])
    sim_hourly_new['Check Daily Load'] = sim_hourly_new['Simulated Daily Load']-sim_hourly_new['Actual Daily Load']
    sim_hourly_new['Correction Factor'] = sim_hourly_new['Check Daily Load']/14

    sim_hourly_new['Simulated Load Factor'] = sim_lf
    sim_hourly_new['Actual Load Factor'] = list(sim_input['Load Factors'])
    sim_hourly_new['Check Load Factor'] = sim_hourly_new['Simulated Load Factor']-sim_hourly_new['Actual Load Factor']


    sim_hourly_final=sim_hourly.copy()


    for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
        sim_hourly_index = list(sim_input['Billing Month']).index(month)
        sim_hourly[month+' Correction'] = [list(sim_hourly_new['Correction Factor'])[sim_hourly_index]]*7 + [0]*10 + [list(sim_hourly_new['Correction Factor'])[sim_hourly_index]]*7
        sim_hourly_final[month] = sim_hourly[month]-sim_hourly[month+' Correction']

    sim_hourly = sim_hourly_final

    sim_lf=[]
    sim_total=[]

    for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
        sim_hourly_index = list(sim_input['Billing Month']).index(month)
        resulting_sim_lf = np.mean(sim_hourly[month])/max(sim_hourly[month])
        sim_lf.append(resulting_sim_lf)
        sim_total.append(sum(sim_hourly[month]))

    sim_hourly_new=sim_hourly.transpose()
    sim_hourly_new.columns = sim_hourly_new.iloc[0]
    sim_hourly_new = sim_hourly_new[1:]


    sim_hourly_new['Simulated Daily Load'] = sim_total
    sim_hourly_new['Actual Daily Load'] = list(sim_input['Daily Consumption'])
    sim_hourly_new['Check Daily Load'] = sim_hourly_new['Simulated Daily Load']-sim_hourly_new['Actual Daily Load']
    sim_hourly_new['Correction Factor'] = sim_hourly_new['Check Daily Load']/14

    sim_hourly_new['Simulated Load Factor'] = sim_lf
    sim_hourly_new['Actual Load Factor'] = list(sim_input['Load Factors'])
    sim_hourly_new['Check Load Factor'] = sim_hourly_new['Simulated Load Factor']-sim_hourly_new['Actual Load Factor']

    sim_hourly_new = sim_hourly_new.transpose()
    sim_hourly_new = sim_hourly_new.reset_index()

    sim_hourly.columns=['Interval','1','2','3','4','5','6','7','8','9','10','11','12']


    sim_hourly_list = []

    for i in range(12):
        sim_hourly_list += list(sim_hourly[str(i+1)]/1000)

    sim_hourly_table = pd.DataFrame()
    sim_hourly_table['Month'] = [1]*24+[2]*24+[3]*24+[4]*24+[5]*24+[6]*24+[7]*24+[8]*24+[9]*24+[10]*24+[11]*24+[12]*24
    sim_hourly_table['Interval'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]*12

    blankdf = pd.DataFrame()
    blankdf['Delimiter'] = ["|"]*len(sim_hourly_table)

    sim_hourly_table['ID_Load'] = sim_hourly_table['Month'].astype(str) + blankdf['Delimiter'] + sim_hourly_table['Interval'].astype(str)
    sim_hourly_table[name] = sim_hourly_list



    sim_load_profile=calendar_db[['Date','Billing Month','Hour']]

    sim_load_profile['Month'] = sim_load_profile['Date'].apply(lambda x:x.month)

    sim_load_profile = sim_load_profile[['Date','Billing Month','Month','Hour']]
    sim_load_profile.columns = ['Date','Billing Month','Month','Interval']


    blankdf = pd.DataFrame()
    blankdf['Delimiter'] = ["|"]*len(sim_load_profile)
    sim_load_profile['ID_Load'] = sim_load_profile['Month'].astype(str) + blankdf['Delimiter'] + sim_load_profile['Interval'].astype(str)

    sim_load_profile = sim_load_profile[['Billing Month','Month','Interval','ID_Load']]

    sim_load_profile = sim_load_profile.merge(sim_hourly_table[['ID_Load',name]],on='ID_Load',how='left')

    sim_load_profile = pd.pivot_table(sim_load_profile, index=['Billing Month', 'Interval'], aggfunc={name:np.mean})
    sim_load_profile = sim_load_profile.reset_index()

    cc_load[name] = sim_load_profile[name]

    return cc_load

hide_toggle('Load Profile Simulator Function')

def load_sim(cc_num):

    cc_node = customer_db.iloc[int(cc_num)]

    total_elapsed = 0

    min_cap=-12000
    max_cap=34000

    t1_start_upload_blank = time.time()

    #Initial Price DB

    customer_prices_db = solar_pac_wesm_forecasts_cc_mid[['Date','ID','ID_Load','Sim0']]

    date_today= datetime.datetime.today()

    start_cc_loadsim=datetime.datetime(date_today.year,12,26)
    end_cc_loadsim=datetime.datetime(date_today.year+1,12,25)

    customer_prices_db = customer_prices_db.loc[(customer_prices_db['Date'] >= start_cc_loadsim) & (customer_prices_db['Date'] < end_cc_loadsim+datetime.timedelta(days=1))]

    customer_load_db = cc_load.iloc[:,2:3]

    t1_stop_upload_blank = time.time()

    elapsed_time_upload_blank = round((t1_stop_upload_blank-t1_start_upload_blank)/60,2)

    print('Initializations Process Time:',elapsed_time_upload_blank)

    total_elapsed += elapsed_time_upload_blank


    t1_start_prereq = time.time()

    #Customer Load

    customer_load_db[cc_node[0]+'_Load'] = cc_load[cc_node[0]]

    #Creating a Temporary DB
    customer_temp_df=customer_prices_db.copy()
    customer_temp_df=customer_temp_df.merge(customer_load_db, on="ID_Load", how="left")

    #Adjusting Prices and Nodes
    load_price_correl = customer_temp_df['Sim0'].corr(customer_temp_df[cc_node[0]+'_Load'])

    final_cc_load = cc_load.iloc[:,:3]

    final_cc_load['Sim0']=customer_load_db[cc_node[0]+'_Load']

    t1_stop_prereq = time.time()

    elapsed_time_prereq = round((t1_stop_prereq-t1_start_prereq)/60,2)

    print('Necessary Prerequisites Process Time:',elapsed_time_prereq)

    total_elapsed += elapsed_time_prereq

    t1_start_simulations = time.time()

    simulated_df = pd.DataFrame()
    simulated_df['RandomNumbers'] = [np.random.rand() for i in range(1000)]

    adjload_sim=[]

    for sim in range(1000):

        rand_load = np.random.rand()
        z_load = simulated_df['RandomNumbers'][sim]*load_price_correl + rand_load*sqrt(1-load_price_correl**2)
        replacement = 0

        if z_load < 0:
            z_load = simulated_df['RandomNumbers'][sim]*load_price_correl + np.random.rand()*sqrt(1-load_price_correl**2)
            if z_load < 0:
                z_load = simulated_df['RandomNumbers'][sim]*load_price_correl + np.random.rand()*sqrt(1-load_price_correl**2)
                if z_load < 0:
                    z_load = simulated_df['RandomNumbers'][sim]*load_price_correl + np.random.rand()*sqrt(1-load_price_correl**2)
                    replacement = z_load
                    if z_load < 0:
                        z_load = simulated_df['RandomNumbers'][sim]*load_price_correl + np.random.rand()*sqrt(1-load_price_correl**2)
                        replacement = z_load
                    else:
                        replacement = z_load
                else:
                    replacement = z_load
            else:
                replacement = z_load
        else:
            replacement = z_load

        adj_factor_customer_load = adj_factor_normal(1, 0.093826, replacement)
        #print(sim, replacement,adj_factor_customer_load)
        adjload_sim.append(adj_factor_customer_load)

    simulated_df['AdjLoad'] = adjload_sim


    for fin_sim in range(1000):

        final_cc_load['Sim'+str(fin_sim+1)]=customer_load_db[cc_node[0]+'_Load']*simulated_df['AdjLoad'][fin_sim]

    t1_stop_simulations = time.time()

    elapsed_time = round((t1_stop_simulations-t1_start_simulations)/60,2)

    print('Simulations Process Time ('+cc_node[0]+'):',elapsed_time)

    total_elapsed+=elapsed_time

    return final_cc_load


hide_toggle('Loads Database Function')

def supplier_portfolio_valuation(supp_num, date_ref,price_cap1=0,profit_share_per1=0,price_cap2=0,profit_share_per2=0):

    if date_toggle!="NONE":
        new_supplier_db = mod_db(supplier_db,date_toggle)
    else:
        new_supplier_db = supplier_db

    #return new_supplier_db

#     if supp_num >= len(supplier_db):
#         print("Invalid supp_num. Maximum supp_num should be", len(supplier_db) - 1)
#         return

    supplier_node = new_supplier_db.iloc[int(supp_num)]

    date_today = datetime.datetime.today()
    date_today_reformat = date_today.strftime('%y%m%d')

    min_cap=-12000
    max_cap=34000
    discount_rate = 0.1214

    total_elapsed_comp=0

    df_supplier_results=pd.DataFrame(columns=['Run','Process Time (Minutes)','SimID',

                                              'Supplier',

                                              'Average Customer Price',
                                        'Average Generator Price',
                                        'Average Line Rental',


                                              'Fixed Customer Price',

                                        'Fixed Supplier Price',
                                        'Line Rental Cap',
                                              'Value'])
    #upload price and load databases

    t1_start_initializations = time.time()


    cc_price_sim=solar_pac_wesm_forecasts_cc_mid
    gen_price_sim=solar_pac_wesm_forecasts_supp_mid

    supp_name_for_sim = supplier_node[0]

    if 'ANDA' in supplier_node[0]:

        supp_load_db=solar_pac_load_profiles[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
           'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID',
           'SolarPacSupplyID',  supplier_node[0],'ANDA (Profit Sharing)']]

    else:

        supp_load_db=solar_pac_load_profiles[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
           'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID',
           'SolarPacSupplyID',  supplier_node[0]]]




    t1_stop_initializations = time.time()

    elapsed_time_initializations = round((t1_stop_initializations-t1_start_initializations)/60,2)

    #print('Uploading CC Load Database Process Time:',elapsed_time_initializations)
    total_elapsed_comp+=elapsed_time_initializations

    t1_start_init_supp = time.time()

    #date calculations
    start_supp_from_db=datetime.datetime(supplier_node[3],supplier_node[1],supplier_node[2])
    start_supp_today=datetime.datetime(date_today.year,date_today.month,date_today.day)

    start_supp=max(start_supp_from_db,start_supp_today)

    if date_toggle=="NONE":
        end_supp=datetime.datetime(supplier_node[6],supplier_node[4],supplier_node[5])
    else:
        end_supp=min(datetime.datetime(supplier_node[6],supplier_node[4],supplier_node[5]),datetime.datetime(date_toggle.year,date_toggle.month,date_toggle.day))

    calendar_supp = calendar_db.loc[(calendar_db['Date'] >= start_supp) & (calendar_db['Date'] < end_supp+datetime.timedelta(days=1))]

    calendar_supp_conso = calendar_supp.copy()
    calendar_supp_conso = calendar_supp_conso[['Date']]

    #Granular DB
    npv_db_original_gp=calendar_supp_conso.copy()
    npv_db_original_npv=calendar_supp_conso.copy()

    supplier_new = calendar_supp.reset_index(drop=True)

    #filtering the three dbs

    cc_price_sim = cc_price_sim.loc[(cc_price_sim['Date'] >= start_supp) & (cc_price_sim['Date'] < end_supp+datetime.timedelta(days=1))]
    cc_price_sim = cc_price_sim.reset_index(drop=True)
    gen_price_sim = gen_price_sim.loc[(gen_price_sim['Date'] >= start_supp) & (gen_price_sim['Date'] < end_supp+datetime.timedelta(days=1))]
    gen_price_sim =gen_price_sim.reset_index(drop=True)
    supp_load_db = supp_load_db.loc[(supp_load_db['Date'] >= start_supp) & (supp_load_db['Date'] < end_supp+datetime.timedelta(days=1))]
    supp_load_db =supp_load_db.reset_index(drop=True)
    #creating supplier columns

    fixed_supplier = [supplier_node[7]]*len(supplier_new)
    capacity_supplier = [supplier_node[8]]*len(supplier_new)
    variable_supplier = [supplier_node[9]]*len(supplier_new)


    supplier_new['Fixed Price'] = fixed_supplier

    supplier_new['Capacity Fee'] = capacity_supplier
    supplier_new['Variable Fee'] = variable_supplier

    t1_stop_init_supp = time.time()
    elapsed_time_init_supp = round((t1_stop_init_supp-t1_start_init_supp)/60,2)

    print('Initializations Process Time:',elapsed_time_init_supp)

    total_elapsed_comp+=elapsed_time_init_supp

    npv_counter_list=[]

    for run_no_supp in range(1001):

        t1_start_supp = time.time()

        #merging datasets
        sim_run_supp='Sim'+str(run_no_supp)

        cc_price_sim_for_supp_comp = cc_price_sim[['ID',sim_run_supp]]
        cc_price_sim_for_supp_comp = cc_price_sim_for_supp_comp.rename(columns={sim_run_supp:'Customer Price Sim'})

        gen_price_sim_for_supp_comp = gen_price_sim[['ID',sim_run_supp]]
        gen_price_sim_for_supp_comp = gen_price_sim_for_supp_comp.rename(columns={sim_run_supp:'Gen Price Sim'})

        if 'MAGAT' in str(supplier_node[0]):
            gen_load_for_comp = supp_load_db[['ID_Load']]
            gen_load_for_comp['MAGAT']=[10]*len(gen_load_for_comp)
        elif 'ANDA' in str(supplier_node[0]):
            gen_load_for_comp = supp_load_db[['ID_Load',supp_name_for_sim,'ANDA (Profit Sharing)']]

        else:
            gen_load_for_comp = supp_load_db[['ID_Load',supp_name_for_sim]]

        supplier_new_temp = supplier_new.copy()
        supplier_new_temp['Customer Price Sim'] = cc_price_sim_for_supp_comp['Customer Price Sim']
        supplier_new_temp['Gen Price Sim'] = gen_price_sim_for_supp_comp['Gen Price Sim']
        supplier_new_temp[supp_name_for_sim] = gen_load_for_comp[supp_name_for_sim]
        supplier_new_temp = supplier_new_temp.rename(columns={supp_name_for_sim:'Load'})

        if 'ANDA' in str(supplier_node[0]):
            supplier_new_temp['ANDA (Profit Sharing)'] = gen_load_for_comp['ANDA (Profit Sharing)']

        if 'ANDA' in str(supplier_node[0]):
            supplier_final = supplier_new_temp[['Date','Billing Month','Billing Year','Day','Hour','Fixed Price','Capacity Fee','Variable Fee','Customer Price Sim','Gen Price Sim','Load','ANDA (Profit Sharing)']]
        else:
            supplier_final = supplier_new_temp[['Date','Billing Month','Billing Year','Day','Hour','Fixed Price','Capacity Fee','Variable Fee','Customer Price Sim','Gen Price Sim','Load']]

        #supplier line rental
        supplier_final['Line Rental'] = supplier_final['Customer Price Sim'] - supplier_final['Gen Price Sim']

        supplier_final['LRFee_Counter1']= supplier_final['Line Rental'].apply(lambda x:final_cashflow_counter_supp1(x,supplier_node))

        supplier_final['LRFee_Counter2']= supplier_final['Line Rental'].apply(lambda x:final_cashflow_counter_supp2(x,supplier_node))

        supplier_final['LRFee_Counter3']= supplier_final['Line Rental'].apply(lambda x:final_cashflow_counter_supp3(x,supplier_node))

        supplier_final['LRFee1'] = [0]*len(supplier_final)

        supplier_final['LRFee2'] = -supplier_final['Line Rental']*supplier_final['Load']

        supplier_final['LRFee3'] = supplier_final['LRFee1']

        supplier_final['Line Rental Fee']=(supplier_final['LRFee_Counter1']*supplier_final['LRFee1'])+(supplier_final['LRFee_Counter2']*supplier_final['LRFee2'])+(supplier_final['LRFee_Counter3']*supplier_final['LRFee3'])

        #supplier computation
        supplier_final['WESM Sales']=supplier_final['Load']*supplier_final['Customer Price Sim']

        supplier_final['Generation Fee'] = -(supplier_final['Fixed Price']+
                                                supplier_final['Capacity Fee']+
                                                supplier_final['Variable Fee'])*supplier_final['Load']

        list_othercosts = ([np.max(supplier_final['Load'])*31*24*supplier_node[7]*1.12*0.0075]+[0]*(365*24))*relativedelta(end_supp,start_supp_from_db).years+[0]*(len(supplier_final)-len(([np.max(supplier_final['Load'])*31*24*supplier_node[7]*1.12*0.0075]+[0]*(365*24))*relativedelta(end_supp,start_supp_from_db).years))

        supplier_final['Other Costs']=list_othercosts[:len(supplier_final)]


        if 'ANDA' in str(supplier_node[0]):
            supplier_final['Price Cap1']=[price_cap1]*len(supplier_final)
            supplier_final['Price Cap2']=[price_cap2]*len(supplier_final)
            supplier_final['Difference2']=supplier_final['Customer Price Sim']-supplier_final['Price Cap2']
            supplier_final['Profit Share2']=supplier_final['Difference2'].apply(lambda x:pos_neg_dif(x))*supplier_final['ANDA (Profit Sharing)']*profit_share_per2

            supplier_final['Difference1']=supplier_final['Customer Price Sim']-supplier_final['Price Cap1']
            supplier_final['Profit Share1']=supplier_final.apply(lambda x:pos_neg_dif_two_val(x['Difference2'],x['Difference1']), axis=1)*supplier_final['ANDA (Profit Sharing)']*profit_share_per1

            supplier_final['Total']=(-supplier_final['Other Costs']+supplier_final['Generation Fee']+supplier_final['Line Rental Fee']+supplier_final['WESM Sales']-supplier_final['Profit Share2']-supplier_final['Profit Share1'])*0.75

        #elif 'STORM' in str(supplier_node[0]) or 'RES' in str(supplier_node[0]):
            #supplier_final['Total']=-supplier_final['Other Costs']+supplier_final['Generation Fee']


        else:
            supplier_final['Total']=(-supplier_final['Other Costs']+supplier_final['Generation Fee']+supplier_final['Line Rental Fee']+supplier_final['WESM Sales'])*0.75

        #calendar_supp_conso = calendar_supp_conso.merge(supplier_final[['Date','Total']],on='Date',how='left')

        #calendar_supp_conso = calendar_supp_conso.rename(columns={'Total':sim_run_supp})

        days_until_today = start_supp-date_ref

        npv_supplier = (supplier_final['Total'] / (1+discount_rate/8760)**np.arange(1, len(supplier_final['Total'])+1)).sum(axis=0)

        if days_until_today.days > 0:
            npv_supplier = npv_supplier/(1+discount_rate/8760)**days_until_today.days

        supplier_final['NPV'] = supplier_final['Total']/(1+discount_rate/8760)**days_until_today.days
        npv_db_original_gp=npv_db_original_gp.merge(supplier_final[['Date','Total']],on='Date',how='left')
        npv_db_original_gp.columns=list(npv_db_original_gp.columns[:len(npv_db_original_gp.columns)-1])+['GP'+str(run_no_supp)]
        npv_db_original_npv=npv_db_original_npv.merge(supplier_final[['Date','NPV']],on='Date',how='left')
        npv_db_original_npv.columns=list(npv_db_original_npv.columns[:len(npv_db_original_npv.columns)-1])+['NPV'+str(run_no_supp)]

        t1_stop_supp = time.time()
        elapsed_time_supp = round((t1_stop_supp-t1_start_supp)/60,2)


        results_list=[run_no_supp, elapsed_time_supp, sim_run_supp,supplier_node[0],
                      np.mean(supplier_final['Customer Price Sim']),
                          np.mean(supplier_final['Gen Price Sim']),
                          np.mean(supplier_final['Line Rental']),
                                        np.max(supplier_final['Load']),

                                        supplier_node[7],
                                        supplier_node[10],
                      npv_supplier]

        df_supplier_results.loc[run_no_supp] = results_list

        npv_counter_list.append(npv_supplier)

        # print(results_list, np.mean(npv_counter_list))


        total_elapsed_comp += elapsed_time_supp

    t1_start_finalizations = time.time()

    #calendar_supp_conso_dup = calendar_supp_conso.iloc[:,1:]

    #calendar_supp_conso[supplier_node[0]] = calendar_supp_conso_dup.mean(axis=1)

    #calendar_supp_conso=calendar_supp_conso[['Date',supplier_node[0]]]

    npv_db[supplier_node[0]] = df_supplier_results['Value']

    #df_supplier_results.to_sql(name_of_file+' Supplier Valuation',sqlEngine, if_exists='replace', index=False)

    #supplier_final.to_excel(name_of_file+' Supplier Valuation '+sim_run_supp+'.xlsx',index=False)

    t1_stop_finalizations = time.time()

    elapsed_time_finalizations = round((t1_stop_finalizations-t1_start_finalizations)/60,2)

    total_elapsed_comp += elapsed_time_finalizations

    print('Total Process Time:',total_elapsed_comp)


hide_toggle('Supplier Portfolio Valuation Function')

def customer_portfolio_valuation_long_term(cc_num,date_ref):

    if date_toggle!="NONE":
        new_customer_db = mod_db(customer_db,date_toggle)
    else:
        new_customer_db = customer_db

    cc_node = new_customer_db.iloc[int(cc_num)]


    date_today = datetime.datetime.today()
    date_today_reformat = date_today.strftime('%y%m%d')

    min_cap=-12000
    max_cap=34000
    discount_rate = 0.1214

    total_elapsed_comp=0

    df_cc_results=pd.DataFrame(columns=['Run','Process Time (Minutes)','SimID',
                                              'Customer',

                                              'Average Customer Price',
                                        'Average Generator Price',
                                        'Average Line Rental',
                                              'Hedge',

                                              'Fixed Customer Price',


                                        'Line Rental Cap',
                                              'Value'])
    #upload price and load databases

    t1_start_initializations = time.time()

    cc_price_sim=solar_pac_wesm_forecasts_cc_mid
    gen_price_sim=solar_pac_wesm_forecasts_supp_mid


    if 'Japan' in str(cc_node[0]):

        cc_load_sim=solar_pac_cc_load_sim_japan
        supp_name_for_sim = 'Japan 25MW'


    t1_stop_initializations = time.time()

    elapsed_time_initializations = round((t1_stop_initializations-t1_start_initializations)/60,2)

    #print('Uploading CC Load Database Process Time:',elapsed_time_initializations)
    total_elapsed_comp+=elapsed_time_initializations

    t1_start_init= time.time()

    #date calculations
    start_cc_from_db=datetime.datetime(cc_node[3],cc_node[1],cc_node[2])
    start_cc_today=datetime.datetime(date_today.year,date_today.month,date_today.day)

    start_cc=max(start_cc_from_db,start_cc_today)

    if date_toggle=="NONE":
        end_cc=datetime.datetime(cc_node[6],cc_node[4],cc_node[5])
    else:
        end_cc=min(datetime.datetime(cc_node[6],cc_node[4],cc_node[5]),datetime.datetime(date_toggle.year,date_toggle.month,date_toggle.day))

    calendar_cc = xs_calendar.loc[(xs_calendar['Date'] >= start_cc) & (xs_calendar['Date'] < end_cc+datetime.timedelta(days=1))]

    calendar_cc_conso = calendar_cc.copy()
    calendar_cc_conso = calendar_cc_conso[['Date']]

    #Granular DB
    npv_db_original_gp=calendar_cc_conso.copy()
    npv_db_original_npv=calendar_cc_conso.copy()

    cc_new = calendar_cc.reset_index(drop=True)

    delim=pd.DataFrame()
    delim['Delimiter'] =["|"]*len(xv)

    cc_new['YearMonthID']=cc_new['Year'].astype('str')+delim['Delimiter']+cc_new['Month'].astype('str')


    fixed_cc = [cc_node[9]]*len(cc_new)

    cc_new['Fixed Price'] = fixed_cc

    t1_stop_init = time.time()
    elapsed_time_init = round((t1_stop_init-t1_start_init)/60,2)

    print('Initializations Process Time:',elapsed_time_init)

    total_elapsed_comp+=elapsed_time_init
    npv_counter_list=[]

    #CC Value Computation

    if 'STORM' in cc_node[0] or 'RES' in cc_node[0]:
        gen_price_sim = solar_pac_wesm_forecasts_supp_mid
        cc_price_sim = solar_pac_wesm_forecasts_cc_mid


    for run_no in range(1001):

        t1_start_comp = time.time()

        #merging datasets
        sim_run='Sim'+str(run_no)

        cc_price_sim_for_comp = cc_price_sim[['SolarPacSupplyID',sim_run]]
        cc_price_sim_for_comp = cc_price_sim_for_comp.rename(columns={sim_run:'Customer Price Sim'})

        #cc_price_sim_for_comp.to_excel('Test1.xlsx')

        gen_price_sim_for_comp = gen_price_sim[['SolarPacSupplyID',sim_run]]
        gen_price_sim_for_comp = gen_price_sim_for_comp.rename(columns={sim_run:'Gen Price Sim'})

        #gen_price_sim_for_comp.to_excel('Test2.xlsx')

        if 'STORM' in cc_node[0] and 'RES' in cc_node[0]:
            cc_load_sim_for_comp = cc_load_sim[['SolarPacSupplyID','Sim0']]
            cc_load_sim_for_comp = cc_load_sim_for_comp.rename(columns={'Sim0':'Load Sim'})
        else:
            cc_load_sim_for_comp = cc_load_sim[['SolarPacSupplyID',sim_run]]
            cc_load_sim_for_comp = cc_load_sim_for_comp.rename(columns={sim_run:'Load Sim'})

        cc_new_temp= cc_new.copy()
        cc_new_temp = cc_new_temp.merge(cc_price_sim_for_comp,on='SolarPacSupplyID',how='left')
        cc_new_temp = cc_new_temp.merge(gen_price_sim_for_comp,on='SolarPacSupplyID',how='left')

        cc_new_temp = cc_new_temp.merge(cc_load_sim_for_comp,on='SolarPacSupplyID',how='left')

        cc_final = cc_new_temp[['Date','Billing Month','Day','Billing Year','Hour','MonthCountID','Fixed Price','Customer Price Sim','Gen Price Sim','Load Sim']]

        #line rental
        cc_final['Line Rental'] = cc_final['Customer Price Sim'] - cc_final['Gen Price Sim']

        #final cashflow
        cc_final['Customer Price_for_Final_Cashflow']=cc_final['Customer Price Sim'].apply(lambda x:min(x,0))

        cc_final['Final_Cashflow_Counter1']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter1(x,cc_node))

        cc_final['Final_Cashflow_Counter2']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter2(x,cc_node))

        cc_final['Final_Cashflow_Counter3']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter3(x,cc_node))

        #if 'STORM' in cc_node[0] or 'RES' in cc_node[0]:
            #cc_final['Final_Cashflow1'] = ((cc_final['Fixed Price'])*(1-0.0075))*cc_final['Load Sim']
            #cc_final['Final_Cashflow2'] = [0]*len(cc_final)
            #cc_final['Final_Cashflow3'] = [0]*len(cc_final)
        #else:
        cc_final['Final_Cashflow1'] = ((cc_final['Fixed Price']+cc_final['Customer Price_for_Final_Cashflow'])*(1-0.0075) - cc_final['Gen Price Sim'])*cc_final['Load Sim']
        cc_final['Final_Cashflow2'] = ((cc_final['Fixed Price']+cc_final['Customer Price_for_Final_Cashflow'])*(1-0.0075) - cc_final['Gen Price Sim'] - [cc_node[12]]*len(cc_final))*cc_final['Load Sim']
        cc_final['Final_Cashflow3'] = ((cc_final['Fixed Price']+cc_final['Customer Price_for_Final_Cashflow'])*(1-0.0075) - cc_final['Customer Price Sim'])*cc_final['Load Sim']


        cc_final['Total']=((cc_final['Final_Cashflow_Counter1']*cc_final['Final_Cashflow1'])+(cc_final['Final_Cashflow_Counter2']*cc_final['Final_Cashflow2'])+(cc_final['Final_Cashflow_Counter3']*cc_final['Final_Cashflow3']))*0.75
        cc_final['Total']=list(cc_final['Total'])[:len(cc_final['Total'])-1]+[list(cc_final['Total'])[-1]+cc_node[14]]

        #cc_final['Total']=list(cc_final['Total'])[:len(cc_final['Total'])-1]+[list(cc_final['Total'])[-1]+2000000/3]

        #calendar_cc_conso = calendar_cc_conso.merge(cc_final[['Date','Total']],on='Date',how='left')

        #calendar_cc_conso = calendar_cc_conso.rename(columns={'Total':sim_run})

        days_until_today = start_cc-date_ref

        npv_cc =(cc_final['Total'] / (1+discount_rate/8760)**np.arange(1, len(cc_final['Total'])+1)).sum(axis=0)

        if days_until_today.days > 0:
            npv_cc = npv_cc/(1+discount_rate/8760)**days_until_today.days

        cc_final['NPV'] = cc_final['Total']/(1+discount_rate/8760)**days_until_today.days
        npv_db_original_gp=npv_db_original_gp.merge(cc_final[['Date','Total']],on='Date',how='left')
        npv_db_original_gp.columns=list(npv_db_original_gp.columns[:len(npv_db_original_gp.columns)-1])+['GP'+str(run_no)]
        npv_db_original_npv=npv_db_original_npv.merge(cc_final[['Date','NPV']],on='Date',how='left')
        npv_db_original_npv.columns=list(npv_db_original_npv.columns[:len(npv_db_original_npv.columns)-1])+['NPV'+str(run_no)]


        t1_stop_comp = time.time()
        elapsed_time_comp = round((t1_stop_comp-t1_start_comp)/60,2)

        results_list=[run_no, elapsed_time_comp, sim_run,
                      cc_node[0],

                      np.mean(cc_final['Customer Price Sim']),
                      np.mean(cc_final['Gen Price Sim']),
                      np.mean(cc_final['Line Rental']),
                                    np.max(cc_final['Load Sim']),
                                    np.mean(cc_final['Fixed Price']),

                                    cc_node[12],

                      npv_cc]

        df_cc_results.loc[run_no] = results_list

        npv_counter_list.append(npv_cc)

        # print(results_list, np.mean(npv_counter_list))


        total_elapsed_comp += elapsed_time_comp

    npv_db[cc_node[0]] = df_cc_results['Value']

    t1_start_finalizations = time.time()

    t1_stop_finalizations = time.time()

    elapsed_time_finalizations = round((t1_stop_finalizations-t1_start_finalizations)/60,2)

    total_elapsed_comp += elapsed_time_finalizations

    print('Total Process Time:',total_elapsed_comp)

hide_toggle('Customer Portfolio Valuation Function (>5 Years of Contract Term)')

def cc_portfolio_valuation_long(cc_num, date_ref, du="N", admin=0):

    if date_toggle!="NONE":
        new_customer_db = mod_db(customer_db,date_toggle)
    else:
        new_customer_db = customer_db

    cc_node = new_customer_db.iloc[int(cc_num)]

    date_today = datetime.datetime.today()
    date_today_reformat = date_today.strftime('%y%m%d')

    min_cap=-12000
    max_cap=34000
    discount_rate = 0.1214

    du_pass=0

    lbt=0.0075

    total_elapsed_comp=0

    df_cc_results=pd.DataFrame(columns=['Run','Process Time (Minutes)','SimID',
                                        'CC',
                                        'Average Customer Price',
                                        'Average Generator Price',
                                        'Average Line Rental',
                                        'Average Load',
                                        'Fixed Customer Price',

                                        'Line Rental Cap',
                                        'Value'])

    #upload price and load databases
    t1_start_initializations = time.time()

    sims_dict = load_sim(cc_num)
    cc_load_sim=sims_dict

    t1_stop_initializations = time.time()

    elapsed_time_initializations = round((t1_stop_initializations-t1_start_initializations)/60,2)

    #print('Uploading CC Load Database Process Time:',elapsed_time_initializations)
    total_elapsed_comp+=elapsed_time_initializations

    t1_start_init = time.time()

    #date calculations
    start_cc_from_db=datetime.datetime(cc_node[3],cc_node[1],cc_node[2])
    start_cc_today=datetime.datetime(date_today.year,date_today.month,date_today.day)

    start_cc=max(start_cc_from_db,start_cc_today)

    if date_toggle=="NONE":
        end_cc=datetime.datetime(cc_node[6],cc_node[4],cc_node[5])
    else:
        end_cc=min(datetime.datetime(cc_node[6],cc_node[4],cc_node[5]),datetime.datetime(date_toggle.year,date_toggle.month,date_toggle.day))

    calendar_cc = calendar_db.loc[(calendar_db['Date'] >= start_cc) & (calendar_db['Date'] < end_cc+datetime.timedelta(days=1))]

    calendar_cc_conso = calendar_cc.copy()
    calendar_cc_conso = calendar_cc_conso[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour']]

    cc_new = calendar_cc.reset_index(drop=True)
    fixed_cc = [cc_node[9]]*len(cc_new)

    onpeakoffpeak = []

    for i in range(len(cc_new)):
        if cc_new['Hour'][i] >= cc_node[7] and cc_new['Hour'][i] <= cc_node[8]:
            onpeakoffpeak.append(cc_node[10])
        else:
            onpeakoffpeak.append(cc_node[11])

    cc_new['Fixed Price'] = fixed_cc
    cc_new['On Peak/Off Peak Price'] = onpeakoffpeak

    t1_stop_init = time.time()
    elapsed_time_init = round((t1_stop_init-t1_start_init)/60,2)

    print('Initializations Process Time:',elapsed_time_init)

    total_elapsed_comp+=elapsed_time_init

    #Granular DB
    npv_db_original_gp=calendar_cc_conso.copy()
    npv_db_original_npv=calendar_cc_conso.copy()

    #CC Value Computation

    npv_counter_list=[]

    for run_no in range(1001):

        t1_start_comp = time.time()

        #merging datasets
        sim_run='Sim'+str(run_no)


        cc_load_sim_for_comp = cc_load_sim[['ID_Load',sim_run]]
        cc_load_sim_for_comp = cc_load_sim_for_comp.rename(columns={sim_run:'Load Sim'})

        cc_new_temp = cc_new.merge(solar_pac_wesm_forecasts_cc_mid[['Date',sim_run]],on="Date",how="left")
        cc_new_temp = cc_new_temp.rename(columns={sim_run:'Customer Price Sim'})
        cc_new_temp = cc_new_temp.merge(solar_pac_wesm_forecasts_supp_mid[['Date',sim_run]],on="Date", how="left")
        cc_new_temp = cc_new_temp.rename(columns={sim_run:'Gen Price Sim'})
        cc_new_temp = cc_new_temp.merge(cc_load_sim_for_comp,on="ID_Load", how="left")

        cc_final = cc_new_temp[['Date','Billing Month','Day','Billing Year','Hour','MonthCountID','Fixed Price','On Peak/Off Peak Price','Customer Price Sim','Gen Price Sim','Load Sim']]

        #line rental
        if du=="N":
            cc_final['Line Rental'] = cc_final['Customer Price Sim'] - cc_final['Gen Price Sim']
        else:
            cc_final['Line Rental'] = [0]*len(cc_final)

        cc_final['Admin Fee']=[admin]*len(cc_final)

        #computation
        cc_final['Customer Price_for_Final_Cashflow']=cc_final.apply(lambda x:min(x['On Peak/Off Peak Price'],x['Customer Price Sim']),axis=1)

        cc_final['LR_Fee_Counter1']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter1(x,cc_node))

        cc_final['LR_Fee_Counter2']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter2(x,cc_node))

        cc_final['LR_Fee_Counter3']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter3(x,cc_node))

        cc_final['LR_Fee1'] = cc_final['Line Rental']*cc_final['Load Sim']

        cc_final['LR_Fee2'] = (cc_final['Line Rental']-cc_node[12]*(len(cc_final)))*cc_final['Load Sim']

        cc_final['LR_Fee3'] = [0]*len(cc_final)

        cc_final['Line Rental Fee'] = (cc_final['LR_Fee_Counter1']*cc_final['LR_Fee1'])+(cc_final['LR_Fee_Counter2']*cc_final['LR_Fee2'])+(cc_final['LR_Fee_Counter3']*cc_final['LR_Fee3'])

        cc_final['Generation Fee'] = ((cc_final['Fixed Price']+cc_final['Admin Fee'])*cc_final['Load Sim'])+cc_final['Customer Price_for_Final_Cashflow']*cc_final['Load Sim']

        cc_final['DU Passthrough Charges'] = du_pass*cc_final['Load Sim']

        #cc_final['DU Passthrough Charges'] = 0

        cc_final_with_monthly_fee = pd.DataFrame()

        #monthly peak load

        month_count_id_unique_keys = list(cc_new['MonthCountID'].unique())

        for month_count_element in month_count_id_unique_keys:
            cc_final_sub = cc_final.loc[cc_new['MonthCountID'] == month_count_element]
            maxload_month = np.max(cc_final_sub['Load Sim'])
            cc_final_sub['Monthly Fee'] =(max(1.9,maxload_month)*cc_node[13]*1000/len(cc_final_sub))

            cc_final_sub['Local Business Tax']=(cc_final_sub['Generation Fee']+cc_final_sub['Monthly Fee']+cc_final['DU Passthrough Charges'])*-lbt
            cc_final_sub['Purchase Power'] = -cc_final_sub['Load Sim']*cc_final_sub['Customer Price Sim']

            cc_final_sub['Total']=cc_final_sub['Generation Fee']+cc_final_sub['Monthly Fee']+cc_final_sub['Line Rental Fee']+cc_final_sub['Purchase Power']+cc_final_sub['Local Business Tax']-cc_final_sub['DU Passthrough Charges']

            cc_final_with_monthly_fee = cc_final_with_monthly_fee.append(cc_final_sub,ignore_index=True)

        cc_final = cc_final_with_monthly_fee.sort_values(by=['Date'])

        cc_final['Total']=list(cc_final['Total'])[:len(cc_final['Total'])-1]+[list(cc_final['Total'])[-1]+cc_node[14]]

        #Granular DB
        cc_final.reset_index(inplace=True)
        cc_final['NPV'] = cc_final['Total'] / (1+discount_rate/8760)**cc_final['index']


        #calendar_cc_conso = calendar_cc_conso.merge(cc_final[['Date','Total']],on='Date',how='left')

        #calendar_cc_conso = calendar_cc_conso.rename(columns={'Total':sim_run})

        days_until_today = start_cc-date_ref

        npv_cc =(cc_final['Total'] / (1+discount_rate/8760)**np.arange(1, len(cc_final['Total'])+1)).sum(axis=0)

        if days_until_today.days > 0:
            npv_cc = npv_cc/(1+discount_rate/8760)**days_until_today.days


        #Granular DB
        cc_final['NPV'] = cc_final['NPV']/(1+discount_rate/len(cc_final['Total']))**days_until_today.days

        npv_db_original_gp=npv_db_original_gp.merge(cc_final[['Date','Total']],on='Date',how='left')
        npv_db_original_gp.columns=list(npv_db_original_gp.columns[:len(npv_db_original_gp.columns)-1])+['GP'+str(run_no)]



        npv_db_original_npv=npv_db_original_npv.merge(cc_final[['Date','NPV']],on='Date',how='left')
        npv_db_original_npv.columns=list(npv_db_original_npv.columns[:len(npv_db_original_npv.columns)-1])+['NPV'+str(run_no)]


        t1_stop_comp = time.time()
        elapsed_time_comp = round((t1_stop_comp-t1_start_comp)/60,2)

        results_list=[run_no, elapsed_time_comp, sim_run,
                    cc_node[0],

                     np.mean(cc_final['Customer Price Sim']),
                    np.mean(cc_final['Gen Price Sim']),
                    np.mean(cc_final['Line Rental']),
                                   np.mean(cc_final['Load Sim']),
                                   cc_node[9],

                                  cc_node[12],

                     npv_cc]
        df_cc_results.loc[run_no] = results_list

        npv_counter_list.append(npv_cc)

        # print(results_list,np.mean(npv_counter_list))

    t1_start_finalizations = time.time()

    #calendar_cc_conso_dup = calendar_cc_conso.iloc[:,1:]

    #calendar_cc_conso[cc_node[0]] = calendar_cc_conso_dup.mean(axis=1)

    #calendar_cc_conso=calendar_cc_conso[['Date',cc_node[0]]]

    npv_db[cc_node[0]] = df_cc_results['Value']

    #df_cc_results.to_sql(name_of_file+' CC Valuation',sqlEngine, if_exists='replace', index=False)

    t1_stop_finalizations = time.time()

    elapsed_time_finalizations = round((t1_stop_finalizations-t1_start_finalizations)/60,2)

    total_elapsed_comp += elapsed_time_finalizations

    print('Total Process Time:',total_elapsed_comp)


    #return calendar_cc_conso

hide_toggle('CC Portfolio Valuation Function (Long)')


def cc_portfolio_valuation_short(cc_num, date_ref, du="N", admin=0):

    if date_toggle!="NONE":
        new_customer_db = mod_db(customer_db,date_toggle)
    else:
        new_customer_db = customer_db

    cc_node = new_customer_db.iloc[int(cc_num)]

    date_today = datetime.datetime.today()
    date_today_reformat = date_today.strftime('%y%m%d')

    min_cap=-12000
    max_cap=34000
    discount_rate = 0.1214

    du_pass=0

    lbt=0.0075

    total_elapsed_comp=0

    df_cc_results=pd.DataFrame(columns=['Run','Process Time (Minutes)','SimID',
                                        'CC',
                                        'Average Customer Price',
                                        'Average Generator Price',
                                        'Average Line Rental',
                                        'Average Load',
                                        'Fixed Customer Price',
                                        'Line Rental Cap',
                                        'Value'])

    #upload price and load databases
    t1_start_initializations = time.time()

    sims_dict = load_sim(cc_num)
    cc_load_sim=sims_dict

    t1_stop_initializations = time.time()

    elapsed_time_initializations = round((t1_stop_initializations-t1_start_initializations)/60,2)

    total_elapsed_comp+=elapsed_time_initializations

    t1_start_init = time.time()

    #date calculations
    start_cc_from_db=datetime.datetime(cc_node[3],cc_node[1],cc_node[2])
    start_cc_today=datetime.datetime(date_today.year,date_today.month,date_today.day)

    start_cc=max(start_cc_from_db,start_cc_today)

    if date_toggle=="NONE":
        end_cc=datetime.datetime(cc_node[6],cc_node[4],cc_node[5])
    else:
        end_cc=min(datetime.datetime(cc_node[6],cc_node[4],cc_node[5]),datetime.datetime(date_toggle.year,date_toggle.month,date_toggle.day))

    calendar_cc = calendar_db.loc[(calendar_db['Date'] >= start_cc) & (calendar_db['Date'] < end_cc+datetime.timedelta(days=1))]

    calendar_cc_conso = calendar_cc.copy()
    calendar_cc_conso = calendar_cc_conso[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour']]

    #Granular DB
    npv_db_original_gp=calendar_cc_conso.copy()
    npv_db_original_npv=calendar_cc_conso.copy()

    cc_new = calendar_cc.reset_index(drop=True)
    fixed_cc = [cc_node[9]]*len(cc_new)

    cc_new['Fixed Price'] = fixed_cc

    t1_stop_init = time.time()
    elapsed_time_init = round((t1_stop_init-t1_start_init)/60,2)

    print('Initializations Process Time:',elapsed_time_init)

    total_elapsed_comp+=elapsed_time_init

    #CC Value Computation

    npv_counter_list=[]

    for run_no in range(1001):

        t1_start_comp = time.time()

        #merging datasets
        sim_run='Sim'+str(run_no)

        #cc_price_sim_for_comp = cc_price_sim[['ID',sim_run]]
        #cc_price_sim_for_comp = cc_price_sim_for_comp.rename(columns={sim_run:'Customer Price Sim'})

        #gen_price_sim_for_comp = gen_price_sim[['ID',sim_run]]
        #gen_price_sim_for_comp = gen_price_sim_for_comp.rename(columns={sim_run:'Gen Price Sim'})

        cc_load_sim_for_comp = cc_load_sim[['ID_Load',sim_run]]
        cc_load_sim_for_comp = cc_load_sim_for_comp.rename(columns={sim_run:'Load Sim'})

        cc_new_temp = cc_new.merge(solar_pac_wesm_forecasts_cc_mid[['Date',sim_run]],on="Date",how="left")
        cc_new_temp = cc_new_temp.rename(columns={sim_run:'Customer Price Sim'})
        cc_new_temp = cc_new_temp.merge(solar_pac_wesm_forecasts_supp_mid[['Date',sim_run]],on="Date", how="left")
        cc_new_temp = cc_new_temp.rename(columns={sim_run:'Gen Price Sim'})
        cc_new_temp = cc_new_temp.merge(cc_load_sim_for_comp,on="ID_Load", how="left")

        cc_final = cc_new_temp[['Date','Billing Month','Day','Billing Year','Hour','MonthCountID','Fixed Price','Customer Price Sim','Gen Price Sim','Load Sim']]

        #line rental
        if du=="N":
            cc_final['Line Rental'] = cc_final['Customer Price Sim'] - cc_final['Gen Price Sim']
        else:
            cc_final['Line Rental'] = [0]*len(cc_final)

        cc_final['Admin Fee']=[admin]*len(cc_final)

        #cc_final['DU Passthrough Charges'] = 1.55*cc_final['Load Sim']
        #cc_final['DU Passthrough Charges'] = -0

        #final cashflow
        cc_final['Customer Price_for_Final_Cashflow']=cc_final['Customer Price Sim'].apply(lambda x:min(x,0))

        cc_final['Final_Cashflow_Counter1']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter1(x,cc_node))

        cc_final['Final_Cashflow_Counter2']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter2(x,cc_node))

        cc_final['Final_Cashflow_Counter3']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter3(x,cc_node))

        cc_final['Final_Cashflow1'] = ((cc_final['Fixed Price']+cc_final['Admin Fee']+cc_final['Customer Price_for_Final_Cashflow']+[du_pass]*len(cc_final))*(1-lbt) - cc_final['Gen Price Sim']-[du_pass]*len(cc_final))*cc_final['Load Sim']

        cc_final['Final_Cashflow2'] = ((cc_final['Fixed Price']+cc_final['Admin Fee']+cc_final['Customer Price_for_Final_Cashflow']+[du_pass]*len(cc_final))*(1-lbt) - cc_final['Gen Price Sim'] - [cc_node[12]]*len(cc_final) -[du_pass]*len(cc_final))*cc_final['Load Sim']

        cc_final['Final_Cashflow3'] = ((cc_final['Fixed Price']+cc_final['Admin Fee']+cc_final['Customer Price_for_Final_Cashflow']+[du_pass]*len(cc_final))*(1-lbt) - cc_final['Customer Price Sim']-[du_pass]*len(cc_final))*cc_final['Load Sim']

        cc_final['Total']=(cc_final['Final_Cashflow_Counter1']*cc_final['Final_Cashflow1'])+(cc_final['Final_Cashflow_Counter2']*cc_final['Final_Cashflow2'])+(cc_final['Final_Cashflow_Counter3']*cc_final['Final_Cashflow3'])

        cc_final['Total']=list(cc_final['Total'])[:len(cc_final['Total'])-1]+[list(cc_final['Total'])[-1]+cc_node[14]]

        #Granular DB
        cc_final.reset_index(inplace=True)
        cc_final['NPV'] = cc_final['Total'] / (1+discount_rate/8760)**cc_final['index']


        #calendar_cc_conso = calendar_cc_conso.merge(cc_final[['Date','Total']],on='Date',how='left')

        #calendar_cc_conso = calendar_cc_conso.rename(columns={'Total':sim_run})

        days_until_today = start_cc-date_ref

        npv_cc =(cc_final['Total'] / (1+discount_rate/8760)**np.arange(1, len(cc_final['Total'])+1)).sum(axis=0)

        if days_until_today.days > 0:
            npv_cc = npv_cc/(1+discount_rate/8760)**days_until_today.days


        #Granular DB
        cc_final['NPV'] = cc_final['NPV']/(1+discount_rate/len(cc_final['Total']))**days_until_today.days
        npv_db_original_gp=npv_db_original_gp.merge(cc_final[['Date','Total']],on='Date',how='left')
        npv_db_original_gp.columns=list(npv_db_original_gp.columns[:len(npv_db_original_gp.columns)-1])+['GP'+str(run_no)]



        npv_db_original_npv=npv_db_original_npv.merge(cc_final[['Date','NPV']],on='Date',how='left')
        npv_db_original_npv.columns=list(npv_db_original_npv.columns[:len(npv_db_original_npv.columns)-1])+['NPV'+str(run_no)]



        t1_stop_comp = time.time()
        elapsed_time_comp = round((t1_stop_comp-t1_start_comp)/60,2)

        results_list=[run_no, elapsed_time_comp, sim_run,
                      cc_node[0],

                      np.mean(cc_final['Customer Price Sim']),
                      np.mean(cc_final['Gen Price Sim']),
                      np.mean(cc_final['Line Rental']),
                                    np.mean(cc_final['Load Sim']),
                                    cc_node[9],
                                    cc_node[12],

                      npv_cc]

        df_cc_results.loc[run_no] = results_list

        npv_counter_list.append(npv_cc)

        # print(results_list,np.mean(npv_counter_list))

        total_elapsed_comp += elapsed_time_comp

    t1_start_finalizations = time.time()

    #calendar_cc_conso_dup = calendar_cc_conso.iloc[:,1:]

    #calendar_cc_conso[cc_node[0]] = calendar_cc_conso_dup.mean(axis=1)

    #calendar_cc_conso=calendar_cc_conso[['Date',cc_node[0]]]

    npv_db[cc_node[0]] = df_cc_results['Value']

    #df_cc_results.to_sql(name_of_file+' CC Valuation',sqlEngine, if_exists='replace', index=False)

    t1_stop_finalizations = time.time()

    elapsed_time_finalizations = round((t1_stop_finalizations-t1_start_finalizations)/60,2)

    total_elapsed_comp += elapsed_time_finalizations

    print('Total Process Time:',total_elapsed_comp)


    #return calendar_cc_conso


hide_toggle('CC Portfolio Valuation Function (Short)')

def cc_portfolio_valuation(cc_num, date_ref, du_cc="N", admin_cc=0):

    cc_node = customer_db.iloc[int(cc_num)]

    if cc_node[10] == 0 and cc_node[11] == 0 and cc_node[13] == 0:
        return cc_portfolio_valuation_short(cc_num, date_ref,du=du_cc,admin=admin_cc)
    else:
        return cc_portfolio_valuation_long(cc_num, date_ref,du=du_cc,admin=admin_cc)

hide_toggle('CC Portfolio Valuation Function')


def wesm_plus(cc_num,gross_up_margin,date_ref):

    if date_toggle!="NONE":
        new_customer_db = mod_db(customer_db,date_toggle)
    else:
        new_customer_db = customer_db

    cc_node = new_customer_db.iloc[int(cc_num)]

    date_today = date_ref
    date_today_reformat = date_today.strftime('%y%m%d')

    min_cap=-12000
    max_cap=34000
    discount_rate = 0.1214

    du_pass=0

    lbt=0.0077

    total_elapsed_comp=0

    df_cc_results=pd.DataFrame(columns=['Run','Process Time (Minutes)','SimID',
                                        'CC',
                                        'Average Customer Price',
                                        'Average Generator Price',
                                        'Average Line Rental',
                                        'Average Load',
                                        'Fixed Customer Price',
                                        'Line Rental Cap',
                                        'Value'])

    #upload price and load databases
    t1_start_initializations = time.time()

    sims_dict = load_sim(cc_num)
    cc_load_sim=sims_dict

    t1_stop_initializations = time.time()

    elapsed_time_initializations = round((t1_stop_initializations-t1_start_initializations)/60,2)

    #print('Uploading CC Load Database Process Time:',elapsed_time_initializations)
    total_elapsed_comp+=elapsed_time_initializations

    t1_start_init = time.time()

    #date calculations
    start_cc_from_db=datetime.datetime(cc_node[3],cc_node[1],cc_node[2])
    start_cc_today=datetime.datetime(date_today.year,date_today.month,date_today.day)

    start_cc=max(start_cc_from_db,start_cc_today)

    if date_toggle=="NONE":
        end_cc=datetime.datetime(cc_node[6],cc_node[4],cc_node[5])
    else:
        end_cc=min(datetime.datetime(cc_node[6],cc_node[4],cc_node[5]),datetime.datetime(date_toggle.year,date_toggle.month,date_toggle.day))

    date_delta = end_cc-start_cc

    calendar_cc = calendar_db.loc[(calendar_db['Date'] >= start_cc) & (calendar_db['Date'] < end_cc+datetime.timedelta(days=1))]

    calendar_cc_conso = calendar_cc.copy()
    calendar_cc_conso = calendar_cc_conso[['Date']]

    cc_new = calendar_cc.reset_index(drop=True)
    fixed_cc = [cc_node[9]]*len(cc_new)

    onpeakoffpeak = []

    for i in range(len(cc_new)):
        if cc_new['Hour'][i] >= cc_node[7] and cc_new['Hour'][i] <= cc_node[8]:
            onpeakoffpeak.append(cc_node[10])
        else:
            onpeakoffpeak.append(cc_node[11])

    cc_new['Fixed Price'] = fixed_cc
    cc_new['On Peak/Off Peak Price'] = onpeakoffpeak

    t1_stop_init = time.time()
    elapsed_time_init = round((t1_stop_init-t1_start_init)/60,2)

    #print('Initializations Process Time:',elapsed_time_init)

    total_elapsed_comp+=elapsed_time_init

    #CC Value Computation

    average_mw=[]

    #Granular DB
    npv_db_original_gp=calendar_cc_conso.copy()
    npv_db_original_npv=calendar_cc_conso.copy()

    npv_cc_list=[]

    for run_no in range(1001):

        t1_start_comp = time.time()

        #merging datasets
        sim_run='Sim'+str(run_no)

        cc_load_sim_for_comp = cc_load_sim[['ID_Load',sim_run]]
        cc_load_sim_for_comp = cc_load_sim_for_comp.rename(columns={sim_run:'Load Sim'})
        cc_new_temp = cc_new.merge(cc_load_sim_for_comp,on="ID_Load", how="left")
        cc_new_temp=cc_new_temp[['Date','Billing Month','Day','Billing Year','Hour','MonthCountID','Load Sim']]

        #Granular DB
        cc_final = cc_new_temp[['Date','Billing Month','Day','Billing Year','Hour','MonthCountID','Load Sim']]
        cc_final['Total CORE Margin']=cc_final['Load Sim']*gross_up_margin
        cc_final.reset_index(inplace=True)
        days_until_today = start_cc-date_today

        npv_cc =(cc_final['Total CORE Margin'] / (1+discount_rate/8760)**np.arange(1, len(cc_final['Total CORE Margin'])+1)).sum(axis=0)

        if days_until_today.days > 0:
            npv_cc = npv_cc/(1+discount_rate/8760)**days_until_today.days

        npv_cc_list.append(npv_cc)

        #Granular DB
        cc_final['NPV'] = cc_final['Total CORE Margin']/(1+discount_rate/len(cc_final['Total CORE Margin']))**days_until_today.days
        npv_db_original_gp=npv_db_original_gp.merge(cc_final[['Date','Total CORE Margin']],on='Date',how='left')
        npv_db_original_gp.columns=list(npv_db_original_gp.columns[:len(npv_db_original_gp.columns)-1])+['GP'+str(run_no)]
        npv_db_original_npv=npv_db_original_npv.merge(cc_final[['Date','NPV']],on='Date',how='left')
        npv_db_original_npv.columns=list(npv_db_original_npv.columns[:len(npv_db_original_npv.columns)-1])+['NPV'+str(run_no)]


        #calendar_cc_conso = calendar_cc_conso.merge(cc_final[['Date','Total']],on='Date',how='left')

        #calendar_cc_conso = calendar_cc_conso.rename(columns={'Total':sim_run})




        average_mw.append(np.mean(cc_new_temp['Load Sim']))

    sim_of_min_index=average_mw.index(min(average_mw))
    sim_of_min = 'Sim'+str(sim_of_min_index)

    cc_load_sim_min_for_comp = cc_load_sim[['ID_Load',sim_of_min]]
    cc_load_sim_min_for_comp = cc_load_sim_min_for_comp.rename(columns={sim_of_min:'Load Sim'})
    cc_new_temp_min = cc_new.merge(cc_load_sim_min_for_comp,on="ID_Load", how="left")

    #return cc_new_temp_min

    cc_final = cc_new_temp_min[['Date','Billing Month','Day','Billing Year','Hour','MonthCountID','Load Sim']]

    #print('Done Final!')

    gross_up_margin_list=[]
    core_margin_list=[]
    ave_core_margin_list=[]


    while gross_up_margin >= 0:
        #print(gross_up_margin)
        gross_up_margin_list.append("₱{:,.3f}/kWh".format(gross_up_margin/1000))
        cc_final['Total CORE Margin']=cc_final['Load Sim']*gross_up_margin
        core_margin_list.append("₱{:,.2f}".format(np.sum(cc_final['Total CORE Margin'])))
        ave_core_margin_list.append("₱{:,.2f}".format(np.sum(cc_final['Total CORE Margin'])/((date_delta.days+1)*12/365)))

        gross_up_margin=gross_up_margin-25

        if gross_up_margin<0:
            break

    customer_pd = pd.DataFrame()

    customer_pd[' ']=['Customer','Lowest Possible Average Load','Duration']
    customer_pd['Information']=[cc_node[0],"{:,.2f} MW".format(min(average_mw))," {:,.1f} Months".format((date_delta.days+1)*12/365)]


    discount_pd = pd.DataFrame()

    discount_pd['Admin Charges']=gross_up_margin_list
    discount_pd['Total CORE Margin'] = core_margin_list
    discount_pd['Average CORE Margin per Month'] = ave_core_margin_list

    results_dict = dict()

    results_dict['Contract Information'] = customer_pd
    results_dict['Offers'] = discount_pd

    #return results_dict

    #Granular DB
    simulations_dict = dict()

    simulations_dict['GP']=npv_db_original_gp
    simulations_dict['NPV']=npv_db_original_npv

    npv_db[cc_node[0]] = npv_cc_list


    return simulations_dict


hide_toggle('WESM Plus Contract Valuation')

"""## Function for getting Cashflow"""

# def supplier_portfolio_valuation(supp_num, date_ref,price_cap1=0,profit_share_per1=0,price_cap2=0,profit_share_per2=0):

#     if date_toggle!="NONE":
#         new_supplier_db = mod_db(supplier_db,date_toggle)
#     else:
#         new_supplier_db = supplier_db

#     #return new_supplier_db

# #     if supp_num >= len(supplier_db):
# #         print("Invalid supp_num. Maximum supp_num should be", len(supplier_db) - 1)
# #         return

#     supplier_node = new_supplier_db.iloc[int(supp_num)]

#     date_today = datetime.datetime.today()
#     date_today_reformat = date_today.strftime('%y%m%d')

#     min_cap=-12000
#     max_cap=34000
#     discount_rate = 0.1214

#     total_elapsed_comp=0

#     df_supplier_results=pd.DataFrame(columns=['Run','Process Time (Minutes)','SimID',

#                                               'Supplier',

#                                               'Average Customer Price',
#                                         'Average Generator Price',
#                                         'Average Line Rental',


#                                               'Fixed Customer Price',

#                                         'Fixed Supplier Price',
#                                         'Line Rental Cap',
#                                               'Value'])
#     #upload price and load databases

#     t1_start_initializations = time.time()


#     cc_price_sim=solar_pac_wesm_forecasts_cc_mid
#     gen_price_sim=solar_pac_wesm_forecasts_supp_mid

#     supp_name_for_sim = supplier_node[0]

#     if 'ANDA' in supplier_node[0]:

#         supp_load_db=solar_pac_load_profiles[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#            'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID',
#            'SolarPacSupplyID',  supplier_node[0],'ANDA (Profit Sharing)']]

#     else:

#         supp_load_db=solar_pac_load_profiles[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#            'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID',
#            'SolarPacSupplyID',  supplier_node[0]]]




#     t1_stop_initializations = time.time()

#     elapsed_time_initializations = round((t1_stop_initializations-t1_start_initializations)/60,2)

#     #print('Uploading CC Load Database Process Time:',elapsed_time_initializations)
#     total_elapsed_comp+=elapsed_time_initializations

#     t1_start_init_supp = time.time()

#     #date calculations
#     start_supp_from_db=datetime.datetime(supplier_node[3],supplier_node[1],supplier_node[2])
#     start_supp_today=datetime.datetime(date_today.year,date_today.month,date_today.day)

#     start_supp=max(start_supp_from_db,start_supp_today)

#     if date_toggle=="NONE":
#         end_supp=datetime.datetime(supplier_node[6],supplier_node[4],supplier_node[5])
#     else:
#         end_supp=min(datetime.datetime(supplier_node[6],supplier_node[4],supplier_node[5]),datetime.datetime(date_toggle.year,date_toggle.month,date_toggle.day))

#     calendar_supp = calendar_db.loc[(calendar_db['Date'] >= start_supp) & (calendar_db['Date'] < end_supp+datetime.timedelta(days=1))]

#     calendar_supp_conso = calendar_supp.copy()
#     calendar_supp_conso = calendar_supp_conso[['Date']]

#     #Granular DB
#     npv_db_original_gp=calendar_supp_conso.copy()
#     npv_db_original_npv=calendar_supp_conso.copy()

#     supplier_new = calendar_supp.reset_index(drop=True)

#     #filtering the three dbs

#     cc_price_sim = cc_price_sim.loc[(cc_price_sim['Date'] >= start_supp) & (cc_price_sim['Date'] < end_supp+datetime.timedelta(days=1))]
#     cc_price_sim = cc_price_sim.reset_index(drop=True)
#     gen_price_sim = gen_price_sim.loc[(gen_price_sim['Date'] >= start_supp) & (gen_price_sim['Date'] < end_supp+datetime.timedelta(days=1))]
#     gen_price_sim =gen_price_sim.reset_index(drop=True)
#     supp_load_db = supp_load_db.loc[(supp_load_db['Date'] >= start_supp) & (supp_load_db['Date'] < end_supp+datetime.timedelta(days=1))]
#     supp_load_db =supp_load_db.reset_index(drop=True)
#     #creating supplier columns

#     fixed_supplier = [supplier_node[7]]*len(supplier_new)
#     capacity_supplier = [supplier_node[8]]*len(supplier_new)
#     variable_supplier = [supplier_node[9]]*len(supplier_new)


#     supplier_new['Fixed Price'] = fixed_supplier

#     supplier_new['Capacity Fee'] = capacity_supplier
#     supplier_new['Variable Fee'] = variable_supplier

#     t1_stop_init_supp = time.time()
#     elapsed_time_init_supp = round((t1_stop_init_supp-t1_start_init_supp)/60,2)

#     print('Initializations Process Time:',elapsed_time_init_supp)

#     total_elapsed_comp+=elapsed_time_init_supp

#     npv_counter_list=[]

#     for run_no_supp in range(1): # changed from 1001 to 1

#         t1_start_supp = time.time()

#         #merging datasets
#         sim_run_supp='Sim'+str(run_no_supp)

#         cc_price_sim_for_supp_comp = cc_price_sim[['ID',sim_run_supp]]
#         cc_price_sim_for_supp_comp = cc_price_sim_for_supp_comp.rename(columns={sim_run_supp:'Customer Price Sim'})

#         gen_price_sim_for_supp_comp = gen_price_sim[['ID',sim_run_supp]]
#         gen_price_sim_for_supp_comp = gen_price_sim_for_supp_comp.rename(columns={sim_run_supp:'Gen Price Sim'})

#         if 'MAGAT' in str(supplier_node[0]):
#             gen_load_for_comp = supp_load_db[['ID_Load']]
#             gen_load_for_comp['MAGAT']=[10]*len(gen_load_for_comp)
#         elif 'ANDA' in str(supplier_node[0]):
#             gen_load_for_comp = supp_load_db[['ID_Load',supp_name_for_sim,'ANDA (Profit Sharing)']]

#         else:
#             gen_load_for_comp = supp_load_db[['ID_Load',supp_name_for_sim]]

#         supplier_new_temp = supplier_new.copy()
#         supplier_new_temp['Customer Price Sim'] = cc_price_sim_for_supp_comp['Customer Price Sim']
#         supplier_new_temp['Gen Price Sim'] = gen_price_sim_for_supp_comp['Gen Price Sim']
#         supplier_new_temp[supp_name_for_sim] = gen_load_for_comp[supp_name_for_sim]
#         supplier_new_temp = supplier_new_temp.rename(columns={supp_name_for_sim:'Load'})

#         if 'ANDA' in str(supplier_node[0]):
#             supplier_new_temp['ANDA (Profit Sharing)'] = gen_load_for_comp['ANDA (Profit Sharing)']

#         if 'ANDA' in str(supplier_node[0]):
#             supplier_final = supplier_new_temp[['Date','Billing Month','Billing Year','Day','Hour','Fixed Price','Capacity Fee','Variable Fee','Customer Price Sim','Gen Price Sim','Load','ANDA (Profit Sharing)']]
#         else:
#             supplier_final = supplier_new_temp[['Date','Billing Month','Billing Year','Day','Hour','Fixed Price','Capacity Fee','Variable Fee','Customer Price Sim','Gen Price Sim','Load']]

#         #supplier line rental
#         supplier_final['Line Rental'] = supplier_final['Customer Price Sim'] - supplier_final['Gen Price Sim']

#         supplier_final['LRFee_Counter1']= supplier_final['Line Rental'].apply(lambda x:final_cashflow_counter_supp1(x,supplier_node))

#         supplier_final['LRFee_Counter2']= supplier_final['Line Rental'].apply(lambda x:final_cashflow_counter_supp2(x,supplier_node))

#         supplier_final['LRFee_Counter3']= supplier_final['Line Rental'].apply(lambda x:final_cashflow_counter_supp3(x,supplier_node))

#         supplier_final['LRFee1'] = [0]*len(supplier_final)

#         supplier_final['LRFee2'] = -supplier_final['Line Rental']*supplier_final['Load']

#         supplier_final['LRFee3'] = supplier_final['LRFee1']

#         supplier_final['Line Rental Fee']=(supplier_final['LRFee_Counter1']*supplier_final['LRFee1'])+(supplier_final['LRFee_Counter2']*supplier_final['LRFee2'])+(supplier_final['LRFee_Counter3']*supplier_final['LRFee3'])

#         #supplier computation
#         supplier_final['WESM Sales']=supplier_final['Load']*supplier_final['Customer Price Sim']

#         supplier_final['Generation Fee'] = -(supplier_final['Fixed Price']+
#                                                 supplier_final['Capacity Fee']+
#                                                 supplier_final['Variable Fee'])*supplier_final['Load']

#         list_othercosts = ([np.max(supplier_final['Load'])*31*24*supplier_node[7]*1.12*0.0075]+[0]*(365*24))*relativedelta(end_supp,start_supp_from_db).years+[0]*(len(supplier_final)-len(([np.max(supplier_final['Load'])*31*24*supplier_node[7]*1.12*0.0075]+[0]*(365*24))*relativedelta(end_supp,start_supp_from_db).years))

#         supplier_final['Other Costs']=list_othercosts[:len(supplier_final)]


#         if 'ANDA' in str(supplier_node[0]):
#             supplier_final['Price Cap1']=[price_cap1]*len(supplier_final)
#             supplier_final['Price Cap2']=[price_cap2]*len(supplier_final)
#             supplier_final['Difference2']=supplier_final['Customer Price Sim']-supplier_final['Price Cap2']
#             supplier_final['Profit Share2']=supplier_final['Difference2'].apply(lambda x:pos_neg_dif(x))*supplier_final['ANDA (Profit Sharing)']*profit_share_per2

#             supplier_final['Difference1']=supplier_final['Customer Price Sim']-supplier_final['Price Cap1']
#             supplier_final['Profit Share1']=supplier_final.apply(lambda x:pos_neg_dif_two_val(x['Difference2'],x['Difference1']), axis=1)*supplier_final['ANDA (Profit Sharing)']*profit_share_per1

#             supplier_final['Total']=(-supplier_final['Other Costs']+supplier_final['Generation Fee']+supplier_final['Line Rental Fee']+supplier_final['WESM Sales']-supplier_final['Profit Share2']-supplier_final['Profit Share1'])*0.75

#         #elif 'STORM' in str(supplier_node[0]) or 'RES' in str(supplier_node[0]):
#             #supplier_final['Total']=-supplier_final['Other Costs']+supplier_final['Generation Fee']


#         else:
#             supplier_final['Total']=(-supplier_final['Other Costs']+supplier_final['Generation Fee']+supplier_final['Line Rental Fee']+supplier_final['WESM Sales'])*0.75

#         #calendar_supp_conso = calendar_supp_conso.merge(supplier_final[['Date','Total']],on='Date',how='left')

#         #calendar_supp_conso = calendar_supp_conso.rename(columns={'Total':sim_run_supp})

#         days_until_today = start_supp-date_ref

#         npv_supplier = (supplier_final['Total'] / (1+discount_rate/8760)**np.arange(1, len(supplier_final['Total'])+1)).sum(axis=0)

#         if days_until_today.days > 0:
#             npv_supplier = npv_supplier/(1+discount_rate/8760)**days_until_today.days

#         supplier_final['NPV'] = supplier_final['Total']/(1+discount_rate/8760)**days_until_today.days
#         npv_db_original_gp=npv_db_original_gp.merge(supplier_final[['Date','Total']],on='Date',how='left')
#         npv_db_original_gp.columns=list(npv_db_original_gp.columns[:len(npv_db_original_gp.columns)-1])+['GP'+str(run_no_supp)]
#         npv_db_original_npv=npv_db_original_npv.merge(supplier_final[['Date','NPV']],on='Date',how='left')
#         npv_db_original_npv.columns=list(npv_db_original_npv.columns[:len(npv_db_original_npv.columns)-1])+['NPV'+str(run_no_supp)]

#         t1_stop_supp = time.time()
#         elapsed_time_supp = round((t1_stop_supp-t1_start_supp)/60,2)


#         results_list=[run_no_supp, elapsed_time_supp, sim_run_supp,supplier_node[0],
#                       np.mean(supplier_final['Customer Price Sim']),
#                           np.mean(supplier_final['Gen Price Sim']),
#                           np.mean(supplier_final['Line Rental']),
#                                         np.max(supplier_final['Load']),

#                                         supplier_node[7],
#                                         supplier_node[10],
#                       npv_supplier]

#         df_supplier_results.loc[run_no_supp] = results_list

#         npv_counter_list.append(npv_supplier)

#         # print(results_list, np.mean(npv_counter_list))


#         total_elapsed_comp += elapsed_time_supp

#     t1_start_finalizations = time.time()

#     #calendar_supp_conso_dup = calendar_supp_conso.iloc[:,1:]

#     #calendar_supp_conso[supplier_node[0]] = calendar_supp_conso_dup.mean(axis=1)

#     #calendar_supp_conso=calendar_supp_conso[['Date',supplier_node[0]]]

#     # npv_db[supplier_node[0]] = df_supplier_results['Value'] #CHANGEDDD

#     #df_supplier_results.to_sql(name_of_file+' Supplier Valuation',sqlEngine, if_exists='replace', index=False)

#     supplier_final.to_excel(f'{supplier_db.iloc[supp_num].SupplierName}.xlsx',index=False)

#     t1_stop_finalizations = time.time()

#     elapsed_time_finalizations = round((t1_stop_finalizations-t1_start_finalizations)/60,2)

#     total_elapsed_comp += elapsed_time_finalizations

#     print('Total Process Time:',total_elapsed_comp)


# hide_toggle('Supplier Portfolio Valuation Function')



# def customer_portfolio_valuation_long_term(cc_num,date_ref):

#     if date_toggle!="NONE":
#         new_customer_db = mod_db(customer_db,date_toggle)
#     else:
#         new_customer_db = customer_db

#     cc_node = new_customer_db.iloc[int(cc_num)]


#     date_today = datetime.datetime.today()
#     date_today_reformat = date_today.strftime('%y%m%d')

#     min_cap=-12000
#     max_cap=34000
#     discount_rate = 0.1214

#     total_elapsed_comp=0

#     df_cc_results=pd.DataFrame(columns=['Run','Process Time (Minutes)','SimID',
#                                               'Customer',

#                                               'Average Customer Price',
#                                         'Average Generator Price',
#                                         'Average Line Rental',
#                                               'Hedge',

#                                               'Fixed Customer Price',


#                                         'Line Rental Cap',
#                                               'Value'])
#     #upload price and load databases

#     t1_start_initializations = time.time()

#     cc_price_sim=solar_pac_wesm_forecasts_cc_mid
#     gen_price_sim=solar_pac_wesm_forecasts_supp_mid


#     if 'Japan' in str(cc_node[0]):

#         cc_load_sim=solar_pac_cc_load_sim_japan
#         supp_name_for_sim = 'Japan 25MW'


#     t1_stop_initializations = time.time()

#     elapsed_time_initializations = round((t1_stop_initializations-t1_start_initializations)/60,2)

#     #print('Uploading CC Load Database Process Time:',elapsed_time_initializations)
#     total_elapsed_comp+=elapsed_time_initializations

#     t1_start_init= time.time()

#     #date calculations
#     start_cc_from_db=datetime.datetime(cc_node[3],cc_node[1],cc_node[2])
#     start_cc_today=datetime.datetime(date_today.year,date_today.month,date_today.day)

#     start_cc=max(start_cc_from_db,start_cc_today)

#     if date_toggle=="NONE":
#         end_cc=datetime.datetime(cc_node[6],cc_node[4],cc_node[5])
#     else:
#         end_cc=min(datetime.datetime(cc_node[6],cc_node[4],cc_node[5]),datetime.datetime(date_toggle.year,date_toggle.month,date_toggle.day))

#     calendar_cc = xs_calendar.loc[(xs_calendar['Date'] >= start_cc) & (xs_calendar['Date'] < end_cc+datetime.timedelta(days=1))]

#     calendar_cc_conso = calendar_cc.copy()
#     calendar_cc_conso = calendar_cc_conso[['Date']]

#     #Granular DB
#     npv_db_original_gp=calendar_cc_conso.copy()
#     npv_db_original_npv=calendar_cc_conso.copy()

#     cc_new = calendar_cc.reset_index(drop=True)

#     delim=pd.DataFrame()
#     delim['Delimiter'] =["|"]*len(xv)

#     cc_new['YearMonthID']=cc_new['Year'].astype('str')+delim['Delimiter']+cc_new['Month'].astype('str')


#     fixed_cc = [cc_node[9]]*len(cc_new)

#     cc_new['Fixed Price'] = fixed_cc

#     t1_stop_init = time.time()
#     elapsed_time_init = round((t1_stop_init-t1_start_init)/60,2)

#     print('Initializations Process Time:',elapsed_time_init)

#     total_elapsed_comp+=elapsed_time_init
#     npv_counter_list=[]

#     #CC Value Computation

#     if 'STORM' in cc_node[0] or 'RES' in cc_node[0]:
#         gen_price_sim = solar_pac_wesm_forecasts_supp_mid
#         cc_price_sim = solar_pac_wesm_forecasts_cc_mid


#     for run_no in range(1):

#         t1_start_comp = time.time()

#         #merging datasets
#         sim_run='Sim'+str(run_no)

#         cc_price_sim_for_comp = cc_price_sim[['SolarPacSupplyID',sim_run]]
#         cc_price_sim_for_comp = cc_price_sim_for_comp.rename(columns={sim_run:'Customer Price Sim'})

#         #cc_price_sim_for_comp.to_excel('Test1.xlsx')

#         gen_price_sim_for_comp = gen_price_sim[['SolarPacSupplyID',sim_run]]
#         gen_price_sim_for_comp = gen_price_sim_for_comp.rename(columns={sim_run:'Gen Price Sim'})

#         #gen_price_sim_for_comp.to_excel('Test2.xlsx')

#         if 'STORM' in cc_node[0] and 'RES' in cc_node[0]:
#             cc_load_sim_for_comp = cc_load_sim[['SolarPacSupplyID','Sim0']]
#             cc_load_sim_for_comp = cc_load_sim_for_comp.rename(columns={'Sim0':'Load Sim'})
#         else:
#             cc_load_sim_for_comp = cc_load_sim[['SolarPacSupplyID',sim_run]]
#             cc_load_sim_for_comp = cc_load_sim_for_comp.rename(columns={sim_run:'Load Sim'})

#         cc_new_temp= cc_new.copy()
#         cc_new_temp = cc_new_temp.merge(cc_price_sim_for_comp,on='SolarPacSupplyID',how='left')
#         cc_new_temp = cc_new_temp.merge(gen_price_sim_for_comp,on='SolarPacSupplyID',how='left')

#         cc_new_temp = cc_new_temp.merge(cc_load_sim_for_comp,on='SolarPacSupplyID',how='left')

#         cc_final = cc_new_temp[['Date','Billing Month','Day','Billing Year','Hour','MonthCountID','Fixed Price','Customer Price Sim','Gen Price Sim','Load Sim']]

#         #line rental
#         cc_final['Line Rental'] = cc_final['Customer Price Sim'] - cc_final['Gen Price Sim']

#         #final cashflow
#         cc_final['Customer Price_for_Final_Cashflow']=cc_final['Customer Price Sim'].apply(lambda x:min(x,0))

#         cc_final['Final_Cashflow_Counter1']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter1(x,cc_node))

#         cc_final['Final_Cashflow_Counter2']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter2(x,cc_node))

#         cc_final['Final_Cashflow_Counter3']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter3(x,cc_node))

#         #if 'STORM' in cc_node[0] or 'RES' in cc_node[0]:
#             #cc_final['Final_Cashflow1'] = ((cc_final['Fixed Price'])*(1-0.0075))*cc_final['Load Sim']
#             #cc_final['Final_Cashflow2'] = [0]*len(cc_final)
#             #cc_final['Final_Cashflow3'] = [0]*len(cc_final)
#         #else:
#         cc_final['Final_Cashflow1'] = ((cc_final['Fixed Price']+cc_final['Customer Price_for_Final_Cashflow'])*(1-0.0075) - cc_final['Gen Price Sim'])*cc_final['Load Sim']
#         cc_final['Final_Cashflow2'] = ((cc_final['Fixed Price']+cc_final['Customer Price_for_Final_Cashflow'])*(1-0.0075) - cc_final['Gen Price Sim'] - [cc_node[12]]*len(cc_final))*cc_final['Load Sim']
#         cc_final['Final_Cashflow3'] = ((cc_final['Fixed Price']+cc_final['Customer Price_for_Final_Cashflow'])*(1-0.0075) - cc_final['Customer Price Sim'])*cc_final['Load Sim']


#         cc_final['Total']=((cc_final['Final_Cashflow_Counter1']*cc_final['Final_Cashflow1'])+(cc_final['Final_Cashflow_Counter2']*cc_final['Final_Cashflow2'])+(cc_final['Final_Cashflow_Counter3']*cc_final['Final_Cashflow3']))*0.75
#         cc_final['Total']=list(cc_final['Total'])[:len(cc_final['Total'])-1]+[list(cc_final['Total'])[-1]+cc_node[14]]

#         #cc_final['Total']=list(cc_final['Total'])[:len(cc_final['Total'])-1]+[list(cc_final['Total'])[-1]+2000000/3]

#         #calendar_cc_conso = calendar_cc_conso.merge(cc_final[['Date','Total']],on='Date',how='left')

#         #calendar_cc_conso = calendar_cc_conso.rename(columns={'Total':sim_run})

#         days_until_today = start_cc-date_ref

#         npv_cc =(cc_final['Total'] / (1+discount_rate/8760)**np.arange(1, len(cc_final['Total'])+1)).sum(axis=0)

#         if days_until_today.days > 0:
#             npv_cc = npv_cc/(1+discount_rate/8760)**days_until_today.days

#         cc_final['NPV'] = cc_final['Total']/(1+discount_rate/8760)**days_until_today.days
#         npv_db_original_gp=npv_db_original_gp.merge(cc_final[['Date','Total']],on='Date',how='left')
#         npv_db_original_gp.columns=list(npv_db_original_gp.columns[:len(npv_db_original_gp.columns)-1])+['GP'+str(run_no)]
#         npv_db_original_npv=npv_db_original_npv.merge(cc_final[['Date','NPV']],on='Date',how='left')
#         npv_db_original_npv.columns=list(npv_db_original_npv.columns[:len(npv_db_original_npv.columns)-1])+['NPV'+str(run_no)]


#         t1_stop_comp = time.time()
#         elapsed_time_comp = round((t1_stop_comp-t1_start_comp)/60,2)

#         results_list=[run_no, elapsed_time_comp, sim_run,
#                       cc_node[0],

#                       np.mean(cc_final['Customer Price Sim']),
#                       np.mean(cc_final['Gen Price Sim']),
#                       np.mean(cc_final['Line Rental']),
#                                     np.max(cc_final['Load Sim']),
#                                     np.mean(cc_final['Fixed Price']),

#                                     cc_node[12],

#                       npv_cc]

#         df_cc_results.loc[run_no] = results_list

#         npv_counter_list.append(npv_cc)

#         # print(results_list, np.mean(npv_counter_list))


#         total_elapsed_comp += elapsed_time_comp

#     # npv_db[cc_node[0]] = df_cc_results['Value']


#     cc_final.to_excel(f'{customer_db.iloc[cc_num].CCName}.xlsx', index = False)

#     t1_start_finalizations = time.time()

#     t1_stop_finalizations = time.time()

#     elapsed_time_finalizations = round((t1_stop_finalizations-t1_start_finalizations)/60,2)

#     total_elapsed_comp += elapsed_time_finalizations

#     print('Total Process Time:',total_elapsed_comp)

# hide_toggle('Customer Portfolio Valuation Function (>5 Years of Contract Term)')

# def cc_portfolio_valuation_long(cc_num, date_ref, du="N", admin=0):

#     if date_toggle!="NONE":
#         new_customer_db = mod_db(customer_db,date_toggle)
#     else:
#         new_customer_db = customer_db

#     cc_node = new_customer_db.iloc[int(cc_num)]

#     date_today = datetime.datetime.today()
#     date_today_reformat = date_today.strftime('%y%m%d')

#     min_cap=-12000
#     max_cap=34000
#     discount_rate = 0.1214

#     du_pass=0

#     lbt=0.0075

#     total_elapsed_comp=0

#     df_cc_results=pd.DataFrame(columns=['Run','Process Time (Minutes)','SimID',
#                                         'CC',
#                                         'Average Customer Price',
#                                         'Average Generator Price',
#                                         'Average Line Rental',
#                                         'Average Load',
#                                         'Fixed Customer Price',

#                                         'Line Rental Cap',
#                                         'Value'])

#     #upload price and load databases
#     t1_start_initializations = time.time()

#     sims_dict = load_sim(cc_num)
#     cc_load_sim=sims_dict

#     t1_stop_initializations = time.time()

#     elapsed_time_initializations = round((t1_stop_initializations-t1_start_initializations)/60,2)

#     #print('Uploading CC Load Database Process Time:',elapsed_time_initializations)
#     total_elapsed_comp+=elapsed_time_initializations

#     t1_start_init = time.time()

#     #date calculations
#     start_cc_from_db=datetime.datetime(cc_node[3],cc_node[1],cc_node[2])
#     start_cc_today=datetime.datetime(date_today.year,date_today.month,date_today.day)

#     start_cc=max(start_cc_from_db,start_cc_today)

#     if date_toggle=="NONE":
#         end_cc=datetime.datetime(cc_node[6],cc_node[4],cc_node[5])
#     else:
#         end_cc=min(datetime.datetime(cc_node[6],cc_node[4],cc_node[5]),datetime.datetime(date_toggle.year,date_toggle.month,date_toggle.day))

#     calendar_cc = calendar_db.loc[(calendar_db['Date'] >= start_cc) & (calendar_db['Date'] < end_cc+datetime.timedelta(days=1))]

#     calendar_cc_conso = calendar_cc.copy()
#     calendar_cc_conso = calendar_cc_conso[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour']]

#     cc_new = calendar_cc.reset_index(drop=True)
#     fixed_cc = [cc_node[9]]*len(cc_new)

#     onpeakoffpeak = []

#     for i in range(len(cc_new)):
#         if cc_new['Hour'][i] >= cc_node[7] and cc_new['Hour'][i] <= cc_node[8]:
#             onpeakoffpeak.append(cc_node[10])
#         else:
#             onpeakoffpeak.append(cc_node[11])

#     cc_new['Fixed Price'] = fixed_cc
#     cc_new['On Peak/Off Peak Price'] = onpeakoffpeak

#     t1_stop_init = time.time()
#     elapsed_time_init = round((t1_stop_init-t1_start_init)/60,2)

#     print('Initializations Process Time:',elapsed_time_init)

#     total_elapsed_comp+=elapsed_time_init

#     #Granular DB
#     npv_db_original_gp=calendar_cc_conso.copy()
#     npv_db_original_npv=calendar_cc_conso.copy()

#     #CC Value Computation

#     npv_counter_list=[]

#     for run_no in range(1):

#         t1_start_comp = time.time()

#         #merging datasets
#         sim_run='Sim'+str(run_no)


#         cc_load_sim_for_comp = cc_load_sim[['ID_Load',sim_run]]
#         cc_load_sim_for_comp = cc_load_sim_for_comp.rename(columns={sim_run:'Load Sim'})

#         cc_new_temp = cc_new.merge(solar_pac_wesm_forecasts_cc_mid[['Date',sim_run]],on="Date",how="left")
#         cc_new_temp = cc_new_temp.rename(columns={sim_run:'Customer Price Sim'})
#         cc_new_temp = cc_new_temp.merge(solar_pac_wesm_forecasts_supp_mid[['Date',sim_run]],on="Date", how="left")
#         cc_new_temp = cc_new_temp.rename(columns={sim_run:'Gen Price Sim'})
#         cc_new_temp = cc_new_temp.merge(cc_load_sim_for_comp,on="ID_Load", how="left")

#         cc_final = cc_new_temp[['Date','Billing Month','Day','Billing Year','Hour','MonthCountID','Fixed Price','On Peak/Off Peak Price','Customer Price Sim','Gen Price Sim','Load Sim']]

#         #line rental
#         if du=="N":
#             cc_final['Line Rental'] = cc_final['Customer Price Sim'] - cc_final['Gen Price Sim']
#         else:
#             cc_final['Line Rental'] = [0]*len(cc_final)

#         cc_final['Admin Fee']=[admin]*len(cc_final)

#         #computation
#         cc_final['Customer Price_for_Final_Cashflow']=cc_final.apply(lambda x:min(x['On Peak/Off Peak Price'],x['Customer Price Sim']),axis=1)

#         cc_final['LR_Fee_Counter1']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter1(x,cc_node))

#         cc_final['LR_Fee_Counter2']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter2(x,cc_node))

#         cc_final['LR_Fee_Counter3']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter3(x,cc_node))

#         cc_final['LR_Fee1'] = cc_final['Line Rental']*cc_final['Load Sim']

#         cc_final['LR_Fee2'] = (cc_final['Line Rental']-cc_node[12]*(len(cc_final)))*cc_final['Load Sim']

#         cc_final['LR_Fee3'] = [0]*len(cc_final)

#         cc_final['Line Rental Fee'] = (cc_final['LR_Fee_Counter1']*cc_final['LR_Fee1'])+(cc_final['LR_Fee_Counter2']*cc_final['LR_Fee2'])+(cc_final['LR_Fee_Counter3']*cc_final['LR_Fee3'])

#         cc_final['Generation Fee'] = ((cc_final['Fixed Price']+cc_final['Admin Fee'])*cc_final['Load Sim'])+cc_final['Customer Price_for_Final_Cashflow']*cc_final['Load Sim']

#         cc_final['DU Passthrough Charges'] = du_pass*cc_final['Load Sim']

#         #cc_final['DU Passthrough Charges'] = 0

#         cc_final_with_monthly_fee = pd.DataFrame()

#         #monthly peak load

#         month_count_id_unique_keys = list(cc_new['MonthCountID'].unique())

#         for month_count_element in month_count_id_unique_keys:
#             cc_final_sub = cc_final.loc[cc_new['MonthCountID'] == month_count_element]
#             maxload_month = np.max(cc_final_sub['Load Sim'])
#             cc_final_sub['Monthly Fee'] =(max(1.9,maxload_month)*cc_node[13]*1000/len(cc_final_sub))

#             cc_final_sub['Local Business Tax']=(cc_final_sub['Generation Fee']+cc_final_sub['Monthly Fee']+cc_final['DU Passthrough Charges'])*-lbt
#             cc_final_sub['Purchase Power'] = -cc_final_sub['Load Sim']*cc_final_sub['Customer Price Sim']

#             cc_final_sub['Total']=cc_final_sub['Generation Fee']+cc_final_sub['Monthly Fee']+cc_final_sub['Line Rental Fee']+cc_final_sub['Purchase Power']+cc_final_sub['Local Business Tax']-cc_final_sub['DU Passthrough Charges']

#             cc_final_with_monthly_fee = cc_final_with_monthly_fee.append(cc_final_sub,ignore_index=True)

#         cc_final = cc_final_with_monthly_fee.sort_values(by=['Date'])

#         cc_final['Total']=list(cc_final['Total'])[:len(cc_final['Total'])-1]+[list(cc_final['Total'])[-1]+cc_node[14]]

#         #Granular DB
#         cc_final.reset_index(inplace=True)
#         cc_final['NPV'] = cc_final['Total'] / (1+discount_rate/8760)**cc_final['index']


#         #calendar_cc_conso = calendar_cc_conso.merge(cc_final[['Date','Total']],on='Date',how='left')

#         #calendar_cc_conso = calendar_cc_conso.rename(columns={'Total':sim_run})

#         days_until_today = start_cc-date_ref

#         npv_cc =(cc_final['Total'] / (1+discount_rate/8760)**np.arange(1, len(cc_final['Total'])+1)).sum(axis=0)

#         if days_until_today.days > 0:
#             npv_cc = npv_cc/(1+discount_rate/8760)**days_until_today.days


#         #Granular DB
#         cc_final['NPV'] = cc_final['NPV']/(1+discount_rate/len(cc_final['Total']))**days_until_today.days

#         npv_db_original_gp=npv_db_original_gp.merge(cc_final[['Date','Total']],on='Date',how='left')
#         npv_db_original_gp.columns=list(npv_db_original_gp.columns[:len(npv_db_original_gp.columns)-1])+['GP'+str(run_no)]



#         npv_db_original_npv=npv_db_original_npv.merge(cc_final[['Date','NPV']],on='Date',how='left')
#         npv_db_original_npv.columns=list(npv_db_original_npv.columns[:len(npv_db_original_npv.columns)-1])+['NPV'+str(run_no)]


#         t1_stop_comp = time.time()
#         elapsed_time_comp = round((t1_stop_comp-t1_start_comp)/60,2)

#         results_list=[run_no, elapsed_time_comp, sim_run,
#                     cc_node[0],

#                      np.mean(cc_final['Customer Price Sim']),
#                     np.mean(cc_final['Gen Price Sim']),
#                     np.mean(cc_final['Line Rental']),
#                                    np.mean(cc_final['Load Sim']),
#                                    cc_node[9],

#                                   cc_node[12],

#                      npv_cc]
#         df_cc_results.loc[run_no] = results_list

#         npv_counter_list.append(npv_cc)

#         # print(results_list,np.mean(npv_counter_list))

#     t1_start_finalizations = time.time()

#     #calendar_cc_conso_dup = calendar_cc_conso.iloc[:,1:]

#     #calendar_cc_conso[cc_node[0]] = calendar_cc_conso_dup.mean(axis=1)

#     #calendar_cc_conso=calendar_cc_conso[['Date',cc_node[0]]]

#     # npv_db[cc_node[0]] = df_cc_results['Value']

#     #df_cc_results.to_sql(name_of_file+' CC Valuation',sqlEngine, if_exists='replace', index=False)
#     cc_final.to_excel(f'{customer_db.iloc[cc_num].CCName}.xlsx', index = False)

#     t1_stop_finalizations = time.time()

#     elapsed_time_finalizations = round((t1_stop_finalizations-t1_start_finalizations)/60,2)

#     total_elapsed_comp += elapsed_time_finalizations

#     print('Total Process Time:',total_elapsed_comp)


#     #return calendar_cc_conso

# hide_toggle('CC Portfolio Valuation Function (Long)')


# def cc_portfolio_valuation_short(cc_num, date_ref, du="N", admin=0):

#     if date_toggle!="NONE":
#         new_customer_db = mod_db(customer_db,date_toggle)
#     else:
#         new_customer_db = customer_db

#     cc_node = new_customer_db.iloc[int(cc_num)]

#     date_today = datetime.datetime.today()
#     date_today_reformat = date_today.strftime('%y%m%d')

#     min_cap=-12000
#     max_cap=34000
#     discount_rate = 0.1214

#     du_pass=0

#     lbt=0.0075

#     total_elapsed_comp=0

#     df_cc_results=pd.DataFrame(columns=['Run','Process Time (Minutes)','SimID',
#                                         'CC',
#                                         'Average Customer Price',
#                                         'Average Generator Price',
#                                         'Average Line Rental',
#                                         'Average Load',
#                                         'Fixed Customer Price',
#                                         'Line Rental Cap',
#                                         'Value'])

#     #upload price and load databases
#     t1_start_initializations = time.time()

#     sims_dict = load_sim(cc_num)
#     cc_load_sim=sims_dict

#     t1_stop_initializations = time.time()

#     elapsed_time_initializations = round((t1_stop_initializations-t1_start_initializations)/60,2)

#     total_elapsed_comp+=elapsed_time_initializations

#     t1_start_init = time.time()

#     #date calculations
#     start_cc_from_db=datetime.datetime(cc_node[3],cc_node[1],cc_node[2])
#     start_cc_today=datetime.datetime(date_today.year,date_today.month,date_today.day)

#     start_cc=max(start_cc_from_db,start_cc_today)

#     if date_toggle=="NONE":
#         end_cc=datetime.datetime(cc_node[6],cc_node[4],cc_node[5])
#     else:
#         end_cc=min(datetime.datetime(cc_node[6],cc_node[4],cc_node[5]),datetime.datetime(date_toggle.year,date_toggle.month,date_toggle.day))

#     calendar_cc = calendar_db.loc[(calendar_db['Date'] >= start_cc) & (calendar_db['Date'] < end_cc+datetime.timedelta(days=1))]

#     calendar_cc_conso = calendar_cc.copy()
#     calendar_cc_conso = calendar_cc_conso[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour']]

#     #Granular DB
#     npv_db_original_gp=calendar_cc_conso.copy()
#     npv_db_original_npv=calendar_cc_conso.copy()

#     cc_new = calendar_cc.reset_index(drop=True)
#     fixed_cc = [cc_node[9]]*len(cc_new)

#     cc_new['Fixed Price'] = fixed_cc

#     t1_stop_init = time.time()
#     elapsed_time_init = round((t1_stop_init-t1_start_init)/60,2)

#     print('Initializations Process Time:',elapsed_time_init)

#     total_elapsed_comp+=elapsed_time_init

#     #CC Value Computation

#     npv_counter_list=[]

#     for run_no in range(1):

#         t1_start_comp = time.time()

#         #merging datasets
#         sim_run='Sim'+str(run_no)

#         #cc_price_sim_for_comp = cc_price_sim[['ID',sim_run]]
#         #cc_price_sim_for_comp = cc_price_sim_for_comp.rename(columns={sim_run:'Customer Price Sim'})

#         #gen_price_sim_for_comp = gen_price_sim[['ID',sim_run]]
#         #gen_price_sim_for_comp = gen_price_sim_for_comp.rename(columns={sim_run:'Gen Price Sim'})

#         cc_load_sim_for_comp = cc_load_sim[['ID_Load',sim_run]]
#         cc_load_sim_for_comp = cc_load_sim_for_comp.rename(columns={sim_run:'Load Sim'})

#         cc_new_temp = cc_new.merge(solar_pac_wesm_forecasts_cc_mid[['Date',sim_run]],on="Date",how="left")
#         cc_new_temp = cc_new_temp.rename(columns={sim_run:'Customer Price Sim'})
#         cc_new_temp = cc_new_temp.merge(solar_pac_wesm_forecasts_supp_mid[['Date',sim_run]],on="Date", how="left")
#         cc_new_temp = cc_new_temp.rename(columns={sim_run:'Gen Price Sim'})
#         cc_new_temp = cc_new_temp.merge(cc_load_sim_for_comp,on="ID_Load", how="left")

#         cc_final = cc_new_temp[['Date','Billing Month','Day','Billing Year','Hour','MonthCountID','Fixed Price','Customer Price Sim','Gen Price Sim','Load Sim']]

#         #line rental
#         if du=="N":
#             cc_final['Line Rental'] = cc_final['Customer Price Sim'] - cc_final['Gen Price Sim']
#         else:
#             cc_final['Line Rental'] = [0]*len(cc_final)

#         cc_final['Admin Fee']=[admin]*len(cc_final)

#         #cc_final['DU Passthrough Charges'] = 1.55*cc_final['Load Sim']
#         #cc_final['DU Passthrough Charges'] = -0

#         #final cashflow
#         cc_final['Customer Price_for_Final_Cashflow']=cc_final['Customer Price Sim'].apply(lambda x:min(x,0))

#         cc_final['Final_Cashflow_Counter1']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter1(x,cc_node))

#         cc_final['Final_Cashflow_Counter2']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter2(x,cc_node))

#         cc_final['Final_Cashflow_Counter3']= cc_final['Line Rental'].apply(lambda x:final_cashflow_counter3(x,cc_node))

#         cc_final['Final_Cashflow1'] = ((cc_final['Fixed Price']+cc_final['Admin Fee']+cc_final['Customer Price_for_Final_Cashflow']+[du_pass]*len(cc_final))*(1-lbt) - cc_final['Gen Price Sim']-[du_pass]*len(cc_final))*cc_final['Load Sim']

#         cc_final['Final_Cashflow2'] = ((cc_final['Fixed Price']+cc_final['Admin Fee']+cc_final['Customer Price_for_Final_Cashflow']+[du_pass]*len(cc_final))*(1-lbt) - cc_final['Gen Price Sim'] - [cc_node[12]]*len(cc_final) -[du_pass]*len(cc_final))*cc_final['Load Sim']

#         cc_final['Final_Cashflow3'] = ((cc_final['Fixed Price']+cc_final['Admin Fee']+cc_final['Customer Price_for_Final_Cashflow']+[du_pass]*len(cc_final))*(1-lbt) - cc_final['Customer Price Sim']-[du_pass]*len(cc_final))*cc_final['Load Sim']

#         cc_final['Total']=(cc_final['Final_Cashflow_Counter1']*cc_final['Final_Cashflow1'])+(cc_final['Final_Cashflow_Counter2']*cc_final['Final_Cashflow2'])+(cc_final['Final_Cashflow_Counter3']*cc_final['Final_Cashflow3'])

#         cc_final['Total']=list(cc_final['Total'])[:len(cc_final['Total'])-1]+[list(cc_final['Total'])[-1]+cc_node[14]]

#         #Granular DB
#         cc_final.reset_index(inplace=True)
#         cc_final['NPV'] = cc_final['Total'] / (1+discount_rate/8760)**cc_final['index']


#         #calendar_cc_conso = calendar_cc_conso.merge(cc_final[['Date','Total']],on='Date',how='left')

#         #calendar_cc_conso = calendar_cc_conso.rename(columns={'Total':sim_run})

#         days_until_today = start_cc-date_ref

#         npv_cc =(cc_final['Total'] / (1+discount_rate/8760)**np.arange(1, len(cc_final['Total'])+1)).sum(axis=0)

#         if days_until_today.days > 0:
#             npv_cc = npv_cc/(1+discount_rate/8760)**days_until_today.days


#         #Granular DB
#         cc_final['NPV'] = cc_final['NPV']/(1+discount_rate/len(cc_final['Total']))**days_until_today.days
#         npv_db_original_gp=npv_db_original_gp.merge(cc_final[['Date','Total']],on='Date',how='left')
#         npv_db_original_gp.columns=list(npv_db_original_gp.columns[:len(npv_db_original_gp.columns)-1])+['GP'+str(run_no)]



#         npv_db_original_npv=npv_db_original_npv.merge(cc_final[['Date','NPV']],on='Date',how='left')
#         npv_db_original_npv.columns=list(npv_db_original_npv.columns[:len(npv_db_original_npv.columns)-1])+['NPV'+str(run_no)]



#         t1_stop_comp = time.time()
#         elapsed_time_comp = round((t1_stop_comp-t1_start_comp)/60,2)

#         results_list=[run_no, elapsed_time_comp, sim_run,
#                       cc_node[0],

#                       np.mean(cc_final['Customer Price Sim']),
#                       np.mean(cc_final['Gen Price Sim']),
#                       np.mean(cc_final['Line Rental']),
#                                     np.mean(cc_final['Load Sim']),
#                                     cc_node[9],
#                                     cc_node[12],

#                       npv_cc]

#         df_cc_results.loc[run_no] = results_list

#         npv_counter_list.append(npv_cc)

#         # print(results_list,np.mean(npv_counter_list))

#         total_elapsed_comp += elapsed_time_comp

#     t1_start_finalizations = time.time()

#     #calendar_cc_conso_dup = calendar_cc_conso.iloc[:,1:]

#     #calendar_cc_conso[cc_node[0]] = calendar_cc_conso_dup.mean(axis=1)

#     #calendar_cc_conso=calendar_cc_conso[['Date',cc_node[0]]]

#     # npv_db[cc_node[0]] = df_cc_results['Value']

#     #df_cc_results.to_sql(name_of_file+' CC Valuation',sqlEngine, if_exists='replace', index=False)
#     cc_final.to_excel(f'{customer_db.iloc[cc_num].CCName}.xlsx', index = False)

#     t1_stop_finalizations = time.time()

#     elapsed_time_finalizations = round((t1_stop_finalizations-t1_start_finalizations)/60,2)

#     total_elapsed_comp += elapsed_time_finalizations

#     print('Total Process Time:',total_elapsed_comp)


#     #return calendar_cc_conso


# hide_toggle('CC Portfolio Valuation Function (Short)')

"""## Functions for Filtering Live Contracts and Showing it as One Cell"""

## FOR FILTERING THE LIVE CONTRACTS AND SHOWING IT AS ONE CELL

def raroc_results(last_npv_col,initial_text, initial_month_inc):

    #Setting Benchmark
    raroc_results = pd.DataFrame(columns=['Customer','Start Date','End Date','Tenor (Years)','Contract Price per kWh','Line Rental Cap per kWh','Peak Load (MW)','Load Factor','Cumulative RAROC', 'Cumulative NPV', 'Cumulative VAR', 'Cumulative 5th Percentile'])

    cumulative_port = [0]*len(npv_db)

    apr_port=npv_db.iloc[:,0:last_npv_col+1].sum(axis=1)

    column_list=list(npv_db.columns[0:last_npv_col+1])

    column_list_load = [i for i in column_list if i in list(customer_db['CCName'])]

    cc_load_total = cc_load[column_list_load].sum(axis=1)

    coincidental_peak = "{:,.2f}".format(max(cc_load_total))

    cumulative_port += apr_port


    mean_npv=np.mean(cumulative_port)
    p5_npv=np.percentile(cumulative_port, 5)
    var_npv= mean_npv-p5_npv
    raroc_npv = mean_npv/var_npv

    raroc_results.loc[0]=[str(initial_text),'','','','','',str(coincidental_peak),coincidental_peak,raroc_npv,mean_npv,var_npv,p5_npv]

    sub_npv_db = npv_db.iloc[:,last_npv_col+1:]


    #Individual Comparisons
    sub_customer_db=customer_db[['CCName','StartMonth','StartDay','StartYear','EndMonth','EndDay','EndYear','CES Gross Profits']]
    sub_supplier_db=supplier_db[['SupplierName','StartMonth','StartDay','StartYear','EndMonth','EndDay','EndYear']]

    sub_db = sub_customer_db.copy()

    for supprow in range(len(sub_supplier_db)):
        sub_db.loc[len(sub_customer_db)+supprow] = list(sub_supplier_db.loc[supprow])+[0]

    datetime_list=[]
    endtime_list=[]
    tenor=[]

    for period in range(len(sub_db)):
        datetime_list.append(datetime.date(sub_db['StartYear'][period],sub_db['StartMonth'][period],sub_db['StartDay'][period]))
        endtime_list.append(datetime.date(sub_db['EndYear'][period],sub_db['EndMonth'][period],sub_db['EndDay'][period]))
        tenor.append(relativedelta(endtime_list[period],datetime_list[period]).years+ceil(relativedelta(endtime_list[period],datetime_list[period]).months*10/12)/10)


    sub_db['StartDate'] = datetime_list
    sub_db['EndDate'] = endtime_list
    sub_db['Tenor (Years)'] = tenor


    #Difference in Max and Min Contract Dates
    max_contract_date = np.max(sub_db['StartDate'])
    min_contract_date = np.min(sub_db['StartDate'])+relativedelta(months=initial_month_inc,days=-25)

    days_diff = max_contract_date - min_contract_date
    actual_days = days_diff.days

    #Generating Resulting RAROC Table
    indiv_raroc_results_orig = raroc_results[['Customer','Start Date','End Date','Tenor (Years)','Cumulative RAROC', 'Cumulative NPV', 'Cumulative VAR', 'Cumulative 5th Percentile']]
    indiv_raroc_results = indiv_raroc_results_orig.copy()

    for months_inc in range(0,actual_days+1):
        filtered_sub_db=sub_db.loc[(sub_db['StartDate']==min_contract_date+relativedelta(days=months_inc))].reset_index()
        #print(filtered_sub_db)


        if len(filtered_sub_db)==0:
            pass

        else:
            for sub_cust in filtered_sub_db['CCName']:
                if sub_cust in sub_npv_db.columns:

                    indiv_npv_values = sub_npv_db[sub_cust]
                    indiv_raroc_contrib = cumulative_port + indiv_npv_values
                    mean_npv=np.mean(indiv_raroc_contrib)
                    p5_npv=np.percentile(indiv_raroc_contrib, 5)
                    var_npv= mean_npv-p5_npv
                    raroc_npv = mean_npv/var_npv
                    indiv_raroc_results.loc[len(indiv_raroc_results)]=[sub_cust,filtered_sub_db['StartDate'][0],filtered_sub_db['EndDate'][0],
                                                                       filtered_sub_db['Tenor (Years)'][list(filtered_sub_db['CCName']).index(sub_cust)],raroc_npv,mean_npv,var_npv,p5_npv]

                else:
                    pass

        indiv_raroc_sort=sorted(list(indiv_raroc_results['Cumulative RAROC'][1:len(indiv_raroc_results['Cumulative RAROC'])+1]),reverse=True)

        for supplier_number in range(len(indiv_raroc_sort)):
            supp_number=list(indiv_raroc_results['Cumulative RAROC'][1:len(indiv_raroc_results['Cumulative RAROC'])+1]).index(indiv_raroc_sort[supplier_number])
            if indiv_raroc_results['Customer'][supp_number+1] in list(supplier_db['SupplierName']):
                gen_supp_load=solar_pac_load_profiles[indiv_raroc_results['Customer'][supp_number+1]]

                cumulative_raroc_cc = sub_npv_db[list(indiv_raroc_results['Customer'])[supp_number+1]]
                cumulative_port += cumulative_raroc_cc
                mean_npv=np.mean(cumulative_port)
                p5_npv=np.percentile(cumulative_port,5)
                var_npv=mean_npv-p5_npv
                raroc_npv = mean_npv/var_npv
                raroc_results.loc[len(raroc_results)]=[indiv_raroc_results['Customer'][supp_number+1],
                                                       min_contract_date+relativedelta(days=months_inc)
                                                       ,indiv_raroc_results['End Date'][supp_number+1],indiv_raroc_results['Tenor (Years)'][supp_number+1],
                                                       supplier_db['FixedPrice'][list(supplier_db['SupplierName']).index(indiv_raroc_results['Customer'][supp_number+1])],
                                                       supplier_db['LRCap'][list(supplier_db['SupplierName']).index(indiv_raroc_results['Customer'][supp_number+1])],
                                                       "{:.2f}".format(np.max(gen_supp_load)),'',
                                                       raroc_npv,mean_npv,var_npv,p5_npv]
            else:
                pass


        for customer_number in range(len(indiv_raroc_sort)):
            cc_number=list(indiv_raroc_results['Cumulative RAROC'][1:len(indiv_raroc_results['Cumulative RAROC'])+1]).index(indiv_raroc_sort[customer_number])
            if indiv_raroc_results['Customer'][cc_number+1] in list(supplier_db['SupplierName']):
                pass
            else:
                if 'Japan' in indiv_raroc_results['Customer'][cc_number+1]:
                    cust_load=solar_pac_cc_load_profiles['Japan 25MW']
                else:
                    cust_load=cc_load[list(indiv_raroc_results['Customer'])[cc_number+1]]
                load_factor=np.mean(cust_load)/np.max(cust_load)
                peak_load_mw=np.max(cust_load)
                cumulative_raroc_cc = sub_npv_db[indiv_raroc_results['Customer'][cc_number+1]]
                cumulative_port += cumulative_raroc_cc
                mean_npv=np.mean(cumulative_port)
                p5_npv=np.percentile(cumulative_port,5)
                var_npv=mean_npv-p5_npv
                raroc_npv = mean_npv/var_npv
                raroc_results.loc[len(raroc_results)]=[indiv_raroc_results['Customer'][cc_number+1],
                                                       min_contract_date+relativedelta(days=months_inc)
                                                       ,indiv_raroc_results['End Date'][supp_number+1],
                                                       indiv_raroc_results['Tenor (Years)'][cc_number+1],
                                                                       customer_db['FixedPrice'][list(customer_db['CCName']).index(indiv_raroc_results['Customer'][cc_number+1])],
                                                                       customer_db['LRCap'][list(customer_db['CCName']).index(indiv_raroc_results['Customer'][cc_number+1])],
                                                                       "{:.2f}".format(peak_load_mw),load_factor,raroc_npv,mean_npv,var_npv,p5_npv]

        indiv_raroc_results = indiv_raroc_results_orig.copy()

    contractprice_list=[]
    lrcap_list=[]
    raroc_lf_list_check=[]

    for lf_x in range(len(list(raroc_results['Load Factor']))):
        if raroc_results['Contract Price per kWh'][lf_x] == '':
            contractprice_list.append('')
        else:
            contractprice_list.append("₱{:,.2f}".format(float(raroc_results['Contract Price per kWh'][lf_x])/1000))

        if raroc_results['Line Rental Cap per kWh'][lf_x] == '':
            lrcap_list.append('')
        else:
            lrcap_list.append("₱{:,.2f}".format(float(raroc_results['Line Rental Cap per kWh'][lf_x])/1000))


        if type(raroc_results['Load Factor'][lf_x]) == float:
            raroc_lf_list_check.append("{:.0%}".format(raroc_results['Load Factor'][lf_x]))
        else:
            raroc_lf_list_check.append('')


    raroc_results['Load Factor']=raroc_lf_list_check
    raroc_results['Contract Price per kWh']=contractprice_list
    raroc_results['Line Rental Cap per kWh']=lrcap_list

    raroc_results['Cumulative RAROC']=["{:.0%}".format(x) for x in raroc_results['Cumulative RAROC']]
    raroc_results['Cumulative NPV']=["₱{:,.2f} M".format(x/10**6) for x in raroc_results['Cumulative NPV']]
    raroc_results['Cumulative VAR']=["₱{:,.2f} M".format(x/10**6) for x in raroc_results['Cumulative VAR']]
    raroc_results['Cumulative 5th Percentile']=["₱{:,.2f} M".format(x/10**6).replace('₱-','-₱') for x in raroc_results['Cumulative 5th Percentile']]

    return raroc_results[['Customer', 'Start Date','End Date', 'Tenor (Years)',
       'Contract Price per kWh', 'Line Rental Cap per kWh', 'Peak Load (MW)',
       'Load Factor', 'Cumulative RAROC', 'Cumulative NPV', 'Cumulative VAR',
       'Cumulative 5th Percentile']]



hide_toggle('Creating RAROC Results Table')

"""## Functions for showing all the Contracts Active and Pipeline"""

###### FUNCTIONS FOR SHOWING ALL THE CONTRACTS ACTIVE AND PIPELINE
def raroc_results(last_npv_col,initial_text, initial_month_inc):

    #Setting Benchmark
    raroc_results = pd.DataFrame(columns=['Customer','Start Date','End Date','Tenor (Years)','Contract Price per kWh','Line Rental Cap per kWh','Peak Load (MW)','Load Factor','Cumulative RAROC', 'Cumulative NPV', 'Cumulative VAR', 'Cumulative 5th Percentile'])

    cumulative_port = [0]*len(npv_db)

    apr_port=npv_db.iloc[:,0:last_npv_col+1].sum(axis=1)

    column_list=list(npv_db.columns[0:last_npv_col+1])

    column_list_load = [i for i in column_list if i in list(customer_db['CCName'])]

    cc_load_total = cc_load[column_list_load].sum(axis=1)

    coincidental_peak = "{:,.2f}".format(max(cc_load_total))

    cumulative_port += apr_port


    mean_npv=np.mean(cumulative_port)
    p5_npv=np.percentile(cumulative_port, 5)
    var_npv= mean_npv-p5_npv
    raroc_npv = mean_npv/var_npv

#     raroc_results.loc[0]=[str(initial_text),'','','','','',str(coincidental_peak),coincidental_peak,raroc_npv,mean_npv,var_npv,p5_npv]

    try:

        start_date_0 = customer_db[customer_db['CCName'] == str(npv_db.columns[0])]['StartDate'].iloc[0].date()

        end_date_0 = customer_db[customer_db['CCName'] == str(npv_db.columns[0])]['EndDate'].iloc[0].date()

        tenor_0 = round(int(((end_date_0 - start_date_0).days)/364))

        name_0 = str(npv_db.columns[last_npv_col])

        contract_price_0 = (customer_db[customer_db['CCName'] == str(npv_db.columns[0])]['FixedPrice'].iloc[0])/1000

        max_load_0 = np.max(cc_load[str(npv_db.columns[0])])

        mean_load_0 = np.mean(cc_load[str(npv_db.columns[0])])

        load_factor_0 = mean_load_0/max_load_0

    except:

        start_date_0 = supplier_db[supplier_db['SupplierName'] == str(npv_db.columns[0])]['StartDate'].iloc[0].date()

        end_date_0 = supplier_db[supplier_db['SupplierName'] == str(npv_db.columns[0])]['EndDate'].iloc[0].date()

        contract_price_0 = (supplier_db[supplier_db['SupplierName'] == str(npv_db.columns[0])]['FixedPrice'].iloc[0])/1000

        tenor_0 = round(int(((end_date_0 - start_date_0).days)/364))

        name_0 = str(npv_db.columns[last_npv_col])



        max_load_0 = np.max(solar_pac_load_profiles[str(npv_db.columns[0])])

        mean_load_0 = np.mean(solar_pac_load_profiles[str(npv_db.columns[0])])

        load_factor_0 = mean_load_0/max_load_0


#     start_date_0 = customer_db[customer_db['CCName'] == str(npv_db.columns[0])]['StartDate'].iloc[0].date()

#     end_date_0 = customer_db[customer_db['CCName'] == str(npv_db.columns[0])]['EndDate'].iloc[0].date()

#     tenor_0 = round(int(((end_date_0 - start_date_0).days)/364))

#     name_0 = str(npv_db.columns[last_npv_col])

#     contract_price_0 = (customer_db[customer_db['CCName'] == str(npv_db.columns[0])]['FixedPrice'].iloc[0])/1000

#     max_load_0 = np.max(cc_load[str(npv_db.columns[0])])

#     mean_load_0 = np.mean(cc_load[str(npv_db.columns[0])])

#     load_factor_0 = mean_load_0/max_load_0


    raroc_results.loc[0]=[name_0,start_date_0,end_date_0,tenor_0,
                          str(contract_price_0),'',str(coincidental_peak),
                          coincidental_peak,raroc_npv,mean_npv,var_npv,p5_npv]

    sub_npv_db = npv_db.iloc[:,last_npv_col+1:]


    #Individual Comparisons
    sub_customer_db=customer_db[['CCName','StartMonth','StartDay','StartYear','EndMonth','EndDay','EndYear','CES Gross Profits']]
    sub_supplier_db=supplier_db[['SupplierName','StartMonth','StartDay','StartYear','EndMonth','EndDay','EndYear']]

    sub_db = sub_customer_db.copy()

    for supprow in range(len(sub_supplier_db)):
        sub_db.loc[len(sub_customer_db)+supprow] = list(sub_supplier_db.loc[supprow])+[0]

    datetime_list=[]
    endtime_list=[]
    tenor=[]

    for period in range(len(sub_db)):
        datetime_list.append(datetime.date(sub_db['StartYear'][period],sub_db['StartMonth'][period],sub_db['StartDay'][period]))
        endtime_list.append(datetime.date(sub_db['EndYear'][period],sub_db['EndMonth'][period],sub_db['EndDay'][period]))
        tenor.append(relativedelta(endtime_list[period],datetime_list[period]).years+ceil(relativedelta(endtime_list[period],datetime_list[period]).months*10/12)/10)


    sub_db['StartDate'] = datetime_list
    sub_db['EndDate'] = endtime_list
    sub_db['Tenor (Years)'] = tenor


    #Difference in Max and Min Contract Dates
    max_contract_date = np.max(sub_db['StartDate'])
    min_contract_date = np.min(sub_db['StartDate'])+relativedelta(months=initial_month_inc,days=-25)

    days_diff = max_contract_date - min_contract_date
    actual_days = days_diff.days

    #Generating Resulting RAROC Table
    indiv_raroc_results_orig = raroc_results[['Customer','Start Date','End Date','Tenor (Years)','Cumulative RAROC', 'Cumulative NPV', 'Cumulative VAR', 'Cumulative 5th Percentile']]
    indiv_raroc_results = indiv_raroc_results_orig.copy()

#     raroc_results.loc[0]=[str(npv_db.columns[last_npv_col]),,'','','','',str(coincidental_peak),coincidental_peak,raroc_npv,mean_npv,var_npv,p5_npv]

    for months_inc in range(0,actual_days+1):
        filtered_sub_db=sub_db.loc[(sub_db['StartDate']==min_contract_date+relativedelta(days=months_inc))].reset_index()
        #print(filtered_sub_db)


        if len(filtered_sub_db)==0:
            pass

        else:
            for sub_cust in filtered_sub_db['CCName']:
                if sub_cust in sub_npv_db.columns:
                    indiv_npv_values = sub_npv_db[sub_cust]
                    # print(f'cumulative_port-{cumulative_port}')
                    # print(f'indiv_npv_values-{indiv_npv_values}')
                    indiv_raroc_contrib = cumulative_port + indiv_npv_values
                    mean_npv=np.mean(indiv_raroc_contrib)
                    p5_npv=np.percentile(indiv_raroc_contrib, 5)
                    var_npv= mean_npv-p5_npv
                    raroc_npv = mean_npv/var_npv
                    indiv_raroc_results.loc[len(indiv_raroc_results)]=[sub_cust,filtered_sub_db['StartDate'][0],filtered_sub_db['EndDate'][0],
                                                                       filtered_sub_db['Tenor (Years)'][list(filtered_sub_db['CCName']).index(sub_cust)],raroc_npv,mean_npv,var_npv,p5_npv]

                else:
                    pass

        indiv_raroc_sort=sorted(list(indiv_raroc_results['Cumulative RAROC'][1:len(indiv_raroc_results['Cumulative RAROC'])+1]),reverse=True)

        for supplier_number in range(len(indiv_raroc_sort)):
            supp_number=list(indiv_raroc_results['Cumulative RAROC'][1:len(indiv_raroc_results['Cumulative RAROC'])+1]).index(indiv_raroc_sort[supplier_number])
            if indiv_raroc_results['Customer'][supp_number+1] in list(supplier_db['SupplierName']):
                gen_supp_load=solar_pac_load_profiles[indiv_raroc_results['Customer'][supp_number+1]]

                cumulative_raroc_cc = sub_npv_db[list(indiv_raroc_results['Customer'])[supp_number+1]]
                cumulative_port += cumulative_raroc_cc
                mean_npv=np.mean(cumulative_port)
                p5_npv=np.percentile(cumulative_port,5)
                var_npv=mean_npv-p5_npv
                raroc_npv = mean_npv/var_npv
                raroc_results.loc[len(raroc_results)]=[indiv_raroc_results['Customer'][supp_number+1],
                                                       min_contract_date+relativedelta(days=months_inc)
                                                       ,indiv_raroc_results['End Date'][supp_number+1],indiv_raroc_results['Tenor (Years)'][supp_number+1],
                                                       supplier_db['FixedPrice'][list(supplier_db['SupplierName']).index(indiv_raroc_results['Customer'][supp_number+1])],
                                                       supplier_db['LRCap'][list(supplier_db['SupplierName']).index(indiv_raroc_results['Customer'][supp_number+1])],
                                                       "{:.2f}".format(np.max(gen_supp_load)),'',
                                                       raroc_npv,mean_npv,var_npv,p5_npv]
            else:
                pass


        for customer_number in range(len(indiv_raroc_sort)):
            cc_number=list(indiv_raroc_results['Cumulative RAROC'][1:len(indiv_raroc_results['Cumulative RAROC'])+1]).index(indiv_raroc_sort[customer_number])
            if indiv_raroc_results['Customer'][cc_number+1] in list(supplier_db['SupplierName']):
                pass
            else:
                if 'Japan' in indiv_raroc_results['Customer'][cc_number+1]:
                    cust_load=solar_pac_cc_load_profiles['Japan 25MW']
                else:
                    cust_load=cc_load[list(indiv_raroc_results['Customer'])[cc_number+1]]
                load_factor=np.mean(cust_load)/np.max(cust_load)
                peak_load_mw=np.max(cust_load)
                cumulative_raroc_cc = sub_npv_db[indiv_raroc_results['Customer'][cc_number+1]]
                cumulative_port += cumulative_raroc_cc
                mean_npv=np.mean(cumulative_port)
                p5_npv=np.percentile(cumulative_port,5)
                var_npv=mean_npv-p5_npv
                raroc_npv = mean_npv/var_npv
                # INSERTED THIS HERE
#                 raroc_results.loc[0]=[str(npv_db.columns[last_npv_col]),'','','','','',str(coincidental_peak),coincidental_peak,raroc_npv,mean_npv,var_npv,p5_npv]
                # INSERTED THIS HERE
                raroc_results.loc[len(raroc_results)]=[indiv_raroc_results['Customer'][cc_number+1],
                                                       min_contract_date+relativedelta(days=months_inc)
                                                       ,indiv_raroc_results['End Date'][supp_number+1],
                                                       indiv_raroc_results['Tenor (Years)'][cc_number+1],
                                                                       customer_db['FixedPrice'][list(customer_db['CCName']).index(indiv_raroc_results['Customer'][cc_number+1])],
                                                                       customer_db['LRCap'][list(customer_db['CCName']).index(indiv_raroc_results['Customer'][cc_number+1])],
                                                                       "{:.2f}".format(peak_load_mw),load_factor,raroc_npv,mean_npv,var_npv,p5_npv]

        indiv_raroc_results = indiv_raroc_results_orig.copy()

    contractprice_list=[]
    lrcap_list=[]
    raroc_lf_list_check=[]

    for lf_x in range(len(list(raroc_results['Load Factor']))):
        if raroc_results['Contract Price per kWh'][lf_x] == '':
            contractprice_list.append('')
        else:
            contractprice_list.append("₱{:,.2f}".format(float(raroc_results['Contract Price per kWh'][lf_x])/1000))

        if raroc_results['Line Rental Cap per kWh'][lf_x] == '':
            lrcap_list.append('')
        else:
            lrcap_list.append("₱{:,.2f}".format(float(raroc_results['Line Rental Cap per kWh'][lf_x])/1000))


        if type(raroc_results['Load Factor'][lf_x]) == float:
            raroc_lf_list_check.append("{:.0%}".format(raroc_results['Load Factor'][lf_x]))
        else:
            raroc_lf_list_check.append('')



    raroc_results['Load Factor']=raroc_lf_list_check
    raroc_results['Contract Price per kWh']=contractprice_list
    raroc_results['Line Rental Cap per kWh']=lrcap_list

    raroc_results['Cumulative RAROC']=["{:.0%}".format(x) for x in raroc_results['Cumulative RAROC']]
    raroc_results['Cumulative NPV']=["₱{:,.2f} M".format(x/10**6) for x in raroc_results['Cumulative NPV']]
    raroc_results['Cumulative VAR']=["₱{:,.2f} M".format(x/10**6) for x in raroc_results['Cumulative VAR']]
    raroc_results['Cumulative 5th Percentile']=["₱{:,.2f} M".format(x/10**6).replace('₱-','-₱') for x in raroc_results['Cumulative 5th Percentile']]

    raroc_results.at[0,'Contract Price per kWh'] =  '₱'+f'{contract_price_0:0.2f}'
    raroc_results.at[0,'Line Rental Cap per kWh'] =  '₱0.00'
    raroc_results.at[0,'Load Factor'] =  str(round(load_factor_0*100)) + '%'

    return raroc_results[['Customer', 'Start Date','End Date', 'Tenor (Years)',
       'Contract Price per kWh', 'Line Rental Cap per kWh', 'Peak Load (MW)',
       'Load Factor', 'Cumulative RAROC', 'Cumulative NPV', 'Cumulative VAR',
       'Cumulative 5th Percentile']]



hide_toggle('Creating RAROC Results Table')

### DATE INPUT
# date_today = datetime.datetime.today()+datetime.timedelta(days=0) #We have the freedom to choose any date as a
# #reference point for our analysis.  Use the code "datetime.datetime(year number,month number,day number)".

# year_1 = 2027
# year_2 = 2028

date_today = datetime.datetime(2024,3,13) #We have the freedom to choose any date as a
#reference point for our analysis.  Use the code "datetime.datetime(year number,month number,day number)".

date_today_reformat = date_today.strftime('%y%m%d')

# date_toggle = datetime.datetime(year_2,12,25)

date_toggle = "NONE" #We have the freedom to evaluate all contracts up to a certain date.  If we want to evaluate
#until the expiry of all contracts, type in "NONE".
#IF ONE YEAR, E.G. TODAY IS datetime.datetime(2023,7,31), THEN PLUGIN TO date_toggle = datetime.datetime(2024,7,31)

# date11 = '20'+date_today_reformat.strip()[:2] +'-'+date_today_reformat.strip()[2:4] +'-'+date_today_reformat.strip()[4:6]


hide_toggle('Choosing Date of Reference (See instructions in the comments)')

#Forecast type either "230606 WESM Forward Curve" or "230605 Lantau WESM Forward Curve"
forecast_type = '230606 WESM Forward Curve'
run_type = 'VEC'

# Note: Base_WESM = '
Base_WESM = 'Base WESM'

# forecast_type = '230605 Lantau WESM Forward Curve with Lan_Vis,Lan_Luz'
# run_type = 'Lantau'

#Note: Base_WESM = 'Base WESM',Base_WESM = 'LanVis Php/kWh',Base_WESM = 'LanLuz Php/kWh',
# Base_WESM = 'LanVis Php/kWh'

hide_toggle('Choosing Forecast Type WESM Forward Curve / Lantau')

"""## Customer DB for Updated MQs"""

customer_db = pd.DataFrame(columns = ['CCName', 'StartMonth','StartDay','StartYear','EndMonth','EndDay','EndYear'
                                      ,'PeakMin','PeakMax','FixedPrice','PeakPrice','OffPeakPrice','LRCap'
                                      ,'MonthlyFee','CES Gross Profits'])


customer_db.loc[0]=['Creative Diecast',12,26,2022,12,25,2023,9,22,3850,0,0,0,0,0]
customer_db.loc[1]=['Asian Plastic 1',1,26,2022,7,25,2023,9,22,4500,0,0,50,0,0]
customer_db.loc[2]=['Asian Plastic 2',1,26,2022,7,25,2023,9,22,4500,0,0,50,0,0]
customer_db.loc[3]=['EMS (Renewal)',10,26,2021,10,25,2023,9,22,7330,0,0,0,0,0]

customer_db.loc[4]=['HEVA Iloilo',12,26,2023,12,25,2024,9,22,6400,0,0,0,0,0]

customer_db.loc[5]=['Pioneer Center',8,26,2021,8,25,2023,9,22,7230,0,0,0,0,0]
customer_db.loc[6]=['CAM Mechatronic',12,26,2023,10,25,2024,9,22,6450,0,0,0,0,0]
customer_db.loc[7]=['Fast Services',4,26,2023,10,25,2023,9,22,6300,0,0,0,0,0]

customer_db.loc[8]=['Treasure Island',1,26,2024,1,25,2025,9,22,6300,0,0,0,0,0]

customer_db.loc[9]=['Calypso',12,30,2022,9,25,2023,9,22,6000,0,0,0,0,0]
customer_db.loc[10]=['GFCC',12,26,2022,7,25,2023,9,22,3850*1.2,0,0,0,0,0]
# customer_db.loc[11]=['Light Rail Manila',10,4,2023,9,25,2024,9,22,6300,0,0,0,0,0] #CHANGED on 09192023(SIR MIKE)

customer_db.loc[11]=['Light Rail Manila',9,26,2023,9,25,2024,9,22,6300,0,0,0,0,0] #CHANGED FROM ASANA ON 11212023(SIR MIKE)

customer_db.loc[12]=['Nustar',8,26,2023,6,25,2024,9,22,6300,0,0,0,0,0]
customer_db.loc[13]=['Fong Shan',3,26,2023,9,25,2023,9,22,6100,0,0,0,0,0]
customer_db.loc[14]=['Serendra Low',2,26,2023,7,25,2023,9,22,6100,0,0,0,0,0]
customer_db.loc[15]=['Serendra High',2,26,2023,7,25,2023,9,22,6100,0,0,0,0,0]
customer_db.loc[16]=['GGPC (Renewal) III',2,26,2023,11,25,2023,9,22,4800,0,0,0,0,0]
customer_db.loc[17]=['Vitarich (Aggregated)',9,26,2023,9,25,2024,9,22,6200,0,0,0,0,0] #CHANGED FROM 6.3 TO 6.2 ON 08222023, CHANGED FROM AUGUST TO SEPTEMBER(SIR MIKE)
customer_db.loc[18]=['AICE2',6,26,2024,6,25,2025,9,22,6000,0,0,0,0,0]
customer_db.loc[19]=['AICE3',6,26,2025,6,25,2028,9,22,6000,0,0,0,0,0]
customer_db.loc[20]=['AICE',6,26,2023,6,25,2024,9,22,6000,0,0,0,0,0]
customer_db.loc[21]=['Japan 25MW',7,26,2025,7,25,2035,9,22,5200,0,0,0,0,0]
customer_db.loc[22]=['EIDC',9,26,2022,9,25,2023,9,22,6000,0,0,0,0,0]
customer_db.loc[23]=['Danao Paper Mill',10,26,2022,10,25,2023,9,22,4850,0,0,0,0,0]
customer_db.loc[24]=['LHAI (Renewal)',3,26,2022,9,25,2023,9,22,0,6500,6500,42000,475,0]
customer_db.loc[25]=['Supercast (Renewal) II',7,26,2022,7,25,2023,9,22,4850,0,0,0,0,0]
customer_db.loc[26]=['Tarlac Mall (Renewal)',10,26,2022,9,25,2023,9,22,4250,0,0,0,0,0]
customer_db.loc[27]=['Yiking Plastic',9,26,2022,9,25,2023,9,22,4900,0,0,0,0,0]
customer_db.loc[28]=['Citiplas Plastic (Renewal)',3,26,2023,9,25,2023,9,22,8333,0,0,0,0,0]
# customer_db.loc[29]=['Treasure Island (Renewal)',7,26,2023,7,25,2024,9,22,6100,0,0,0,0,0]
#customer_db.loc[30]=['Customer X',7,26,2025,7,25,2040,9,22,4600,0,0,0,0,0]
customer_db.loc[31]=['GGPC MQ',11,26,2023,6,25,2024,9,22,6200,0,0,0,0,0]
customer_db.loc[32]=['Aeonprime',6,26,2023,12,25,2023,9,22,6200,0,0,0,0,0]
customer_db.loc[33]=['Polaris',6,26,2023,12,25,2023,9,22,6200,0,0,0,0,0]
customer_db.loc[34]=['HEVA La Paz',5,26,2023,8,25,2023,9,22,6200,0,0,0,0,0]

customer_db.loc[35]=['557 Feathermeal (Renewal) MQ',8,26,2023,6,25,2024,9,22,6200,0,0,0,0,0]

customer_db.loc[36]=['557 Feathermeal (WESM+)',6,26,2023,12,25,2023,9,22,0,0,0,0,0,0]
customer_db.loc[37]=['Vitarich (WESM+)',6,26,2023,12,25,2023,9,22,0,0,0,0,0,0]
customer_db.loc[38]=['Asian Plastic 1 (WESM+)',7,26,2023,10,25,2023,9,22,0,0,0,0,0,0]
customer_db.loc[39]=['Asian Plastic 2 (WESM+)',7,26,2023,10,25,2023,9,22,0,0,0,0,0,0]
customer_db.loc[40]=['Pioneer Center (WESM+)',8,26,2023,2,25,2024,9,22,0,0,0,0,0,0]
customer_db.loc[41]=['HEVA Rizal (WESM+)',6,26,2023,9,25,2023,9,22,0,0,0,0,0,0]
customer_db.loc[42]=['HYP-X',8,26,2023,8,25,2024,9,22,6500,0,0,0,0,0]
customer_db.loc[43]=['Supercast MQ',11,26,2023,6,25,2024,9,22,6300,0,0,0,0,0]
customer_db.loc[44]=['Pioneer Center A',10,26,2023,10,25,2024,9,22,6350,0,0,0,0,0]
customer_db.loc[45]=['Tarlac Mall A',11,26,2023,6,25,2024,9,22,6300,0,0,0,0,0]
customer_db.loc[46]=['HYP-Y',11,26,2023,6,25,2024,9,22,6300,0,0,0,0,0]
customer_db.loc[47]=['IMCC-1',3,26,2024,3,25,2034,9,22,6000,0,0,0,0,0] #3.5
customer_db.loc[48]=['IMCC-2',3,26,2025,3,25,2035,9,22,6000,0,0,0,0,0]

#ADDED ON 8132023
customer_db.loc[49]=['HEVA Iloilo (WESM+)',6,26,2023,12,25,2023,9,22,0,0,0,0,0,0]
customer_db.loc[50]=['Treasure Island (WESM+)',7,26,2023,1,25,2024,9,22,0,0,0,0,0,0]

# Tarlac Mall A,Supercast (Renewal) A,'HEVA Iloilo (WESM+)''Treasure Island (WESM+)'

#ADDED ON 8152023
customer_db.loc[51]=['DD-90',9,26,2023,9,25,2024,9,22,5400,0,0,0,0,0]
customer_db.loc[52]=['DD-60',9,26,2023,9,25,2024,9,22,5500,0,0,0,0,0]
customer_db.loc[53]=['DD-45',9,26,2023,9,25,2024,9,22,5600,0,0,0,0,0]
customer_db.loc[54]=['VFI',10,26,2023,10,25,2025,9,22,6200,0,0,0,0,0]

#ADDED ON 8172023
customer_db.loc[55]=['VFI-85',9,26,2023,9,25,2024,9,22,6000,0,0,0,0,0]
customer_db.loc[56]=['VFI-80',9,26,2023,9,25,2024,9,22,6000,0,0,0,0,0]
customer_db.loc[57]=['VFI-75',9,26,2023,9,25,2024,9,22,6000,0,0,0,0,0]

#ADDED ON 8222023
customer_db.loc[58]=['Customer-X-5.0',7,26,2026,7,25,2041,9,22,4800,0,0,0,0,0]
customer_db.loc[59]=['Customer-X-5.5',7,26,2026,7,25,2041,9,22,5500,0,0,0,0,0]

#ADDED ON 8312023
# customer_db.loc[60]=['C&S',10,26,2023,10,25,2024,9,22,6500,0,0,0,0,0]

customer_db.loc[60]=['CASADI',2,26,2024,12,25,2024,9,22,6500,0,0,0,0,0] #CHANGED FROM ASANA ON 11212023

#ADDED ON 9182023
customer_db.loc[61]=['RLC-GAL',12,26,2023,12,25,2025,9,22,6300,0,0,0,0,0]

#ADDED ON 9192023
customer_db.loc[62]=['GLAS',10,26,2023,10,25,2024,9,22,6400,0,0,0,0,0]
# customer_db.loc[63]=['Fast Logistics',10,26,2023,10,25,2024,9,22,6300,0,0,0,0,0]

customer_db.loc[63]=['Fast Logistics',10,26,2023,6,25,2024,9,22,6300,0,0,0,0,0] #CHANGED FROM ASANA ON 11212023(SIRMIKE)


#ADDED ON 9202023
customer_db.loc[64]=['Aeonprime A',10,26,2023,10,25,2024,9,22,6400,0,0,0,0,0]
customer_db.loc[65]=['Polaris A',10,26,2023,10,25,2024,9,22,6400,0,0,0,0,0]

#ADDED ON 9202023
customer_db.loc[66]=['HEVA Rizal',10,26,2023,10,25,2024,9,22,6400,0,0,0,0,0]


customer_db.loc[67]=['Creative Diecast-6.5 MQ',10,26,2023,6,25,2024,9,22,6500,0,0,0,0,0]

#ADDED ON 09282023

customer_db.loc[68]=['Vitarich MQ',10,26,2023,10,25,2024,9,22,6500,0,0,0,0,0]

customer_db.loc[69]=['Yiking MQ',10,26,2023,10,25,2024,9,22,6500,0,0,0,0,0]

customer_db.loc[70]=['EMS MQ',12,26,2023,10,25,2024,9,22,6500,0,0,0,0,0]

#ADDED ON 1022023

customer_db.loc[71]=['Kings Quality',10,26,2023,10,25,2024,9,22,6500,0,0,0,0,0]

#ADDED ON 10042023

customer_db.loc[72] = ['EIDC MQ',10,26,2023,10,25,2024,9,22,6400,0,0,0,0,0]

customer_db.loc[73] = ['Excel Towers A',11,26,2023,11,25,2024,9,22,6400,0,0,0,0,0]

#ADDED ON 10062023

# customer_db.loc[74] = ['One Montage',11,26,2023,11,25,2024,9,22,6400,0,0,0,0,0]

customer_db.loc[74] = ['One Montage',12,26,2023,12,25,2024,9,22,6400,0,0,0,0,0] #CHANGED FROM ASANA ON 11212023


customer_db.loc[75] = ['IMCC',3,26,2024,3,25,2026,9,22,3200,0,0,0,0,0]

#ADDED ON 11062023
customer_db.loc[76] = ['Park Centrale Tower',11,26,2023,11,25,2024,9,22,6500,0,0,0,0,0]
customer_db.loc[77] = ['Neltex',1,26,2025,10,25,2025,9,22,6500,0,0,0,0,0]
customer_db.loc[78]=['CAM MQ',12,26,2023,10,25,2024,9,22,6450,0,0,0,0,0]

#ADDED ON 11152023
customer_db.loc[79] = ['Golden Great',2,26,2024,2,25,2025,9,22,6300,0,0,0,0,0]
customer_db.loc[80]=['Oversea Feeds',2,26,2024,2,25,2026,9,22,6300,0,0,0,0,0]

customer_db.loc[81]=['Customer-X-30',6,26,2025,6,25,2045,9,22,5000,0,0,0,0,0]

#ADDED ON 11212023

customer_db.loc[82]=['AICE4',6,26,2024,6,25,2028,9,22,6000,0,0,0,0,0]
customer_db.loc[83]=['Fong Shan A',11,26,2023,11,25,2024,9,22,6500,0,0,0,0,0]
customer_db.loc[84]=['TIIC-Pilit',1,26,2024,1,25,2025,9,22,6400,0,0,0,0,0]
customer_db.loc[85]=['Waterfront-Cebu-60',1,26,2024,1,25,2026,9,22,6300,0,0,0,0,0]
customer_db.loc[86]=['Waterfront-Cebu-70',1,26,2024,1,25,2026,9,22,6300,0,0,0,0,0]
customer_db.loc[87]=['Waterfront-Cebu',1,26,2024,1,25,2026,9,22,6500,0,0,0,0,0]
customer_db.loc[88]=['CustomerX-70%',6,26,2024,6,25,2026,9,22,5900,0,0,0,0,0] #CustomerX-5MW-70%
customer_db.loc[89]=['CustomerX-5MW-70%',3,26,2024,3,25,2025,9,22,6500,0,0,0,0,0] #CustomerX-5MW-70%

#WESM+
customer_db.loc[90]=['GFCC-W',12,26,2023,12,25,2024,9,22,6000,0,0,0,0,0] #CustomerX-5MW-70%

customer_db.loc[91]=['EMS-W',12,26,2023,12,25,2024,9,22,6000,0,0,0,0,0] #CustomerX-5MW-70%

customer_db.loc[92]=['HEVALAPAZ-W',12,26,2023,12,25,2024,9,22,6000,0,0,0,0,0] #CustomerX-5MW-70%

customer_db.loc[93]=['HELIX AGG-W',12,26,2023,12,25,2024,9,22,6000,0,0,0,0,0] #CustomerX-5MW-70%

customer_db.loc[94]=['CALYPSO1-W',12,26,2023,12,25,2024,9,22,6000,0,0,0,0,0] #CustomerX-5MW-70%

customer_db.loc[95]=['CALYPSO2-W',12,26,2023,12,25,2024,9,22,6000,0,0,0,0,0] #CustomerX-5MW-70%

customer_db.loc[96]=['CITIPLAS PLASTIC-W',12,26,2023,12,25,2024,9,22,6000,0,0,0,0,0] #CustomerX-5MW-70%

customer_db.loc[97]=['MULTI-PACK-W',12,26,2023,12,25,2024,9,22,6000,0,0,0,0,0] #CustomerX-5MW-70%

customer_db.loc[98]=['ASIAN PLASTIC-W',12,26,2023,12,25,2024,9,22,6000,0,0,0,0,0] #CustomerX-5MW-70%

customer_db.loc[99]=['LEE CHOU TIAM-W',12,26,2023,12,25,2024,9,22,6000,0,0,0,0,0] #CustomerX-5MW-70%

customer_db.loc[100]=['CustomerY-70%',6,26,2024,6,25,2025,9,22,6300,0,0,0,0,0] #CustomerY-5MW-70%
customer_db.loc[101]=['CustomerY-70%-A',5,26,2024,5,25,2025,9,22,6400,0,0,0,0,0] #CustomerY-5MW-70%
customer_db.loc[102]=['Saffron',3,26,2024,3,25,2025,9,22,7000,0,0,0,0,0] #CustomerY-5MW-70%
customer_db.loc[103]=['UST Load',3,26,2024,3,25,2026,9,22,5700,0,0,0,0,0] #CustomerY-5MW-70%

#PIPELINE
customer_db.loc[104]=['May Harvest',4,26,2024,4,25,2026,9,22,5900,0,0,0,0,0] #CustomerY-5MW-70%


# CustomerY-70%

#GLAS, FAST LOGISTICS,C&S

#CORENERGY OFFERS
#DU PLUS  = FIXED PRICE + ADMIN FEE
#SHORTTERM = FIXED PRICE ONLY
#WESM PLUS = ADMIN FEE ONLY
#LONGTERM = FIXED PRICE

#Copy a line above and input new customer information.  For example,
#customer_db.loc[31]=['<name of customer>',<start month>,<start day>,<start year>,<end month>,<end day>,<end year>,9,22,<fixed price>,0,0,<line rental cap, usually 0>,0,<CES gross profits, usually 0>]

#If you want to erase a certain customer from the analysis, feel free to put a hashtag or a comment symbol before a line.

customer_db=customer_db.reset_index(drop=True)

customer_db['EndDate']=customer_db[['EndYear','EndMonth','EndDay']].apply(lambda x:datetime.datetime(x['EndYear'],x['EndMonth'],x['EndDay']),axis=1)
customer_db['StartDate']=customer_db[['StartYear','StartMonth','StartDay']].apply(lambda x:datetime.datetime(x['StartYear'],x['StartMonth'],x['StartDay']),axis=1)


hide_toggle("Current Customer Information (See instructions in comments)")

supplier_db = pd.DataFrame(columns = ['SupplierName', 'StartMonth','StartDay','StartYear','EndMonth','EndDay','EndYear'
                                      ,'FixedPrice','CapacityFee','VariablePrice','LRCap'])

# ['SupplierName', 'StartMonth','StartDay','StartYear','EndMonth','EndDay','EndYear'
#                                       ,'FixedPrice'(PHP/MW-HR),'CapacityFee'(PHP/MW-HR),'VariablePrice'(PHP/MW-HR),'LRCap'(PHP/MW-HR)])

supplier_db.loc[0]=['TVI',12,26,2022,12,25,2024,5350,0,0,42000]
# supplier_db.loc[1]=['LWEC',2,26,2025,12,25,2045,3830,0,0,42000] #STORM
supplier_db.loc[1]=['LWEC-VENA-50MW',6,26,2025,6,25,2046,3830,0,0,42000] #STORM
supplier_db.loc[2]=['SSREC',6,26,2025,6,25,2045,4250,0,0,42000] #ANDA

# supplier_db.loc[1]=['LWEC-VENA-50MW',6,26,2025,6,25,2028,3830,0,0,42000] #STORM
# supplier_db.loc[2]=['SSREC',6,26,2025,6,25,2028,4250,0,0,42000] #ANDA

# supplier_db.loc[3]=['Wind Farm',10,26,2023,10,25,2048,3790,0,0,42000]
# supplier_db.loc[4]=['SEM-Calaca',10,26,2023,10,25,2025,5980.1,0,0,42000] #5980.1
# supplier_db.loc[5]=['LWEC-TBC',7,26,2026,7,25,2041,3750,0,0,42000]
# supplier_db.loc[6]=['SIAEC',10,26,2023,9,25,2043,5300,0,0,42000]
# supplier_db.loc[7]=['LWEC-TBC-67.2',7,26,2026,7,25,2041,4750,0,0,42000]
# supplier_db.loc[8]=['SLPGC',9,26,2023,9,25,2024,5980.1,0,0,42000] #5980.1
# supplier_db.loc[5]=['SEM-Calaca-5MW',10,26,2023,10,25,2024,5900,0,0,42000]

supplier_db.loc[5]=['SEM-Calaca-5MW',11,26,2023,10,25,2024,5900,0,0,42000]

# supplier_db.loc[6]=['SEM-Calaca-7MW',10,26,2023,10,25,2025,5980.1,0,0,42000]
supplier_db.loc[7]=['SEM-Calaca-3MW',3,26,2024,3,25,2025,5800,0,0,42000]

supplier_db.loc[8]=['LWEC-TBC-67.2',9,26,2026,9,25,2041,4800,0,0,42000] # RUN FOR VEC AND LANTAU TOGETHER WITH ALL THE SIGNED

supplier_db.loc[9]=['SEM-Calaca-2MW',1,26,2024,1,25,2025,5900,0,0,42000]



supplier_db.loc[10]=['Kermit-C',6,26,2024,12,25,2030,6000,0,0,42000] #63MW

supplier_db.loc[11]=['Saturn-S',6,26,2025,6,25,2045,4000,0,0,42000] #50MW

supplier_db.loc[12]=['Beacon-S',6,26,2026,12,25,2030,6000,0,0,42000] #40MW

supplier_db.loc[13]=['Horus-S',6,26,2026,12,25,2030,6000,0,0,42000] #50MW

supplier_db.loc[14]=['Juno-S',6,26,2026,12,25,2030,6000,0,0,42000] #50MW


supplier_db.loc[15]=['Neptune-S',6,26,2026,12,25,2030,6000,0,0,42000] #30MW


supplier_db.loc[16]=['Rocket-W',6,26,2026,12,25,2030,6000,0,0,42000] #50MW


supplier_db.loc[17]=['Tabango,Leyte-S',6,26,2027,12,25,2030,6000,0,0,42000] #38MW


supplier_db.loc[18]=['Medellin-S',6,26,2027,12,25,2030,6000,0,0,42000] #50MW


supplier_db.loc[19]=['Capiz-W',6,26,2028,12,25,2030,6000,0,0,42000] #75MW


supplier_db.loc[20]=['Lyra-W',6,26,2028,12,25,2030,6000,0,0,42000] #88MW

supplier_db.loc[21]=['Northern,Samar-W',6,26,2029,12,25,2030,6000,0,0,42000] #50MW

supplier_db.loc[22]=['Quezon Province-W',6,26,2030,12,25,2030,6000,0,0,42000] #63MW


supplier_db.loc[23]=['Solar-A',3,26,2024,3,25,2025,5500,0,0,42000] #10MW

supplier_db.loc[24]=['SIAEC-B',3,26,2024,3,25,2025,5500,0,0,42000] #63MW

supplier_db.loc[25]=['GENCO-5MW',3,26,2024,3,25,2026,6000,0,0,42000] #10MW
supplier_db.loc[26]=['GENCO-5MW-A',6,26,2024,6,25,2025,5500,0,0,42000] #10MW

# supplier_db.loc[27]=['SIAEC-Jun',6,26,2024,3,25,2026,4800,0,0,42000] #22DCMW

supplier_db.loc[27]=['SIAEC-Jun',6,26,2024,6,25,2026,5750,0,0,42000] #22DCMW


supplier_db.loc[28]=['SIAEC-Jul',6,26,2024,6,25,2044,5750,0,0,42000] #22DCMW
supplier_db.loc[29]=['SIAEC-Aug',8,26,2024,8,25,2026,5000,0,0,42000] #22DCMW
supplier_db.loc[30]=['SIAEC-Sept',9,26,2024,9,25,2026,5000,0,0,42000] #22DCMW
supplier_db.loc[31]=['SIAEC-Oct',10,26,2024,10,25,2026,5000,0,0,42000] #22DCMW




# supply_load_list = ['SolarPacSupplyID', 'KSPC 15MW','KSPC 20MW','SLPGC (Extension)',
#                     'TVI','ANDA','ANDA (Profit Sharing)','VEC Bulacan','VEC Pangasinan',
#                     'Solar Pacific','Isabela','Bataan','STORM','Sungrow','Technergy','HYPOTHETICAL BASELOAD',
#                     'HYPOTHETICAL SOLAR','Solar Valley','RES','CC','Aries','HYPOTHETICAL 25MW','MPC','Wind Farm',
#                     'LWEC-VENA10X','SSREC10X', 'LWEC-TBC', 'LWEC-TBC-67.2','SEM-Calaca-5MW','SEM-Calaca-3MW','LWEC','SSREC',
#                     'SEM-Calaca-2MW','SOLAR-5MW-A','SSREC-5MW-B','Solar-A','Solar-B','SIAEC-B']
supply_load_list = ['SolarPacSupplyID', 'KSPC 15MW','KSPC 20MW','SLPGC (Extension)',
                    # 'TVI',
                    'ANDA','ANDA (Profit Sharing)','VEC Bulacan','VEC Pangasinan',
                    'Solar Pacific','Isabela','Bataan',
                    # 'STORM',
                    'Sungrow','Technergy','HYPOTHETICAL BASELOAD',
                    'HYPOTHETICAL SOLAR','Solar Valley','RES','CC','Aries','HYPOTHETICAL 25MW','MPC','Wind Farm',
                    # 'LWEC-VENA10X','SSREC10X', 'LWEC-TBC', 'LWEC-TBC-67.2','SEM-Calaca-5MW','SEM-Calaca-3MW','LWEC','SSREC',
                    # 'SEM-Calaca-2MW','SOLAR-5MW-A','SSREC-5MW-B','Solar-A','Solar-B','SIAEC-B'
                   ] + list(supplier_db['SupplierName'])


#Copy a line above and input new supplier information.  For example,
#supplier_db.loc[3]=['<name of customer>',<start month>,<start day>,<start year>,<end month>,<end day>,<end year>,<fixed price>,0,0,<line rental cap, usually 42000>]

#If you want to erase a certain supplier from the analysis, feel free to put a hashtag or a comment symbol before a line.

supplier_db=supplier_db.reset_index(drop=True)

supplier_db['EndDate']=supplier_db[['EndYear','EndMonth','EndDay']].apply(lambda x:datetime.datetime(x['EndYear'],x['EndMonth'],x['EndDay']),axis=1)

supplier_db['StartDate']=supplier_db[['StartYear','StartMonth','StartDay']].apply(lambda x:datetime.datetime(x['StartYear'],x['StartMonth'],x['StartDay']),axis=1)


hide_toggle("Current Supplier Information (See instructions in comments)")

cc_load=pd.read_parquet(fr'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\{date_today_reformat} CC Load.parquet')
print(f"{date_today_reformat} CC Load- DONE")

npv_db = pd.read_parquet(fr'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\{date_today_reformat} NPVDatabase ({run_type}).parquet')
print(f"{date_today_reformat} NPVDatabase ({run_type})- DONE")

# npv_db = pd.read_parquet(fr'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\{date_today_reformat} NPVDatabase ({run_type}).parquet')
# print(f"npv_db {date_today_reformat} {run_type} - DONE")

calendar_db = pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\calendar.parquet')
print("calendar_db - DONE")

location_db = pd.read_excel(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\location_db.xlsx')
print("location_db - DONE")

hide_toggle('Upload Three Excel Databases')

"""## Load Simulation"""

name_res="May Harvest"

load_factor = 70

# upper = 1372488.065

# lower = 1372488.065

january_kw=926099487/1000

january_pf= load_factor

february_kw= 855213016/1000


february_pf=load_factor

march_kw=february_kw



march_pf=load_factor



april_kw=january_kw



april_pf=load_factor
 #load_factor

may_kw=915808775/1000



may_pf=load_factor
 #load_factor

june_kw=915808775/1000



june_pf=load_factor
 #load_factor

july_kw=915808775/1000



july_pf= load_factor
#load_factor

august_kw=915808775/1000



august_pf=load_factor
 #load_factor

september_kw=920330600/1000



september_pf=load_factor
 #load_factor

october_kw=920330600/1000



october_pf=load_factor
 #load_factor

november_kw=1024101225/1000


november_pf=load_factor
 #

december_kw=1020287800/1000


december_pf=load_factor


cc_load=load_profile_simulator(name_cc=name_res,january=january_kw,february=february_kw,march=march_kw,
                               april=april_kw,may_load=may_kw,june=june_kw,
                               july=july_kw,august=august_kw,september=september_kw,
                               october=october_kw,november=november_kw,december=december_kw,
                           january_lf=january_pf, february_lf=february_pf, march_lf=march_pf,
                               april_lf=april_pf, may_lf=may_pf, june_lf=june_pf,
                               july_lf=july_pf, august_lf=august_pf, september_lf=september_pf,
                          october_lf=october_pf, november_lf=november_pf, december_lf=december_pf)

hide_toggle('Load Profile Simulation Proper')

"""## Create Load Simulations"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# forecast_type = '230606 WESM Forward Curve'
# run_type = 'VEC'
# 
# # Note: Base_WESM = '
# Base_WESM = 'Base WESM'
# 
# #Uploading 1000 Customer Prices and 1000 Gen Prices
# creatdie_gwap1=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Creative Diecast GWAP 1000 Sims CC Prices.parquet')
# creatdie_gwap2=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Creative Diecast GWAP 1000 Sims CC Load.parquet')
# creatdie_gwap3=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Creative Diecast GWAP 1000 Sims Gen Prices.parquet')
# 
# 
# creatdie_gwap=dict()
# 
# creatdie_gwap['CC Prices']=creatdie_gwap1
# creatdie_gwap['CC Load']=creatdie_gwap2
# creatdie_gwap['Gen Prices']=creatdie_gwap3
# 
# 
# #Creating a long-term calendar (supply)
# solar_pac_calendar = calendar_db.loc[(calendar_db['Date']>=datetime.datetime(2021,12,26)) & (calendar_db['Date']<datetime.datetime(2060,12,26))]
# solar_pac_calendar = solar_pac_calendar.reset_index()
# del solar_pac_calendar['index']
# 
# solar_pac_calendar['Year'] = solar_pac_calendar['Date'].apply(lambda x:x.year)
# solar_pac_calendar['Month'] = solar_pac_calendar['Date'].apply(lambda x:x.month)
# 
# 
# blankdf = pd.DataFrame()
# blankdf['Delimiter'] = ["|"]*len(solar_pac_calendar)
# 
# solar_pac_calendar['YearMonthIntervalID'] = solar_pac_calendar['Year'].astype(str) + blankdf['Delimiter'] + solar_pac_calendar['Month'].astype(str) + blankdf['Delimiter']+solar_pac_calendar['Hour'].astype(str)
# solar_pac_calendar['SolarPacSupplyID'] = solar_pac_calendar['Billing Year'].astype(str) + blankdf['Delimiter'] + solar_pac_calendar['Billing Month'].astype(str) + blankdf['Delimiter']+solar_pac_calendar['Day'].astype(str)+ blankdf['Delimiter']+solar_pac_calendar['Hour'].astype(str)
# solar_pac_calendar['YearMonthDayIntervalID'] = solar_pac_calendar['Year'].astype(str) + blankdf['Delimiter'] + solar_pac_calendar['Month'].astype(str)+ blankdf['Delimiter'] + solar_pac_calendar['Day'].astype(str) + blankdf['Delimiter']+solar_pac_calendar['Hour'].astype(str)
# 
# 
# 
# 
# #Uploading WESM Forecasts
# # wesm_forecasts = pd.read_parquet(fr'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\{forecast_type}.parquet') # ORIG
# 
# 
# wesm_forecasts = pd.read_parquet(fr'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\{forecast_type}-1.parquet') # VEC2.0
# 
# 
# 
# blankdf_gwap = pd.DataFrame()
# blankdf_gwap['Delimiter'] = ["|"]*len(wesm_forecasts)
# 
# wesm_forecasts['YearMonthDayIntervalID'] = wesm_forecasts['Year'].astype(str) + blankdf_gwap['Delimiter'] +wesm_forecasts['Month'].astype(str)+ blankdf_gwap['Delimiter']+wesm_forecasts['Day'].astype(str)+ blankdf_gwap['Delimiter']+wesm_forecasts['Hour'].astype(str)
# 
# 
# solar_pac_wesm_forecasts=solar_pac_calendar.merge(wesm_forecasts[['YearMonthDayIntervalID',
#                                                      f'{Base_WESM}',
#                                                      #'Adjusted WESM',
#                                                      #'High Adjusted WESM'
#                                                                  ]],on='YearMonthDayIntervalID',how='left')
# 
# 
# 
# # solar_pac_load_profiles_excel = pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\siaechalf.parquet')
# solar_pac_load_profiles_excel = pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\240131 Solar Pac Load Profiles.parquet') # siaechalf.parquet
# #
# # solar_pac_load_profiles=solar_pac_calendar.merge(solar_pac_load_profiles_excel[['SolarPacSupplyID', 'KSPC 15MW','KSPC 20MW','SLPGC (Extension)',
# #                                                                                 'TVI','ANDA','ANDA (Profit Sharing)','VEC Bulacan','VEC Pangasinan',
# #                                                      'Solar Pacific',
# #                                                      'Isabela',
# #                                                      'Bataan','STORM','Sungrow','Technergy','HYPOTHETICAL BASELOAD','HYPOTHETICAL SOLAR','Solar Valley','RES','CC','Aries',
# #                                                                                'HYPOTHETICAL 25MW','MPC','Wind Farm','SEM-Calaca','LWEC-TBC','LWEC-TBC-67.2',
#                                                                                  # 'SLPGC','SEM-Calaca-5MW','SEM-Calaca-7MW',]],on='SolarPacSupplyID',how='left')
# 
# solar_pac_load_profiles=solar_pac_calendar.merge(solar_pac_load_profiles_excel[supply_load_list],on='SolarPacSupplyID',how='left')
# 
# # ['SEM-Calaca', 'LWEC-TBC', 'LWEC-TBC-67.2', 'SLPGC', 'SEM-Calaca-5MW', 'SEM-Calaca-7MW']
# # solar_pac_load_profiles['Wind Farm']=0.7*solar_pac_load_profiles['Wind Farm'] #70%
# #Extending Simulations
# 
# solar_pac_wesm_forecasts_supp_low=solar_pac_wesm_forecasts[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#        'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID']]
# solar_pac_wesm_forecasts_supp_mid = solar_pac_wesm_forecasts_supp_low.copy()
# solar_pac_wesm_forecasts_cc_mid = solar_pac_wesm_forecasts_supp_low.copy()
# 
# 
# last_wesm_supp_price = list(creatdie_gwap['Gen Prices']['Sim0'])[-1]
# 
# solar_pac_gen_multipliers = solar_pac_wesm_forecasts.copy()
# 
# solar_pac_gen_multipliers['WESM Mid']=solar_pac_gen_multipliers[f'{Base_WESM}']/last_wesm_supp_price
# 
# for i in range(1001):
# 
#     last_wesm_supp_price_sim = list(creatdie_gwap['Gen Prices']['Sim'+str(i)])[-1]
#     solar_pac_wesm_forecasts_supp_mid['Sim'+str(i)]=solar_pac_gen_multipliers['WESM Mid']*last_wesm_supp_price_sim
# 
#     last_wesm_cc_price_sim = list(creatdie_gwap['CC Prices']['Sim'+str(i)])[-1]
#     solar_pac_wesm_forecasts_cc_mid['Sim'+str(i)] = solar_pac_gen_multipliers['WESM Mid']*last_wesm_cc_price_sim
# 
#     print('Sim'+str(i))
# 
# solar_pac_wesm_forecasts_supp_mid=solar_pac_wesm_forecasts_supp_mid.dropna()
# solar_pac_wesm_forecasts_cc_mid=solar_pac_wesm_forecasts_cc_mid.dropna()
# 
# solar_pac_wesm_forecasts_supp_mid=solar_pac_wesm_forecasts_supp_mid.reset_index()
# solar_pac_wesm_forecasts_cc_mid=solar_pac_wesm_forecasts_cc_mid.reset_index()
# 
# del solar_pac_wesm_forecasts_supp_mid['index']
# del solar_pac_wesm_forecasts_cc_mid['index']
# 
# # Creating File for the simulated 1000 scenarios
# # solar_pac_wesm_forecasts_supp_mid.to_csv('230804 Lantau CSV WESM Forecast.csv',index = False)
# 
# #Uploading 1000 Customer Loads
# 
# x_gwap2=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Customer X GWAP 1000 Sims CC Load.parquet')
# 
# x_gwap=dict()
# 
# x_gwap['CC Load']=x_gwap2
# 
# 
# 
# #Creating a long-term calendar (customer)
# 
# xs_calendar = calendar_db.loc[(calendar_db['Date']>=datetime.datetime(2022,12,26)) & (calendar_db['Date']<datetime.datetime(2048,12,26))]
# xs_calendar = xs_calendar.reset_index()
# del xs_calendar['index']
# 
# xs_calendar['Year'] = xs_calendar['Date'].apply(lambda x:x.year)
# xs_calendar['Month'] = xs_calendar['Date'].apply(lambda x:x.month)
# 
# 
# blankdf = pd.DataFrame()
# blankdf['Delimiter'] = ["|"]*len(xs_calendar)
# 
# xs_calendar['YearMonthIntervalID'] = xs_calendar['Year'].astype(str) + blankdf['Delimiter'] + xs_calendar['Month'].astype(str) + blankdf['Delimiter']+xs_calendar['Hour'].astype(str)
# xs_calendar['SolarPacSupplyID'] = xs_calendar['Billing Year'].astype(str) + blankdf['Delimiter'] + xs_calendar['Billing Month'].astype(str) + blankdf['Delimiter']+xs_calendar['Day'].astype(str)+ blankdf['Delimiter']+xs_calendar['Hour'].astype(str)
# 
# 
# 
# 
# #Uploading CC Load Profiles
# 
# solar_pac_wesm_forecasts=solar_pac_calendar.merge(wesm_forecasts[['YearMonthDayIntervalID',
#                                                      f'{Base_WESM}'
#                                                                  ]],on='YearMonthDayIntervalID',how='left')
# 
# 
# solar_pac_cc_load_profiles_excel = pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\230120 Xs CC Load Profiles.parquet')
# 
# solar_pac_cc_load_profiles=solar_pac_calendar.merge(solar_pac_cc_load_profiles_excel[['SolarPacSupplyID','Japan 25MW']],on='SolarPacSupplyID',how='left')
# 
# 
# solar_pac_cc_load_sim = solar_pac_cc_load_profiles[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#        'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID',
#        'SolarPacSupplyID']]
# 
# 
# #Creating 1000 load simulations
# 
# last_cc_load = list(x_gwap['CC Load']['Sim0'])[-1]
# 
# solar_pac_cc_load_multipliers=solar_pac_cc_load_sim.copy()
# solar_pac_cc_load_multipliers['Japan Multipliers']=solar_pac_cc_load_profiles['Japan 25MW']/last_cc_load
# solar_pac_cc_load_sim_japan=solar_pac_cc_load_sim.copy()
# 
# 
# 
# for i in range(1001):
# 
#     last_cc_load = list(x_gwap['CC Load']['Sim'+str(i)])[-1]
#     solar_pac_cc_load_sim_japan['Sim'+str(i)]=solar_pac_cc_load_multipliers['Japan Multipliers']*last_cc_load
#     print('Sim'+str(i))
# 
# 
# 
# #Extension of Customer/Supply WESM Prices
# 
# blankdf = pd.DataFrame()
# blankdf['Delimiter'] = ["|"]*len(solar_pac_wesm_forecasts_supp_low)
# 
# solar_pac_wesm_forecasts_supp_mid['SolarPacSupplyID'] =solar_pac_wesm_forecasts_supp_mid['Billing Year'].astype(str) + blankdf['Delimiter'] + solar_pac_wesm_forecasts_supp_mid['Billing Month'].astype(str) + blankdf['Delimiter']+solar_pac_wesm_forecasts_supp_mid['Day'].astype(str)+ blankdf['Delimiter']+solar_pac_wesm_forecasts_supp_mid['Hour'].astype(str)
# solar_pac_wesm_forecasts_cc_mid['SolarPacSupplyID'] =solar_pac_wesm_forecasts_cc_mid['Billing Year'].astype(str) + blankdf['Delimiter'] + solar_pac_wesm_forecasts_cc_mid['Billing Month'].astype(str) + blankdf['Delimiter']+solar_pac_wesm_forecasts_cc_mid['Day'].astype(str)+ blankdf['Delimiter']+solar_pac_wesm_forecasts_cc_mid['Hour'].astype(str)
# 
# 
# #Extension of long-term calendar (customer)
# xs_calendar['SolarPacSupplyID'] = xs_calendar['Billing Year'].astype(str) + blankdf['Delimiter'] + xs_calendar['Billing Month'].astype(str) + blankdf['Delimiter']+xs_calendar['Day'].astype(str)+ blankdf['Delimiter']+xs_calendar['Hour'].astype(str)
# 
# xv=xs_calendar.copy()
# 
# delim=pd.DataFrame()
# delim['Delimiter'] =["|"]*len(xv)
# 
# xv['YearMonthID']=xv['Year'].astype('str')+delim['Delimiter']+xv['Month'].astype('str')
# 
# hide_toggle('Black-Box Processing of Simulations for Long-Term Contracts (Time-Consuming)')

"""## Original Blackbox Processing"""

# %%time #OG

# #Uploading 1000 Customer Prices and 1000 Gen Prices
# creatdie_gwap1=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Creative Diecast GWAP 1000 Sims CC Prices.parquet')
# creatdie_gwap2=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Creative Diecast GWAP 1000 Sims CC Load.parquet')
# creatdie_gwap3=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Creative Diecast GWAP 1000 Sims Gen Prices.parquet')


# creatdie_gwap=dict()

# creatdie_gwap['CC Prices']=creatdie_gwap1
# creatdie_gwap['CC Load']=creatdie_gwap2
# creatdie_gwap['Gen Prices']=creatdie_gwap3


# #Creating a long-term calendar (supply)
# solar_pac_calendar = calendar_db.loc[(calendar_db['Date']>=datetime.datetime(2021,12,26)) & (calendar_db['Date']<datetime.datetime(2060,12,26))]
# solar_pac_calendar = solar_pac_calendar.reset_index()
# del solar_pac_calendar['index']

# solar_pac_calendar['Year'] = solar_pac_calendar['Date'].apply(lambda x:x.year)
# solar_pac_calendar['Month'] = solar_pac_calendar['Date'].apply(lambda x:x.month)


# blankdf = pd.DataFrame()
# blankdf['Delimiter'] = ["|"]*len(solar_pac_calendar)

# solar_pac_calendar['YearMonthIntervalID'] = solar_pac_calendar['Year'].astype(str) + blankdf['Delimiter'] + solar_pac_calendar['Month'].astype(str) + blankdf['Delimiter']+solar_pac_calendar['Hour'].astype(str)
# solar_pac_calendar['SolarPacSupplyID'] = solar_pac_calendar['Billing Year'].astype(str) + blankdf['Delimiter'] + solar_pac_calendar['Billing Month'].astype(str) + blankdf['Delimiter']+solar_pac_calendar['Day'].astype(str)+ blankdf['Delimiter']+solar_pac_calendar['Hour'].astype(str)
# solar_pac_calendar['YearMonthDayIntervalID'] = solar_pac_calendar['Year'].astype(str) + blankdf['Delimiter'] + solar_pac_calendar['Month'].astype(str)+ blankdf['Delimiter'] + solar_pac_calendar['Day'].astype(str) + blankdf['Delimiter']+solar_pac_calendar['Hour'].astype(str)




# #Uploading WESM Forecasts
# wesm_forecasts = pd.read_parquet(fr'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\{forecast_type}.parquet')


# blankdf_gwap = pd.DataFrame()
# blankdf_gwap['Delimiter'] = ["|"]*len(wesm_forecasts)

# wesm_forecasts['YearMonthDayIntervalID'] = wesm_forecasts['Year'].astype(str) + blankdf_gwap['Delimiter'] +wesm_forecasts['Month'].astype(str)+ blankdf_gwap['Delimiter']+wesm_forecasts['Day'].astype(str)+ blankdf_gwap['Delimiter']+wesm_forecasts['Hour'].astype(str)


# solar_pac_wesm_forecasts=solar_pac_calendar.merge(wesm_forecasts[['YearMonthDayIntervalID',
#                                                      'Base WESM',
#                                                      #'Adjusted WESM',
#                                                      #'High Adjusted WESM'
#                                                                  ]],on='YearMonthDayIntervalID',how='left')




# solar_pac_load_profiles_excel = pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\231116 Solar Pac Load Profiles.parquet')

# # solar_pac_load_profiles=solar_pac_calendar.merge(solar_pac_load_profiles_excel[['SolarPacSupplyID', 'KSPC 15MW','KSPC 20MW','SLPGC (Extension)',
# #                                                                                 'TVI','ANDA','ANDA (Profit Sharing)','VEC Bulacan','VEC Pangasinan',
# #                                                      'Solar Pacific',
# #                                                      'Isabela',
# #                                                      'Bataan','STORM','Sungrow','Technergy','HYPOTHETICAL BASELOAD','HYPOTHETICAL SOLAR','Solar Valley','RES','CC','Aries',
# #                                                                                'HYPOTHETICAL 25MW','MPC','Wind Farm','SEM-Calaca','LWEC-TBC','LWEC-TBC-67.2',
# #                                                                                 'SLPGC','SEM-Calaca-5MW','SEM-Calaca-7MW',]],on='SolarPacSupplyID',how='left')

# solar_pac_load_profiles=solar_pac_calendar.merge(solar_pac_load_profiles_excel[supply_load_list],on='SolarPacSupplyID',how='left')

# # ['SEM-Calaca', 'LWEC-TBC', 'LWEC-TBC-67.2', 'SLPGC', 'SEM-Calaca-5MW', 'SEM-Calaca-7MW']
# # solar_pac_load_profiles['Wind Farm']=0.7*solar_pac_load_profiles['Wind Farm'] #70%
# #Extending Simulations

# solar_pac_wesm_forecasts_supp_low=solar_pac_wesm_forecasts[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#        'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID']]
# solar_pac_wesm_forecasts_supp_mid = solar_pac_wesm_forecasts_supp_low.copy()
# solar_pac_wesm_forecasts_cc_mid = solar_pac_wesm_forecasts_supp_low.copy()


# last_wesm_supp_price = list(creatdie_gwap['Gen Prices']['Sim0'])[-1]

# solar_pac_gen_multipliers = solar_pac_wesm_forecasts.copy()

# solar_pac_gen_multipliers['WESM Mid']=solar_pac_gen_multipliers['Base WESM']/last_wesm_supp_price

# for i in range(1001):

#     last_wesm_supp_price_sim = list(creatdie_gwap['Gen Prices']['Sim'+str(i)])[-1]
#     solar_pac_wesm_forecasts_supp_mid['Sim'+str(i)]=solar_pac_gen_multipliers['WESM Mid']*last_wesm_supp_price_sim

#     last_wesm_cc_price_sim = list(creatdie_gwap['CC Prices']['Sim'+str(i)])[-1]
#     solar_pac_wesm_forecasts_cc_mid['Sim'+str(i)] = solar_pac_gen_multipliers['WESM Mid']*last_wesm_cc_price_sim

#     print('Sim'+str(i))

# solar_pac_wesm_forecasts_supp_mid=solar_pac_wesm_forecasts_supp_mid.dropna()
# solar_pac_wesm_forecasts_cc_mid=solar_pac_wesm_forecasts_cc_mid.dropna()

# solar_pac_wesm_forecasts_supp_mid=solar_pac_wesm_forecasts_supp_mid.reset_index()
# solar_pac_wesm_forecasts_cc_mid=solar_pac_wesm_forecasts_cc_mid.reset_index()

# del solar_pac_wesm_forecasts_supp_mid['index']
# del solar_pac_wesm_forecasts_cc_mid['index']

# # Creating File for the simulated 1000 scenarios
# # solar_pac_wesm_forecasts_supp_mid.to_csv('230804 Lantau CSV WESM Forecast.csv',index = False)

# #Uploading 1000 Customer Loads

# x_gwap2=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Customer X GWAP 1000 Sims CC Load.parquet')

# x_gwap=dict()

# x_gwap['CC Load']=x_gwap2



# #Creating a long-term calendar (customer)

# xs_calendar = calendar_db.loc[(calendar_db['Date']>=datetime.datetime(2022,12,26)) & (calendar_db['Date']<datetime.datetime(2048,12,26))]
# xs_calendar = xs_calendar.reset_index()
# del xs_calendar['index']

# xs_calendar['Year'] = xs_calendar['Date'].apply(lambda x:x.year)
# xs_calendar['Month'] = xs_calendar['Date'].apply(lambda x:x.month)


# blankdf = pd.DataFrame()
# blankdf['Delimiter'] = ["|"]*len(xs_calendar)

# xs_calendar['YearMonthIntervalID'] = xs_calendar['Year'].astype(str) + blankdf['Delimiter'] + xs_calendar['Month'].astype(str) + blankdf['Delimiter']+xs_calendar['Hour'].astype(str)
# xs_calendar['SolarPacSupplyID'] = xs_calendar['Billing Year'].astype(str) + blankdf['Delimiter'] + xs_calendar['Billing Month'].astype(str) + blankdf['Delimiter']+xs_calendar['Day'].astype(str)+ blankdf['Delimiter']+xs_calendar['Hour'].astype(str)




# #Uploading CC Load Profiles

# solar_pac_wesm_forecasts=solar_pac_calendar.merge(wesm_forecasts[['YearMonthDayIntervalID',
#                                                      'Base WESM'
#                                                                  ]],on='YearMonthDayIntervalID',how='left')


# solar_pac_cc_load_profiles_excel = pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\230120 Xs CC Load Profiles.parquet')

# solar_pac_cc_load_profiles=solar_pac_calendar.merge(solar_pac_cc_load_profiles_excel[['SolarPacSupplyID','Japan 25MW']],on='SolarPacSupplyID',how='left')


# solar_pac_cc_load_sim = solar_pac_cc_load_profiles[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#        'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID',
#        'SolarPacSupplyID']]


# #Creating 1000 load simulations

# last_cc_load = list(x_gwap['CC Load']['Sim0'])[-1]

# solar_pac_cc_load_multipliers=solar_pac_cc_load_sim.copy()
# solar_pac_cc_load_multipliers['Japan Multipliers']=solar_pac_cc_load_profiles['Japan 25MW']/last_cc_load
# solar_pac_cc_load_sim_japan=solar_pac_cc_load_sim.copy()



# for i in range(1001):

#     last_cc_load = list(x_gwap['CC Load']['Sim'+str(i)])[-1]
#     solar_pac_cc_load_sim_japan['Sim'+str(i)]=solar_pac_cc_load_multipliers['Japan Multipliers']*last_cc_load
#     print('Sim'+str(i))



# #Extension of Customer/Supply WESM Prices

# blankdf = pd.DataFrame()
# blankdf['Delimiter'] = ["|"]*len(solar_pac_wesm_forecasts_supp_low)

# solar_pac_wesm_forecasts_supp_mid['SolarPacSupplyID'] =solar_pac_wesm_forecasts_supp_mid['Billing Year'].astype(str) + blankdf['Delimiter'] + solar_pac_wesm_forecasts_supp_mid['Billing Month'].astype(str) + blankdf['Delimiter']+solar_pac_wesm_forecasts_supp_mid['Day'].astype(str)+ blankdf['Delimiter']+solar_pac_wesm_forecasts_supp_mid['Hour'].astype(str)
# solar_pac_wesm_forecasts_cc_mid['SolarPacSupplyID'] =solar_pac_wesm_forecasts_cc_mid['Billing Year'].astype(str) + blankdf['Delimiter'] + solar_pac_wesm_forecasts_cc_mid['Billing Month'].astype(str) + blankdf['Delimiter']+solar_pac_wesm_forecasts_cc_mid['Day'].astype(str)+ blankdf['Delimiter']+solar_pac_wesm_forecasts_cc_mid['Hour'].astype(str)


# #Extension of long-term calendar (customer)
# xs_calendar['SolarPacSupplyID'] = xs_calendar['Billing Year'].astype(str) + blankdf['Delimiter'] + xs_calendar['Billing Month'].astype(str) + blankdf['Delimiter']+xs_calendar['Day'].astype(str)+ blankdf['Delimiter']+xs_calendar['Hour'].astype(str)

# xv=xs_calendar.copy()

# delim=pd.DataFrame()
# delim['Delimiter'] =["|"]*len(xv)

# xv['YearMonthID']=xv['Year'].astype('str')+delim['Delimiter']+xv['Month'].astype('str')

hide_toggle('Black-Box Processing of Simulations for Long-Term Contracts (Time-Consuming)')

"""Creating Luzon Visayas Filter using location_db"""

cc_luzon_s = list(location_db[location_db['Grid'] == 'LUZON']['CCName'])

cc_visayas_s = list(location_db[location_db['Grid'] == 'VISAYAS']['CCName'])

index_active_cc_luzon = []

index_active_cc_visayas = []


for cc_luzon in cc_luzon_s:
    index = customer_db.index[customer_db['CCName'] == cc_luzon][0]
    index_active_cc_luzon.append(index)

print(index_active_cc_luzon)

for cc_visayas in cc_visayas_s:
    index = customer_db.index[customer_db['CCName'] == cc_visayas][0]
    index_active_cc_visayas.append(index)

print(index_active_cc_visayas)

"""## Loading Simulations Lantau Luzon"""

#Forecast type either "230606 WESM Forward Curve" or "230605 Lantau WESM Forward Curve"
# forecast_type = '230606 WESM Forward Curve'
# run_type = 'VEC'

# # Note: Base_WESM = '
# Base_WESM = 'Base WESM'

forecast_type = '230605 Lantau WESM Forward Curve with Lan_Vis,Lan_Luz'
run_type = 'Lantau'

#Note: Base_WESM = 'Base WESM',Base_WESM = 'LanVis Php/kWh',Base_WESM = 'LanLuz Php/kWh',
Base_WESM = 'LanLuz Php/kWh'

hide_toggle('Choosing Forecast Type WESM Forward Curve / Lantau')

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# #Uploading 1000 Customer Prices and 1000 Gen Prices
# creatdie_gwap1=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Creative Diecast GWAP 1000 Sims CC Prices.parquet')
# creatdie_gwap2=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Creative Diecast GWAP 1000 Sims CC Load.parquet')
# creatdie_gwap3=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Creative Diecast GWAP 1000 Sims Gen Prices.parquet')
# 
# 
# creatdie_gwap=dict()
# 
# creatdie_gwap['CC Prices']=creatdie_gwap1
# creatdie_gwap['CC Load']=creatdie_gwap2
# creatdie_gwap['Gen Prices']=creatdie_gwap3
# 
# 
# #Creating a long-term calendar (supply)
# solar_pac_calendar = calendar_db.loc[(calendar_db['Date']>=datetime.datetime(2021,12,26)) & (calendar_db['Date']<datetime.datetime(2060,12,26))]
# solar_pac_calendar = solar_pac_calendar.reset_index()
# del solar_pac_calendar['index']
# 
# solar_pac_calendar['Year'] = solar_pac_calendar['Date'].apply(lambda x:x.year)
# solar_pac_calendar['Month'] = solar_pac_calendar['Date'].apply(lambda x:x.month)
# 
# 
# blankdf = pd.DataFrame()
# blankdf['Delimiter'] = ["|"]*len(solar_pac_calendar)
# 
# solar_pac_calendar['YearMonthIntervalID'] = solar_pac_calendar['Year'].astype(str) + blankdf['Delimiter'] + solar_pac_calendar['Month'].astype(str) + blankdf['Delimiter']+solar_pac_calendar['Hour'].astype(str)
# solar_pac_calendar['SolarPacSupplyID'] = solar_pac_calendar['Billing Year'].astype(str) + blankdf['Delimiter'] + solar_pac_calendar['Billing Month'].astype(str) + blankdf['Delimiter']+solar_pac_calendar['Day'].astype(str)+ blankdf['Delimiter']+solar_pac_calendar['Hour'].astype(str)
# solar_pac_calendar['YearMonthDayIntervalID'] = solar_pac_calendar['Year'].astype(str) + blankdf['Delimiter'] + solar_pac_calendar['Month'].astype(str)+ blankdf['Delimiter'] + solar_pac_calendar['Day'].astype(str) + blankdf['Delimiter']+solar_pac_calendar['Hour'].astype(str)
# 
# 
# 
# 
# #Uploading WESM Forecasts
# wesm_forecasts = pd.read_parquet(fr'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\{forecast_type}.parquet')
# 
# 
# blankdf_gwap = pd.DataFrame()
# blankdf_gwap['Delimiter'] = ["|"]*len(wesm_forecasts)
# 
# wesm_forecasts['YearMonthDayIntervalID'] = wesm_forecasts['Year'].astype(str) + blankdf_gwap['Delimiter'] +wesm_forecasts['Month'].astype(str)+ blankdf_gwap['Delimiter']+wesm_forecasts['Day'].astype(str)+ blankdf_gwap['Delimiter']+wesm_forecasts['Hour'].astype(str)
# 
# 
# solar_pac_wesm_forecasts=solar_pac_calendar.merge(wesm_forecasts[['YearMonthDayIntervalID',
#                                                      f'{Base_WESM}',
#                                                      #'Adjusted WESM',
#                                                      #'High Adjusted WESM'
#                                                                  ]],on='YearMonthDayIntervalID',how='left')
# 
# 
# 
# 
# solar_pac_load_profiles_excel = pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\231116 Solar Pac Load Profiles.parquet')
# 
# # solar_pac_load_profiles=solar_pac_calendar.merge(solar_pac_load_profiles_excel[['SolarPacSupplyID', 'KSPC 15MW','KSPC 20MW','SLPGC (Extension)',
# #                                                                                 'TVI','ANDA','ANDA (Profit Sharing)','VEC Bulacan','VEC Pangasinan',
# #                                                      'Solar Pacific',
# #                                                      'Isabela',
# #                                                      'Bataan','STORM','Sungrow','Technergy','HYPOTHETICAL BASELOAD','HYPOTHETICAL SOLAR','Solar Valley','RES','CC','Aries',
# #                                                                                'HYPOTHETICAL 25MW','MPC','Wind Farm','SEM-Calaca','LWEC-TBC','LWEC-TBC-67.2',
# #                                                                                 'SLPGC','SEM-Calaca-5MW','SEM-Calaca-7MW',]],on='SolarPacSupplyID',how='left')
# 
# solar_pac_load_profiles=solar_pac_calendar.merge(solar_pac_load_profiles_excel[supply_load_list],on='SolarPacSupplyID',how='left')
# # ['SEM-Calaca', 'LWEC-TBC', 'LWEC-TBC-67.2', 'SLPGC', 'SEM-Calaca-5MW', 'SEM-Calaca-7MW']
# # solar_pac_load_profiles['Wind Farm']=0.7*solar_pac_load_profiles['Wind Farm'] #70%
# #Extending Simulations
# 
# solar_pac_wesm_forecasts_supp_low=solar_pac_wesm_forecasts[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#        'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID']]
# solar_pac_wesm_forecasts_supp_mid = solar_pac_wesm_forecasts_supp_low.copy()
# solar_pac_wesm_forecasts_cc_mid = solar_pac_wesm_forecasts_supp_low.copy()
# 
# 
# last_wesm_supp_price = list(creatdie_gwap['Gen Prices']['Sim0'])[-1]
# 
# solar_pac_gen_multipliers = solar_pac_wesm_forecasts.copy()
# 
# solar_pac_gen_multipliers['WESM Mid']=solar_pac_gen_multipliers[f'{Base_WESM}']/last_wesm_supp_price
# 
# for i in range(1001):
# 
#     last_wesm_supp_price_sim = list(creatdie_gwap['Gen Prices']['Sim'+str(i)])[-1]
#     solar_pac_wesm_forecasts_supp_mid['Sim'+str(i)]=solar_pac_gen_multipliers['WESM Mid']*last_wesm_supp_price_sim
# 
#     last_wesm_cc_price_sim = list(creatdie_gwap['CC Prices']['Sim'+str(i)])[-1]
#     solar_pac_wesm_forecasts_cc_mid['Sim'+str(i)] = solar_pac_gen_multipliers['WESM Mid']*last_wesm_cc_price_sim
# 
#     print('Sim'+str(i))
# 
# solar_pac_wesm_forecasts_supp_mid=solar_pac_wesm_forecasts_supp_mid.dropna()
# solar_pac_wesm_forecasts_cc_mid=solar_pac_wesm_forecasts_cc_mid.dropna()
# 
# solar_pac_wesm_forecasts_supp_mid=solar_pac_wesm_forecasts_supp_mid.reset_index()
# solar_pac_wesm_forecasts_cc_mid=solar_pac_wesm_forecasts_cc_mid.reset_index()
# 
# del solar_pac_wesm_forecasts_supp_mid['index']
# del solar_pac_wesm_forecasts_cc_mid['index']
# 
# # Creating File for the simulated 1000 scenarios
# solar_pac_wesm_forecasts_supp_mid.to_csv('230804 Lantau CSV WESM Forecast.csv',index = False)
# 
# #Uploading 1000 Customer Loads
# 
# x_gwap2=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Customer X GWAP 1000 Sims CC Load.parquet')
# 
# x_gwap=dict()
# 
# x_gwap['CC Load']=x_gwap2
# 
# 
# 
# #Creating a long-term calendar (customer)
# 
# xs_calendar = calendar_db.loc[(calendar_db['Date']>=datetime.datetime(2022,12,26)) & (calendar_db['Date']<datetime.datetime(2048,12,26))]
# xs_calendar = xs_calendar.reset_index()
# del xs_calendar['index']
# 
# xs_calendar['Year'] = xs_calendar['Date'].apply(lambda x:x.year)
# xs_calendar['Month'] = xs_calendar['Date'].apply(lambda x:x.month)
# 
# 
# blankdf = pd.DataFrame()
# blankdf['Delimiter'] = ["|"]*len(xs_calendar)
# 
# xs_calendar['YearMonthIntervalID'] = xs_calendar['Year'].astype(str) + blankdf['Delimiter'] + xs_calendar['Month'].astype(str) + blankdf['Delimiter']+xs_calendar['Hour'].astype(str)
# xs_calendar['SolarPacSupplyID'] = xs_calendar['Billing Year'].astype(str) + blankdf['Delimiter'] + xs_calendar['Billing Month'].astype(str) + blankdf['Delimiter']+xs_calendar['Day'].astype(str)+ blankdf['Delimiter']+xs_calendar['Hour'].astype(str)
# 
# 
# 
# 
# #Uploading CC Load Profiles
# 
# solar_pac_wesm_forecasts=solar_pac_calendar.merge(wesm_forecasts[['YearMonthDayIntervalID',
#                                                      f'{Base_WESM}'
#                                                                  ]],on='YearMonthDayIntervalID',how='left')
# 
# 
# solar_pac_cc_load_profiles_excel = pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\230120 Xs CC Load Profiles.parquet')
# 
# solar_pac_cc_load_profiles=solar_pac_calendar.merge(solar_pac_cc_load_profiles_excel[['SolarPacSupplyID','Japan 25MW']],on='SolarPacSupplyID',how='left')
# 
# 
# solar_pac_cc_load_sim = solar_pac_cc_load_profiles[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#        'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID',
#        'SolarPacSupplyID']]
# 
# 
# #Creating 1000 load simulations
# 
# last_cc_load = list(x_gwap['CC Load']['Sim0'])[-1]
# 
# solar_pac_cc_load_multipliers=solar_pac_cc_load_sim.copy()
# solar_pac_cc_load_multipliers['Japan Multipliers']=solar_pac_cc_load_profiles['Japan 25MW']/last_cc_load
# solar_pac_cc_load_sim_japan=solar_pac_cc_load_sim.copy()
# 
# 
# 
# for i in range(1001):
# 
#     last_cc_load = list(x_gwap['CC Load']['Sim'+str(i)])[-1]
#     solar_pac_cc_load_sim_japan['Sim'+str(i)]=solar_pac_cc_load_multipliers['Japan Multipliers']*last_cc_load
#     print('Sim'+str(i))
# 
# 
# 
# #Extension of Customer/Supply WESM Prices
# 
# blankdf = pd.DataFrame()
# blankdf['Delimiter'] = ["|"]*len(solar_pac_wesm_forecasts_supp_low)
# 
# solar_pac_wesm_forecasts_supp_mid['SolarPacSupplyID'] =solar_pac_wesm_forecasts_supp_mid['Billing Year'].astype(str) + blankdf['Delimiter'] + solar_pac_wesm_forecasts_supp_mid['Billing Month'].astype(str) + blankdf['Delimiter']+solar_pac_wesm_forecasts_supp_mid['Day'].astype(str)+ blankdf['Delimiter']+solar_pac_wesm_forecasts_supp_mid['Hour'].astype(str)
# solar_pac_wesm_forecasts_cc_mid['SolarPacSupplyID'] =solar_pac_wesm_forecasts_cc_mid['Billing Year'].astype(str) + blankdf['Delimiter'] + solar_pac_wesm_forecasts_cc_mid['Billing Month'].astype(str) + blankdf['Delimiter']+solar_pac_wesm_forecasts_cc_mid['Day'].astype(str)+ blankdf['Delimiter']+solar_pac_wesm_forecasts_cc_mid['Hour'].astype(str)
# 
# 
# #Extension of long-term calendar (customer)
# xs_calendar['SolarPacSupplyID'] = xs_calendar['Billing Year'].astype(str) + blankdf['Delimiter'] + xs_calendar['Billing Month'].astype(str) + blankdf['Delimiter']+xs_calendar['Day'].astype(str)+ blankdf['Delimiter']+xs_calendar['Hour'].astype(str)
# 
# xv=xs_calendar.copy()
# 
# delim=pd.DataFrame()
# delim['Delimiter'] =["|"]*len(xv)
# 
# xv['YearMonthID']=xv['Year'].astype('str')+delim['Delimiter']+xv['Month'].astype('str')
# 
# hide_toggle('Black-Box Processing of Simulations for Long-Term Contracts (Time-Consuming)')

"""## Simulating CC Luzon"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# for i in tqdm(index_active_cc_luzon[:round(len(index_active_cc_luzon)/2)]):
#     try:
#         cc_portfolio_valuation(cc_num=i,date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))
#         print(f'DONE-{i}')
#     except:
#         print(f'FAILED-{i}')
#         continue
# 
# run_counter = "LUZON"
# 
# npv_db.to_excel(date_today_reformat+f' NPVDatabase ({run_type})-{run_counter}-updateddates.xlsx',index=False)
# 
# print(f"{date_today_reformat} ({run_type})-{run_counter}")
# 
# hide_toggle('PROTOTYPE RUN LOOPS')

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# for i in tqdm(index_active_cc_luzon[round(len(index_active_cc_luzon)/2):]):
#     try:
#         cc_portfolio_valuation(cc_num=i,date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))
#         print(f'DONE-{i}')
#     except:
#         print(f'FAILED-{i}')
#         continue
# 
# run_counter = "LUZON"
# 
# npv_db.to_excel(date_today_reformat+f' NPVDatabase ({run_type})-{run_counter}-updateddates-0.5.xlsx',index=False)
# 
# print(f"{date_today_reformat} ({run_type})-{run_counter}")
# 
# hide_toggle('PROTOTYPE RUN LOOPS')
#

"""## Loading Simulations Lantau Visayas"""

#Forecast type either "230606 WESM Forward Curve" or "230605 Lantau WESM Forward Curve"
# forecast_type = '230606 WESM Forward Curve'
# run_type = 'VEC'

# # Note: Base_WESM = '
# Base_WESM = 'Base WESM'

forecast_type = '230605 Lantau WESM Forward Curve with Lan_Vis,Lan_Luz'
run_type = 'Lantau'

#Note: Base_WESM = 'Base WESM',Base_WESM = 'LanVis Php/kWh',Base_WESM = 'LanLuz Php/kWh',
Base_WESM = 'LanVis Php/kWh'

hide_toggle('Choosing Forecast Type WESM Forward Curve / Lantau')

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# #Uploading 1000 Customer Prices and 1000 Gen Prices
# creatdie_gwap1=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Creative Diecast GWAP 1000 Sims CC Prices.parquet')
# creatdie_gwap2=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Creative Diecast GWAP 1000 Sims CC Load.parquet')
# creatdie_gwap3=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Creative Diecast GWAP 1000 Sims Gen Prices.parquet')
# 
# 
# creatdie_gwap=dict()
# 
# creatdie_gwap['CC Prices']=creatdie_gwap1
# creatdie_gwap['CC Load']=creatdie_gwap2
# creatdie_gwap['Gen Prices']=creatdie_gwap3
# 
# 
# #Creating a long-term calendar (supply)
# solar_pac_calendar = calendar_db.loc[(calendar_db['Date']>=datetime.datetime(2021,12,26)) & (calendar_db['Date']<datetime.datetime(2060,12,26))]
# solar_pac_calendar = solar_pac_calendar.reset_index()
# del solar_pac_calendar['index']
# 
# solar_pac_calendar['Year'] = solar_pac_calendar['Date'].apply(lambda x:x.year)
# solar_pac_calendar['Month'] = solar_pac_calendar['Date'].apply(lambda x:x.month)
# 
# 
# blankdf = pd.DataFrame()
# blankdf['Delimiter'] = ["|"]*len(solar_pac_calendar)
# 
# solar_pac_calendar['YearMonthIntervalID'] = solar_pac_calendar['Year'].astype(str) + blankdf['Delimiter'] + solar_pac_calendar['Month'].astype(str) + blankdf['Delimiter']+solar_pac_calendar['Hour'].astype(str)
# solar_pac_calendar['SolarPacSupplyID'] = solar_pac_calendar['Billing Year'].astype(str) + blankdf['Delimiter'] + solar_pac_calendar['Billing Month'].astype(str) + blankdf['Delimiter']+solar_pac_calendar['Day'].astype(str)+ blankdf['Delimiter']+solar_pac_calendar['Hour'].astype(str)
# solar_pac_calendar['YearMonthDayIntervalID'] = solar_pac_calendar['Year'].astype(str) + blankdf['Delimiter'] + solar_pac_calendar['Month'].astype(str)+ blankdf['Delimiter'] + solar_pac_calendar['Day'].astype(str) + blankdf['Delimiter']+solar_pac_calendar['Hour'].astype(str)
# 
# 
# 
# 
# #Uploading WESM Forecasts
# wesm_forecasts = pd.read_parquet(fr'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\{forecast_type}.parquet')
# 
# 
# blankdf_gwap = pd.DataFrame()
# blankdf_gwap['Delimiter'] = ["|"]*len(wesm_forecasts)
# 
# wesm_forecasts['YearMonthDayIntervalID'] = wesm_forecasts['Year'].astype(str) + blankdf_gwap['Delimiter'] +wesm_forecasts['Month'].astype(str)+ blankdf_gwap['Delimiter']+wesm_forecasts['Day'].astype(str)+ blankdf_gwap['Delimiter']+wesm_forecasts['Hour'].astype(str)
# 
# 
# solar_pac_wesm_forecasts=solar_pac_calendar.merge(wesm_forecasts[['YearMonthDayIntervalID',
#                                                      f'{Base_WESM}',
#                                                      #'Adjusted WESM',
#                                                      #'High Adjusted WESM'
#                                                                  ]],on='YearMonthDayIntervalID',how='left')
# 
# solar_pac_load_profiles_excel = pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\231116 Solar Pac Load Profiles.parquet')
# 
# solar_pac_load_profiles=solar_pac_calendar.merge(solar_pac_load_profiles_excel[supply_load_list],on='SolarPacSupplyID',how='left')
# 
# # ['SEM-Calaca', 'LWEC-TBC', 'LWEC-TBC-67.2', 'SLPGC', 'SEM-Calaca-5MW', 'SEM-Calaca-7MW']
# # solar_pac_load_profiles['Wind Farm']=0.7*solar_pac_load_profiles['Wind Farm'] #70
# 
# #Extending Simulations
# 
# solar_pac_wesm_forecasts_supp_low=solar_pac_wesm_forecasts[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#        'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID']]
# solar_pac_wesm_forecasts_supp_mid = solar_pac_wesm_forecasts_supp_low.copy()
# solar_pac_wesm_forecasts_cc_mid = solar_pac_wesm_forecasts_supp_low.copy()
# 
# 
# last_wesm_supp_price = list(creatdie_gwap['Gen Prices']['Sim0'])[-1]
# 
# solar_pac_gen_multipliers = solar_pac_wesm_forecasts.copy()
# 
# solar_pac_gen_multipliers['WESM Mid']=solar_pac_gen_multipliers[f'{Base_WESM}']/last_wesm_supp_price
# 
# for i in range(1001):
# 
#     last_wesm_supp_price_sim = list(creatdie_gwap['Gen Prices']['Sim'+str(i)])[-1]
#     solar_pac_wesm_forecasts_supp_mid['Sim'+str(i)]=solar_pac_gen_multipliers['WESM Mid']*last_wesm_supp_price_sim
# 
#     last_wesm_cc_price_sim = list(creatdie_gwap['CC Prices']['Sim'+str(i)])[-1]
#     solar_pac_wesm_forecasts_cc_mid['Sim'+str(i)] = solar_pac_gen_multipliers['WESM Mid']*last_wesm_cc_price_sim
# 
#     print('Sim'+str(i))
# 
# solar_pac_wesm_forecasts_supp_mid=solar_pac_wesm_forecasts_supp_mid.dropna()
# solar_pac_wesm_forecasts_cc_mid=solar_pac_wesm_forecasts_cc_mid.dropna()
# 
# solar_pac_wesm_forecasts_supp_mid=solar_pac_wesm_forecasts_supp_mid.reset_index()
# solar_pac_wesm_forecasts_cc_mid=solar_pac_wesm_forecasts_cc_mid.reset_index()
# 
# del solar_pac_wesm_forecasts_supp_mid['index']
# del solar_pac_wesm_forecasts_cc_mid['index']
# 
# # Creating File for the simulated 1000 scenarios
# # solar_pac_wesm_forecasts_supp_mid.to_csv('230804 Lantau CSV WESM Forecast.csv',index = False)
# 
# #Uploading 1000 Customer Loads
# 
# x_gwap2=pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\220309 Customer X GWAP 1000 Sims CC Load.parquet')
# 
# x_gwap=dict()
# 
# x_gwap['CC Load']=x_gwap2
# 
# 
# 
# #Creating a long-term calendar (customer)
# 
# xs_calendar = calendar_db.loc[(calendar_db['Date']>=datetime.datetime(2022,12,26)) & (calendar_db['Date']<datetime.datetime(2048,12,26))]
# xs_calendar = xs_calendar.reset_index()
# del xs_calendar['index']
# 
# xs_calendar['Year'] = xs_calendar['Date'].apply(lambda x:x.year)
# xs_calendar['Month'] = xs_calendar['Date'].apply(lambda x:x.month)
# 
# 
# blankdf = pd.DataFrame()
# blankdf['Delimiter'] = ["|"]*len(xs_calendar)
# 
# xs_calendar['YearMonthIntervalID'] = xs_calendar['Year'].astype(str) + blankdf['Delimiter'] + xs_calendar['Month'].astype(str) + blankdf['Delimiter']+xs_calendar['Hour'].astype(str)
# xs_calendar['SolarPacSupplyID'] = xs_calendar['Billing Year'].astype(str) + blankdf['Delimiter'] + xs_calendar['Billing Month'].astype(str) + blankdf['Delimiter']+xs_calendar['Day'].astype(str)+ blankdf['Delimiter']+xs_calendar['Hour'].astype(str)
# 
# 
# 
# 
# #Uploading CC Load Profiles
# 
# solar_pac_wesm_forecasts=solar_pac_calendar.merge(wesm_forecasts[['YearMonthDayIntervalID',
#                                                      f'{Base_WESM}'
#                                                                  ]],on='YearMonthDayIntervalID',how='left')
# 
# 
# solar_pac_cc_load_profiles_excel = pd.read_parquet(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\230120 Xs CC Load Profiles.parquet')
# 
# solar_pac_cc_load_profiles=solar_pac_calendar.merge(solar_pac_cc_load_profiles_excel[['SolarPacSupplyID','Japan 25MW']],on='SolarPacSupplyID',how='left')
# 
# 
# solar_pac_cc_load_sim = solar_pac_cc_load_profiles[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#        'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID',
#        'SolarPacSupplyID']]
# 
# 
# #Creating 1000 load simulations
# 
# last_cc_load = list(x_gwap['CC Load']['Sim0'])[-1]
# 
# solar_pac_cc_load_multipliers=solar_pac_cc_load_sim.copy()
# solar_pac_cc_load_multipliers['Japan Multipliers']=solar_pac_cc_load_profiles['Japan 25MW']/last_cc_load
# solar_pac_cc_load_sim_japan=solar_pac_cc_load_sim.copy()
# 
# 
# 
# for i in range(1001):
# 
#     last_cc_load = list(x_gwap['CC Load']['Sim'+str(i)])[-1]
#     solar_pac_cc_load_sim_japan['Sim'+str(i)]=solar_pac_cc_load_multipliers['Japan Multipliers']*last_cc_load
#     print('Sim'+str(i))
# 
# 
# 
# #Extension of Customer/Supply WESM Prices
# 
# blankdf = pd.DataFrame()
# blankdf['Delimiter'] = ["|"]*len(solar_pac_wesm_forecasts_supp_low)
# 
# solar_pac_wesm_forecasts_supp_mid['SolarPacSupplyID'] =solar_pac_wesm_forecasts_supp_mid['Billing Year'].astype(str) + blankdf['Delimiter'] + solar_pac_wesm_forecasts_supp_mid['Billing Month'].astype(str) + blankdf['Delimiter']+solar_pac_wesm_forecasts_supp_mid['Day'].astype(str)+ blankdf['Delimiter']+solar_pac_wesm_forecasts_supp_mid['Hour'].astype(str)
# solar_pac_wesm_forecasts_cc_mid['SolarPacSupplyID'] =solar_pac_wesm_forecasts_cc_mid['Billing Year'].astype(str) + blankdf['Delimiter'] + solar_pac_wesm_forecasts_cc_mid['Billing Month'].astype(str) + blankdf['Delimiter']+solar_pac_wesm_forecasts_cc_mid['Day'].astype(str)+ blankdf['Delimiter']+solar_pac_wesm_forecasts_cc_mid['Hour'].astype(str)
# 
# 
# #Extension of long-term calendar (customer)
# xs_calendar['SolarPacSupplyID'] = xs_calendar['Billing Year'].astype(str) + blankdf['Delimiter'] + xs_calendar['Billing Month'].astype(str) + blankdf['Delimiter']+xs_calendar['Day'].astype(str)+ blankdf['Delimiter']+xs_calendar['Hour'].astype(str)
# 
# xv=xs_calendar.copy()
# 
# delim=pd.DataFrame()
# delim['Delimiter'] =["|"]*len(xv)
# 
# xv['YearMonthID']=xv['Year'].astype('str')+delim['Delimiter']+xv['Month'].astype('str')
# 
# hide_toggle('Black-Box Processing of Simulations for Long-Term Contracts (Time-Consuming)')

"""## Simulating CC Visayas"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# for i in index_active_cc_visayas:
#     try:
#         cc_portfolio_valuation(cc_num=i,date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))
#         print(f'DONE-{i}')
#     except:
#         print(f'FAILED-{i}')
#         continue
# 
# run_counter = "VISAYAS"
# 
# npv_db.to_excel(date_today_reformat+f' NPVDatabase ({run_type})-{run_counter}-updateddates.xlsx',index=False)
# 
# print(f"{date_today_reformat} ({run_type})-{run_counter}")
# 
# hide_toggle('PROTOTYPE RUN LOOPS')

"""## Contract Checking for Updated MQ"""

# list((customer_db[((customer_db['EndDate']>='2023-09-04')& (customer_db['StartDate']<='2028-06-25'))])['CCName']) #till

# Pipelines = ['EMS MQ','IMCC-1','Park Centrale Tower','Neltex','Golden Great','Oversea Feeds']

Pipelines = [
    'EMS MQ','IMCC-1',
             # 'UST Load',
             # 'CustomerX-70%',
             # 'CustomerY-70%',
            ]

# Pipelines = list(customer_db['CCName'][-10:])

# Signed_CCs = ['EMS (Renewal)', '557 Feathermeal (Renewal)', 'Light Rail Manila',
#                'GGPC (Renewal) IV', 'AICE2', 'AICE3', 'Tarlac Mall A',
#               'Supercast (Renewal) A', 'C&S',  'Fast Logistics', 'HEVA Rizal',
#                  'Pioneer Center A','Vitarich','Yiking Plastic A','EMS A',
#                  'Kings Quality','EIDC-6.4','Polaris A','Aeonprime A','Excel Towers A','Creative Diecast-6.5', 'One Montage',
#               'IMCC-1','IMCC-2','Park Centrale Tower','Neltex','CAM_MQ','Golden Great','Oversea Feeds']

# [item for item in Signed_CCs if item not in Pipelines]


Signed_CCs = ['557 Feathermeal (Renewal) MQ', 'Light Rail Manila',
               'GGPC MQ', 'AICE4', 'Tarlac Mall A',
              'Supercast MQ', 'CASADI',  'Fast Logistics', 'HEVA Rizal','HEVA Iloilo',
                 'Pioneer Center A','Vitarich MQ','Yiking MQ','EMS MQ',
                 'Kings Quality','EIDC MQ','Polaris A','Aeonprime A',
              'Excel Towers A','Creative Diecast-6.5 MQ', 'One Montage',
              # 'IMCC-1',
              # ,'Park Centrale Tower'
              # ,'Neltex','Golden Great','Oversea Feeds',
              'Fong Shan A','Treasure Island','TIIC-Pilit','CAM MQ',
              # 'UST Load',
              # 'May Harvest',
              # # # 'CustomerX-5MW-70%',
              # 'CustomerX-70%',
              # 'CustomerY-70%',
              # 'CustomerY-70%-A',
             ] #


Signed_Supplys = ['TVI','LWEC-VENA-50MW', 'SSREC','SEM-Calaca-5MW',
                  # 'SIAEC-Jun',
                  # 'SIAEC-B',
                  # 'Solar-A','GENCO-5MW',
                  # 'GENCO-5MW-A'
                 ] #'LWEC-VENA-50MW','GENCO-5MW'

# + list(supplier_db['SupplierName'])[7:-2]
# Signed_Supplys = list(supplier_db['SupplierName'])[7:-2] + ['LWEC-VENA-50MW']

Signed_WESMplus = ['Creative Diecast', 'HEVA Iloilo', 'CAM Mechatronic', 'Fast Services',
                    'Calypso', 'Fong Shan', 'GGPC (Renewal) III', 'AICE', 'EIDC', 'Danao Paper Mill',
                    'LHAI (Renewal)', 'Tarlac Mall (Renewal)', 'Yiking Plastic','EMS MQ'
                    'Citiplas Plastic (Renewal)', 'Aeonprime', 'Polaris', '557 Feathermeal (WESM+)',
                    'Vitarich (WESM+)', 'Asian Plastic 1 (WESM+)', 'Asian Plastic 2 (WESM+)',
                    'Pioneer Center (WESM+)', 'HEVA Rizal (WESM+)', 'HEVA Iloilo (WESM+)', 'Treasure Island (WESM+)']

Active_CCs = list((customer_db[(customer_db['EndDate']>= str(date_today)[:-9])]['CCName']))
# print(Active_CCs)

Active_Suppliers = list((supplier_db[(supplier_db['EndDate']>= str(date_today)[:-9])]['SupplierName']))

# Active_CCs = list((customer_db[(customer_db['EndDate']>=str(date_today)) & (customer_db['StartDate']<=str(date_toggle)) ]['CCName']))
# # print(Active_CCs)

# Active_Suppliers = list((supplier_db[(supplier_db['EndDate']>=str(date_today))& (supplier_db['StartDate']<=str(date_toggle))]['SupplierName']))



print(f'Simulation Start Date = {date_today}')

print('.........................')

List_Active_Contracts = []
List_Active_Suppliers = []
List_Active_WESMplus = []

List_Expired_Inactive_Contracts = []
List_Expired_Inactive_Suppliers = []
List_Expired_Inactive_WESMplus = []

index_active_cc = []
index_active_supplier = []
index_active_wesmplus = []
index_pipeline = []

index_to_delete_cc = []
index_to_delete_supplier = []
index_to_delete_wesmplus = []



for Signed_WESM in Signed_WESMplus:
    if Signed_WESM in Active_CCs:
        print(f'{Signed_WESM} - Active WESM')
        List_Active_WESMplus.append(Signed_WESM)

    else:
        print(f'{Signed_WESM} - Expired/Inactive**************')
        List_Expired_Inactive_WESMplus.append(Signed_WESM)


for Signed_Supply in Signed_Supplys:
    if Signed_Supply in Active_Suppliers:
        print(f'{Signed_Supply} - Active')
        List_Active_Suppliers.append(Signed_Supply)

    else:
        print(f'{Signed_Supply} - Expired/Inactive**************')
        List_Expired_Inactive_Suppliers.append(Signed_Supply)



print('.........................')

print('.........................')

for Signed_CC in Signed_CCs:
    if Signed_CC in Active_CCs:
        print(f'{Signed_CC} - Active')
        List_Active_Contracts.append(Signed_CC)

    else:
        print(f'{Signed_CC} - Expired/Inactive**************')
        List_Expired_Inactive_Contracts.append(Signed_CC)

print('.........................')


print('.........................')



for List_Active_Contract in List_Active_Contracts:
    index = customer_db.index[customer_db['CCName'] == List_Active_Contract][0]
    index_active_cc.append(index)

print(f"Index to Active CC: {index_active_cc}")

print(f'Active CC Contracts = {List_Active_Contracts}')

print('.........................')

for List_Active_Supplier in List_Active_Suppliers:
    index = supplier_db.index[supplier_db['SupplierName'] == List_Active_Supplier][0]
    index_active_supplier.append(index)

print(f"Index to Active Supplier: {index_active_supplier}")
print(f'Active Supplier Contracts = {List_Active_Suppliers}')

print('.........................')

#WESM
for List_Active_WESM in List_Active_WESMplus:
    index = customer_db.index[customer_db['CCName'] == List_Active_WESM][0]
    index_active_wesmplus.append(index)

print(f"Index to Active WESMplus: {index_active_wesmplus}")
print(f'Active WESMplus Contracts = {List_Active_WESMplus}')

print('.........................')

for List_Expired_Inactive_Supplier in List_Expired_Inactive_Suppliers:
    index = supplier_db.index[supplier_db['SupplierName'] == List_Expired_Inactive_Supplier][0]
    index_to_delete_supplier.append(index)

print(f"Index to delete Supplier: {index_to_delete_supplier}")
print(f'Expired Supplier Contracts = {List_Expired_Inactive_Suppliers}')


print('.........................')



for List_Expired_Inactive_Contract in List_Expired_Inactive_Contracts:
    index = customer_db.index[customer_db['CCName'] == List_Expired_Inactive_Contract][0]
    index_to_delete_cc.append(index)

print(f"Index to delete CC: {index_to_delete_cc}")
print(f'Expired CC Contracts = {List_Expired_Inactive_Contracts}')

print('.........................')

# for List_Expired_Inactive_WESM in List_Expired_Inactive_WESMplus:
#     index = customer_db.index[customer_db['CCName'] == List_Expired_Inactive_WESM][0]
#     index_to_delete_wesmplus.append(index)

# print(f"Index to delete WESMplus: {index_to_delete_wesmplus}")
# print(f'Expired WESMplus Contracts = {List_Expired_Inactive_WESMplus}')


#CREATING AUTOMATED SORTED LIST FOR NPV WITHOUT PIPELINES

main_list = (List_Active_Contracts) + (List_Active_Suppliers)


npv_list = [item for item in main_list if item not in Pipelines]


npv_df = pd.DataFrame(npv_list)

#creating a sort dataframe getting dates from customer_db and supplier_db

sort_df = pd.DataFrame(columns = ['Contracts','Start Date','End Date'])

#customer
# new_data = {'Contracts': npv_list[0] ,
#             'Start Date': str(customer_db[customer_db['CCName'] == str(npv_list[0])].iloc[0]['StartDate']).strip()[:-9]
#             , 'End Date': str(customer_db[customer_db['CCName'] == str(npv_list[0])].iloc[0]['EndDate']).strip()[:-9]}

#supplier
# new_data = {'Contracts': npv_list[0] ,
#             'Start Date': str(customer_db[customer_db['SupplierName'] == str(npv_list[0])].iloc[0]['StartDate']).strip()[:-9]
#             , 'End Date': str(customer_db[customer_db['SupplierName'] == str(npv_list[0])].iloc[0]['EndDate']).strip()[:-9]}


# sort_df.loc[0] = new_data

for i in npv_list:
    try:
        new_data = {'Contracts': npv_list[(npv_df[npv_df[0] == str(i)].index)[0]] ,
                'Start Date': str(customer_db[customer_db['CCName'] == str(npv_list[(npv_df[npv_df[0] == str(i)].index)[0]])].iloc[0]['StartDate']).strip()[:-9]
                , 'End Date': str(customer_db[customer_db['CCName'] == str(npv_list[(npv_df[npv_df[0] == str(i)].index)[0]])].iloc[0]['EndDate']).strip()[:-9]}

        sort_df.loc[(npv_df[npv_df[0] == str(i)].index)[0]] = new_data

    except:
        new_data = {'Contracts': npv_list[(npv_df[npv_df[0] == str(i)].index)[0]] ,
            'Start Date': str(supplier_db[supplier_db['SupplierName'] == str(npv_list[(npv_df[npv_df[0] == str(i)].index)[0]])].iloc[0]['StartDate']).strip()[:-9]
            , 'End Date': str(supplier_db[supplier_db['SupplierName'] == str(npv_list[(npv_df[npv_df[0] == str(i)].index)[0]])].iloc[0]['EndDate']).strip()[:-9]}


        sort_df.loc[(npv_df[npv_df[0] == str(i)].index)[0]] = new_data



sort_df = sort_df.sort_values(by='Start Date')

theNPVLIST = list(sort_df['Contracts'])

for Pipeline in Pipelines:
    index = customer_db.index[customer_db['CCName'] == Pipeline][0]
    index_pipeline.append(index)

print(f"Index Pipelines: {index_pipeline}")

theNPVLIST

# index = customer_db.index[customer_db['CCName'] == 'Fast Services'][0]
# print("Index:", index)



###CREATING AUTOMATED SORTED LIST FOR NPV WITH PIPELINES

main_list1 = (List_Active_Contracts) + (List_Active_Suppliers) + Pipelines


# npv_list = [item for item in main_list if item not in Pipelines]


npv_df = pd.DataFrame(main_list1)

#creating a sort dataframe getting dates from customer_db and supplier_db

sort_df = pd.DataFrame(columns = ['Contracts','Start Date','End Date'])

#customer
# new_data = {'Contracts': npv_list[0] ,
#             'Start Date': str(customer_db[customer_db['CCName'] == str(npv_list[0])].iloc[0]['StartDate']).strip()[:-9]
#             , 'End Date': str(customer_db[customer_db['CCName'] == str(npv_list[0])].iloc[0]['EndDate']).strip()[:-9]}

#supplier
# new_data = {'Contracts': npv_list[0] ,
#             'Start Date': str(customer_db[customer_db['SupplierName'] == str(npv_list[0])].iloc[0]['StartDate']).strip()[:-9]
#             , 'End Date': str(customer_db[customer_db['SupplierName'] == str(npv_list[0])].iloc[0]['EndDate']).strip()[:-9]}


# sort_df.loc[0] = new_data

for i in main_list1:
    try:
        new_data = {'Contracts': main_list1[(npv_df[npv_df[0] == str(i)].index)[0]] ,
                'Start Date': str(customer_db[customer_db['CCName'] == str(main_list1[(npv_df[npv_df[0] == str(i)].index)[0]])].iloc[0]['StartDate']).strip()[:-9]
                , 'End Date': str(customer_db[customer_db['CCName'] == str(main_list1[(npv_df[npv_df[0] == str(i)].index)[0]])].iloc[0]['EndDate']).strip()[:-9]}

        sort_df.loc[(npv_df[npv_df[0] == str(i)].index)[0]] = new_data

    except:
        new_data = {'Contracts': main_list1[(npv_df[npv_df[0] == str(i)].index)[0]] ,
            'Start Date': str(supplier_db[supplier_db['SupplierName'] == str(main_list1[(npv_df[npv_df[0] == str(i)].index)[0]])].iloc[0]['StartDate']).strip()[:-9]
            , 'End Date': str(supplier_db[supplier_db['SupplierName'] == str(main_list1[(npv_df[npv_df[0] == str(i)].index)[0]])].iloc[0]['EndDate']).strip()[:-9]}


        sort_df.loc[(npv_df[npv_df[0] == str(i)].index)[0]] = new_data

sort_df = sort_df.sort_values(by='Start Date')

theNPVPIPELIST = list(sort_df['Contracts'])

# for Pipeline in Pipelines:
#     index = customer_db.index[customer_db['CCName'] == Pipeline][0]
#     index_pipeline.append(index)

# print(f"Index Pipelines: {index_pipeline}")

theNPVLIST

"""## Prototype Simulation Testing using Loops"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# for i in index_active_cc:
#     try:
#         cc_portfolio_valuation(cc_num=i,date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))
#         print(f'DONE-{i}')
#     except:
#         print(f'FAILED-{i}')
#         continue
# 
# run_counter = "1"
# 
# npv_db.to_excel(date_today_reformat+f' NPVDatabase ({run_type})-{run_counter}-updateddates1.xlsx',index=False)
# 
# print(f"{date_today_reformat} ({run_type})-{run_counter}")
# 
# hide_toggle('PROTOTYPE RUN LOOPS')
#

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# for i in index_active_supplier:
#     try:
#         supplier_portfolio_valuation(supp_num=i, date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))
#         print(f'DONE-{i}')
#     except:
#         print(f'FAILED-{i}')
#         continue
# 
# run_counter = "1"
# 
# npv_db.to_excel(date_today_reformat+f' NPVDatabase ({run_type})-{run_counter}.xlsx',index=False)
# 
# print(f"{date_today_reformat} ({run_type})-{run_counter}")
# 
# List_Active_Contracts + List_Active_Suppliers
# 
# hide_toggle('PROTOTYPE RUN LOOPS')

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# for i in index_pipeline:
#     try:
#         cc_portfolio_valuation(cc_num=i,date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))
#         print(f'DONE-{i}')
#     except:
#         print(f'FAILED-{i}')
#         continue
# run_counter = "1"
# 
# npv_db.to_excel(date_today_reformat+f' NPVDatabase ({run_type})-{run_counter}-pipeline.xlsx',index=False)
# 
# print(f"{date_today_reformat} ({run_type})-{run_counter}")
#

cc_portfolio_valuation(cc_num=102,date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))
cc_portfolio_valuation(cc_num=86,date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))


supplier_portfolio_valuation(supp_num=24, date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))

# supplier_portfolio_valuation(supp_num=1, date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))
# supplier_portfolio_valuation(supp_num=2, date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))

# supplier_portfolio_valuation(supp_num=25, date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))
# supplier_portfolio_valuation(supp_num=26, date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))
# supplier_portfolio_valuation(supp_num=27, date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))
# supplier_portfolio_valuation(supp_num=28, date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))

# cc_portfolio_valuation(cc_num=101,date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))

"""## Running Pipelines"""

# %%time

# for i in index_pipeline:
#     try:
#         cc_portfolio_valuation(cc_num=i,date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))
#         print(f'DONE-{i}')
#     except:
#         print(f'FAILED-{i}')
#         continue
# run_counter = "1"

# npv_db.to_excel(date_today_reformat+f' NPVDatabase ({run_type})-{run_counter}-pipeline.xlsx',index=False)

# print(f"{date_today_reformat} ({run_type})-{run_counter}")

"""## Save Updated Customer Load and Net Present Value Database"""

cc_load.to_parquet(date_today_reformat+' CC Load.parquet',index=False)
npv_db.to_parquet(date_today_reformat+f' NPVDatabase ({run_type}).parquet',index=False)


# npv_db.to_parquet(date_today_reformat+f' DashNPV ({run_type}).parquet',index=False)


print(date_today_reformat+f' NPVDatabase ({run_type}).parquet')
hide_toggle('Save Work')

# npv_db = pd.read_parquet(fr'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\{date_today_reformat} NPVDatabase (VEC).parquet')
# print(f"{date_today_reformat} NPVDatabase ({run_type})- DONE")

# npv_list = [item for item in main_list if item not in Pipelines]

# npv_db = npv_db[theNPVLIST + list(['CAM MQ'])]

# npv_db = npv_db[theNPVLIST]

# npv_db = npv_db[Pipelines]

theNPVLIST
# Pipelines

"""## Displaying RAROC"""

# npv_db = npv_db[theNPVLIST + list([
#     # 'SIAEC-Jun',
#                                    # 'CustomerX-70%',
#                                    # 'May Harvest',
#                                   ])]
# npv_db = npv_db[theNPVLIST + list(['SIAEC-Jun','May Harvest'])]
# npv_db = npv_db[theNPVLIST + list(['UST','SIAEC-Aug'])]
# npv_db = npv_db[theNPVLIST + list(['UST','SIAEC-Oct'])]
# npv_db = npv_db[theNPVLIST + list(['CustomerX-70%','SIAEC'])]

npv_db = npv_db[theNPVLIST]
raroc=raroc_results(0,'Portfolio as of ' + date_today_reformat, 0)
#
#For the first input above "raroc", key-in the column number
#of the last contract that is currently on-going in CORE

#To check the list of contracts that have net present values after step 7,
#feel free to key-in "npv_db.columns"

raroc=raroc.replace(0, '')


# raroc=raroc.replace('₱0.00', 'LR Exc')

# raroc=raroc.replace('₱42.00', 'LR Exc')

# raroc=raroc.replace('Japan 25MW', 'Minebea Mitsumi')

# raroc=raroc.replace('Portfolio as of 230711', "Portfolio as of July 31, 2023")

raroc['Line Rental Cap per kWh'] = 'LR EX'

# raroc['Contract Price per kWh'] = raroc['Contract Price per kWh'].replace('₱', '')

customer_db1 = customer_db
supplier_db1 = supplier_db
customer_list = list(raroc['Customer'])

supply_list = []
failed_toappend_list = []
failed_load_factor_list = []

for i in customer_list:

    try:
        enddate =str(customer_db1[customer_db1['CCName'] == str(i)].iloc[0]['EndDate']).strip()[:10]
        indexdate = raroc[raroc['Customer']==str(i)].index[0]
        raroc.at[indexdate, 'End Date'] = enddate
    except:
        supply_list.append(str(i))
        continue

for i in supply_list:
    try:
        enddate =str(supplier_db1[supplier_db1['SupplierName'] == str(i)].iloc[0]['EndDate']).strip()[:10]
        indexdate = raroc[raroc['Customer']==str(i)].index[0]
        raroc.at[indexdate, 'End Date'] = enddate
    except:
        failed_toappend_list.append(str(i))
        continue

for i in supply_list:
    try:
        loadfactor1 = str(round((np.mean(solar_pac_load_profiles[str(i)])/np.max(solar_pac_load_profiles[str(i)]))*100)) + '%'
        indexdate = raroc[raroc['Customer']==str(i)].index[0]
        raroc.at[indexdate, 'Load Factor'] = loadfactor1
    except:
        failed_load_factor_list.append(str(i))
        continue

print(failed_toappend_list)
print(failed_load_factor_list)

raroc['Contract Price per kWh'] =raroc['Contract Price per kWh'].str.replace('₱','')


raroc['Cumulative NPV'] =raroc['Cumulative NPV'].str.replace('₱','').str.replace(' M','')
raroc['Cumulative VAR'] =raroc['Cumulative VAR'].str.replace('₱','').str.replace(' M','')
raroc['Cumulative 5th Percentile'] =raroc['Cumulative 5th Percentile'].str.replace('₱','').str.replace(' M','')


raroc = raroc.rename(columns = {'Contract Price per kWh':'Contract Price PHP per kWh','Cumulative NPV':'Cumulative NPV (PHP Mil)', 'Cumulative VAR':'Cumulative VAR (PHP Mil)',
       'Cumulative 5th Percentile':'Cumulative 5th Percentile (PHP Mil)'})

for i in list(supplier_db['SupplierName']):
    try:
        supply_index = raroc[raroc['Customer'] == str(i)].index[0]

#         raroc.at[supply_index, 'Peak Load (MW)']

        # raroc.at[supply_index,'Peak Supply (MW)'] = raroc.at[supply_index, 'Peak Load (MW)']
        raroc.at[supply_index,'Peak Supply (MW)'] = round(np.max(solar_pac_load_profiles[str(i)]),2)

        raroc.at[supply_index,'Peak Load (MW)'] = ''

    except:
        print(f'Failed to change {i}')
        continue

raroc['Peak Supply (MW)'] = raroc['Peak Supply (MW)'].replace(np.nan, '')

for i in list(customer_db['CCName']):
    try:
        supply_index = raroc[raroc['Customer'] == str(i)].index[0]

#         raroc.at[supply_index, 'Peak Load (MW)']

        # raroc.at[supply_index,'Peak Supply (MW)'] = raroc.at[supply_index, 'Peak Load (MW)']
        raroc.at[supply_index,'Peak Load @ Month-Hr'] = str(pd.DataFrame(cc_load.loc[cc_load[str(i)].idxmax()]).T['Month_Hr'].iloc[0])

        # raroc.at[supply_index,'Peak Load (MW)'] = pd.DataFrame(cc_load.loc[cc_load[str(i)].idxmax()]).T['Month_Hr'].iloc[0]
        print(f'Updated peak Month-Hr {i}')
    except:
        # raroc.at[supply_index,'Peak @ Month-Hr'] = str('')
        # print(f'Failed to change peak Month-Hr {i}')

        # raroc.at[supply_index,'Peak @ Month-Hr'] = ''
        continue

raroc['Peak Load @ Month-Hr'] = raroc['Peak Load @ Month-Hr'].astype(str).replace('nan','')

raroc = raroc[['Customer', 'Start Date', 'End Date', 'Tenor (Years)',
       'Contract Price PHP per kWh', 'Line Rental Cap per kWh',
       'Peak Load (MW)','Peak Load @ Month-Hr', 'Load Factor', 'Peak Supply (MW)', 'Cumulative RAROC',
       'Cumulative NPV (PHP Mil)', 'Cumulative VAR (PHP Mil)',
       'Cumulative 5th Percentile (PHP Mil)']]



# raroc = raroc.sort_values(by='Start Date')

# raroc['Start Date'] = pd.to_datetime(raroc['Start Date'])
# raroc['End Date'] = pd.to_datetime(raroc['End Date'])

# raroc['Tenor (Years)'] = round((raroc['End Date'] - raroc['Start Date']).dt.days / 365, 1)

# raroc=raroc['Peak @ Month-Hr'].fillna['']
raroc.to_excel(f'raroc {date_today_reformat}.xlsx',index = False)

hide_toggle('RAROC Results')

raroc

"""# Load and Price Optimization Automation

## Load Optimization
"""

def optimization_load(init_loadx):
    global npv_db
    cc_load['CustomerX-70%'] = (cc_load['CustomerX-70%']/np.max(cc_load['CustomerX-70%'])) * init_loadx

    cc_index1 = customer_db[customer_db['CCName']=='CustomerX-70%'].index[0]

    print('running simulation cust-x')

    cc_portfolio_valuation(cc_num=cc_index1,date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))

    #ATTACHED RAROC RESULTS FUNCTION AND CHANGED THE RAROC TO CSV TO MAX LOAD
    npv_db = npv_db[theNPVLIST]

    raroc=raroc_results(0,'Portfolio as of ' + date_today_reformat, 0)

    # npv_db = npv_db[theNPVLIST]
    #For the first input above "raroc", key-in the column number
    #of the last contract that is currently on-going in CORE

    #To check the list of contracts that have net present values after step 7,
    #feel free to key-in "npv_db.columns"

    raroc=raroc.replace(0, '')


    # raroc=raroc.replace('₱0.00', 'LR Exc')

    # raroc=raroc.replace('₱42.00', 'LR Exc')

    # raroc=raroc.replace('Japan 25MW', 'Minebea Mitsumi')

    # raroc=raroc.replace('Portfolio as of 230711', "Portfolio as of July 31, 2023")

    raroc['Line Rental Cap per kWh'] = 'LR EX'

    # raroc['Contract Price per kWh'] = raroc['Contract Price per kWh'].replace('₱', '')

    customer_db1 = customer_db
    supplier_db1 = supplier_db
    customer_list = list(raroc['Customer'])

    supply_list = []
    failed_toappend_list = []
    failed_load_factor_list = []

    for i in customer_list:

        try:
            enddate =str(customer_db1[customer_db1['CCName'] == str(i)].iloc[0]['EndDate']).strip()[:10]
            indexdate = raroc[raroc['Customer']==str(i)].index[0]
            raroc.at[indexdate, 'End Date'] = enddate
        except:
            supply_list.append(str(i))
            continue

    for i in supply_list:
        try:
            enddate =str(supplier_db1[supplier_db1['SupplierName'] == str(i)].iloc[0]['EndDate']).strip()[:10]
            indexdate = raroc[raroc['Customer']==str(i)].index[0]
            raroc.at[indexdate, 'End Date'] = enddate
        except:
            failed_toappend_list.append(str(i))
            continue

    for i in supply_list:
        try:
            loadfactor1 = str(round((np.mean(solar_pac_load_profiles[str(i)])/np.max(solar_pac_load_profiles[str(i)]))*100)) + '%'
            indexdate = raroc[raroc['Customer']==str(i)].index[0]
            raroc.at[indexdate, 'Load Factor'] = loadfactor1
        except:
            failed_load_factor_list.append(str(i))
            continue

    print(failed_toappend_list)
    print(failed_load_factor_list)

    raroc['Contract Price per kWh'] =raroc['Contract Price per kWh'].str.replace('₱','')


    raroc['Cumulative NPV'] =raroc['Cumulative NPV'].str.replace('₱','').str.replace(' M','')
    raroc['Cumulative VAR'] =raroc['Cumulative VAR'].str.replace('₱','').str.replace(' M','')
    raroc['Cumulative 5th Percentile'] =raroc['Cumulative 5th Percentile'].str.replace('₱','').str.replace(' M','')


    raroc = raroc.rename(columns = {'Contract Price per kWh':'Contract Price PHP per kWh','Cumulative NPV':'Cumulative NPV (PHP Mil)', 'Cumulative VAR':'Cumulative VAR (PHP Mil)',
           'Cumulative 5th Percentile':'Cumulative 5th Percentile (PHP Mil)'})

    for i in list(supplier_db['SupplierName']):
        try:
            supply_index = raroc[raroc['Customer'] == str(i)].index[0]

    #         raroc.at[supply_index, 'Peak Load (MW)']

            # raroc.at[supply_index,'Peak Supply (MW)'] = raroc.at[supply_index, 'Peak Load (MW)']
            raroc.at[supply_index,'Peak Supply (MW)'] = round(np.max(solar_pac_load_profiles[str(i)]),2)

            raroc.at[supply_index,'Peak Load (MW)'] = ''

        except:
            print(f'Failed to change {i}')
            continue

    raroc['Peak Supply (MW)'] = raroc['Peak Supply (MW)'].replace(np.nan, '')

    for i in list(customer_db['CCName']):
        try:
            supply_index = raroc[raroc['Customer'] == str(i)].index[0]

    #         raroc.at[supply_index, 'Peak Load (MW)']

            # raroc.at[supply_index,'Peak Supply (MW)'] = raroc.at[supply_index, 'Peak Load (MW)']
            raroc.at[supply_index,'Peak Load @ Month-Hr'] = str(pd.DataFrame(cc_load.loc[cc_load[str(i)].idxmax()]).T['Month_Hr'].iloc[0])

            # raroc.at[supply_index,'Peak Load (MW)'] = pd.DataFrame(cc_load.loc[cc_load[str(i)].idxmax()]).T['Month_Hr'].iloc[0]
            print(f'Updated peak Month-Hr {i}')
        except:
            # raroc.at[supply_index,'Peak @ Month-Hr'] = str('')
            # print(f'Failed to change peak Month-Hr {i}')

            # raroc.at[supply_index,'Peak @ Month-Hr'] = ''
            continue

    raroc['Peak Load @ Month-Hr'] = raroc['Peak Load @ Month-Hr'].astype(str).replace('nan','')

    raroc = raroc[['Customer', 'Start Date', 'End Date', 'Tenor (Years)',
           'Contract Price PHP per kWh', 'Line Rental Cap per kWh',
           'Peak Load (MW)','Peak Load @ Month-Hr', 'Load Factor', 'Peak Supply (MW)', 'Cumulative RAROC',
           'Cumulative NPV (PHP Mil)', 'Cumulative VAR (PHP Mil)',
           'Cumulative 5th Percentile (PHP Mil)']]
    # raroc = raroc.sort_values(by='Start Date')

    # raroc['Start Date'] = pd.to_datetime(raroc['Start Date'])
    # raroc['End Date'] = pd.to_datetime(raroc['End Date'])

    # raroc['Tenor (Years)'] = round((raroc['End Date'] - raroc['Start Date']).dt.days / 365, 1)

    # raroc=raroc['Peak @ Month-Hr'].fillna['']
    raroc.to_excel(f'load-{str(np.max(cc_load["CustomerX-70%"]))}-raroc {date_today_reformat}-.xlsx', index=False)

    print(f'RAROC Done - Load {str(np.max(cc_load["CustomerX-70%"]))}')

    ending_raroc = float(raroc.iloc[-1]['Cumulative RAROC'].strip()[0:-1])
    print(f'{ending_raroc}')

    return ending_raroc


# customer_db.loc[customer_db['CCName'] == 'CustomerX-70%', 'FixedPrice'] = initial Price

max_attempts = 30  # Set the maximum number of attempts
current_attempt = 0
current_ending_raroc = 66
loadx = 1

while current_attempt < max_attempts:
      # Get input value from user
    ending_raroc = optimization_load(int(loadx))  # Call your function

    if ending_raroc > current_ending_raroc:
        print("Load Optimization Successful!")
        break  # Exit the loop if the function was successful
    else:
        loadx += 1.5
        print(f"Attempt {current_attempt + 1} was unsuccessful. Retrying... load - {loadx}")
        current_attempt += 1

if current_attempt == max_attempts:
    print("Maximum attempts reached. Function was not successful.")

"""## PriceX Optimization"""

# customer_db.loc[customer_db['CCName'] == 'CustomerX-70%', 'FixedPrice'] = initial Price #change price
def optimization_price(init_pricex,customer_x):
    global npv_db

    cc_index1 = customer_db[customer_db['CCName']==f'{customer_x}'].index[0]

    customer_db.loc[customer_db['CCName'] == f'{customer_x}', 'FixedPrice'] = init_pricex #change price

    print('running simulation cust-x')
    print(f'{customer_x}-{init_pricex}')

    cc_portfolio_valuation(cc_num=cc_index1,date_ref=datetime.datetime(date_today.year,date_today.month,date_today.day))

    #ATTACHED RAROC RESULTS FUNCTION AND CHANGED THE RAROC TO CSV TO MAX LOAD

    npv_db = npv_db[theNPVLIST]
    raroc=raroc_results(0,'Portfolio as of ' + date_today_reformat, 0)

    # npv_db = npv_db[theNPVLIST + list(['May Harvest','SIAEC-Jun','CustomerX-70%'])]
    #For the first input above "raroc", key-in the column number
    #of the last contract that is currently on-going in CORE

    #To check the list of contracts that have net present values after step 7,
    #feel free to key-in "npv_db.columns"

    raroc=raroc.replace(0, '')


    # raroc=raroc.replace('₱0.00', 'LR Exc')

    # raroc=raroc.replace('₱42.00', 'LR Exc')

    # raroc=raroc.replace('Japan 25MW', 'Minebea Mitsumi')

    # raroc=raroc.replace('Portfolio as of 230711', "Portfolio as of July 31, 2023")

    raroc['Line Rental Cap per kWh'] = 'LR EX'

    # raroc['Contract Price per kWh'] = raroc['Contract Price per kWh'].replace('₱', '')

    customer_db1 = customer_db
    supplier_db1 = supplier_db
    customer_list = list(raroc['Customer'])

    supply_list = []
    failed_toappend_list = []
    failed_load_factor_list = []

    for i in customer_list:

        try:
            enddate =str(customer_db1[customer_db1['CCName'] == str(i)].iloc[0]['EndDate']).strip()[:10]
            indexdate = raroc[raroc['Customer']==str(i)].index[0]
            raroc.at[indexdate, 'End Date'] = enddate
        except:
            supply_list.append(str(i))
            continue

    for i in supply_list:
        try:
            enddate =str(supplier_db1[supplier_db1['SupplierName'] == str(i)].iloc[0]['EndDate']).strip()[:10]
            indexdate = raroc[raroc['Customer']==str(i)].index[0]
            raroc.at[indexdate, 'End Date'] = enddate
        except:
            failed_toappend_list.append(str(i))
            continue

    for i in supply_list:
        try:
            loadfactor1 = str(round((np.mean(solar_pac_load_profiles[str(i)])/np.max(solar_pac_load_profiles[str(i)]))*100)) + '%'
            indexdate = raroc[raroc['Customer']==str(i)].index[0]
            raroc.at[indexdate, 'Load Factor'] = loadfactor1
        except:
            failed_load_factor_list.append(str(i))
            continue

    print(failed_toappend_list)
    print(failed_load_factor_list)

    raroc['Contract Price per kWh'] =raroc['Contract Price per kWh'].str.replace('₱','')


    raroc['Cumulative NPV'] =raroc['Cumulative NPV'].str.replace('₱','').str.replace(' M','')
    raroc['Cumulative VAR'] =raroc['Cumulative VAR'].str.replace('₱','').str.replace(' M','')
    raroc['Cumulative 5th Percentile'] =raroc['Cumulative 5th Percentile'].str.replace('₱','').str.replace(' M','')


    raroc = raroc.rename(columns = {'Contract Price per kWh':'Contract Price PHP per kWh','Cumulative NPV':'Cumulative NPV (PHP Mil)', 'Cumulative VAR':'Cumulative VAR (PHP Mil)',
           'Cumulative 5th Percentile':'Cumulative 5th Percentile (PHP Mil)'})

    for i in list(supplier_db['SupplierName']):
        try:
            supply_index = raroc[raroc['Customer'] == str(i)].index[0]

    #         raroc.at[supply_index, 'Peak Load (MW)']

            # raroc.at[supply_index,'Peak Supply (MW)'] = raroc.at[supply_index, 'Peak Load (MW)']
            raroc.at[supply_index,'Peak Supply (MW)'] = round(np.max(solar_pac_load_profiles[str(i)]),2)

            raroc.at[supply_index,'Peak Load (MW)'] = ''

        except:
            print(f'Failed to change {i}')
            continue

    raroc['Peak Supply (MW)'] = raroc['Peak Supply (MW)'].replace(np.nan, '')

    for i in list(customer_db['CCName']):
        try:
            supply_index = raroc[raroc['Customer'] == str(i)].index[0]

    #         raroc.at[supply_index, 'Peak Load (MW)']

            # raroc.at[supply_index,'Peak Supply (MW)'] = raroc.at[supply_index, 'Peak Load (MW)']
            raroc.at[supply_index,'Peak Load @ Month-Hr'] = str(pd.DataFrame(cc_load.loc[cc_load[str(i)].idxmax()]).T['Month_Hr'].iloc[0])

            # raroc.at[supply_index,'Peak Load (MW)'] = pd.DataFrame(cc_load.loc[cc_load[str(i)].idxmax()]).T['Month_Hr'].iloc[0]
            print(f'Updated peak Month-Hr {i}')
        except:
            # raroc.at[supply_index,'Peak @ Month-Hr'] = str('')
            # print(f'Failed to change peak Month-Hr {i}')

            # raroc.at[supply_index,'Peak @ Month-Hr'] = ''
            continue

    raroc['Peak Load @ Month-Hr'] = raroc['Peak Load @ Month-Hr'].astype(str).replace('nan','')

    raroc = raroc[['Customer', 'Start Date', 'End Date', 'Tenor (Years)',
           'Contract Price PHP per kWh', 'Line Rental Cap per kWh',
           'Peak Load (MW)','Peak Load @ Month-Hr', 'Load Factor', 'Peak Supply (MW)', 'Cumulative RAROC',
           'Cumulative NPV (PHP Mil)', 'Cumulative VAR (PHP Mil)',
           'Cumulative 5th Percentile (PHP Mil)']]


    # raroc = raroc.sort_values(by='Start Date')

    # raroc['Start Date'] = pd.to_datetime(raroc['Start Date'])
    # raroc['End Date'] = pd.to_datetime(raroc['End Date'])

    # raroc['Tenor (Years)'] = round((raroc['End Date'] - raroc['Start Date']).dt.days / 365, 1)

    # raroc=raroc['Peak @ Month-Hr'].fillna['']
    raroc.to_excel(f'Price-{str(init_pricex)}-CC-{str(customer_x)}-raroc {date_today_reformat}-.xlsx', index=False)

    print(f'RAROC Done - Price-{str(init_pricex)}-CC-{str(customer_x)}')

    ending_raroc = float(raroc.iloc[-1]['Cumulative RAROC'].strip()[0:-1])
    print(f'{ending_raroc}')

    return ending_raroc

max_attempts = 40  # Set the maximum number of attempts
current_attempt = 0
current_ending_raroc = 10000 # set Case 0 Ending RAROC
pricex = 5000
customerx = 'CustomerX-70%'

while current_attempt < max_attempts:
      # Get input value from user
    ending_raroc = optimization_price(pricex,customerx)  # Call your function

    if ending_raroc > current_ending_raroc:
        print("Load Optimization Successful!")
        break  # Exit the loop if the function was successful
    else:
        pricex += 250
        print(f"Attempt {current_attempt + 1} was unsuccessful. Retrying... load - {pricex}")
        current_attempt += 1

if current_attempt == max_attempts:
    print("Maximum attempts reached. Function was not successful.")
# customer_db.loc[customer_db['CCName'] == 'CustomerX-70%', 'FixedPrice'] = initial Price

raroc

"""# Portfolio RAROC Power BI Dashboard

## Gathering Forecast and Load Profiles
"""

date_today = datetime.datetime.today()

# date_today = datetime.datetime(2023,1,1)

wesm_forecasts = pd.read_parquet(fr'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\230605 Lantau WESM Forward Curve.parquet')

sales_dashboard_source=solar_pac_wesm_forecasts_supp_mid[list(solar_pac_wesm_forecasts_supp_mid.columns)[:12]]
sales_dashboard_source.columns=['Date','Billing Year','Billing Month','Day','Hour','MonthCountID','ID','ID_Load','Year','Month','YearMonthIntervalID','VECForecasts']
sales_dashboard_source=sales_dashboard_source.merge(wesm_forecasts[['Date','Base WESM']],on='Date',how='left')
sales_dashboard_source.columns=['Date','Billing Year','Billing Month','Day','Hour','MonthCountID','ID','ID_Load','Year','Month','YearMonthIntervalID','VECForecasts','LantauForecasts']
sales_dashboard_source=sales_dashboard_source.loc[sales_dashboard_source['Date']>=date_today]
sales_dashboard_source=sales_dashboard_source.dropna()
sales_dashboard_source=sales_dashboard_source.reset_index(drop=True)

for supplier_name in range(len(supplier_db)):
    supplier_list=list(supplier_db.loc[supplier_name])

    if "(Mid)" in supplier_list[0]:
        supplier_name_for_extract=supplier_list[0][:len(supplier_list[0])-6]
    else:
        supplier_name_for_extract=supplier_list[0]

    supplier_begin=max(date_today,datetime.datetime(supplier_list[3],supplier_list[1],supplier_list[2]))
    supplier_end=datetime.datetime(supplier_list[6],supplier_list[4],supplier_list[5])
    supplier_sub_load=solar_pac_load_profiles.loc[(solar_pac_load_profiles['Date']>=supplier_begin) & (solar_pac_load_profiles['Date']<=supplier_end)]
    sales_dashboard_source=sales_dashboard_source.merge(supplier_sub_load[['Date',supplier_name_for_extract]],on='Date',how='left')

    print(supplier_name_for_extract+' Done!')


for customer_name in range(len(customer_db)):
    customer_list=list(customer_db.loc[customer_name])

    customer_begin=max(date_today,datetime.datetime(customer_list[3],customer_list[1],customer_list[2]))
    customer_end=datetime.datetime(customer_list[6],customer_list[4],customer_list[5])

    if customer_list[0] in solar_pac_cc_load_profiles.columns:
        customer_sub_load=solar_pac_cc_load_profiles.loc[(solar_pac_cc_load_profiles['Date']>=customer_begin) & (solar_pac_cc_load_profiles['Date']<=customer_end)]
        sales_dashboard_source=sales_dashboard_source.merge(customer_sub_load[['Date',customer_list[0]]],on='Date',how='left')

    else:
        customer_sub_load=calendar_db.loc[(calendar_db['Date']>=customer_begin) & (calendar_db['Date']<=customer_end)]
        customer_sub_load=customer_sub_load.merge(cc_load[['ID_Load',customer_list[0]]], on='ID_Load',how='left')
        sales_dashboard_source=sales_dashboard_source.merge(customer_sub_load[['Date',customer_list[0]]],on='Date',how='left')

    print(customer_list[0]+' Done!')

hide_toggle('Gathering Forecasts and Load Profiles')





"""## Supply and Demand Dashboard Data"""

#######
##TESTING -------


# sales_dashboard_source=sales_dashboard_source[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#        'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID', 'VECForecasts',
#        'LantauForecasts', 'TVI', 'LWEC', 'SSREC','SEM-Calaca-5MW',
#        'EMS (Renewal)', '557 Feathermeal (Renewal)', 'Light Rail Manila',
#                'GGPC (Renewal) IV', 'AICE2', 'AICE3', 'Tarlac Mall A',
#               'Supercast (Renewal) A', 'C&S',  'Fast Logistics', 'HEVA Rizal',
#                  'Pioneer Center A',
#                 'Kings Quality','EIDC-6.4',
#                  'Creative Diecast-6.5','Yiking Plastic A','Vitarich',
#                  'Aeonprime A', 'Polaris A', 'Excel Towers A','One Montage',
#                     'IMCC-1','IMCC-2','EMS A','Park Centrale Tower']] # PIPELINE CONTRACTS

# sales_dashboard_source=sales_dashboard_source[ list(['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#        'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID', 'VECForecasts',
#        'LantauForecasts']) + list([item for item in List_Active_Contracts if item not in Pipelines]) + list(Signed_Supplys) + list(Pipelines) ] # PIPELINE CONTRACTS

sales_dashboard_source=sales_dashboard_source[ list(['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
       'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID', 'VECForecasts',
       'LantauForecasts']) + list(['557 Feathermeal (Renewal) MQ',
 'Light Rail Manila',
 'GGPC MQ',
 'AICE4',
 'Tarlac Mall A',
 'Supercast MQ',
 'CASADI',
 'Fast Logistics',
 'HEVA Rizal',
 'HEVA Iloilo',
 'Pioneer Center A',
 'Vitarich MQ',
 'Yiking MQ',
 'Kings Quality',
 'EIDC MQ',
 'Polaris A',
 'Aeonprime A',
 'Excel Towers A',
 'Creative Diecast-6.5 MQ',
 'One Montage',
 'Fong Shan A',
 'Treasure Island',
 'TIIC-Pilit',
 'CAM MQ',
 'TVI',
 'LWEC-VENA-50MW',
 'SSREC',
 'SEM-Calaca-5MW',
 'SIAEC-Jun','GENCO-5MW',
 # 'EMS MQ',
 'May Harvest',
 'UST Load'])]

df = sales_dashboard_source

# cc_list = list(df.columns)[17:-3]

cc_list = [item for item in List_Active_Contracts if item not in Pipelines]

# Signed_Supplys = ['TVI','LWEC', 'SSREC','SEM-Calaca-5MW']

# pipe_list = Pipelines
pipe_list = ['UST Load','May Harvest']

sup_list = Signed_Supplys + list(['SIAEC-Jun','GENCO-5MW',])

# cc_list = ['EMS (Renewal)', '557 Feathermeal (Renewal)', 'Light Rail Manila',
#                'GGPC (Renewal) IV', 'AICE2', 'AICE3', 'Tarlac Mall A',
#               'Supercast (Renewal) A', 'C&S',  'Fast Logistics', 'HEVA Rizal',
#                  'Pioneer Center A',
#                  'Kings Quality','EIDC-6.4','Creative Diecast-6.5','Yiking Plastic A','Vitarich',
#                  'Aeonprime A', 'Polaris A', 'Excel Towers A','One Montage']

# # sup_list = list(df.columns)[13:17]

# sup_list = ['TVI', 'LWEC', 'SSREC','SEM-Calaca-5MW']

# # pipe_list =  list(df.columns)[-3:]
# pipe_list =  ['IMCC-1','IMCC-2','EMS A','Park Centrale Tower']

df_list = []

Forecast =  'VECForecasts' # 'LantauForecasts'
# Forecast =  'LantauForecasts'

for i in cc_list:
    df1 = sales_dashboard_source[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
       'ID', 'ID_Load', 'Year', 'Month','VECForecasts','LantauForecasts',str(i)]]
    df1['CC_Supply_Source'] = str(i)
    df1.rename(columns = {str(i):'Load Profile'}, inplace = True)
    df1['Contract_Status'] = 'Contracted'

    #######
    df1['Exp/Rev_source'] = str(i)
#     df1.rename(columns = {str(i):'Load Profile'}, inplace = True)
#     df1['Contract_Status'] = 'Contracted'
    df1['WESM PP'] = df1[Forecast] * df1['Load Profile']

    df1['Contract Price(PhPperMWh)'] = customer_db[customer_db['CCName'] == str(i)].iloc[0]['FixedPrice']

    df1['BCQ Sales'] = df1['Contract Price(PhPperMWh)'] * df1['Load Profile']
    df1['PSA Expense'] = 0
    df1['WESM Sales'] = 0
    df1['Supply Profile'] = 0
    df1['Contracted'] = str(i)
    df1['Pipelines'] = 'z1'
    df1['Contracted Supply'] = 's1'
    df1['Contracted CC'] = str(i)

    df_list.append(df1)

for i in pipe_list:
    df1 = sales_dashboard_source[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
       'ID', 'ID_Load', 'Year', 'Month','VECForecasts','LantauForecasts',str(i)]]
    df1['CC_Supply_Source'] = str(i)
    df1.rename(columns = {str(i):'Load Profile'}, inplace = True)
    df1['Contract_Status'] = 'Pipeline'

    ###
    df1['Exp/Rev_source'] = str(i)
#     df1.rename(columns = {str(i):'Load Profile'}, inplace = True)
#     df1['Contract_Status'] = 'Contracted'
    df1['WESM PP'] = df1[Forecast] * df1['Load Profile']

    df1['Contract Price(PhPperMWh)'] = customer_db[customer_db['CCName'] == str(i)].iloc[0]['FixedPrice']

    df1['BCQ Sales'] = df1['Contract Price(PhPperMWh)'] * df1['Load Profile']
    df1['PSA Expense'] = 0
    df1['WESM Sales'] = 0
    df1['Supply Profile'] = 0
    df1['Contracted'] = 'b2'
    df1['Pipelines'] = str(i)
    df1['Contracted Supply'] = 's1'
    df1['Contracted CC'] = 'c1'



    df_list.append(df1)

for i in sup_list:
    df1 = sales_dashboard_source[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
       'ID', 'ID_Load', 'Year', 'Month','VECForecasts','LantauForecasts',str(i)]]
    df1['CC_Supply_Source'] = str(i)
    df1['Contract_Status'] = 'Contracted'
#     df1.rename(columns = {str(i):'Load Profile'}, inplace = True)

    ######
#     df1['Source_Rev'] = str(i)
    df1['a'] = df1[str(i)]
    df1.rename(columns = {'a':'Supply Profile'}, inplace = True)
#     df1['Contract_Status'] = 'Contracted'
    df1['WESM Sales'] = df1[Forecast] * df1['Supply Profile']
    df1['BCQ Sales'] = 0

    df1['PSA Expense'] = df1['Supply Profile'] *int(supplier_db[supplier_db['SupplierName'] == str(i)].iloc[0]['FixedPrice'])
    df1['Exp/Rev_source'] = str(i)
    df1['WESM PP'] = 0
    df1['Load Profile'] = 0
    df1['Contracted'] = str(i)
    df1['Pipelines'] = 'z1'
    df1['Contracted Supply'] = str(i)
    df1['Contracted CC'] = 'c1'


    df_list.append(df1)

# for i in cc_list:
#     df1 = sales_dashboard_source[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#        'ID', 'ID_Load', 'Year', 'Month','VECForecasts','LantauForecasts',str(i)]]
#     df1['Source_Rev'] = str(i)
#     df1.rename(columns = {str(i):'Load Profile'}, inplace = True)
#     df1['Contract_Status'] = 'Contracted'
#     df1['WESM PP'] = df1['VECForecasts'] * df1['Load Profile']

#     df1['Contract Price(PhPperMWh)'] = customer_db[customer_db['CCName'] == f'{i}'].iloc[0]['FixedPrice']

#     df1['BCQ Sales'] = df1['Contract Price(PhPperMWh)'] * df1['Load Profile']

#     df_list.append(df1)

# for i in sup_list:
#     df1 = sales_dashboard_source[['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
#        'ID', 'ID_Load', 'Year', 'Month','VECForecasts','LantauForecasts',str(i)]]
#     df1['Source_Rev'] = str(i)
#     df1.rename(columns = {str(i):'Load Profile'}, inplace = True)
#     df1['Contract_Status'] = 'Contracted'
#     df1['WESM Sales'] = df1['VECForecasts'] * df1['Load Profile']
#     df1['PSA Expense'] = df1['Load Profile'] *(5.35*1000)
#     df1['PSA Expense Source'] = str(i)
#     df_list.append(df1)

result_df = pd.concat(df_list, axis=0)

result_df.reset_index(drop=True, inplace=True)

result_df = pd.DataFrame(result_df)

result_df = result_df.replace('SEM-Calaca-5MW','SCPC')
# BCQ_total

# result_df.to_csv(f'LoadProfile-{date_today_reformat}-V8.4-prototype-1.csv', index = False) # RUN THIS FOR DASHBOAR SOURCE FILE

# print(f'LoadProfile-{date_today_reformat}-V7.csv')

# hide_toggle('Gathering Total Supply and Demand (See instructions in the comments)')
result_df

"""## 5th Percentile Data"""

npv_db = pd.read_parquet(fr'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\{date_today_reformat} NPVDatabase ({run_type}).parquet')

###### FUNCTIONS FOR SHOWING ALL THE CONTRACTS ACTIVE AND PIPELINE
def raroc_results(last_npv_col,initial_text, initial_month_inc):

    #Setting Benchmark
    raroc_results = pd.DataFrame(columns=['Customer','Start Date','End Date','Tenor (Years)','Contract Price per kWh','Line Rental Cap per kWh','Peak Load (MW)','Load Factor','Cumulative RAROC', 'Cumulative NPV', 'Cumulative VAR', 'Cumulative 5th Percentile'])

    cumulative_port = [0]*len(npv_db)

    apr_port=npv_db.iloc[:,0:last_npv_col+1].sum(axis=1)

    column_list=list(npv_db.columns[0:last_npv_col+1])

    column_list_load = [i for i in column_list if i in list(customer_db['CCName'])]

    cc_load_total = cc_load[column_list_load].sum(axis=1)

    coincidental_peak = "{:,.2f}".format(max(cc_load_total))

    cumulative_port += apr_port


    mean_npv=np.mean(cumulative_port)
    p5_npv=np.percentile(cumulative_port, 5)
    var_npv= mean_npv-p5_npv
    raroc_npv = mean_npv/var_npv

#     raroc_results.loc[0]=[str(initial_text),'','','','','',str(coincidental_peak),coincidental_peak,raroc_npv,mean_npv,var_npv,p5_npv]

    try:

        start_date_0 = customer_db[customer_db['CCName'] == str(npv_db.columns[0])]['StartDate'].iloc[0].date()

        end_date_0 = customer_db[customer_db['CCName'] == str(npv_db.columns[0])]['EndDate'].iloc[0].date()

        tenor_0 = round(int(((end_date_0 - start_date_0).days)/364))

        name_0 = str(npv_db.columns[last_npv_col])

        contract_price_0 = (customer_db[customer_db['CCName'] == str(npv_db.columns[0])]['FixedPrice'].iloc[0])/1000

        max_load_0 = np.max(cc_load[str(npv_db.columns[0])])

        mean_load_0 = np.mean(cc_load[str(npv_db.columns[0])])

        load_factor_0 = mean_load_0/max_load_0

    except:

        start_date_0 = supplier_db[supplier_db['SupplierName'] == str(npv_db.columns[0])]['StartDate'].iloc[0].date()

        end_date_0 = supplier_db[supplier_db['SupplierName'] == str(npv_db.columns[0])]['EndDate'].iloc[0].date()

        contract_price_0 = (supplier_db[supplier_db['SupplierName'] == str(npv_db.columns[0])]['FixedPrice'].iloc[0])/1000

        tenor_0 = round(int(((end_date_0 - start_date_0).days)/364))

        name_0 = str(npv_db.columns[last_npv_col])



        max_load_0 = np.max(solar_pac_load_profiles[str(npv_db.columns[0])])

        mean_load_0 = np.mean(solar_pac_load_profiles[str(npv_db.columns[0])])

        load_factor_0 = mean_load_0/max_load_0


#     start_date_0 = customer_db[customer_db['CCName'] == str(npv_db.columns[0])]['StartDate'].iloc[0].date()

#     end_date_0 = customer_db[customer_db['CCName'] == str(npv_db.columns[0])]['EndDate'].iloc[0].date()

#     tenor_0 = round(int(((end_date_0 - start_date_0).days)/364))

#     name_0 = str(npv_db.columns[last_npv_col])

#     contract_price_0 = (customer_db[customer_db['CCName'] == str(npv_db.columns[0])]['FixedPrice'].iloc[0])/1000

#     max_load_0 = np.max(cc_load[str(npv_db.columns[0])])

#     mean_load_0 = np.mean(cc_load[str(npv_db.columns[0])])

#     load_factor_0 = mean_load_0/max_load_0


    raroc_results.loc[0]=[name_0,start_date_0,end_date_0,tenor_0,
                          str(contract_price_0),'',str(coincidental_peak),
                          coincidental_peak,raroc_npv,mean_npv,var_npv,p5_npv]

    sub_npv_db = npv_db.iloc[:,last_npv_col+1:]


    #Individual Comparisons
    sub_customer_db=customer_db[['CCName','StartMonth','StartDay','StartYear','EndMonth','EndDay','EndYear','CES Gross Profits']]
    sub_supplier_db=supplier_db[['SupplierName','StartMonth','StartDay','StartYear','EndMonth','EndDay','EndYear']]

    sub_db = sub_customer_db.copy()

    for supprow in range(len(sub_supplier_db)):
        sub_db.loc[len(sub_customer_db)+supprow] = list(sub_supplier_db.loc[supprow])+[0]

    datetime_list=[]
    endtime_list=[]
    tenor=[]

    for period in range(len(sub_db)):
        datetime_list.append(datetime.date(sub_db['StartYear'][period],sub_db['StartMonth'][period],sub_db['StartDay'][period]))
        endtime_list.append(datetime.date(sub_db['EndYear'][period],sub_db['EndMonth'][period],sub_db['EndDay'][period]))
        tenor.append(relativedelta(endtime_list[period],datetime_list[period]).years+ceil(relativedelta(endtime_list[period],datetime_list[period]).months*10/12)/10)


    sub_db['StartDate'] = datetime_list
    sub_db['EndDate'] = endtime_list
    sub_db['Tenor (Years)'] = tenor


    #Difference in Max and Min Contract Dates
    max_contract_date = np.max(sub_db['StartDate'])
    min_contract_date = np.min(sub_db['StartDate'])+relativedelta(months=initial_month_inc,days=-25)

    days_diff = max_contract_date - min_contract_date
    actual_days = days_diff.days

    #Generating Resulting RAROC Table
    indiv_raroc_results_orig = raroc_results[['Customer','Start Date','End Date','Tenor (Years)','Cumulative RAROC', 'Cumulative NPV', 'Cumulative VAR', 'Cumulative 5th Percentile']]
    indiv_raroc_results = indiv_raroc_results_orig.copy()

#     raroc_results.loc[0]=[str(npv_db.columns[last_npv_col]),,'','','','',str(coincidental_peak),coincidental_peak,raroc_npv,mean_npv,var_npv,p5_npv]

    for months_inc in range(0,actual_days+1):
        filtered_sub_db=sub_db.loc[(sub_db['StartDate']==min_contract_date+relativedelta(days=months_inc))].reset_index()
        #print(filtered_sub_db)


        if len(filtered_sub_db)==0:
            pass

        else:
            for sub_cust in filtered_sub_db['CCName']:
                if sub_cust in sub_npv_db.columns:
                    indiv_npv_values = sub_npv_db[sub_cust]
                    indiv_raroc_contrib = cumulative_port + indiv_npv_values
                    mean_npv=np.mean(indiv_raroc_contrib)
                    p5_npv=np.percentile(indiv_raroc_contrib, 5)
                    var_npv= mean_npv-p5_npv
                    raroc_npv = mean_npv/var_npv
                    indiv_raroc_results.loc[len(indiv_raroc_results)]=[sub_cust,filtered_sub_db['StartDate'][0],filtered_sub_db['EndDate'][0],
                                                                       filtered_sub_db['Tenor (Years)'][list(filtered_sub_db['CCName']).index(sub_cust)],raroc_npv,mean_npv,var_npv,p5_npv]

                else:
                    pass

        indiv_raroc_sort=sorted(list(indiv_raroc_results['Cumulative RAROC'][1:len(indiv_raroc_results['Cumulative RAROC'])+1]),reverse=True)

        for supplier_number in range(len(indiv_raroc_sort)):
            supp_number=list(indiv_raroc_results['Cumulative RAROC'][1:len(indiv_raroc_results['Cumulative RAROC'])+1]).index(indiv_raroc_sort[supplier_number])
            if indiv_raroc_results['Customer'][supp_number+1] in list(supplier_db['SupplierName']):
                gen_supp_load=solar_pac_load_profiles[indiv_raroc_results['Customer'][supp_number+1]]

                cumulative_raroc_cc = sub_npv_db[list(indiv_raroc_results['Customer'])[supp_number+1]]
                cumulative_port += cumulative_raroc_cc
                mean_npv=np.mean(cumulative_port)
                p5_npv=np.percentile(cumulative_port,5)
                var_npv=mean_npv-p5_npv
                raroc_npv = mean_npv/var_npv
                raroc_results.loc[len(raroc_results)]=[indiv_raroc_results['Customer'][supp_number+1],
                                                       min_contract_date+relativedelta(days=months_inc)
                                                       ,indiv_raroc_results['End Date'][supp_number+1],indiv_raroc_results['Tenor (Years)'][supp_number+1],
                                                       supplier_db['FixedPrice'][list(supplier_db['SupplierName']).index(indiv_raroc_results['Customer'][supp_number+1])],
                                                       supplier_db['LRCap'][list(supplier_db['SupplierName']).index(indiv_raroc_results['Customer'][supp_number+1])],
                                                       "{:.2f}".format(np.max(gen_supp_load)),'',
                                                       raroc_npv,mean_npv,var_npv,p5_npv]
            else:
                pass


        for customer_number in range(len(indiv_raroc_sort)):
            cc_number=list(indiv_raroc_results['Cumulative RAROC'][1:len(indiv_raroc_results['Cumulative RAROC'])+1]).index(indiv_raroc_sort[customer_number])
            if indiv_raroc_results['Customer'][cc_number+1] in list(supplier_db['SupplierName']):
                pass
            else:
                if 'Japan' in indiv_raroc_results['Customer'][cc_number+1]:
                    cust_load=solar_pac_cc_load_profiles['Japan 25MW']
                else:
                    cust_load=cc_load[list(indiv_raroc_results['Customer'])[cc_number+1]]
                load_factor=np.mean(cust_load)/np.max(cust_load)
                peak_load_mw=np.max(cust_load)
                cumulative_raroc_cc = sub_npv_db[indiv_raroc_results['Customer'][cc_number+1]]
                cumulative_port += cumulative_raroc_cc
                mean_npv=np.mean(cumulative_port)
                p5_npv=np.percentile(cumulative_port,5)
                var_npv=mean_npv-p5_npv
                raroc_npv = mean_npv/var_npv
                # INSERTED THIS HERE
#                 raroc_results.loc[0]=[str(npv_db.columns[last_npv_col]),'','','','','',str(coincidental_peak),coincidental_peak,raroc_npv,mean_npv,var_npv,p5_npv]
                # INSERTED THIS HERE
                raroc_results.loc[len(raroc_results)]=[indiv_raroc_results['Customer'][cc_number+1],
                                                       min_contract_date+relativedelta(days=months_inc)
                                                       ,indiv_raroc_results['End Date'][supp_number+1],
                                                       indiv_raroc_results['Tenor (Years)'][cc_number+1],
                                                                       customer_db['FixedPrice'][list(customer_db['CCName']).index(indiv_raroc_results['Customer'][cc_number+1])],
                                                                       customer_db['LRCap'][list(customer_db['CCName']).index(indiv_raroc_results['Customer'][cc_number+1])],
                                                                       "{:.2f}".format(peak_load_mw),load_factor,raroc_npv,mean_npv,var_npv,p5_npv]

        indiv_raroc_results = indiv_raroc_results_orig.copy()

    contractprice_list=[]
    lrcap_list=[]
    raroc_lf_list_check=[]

    for lf_x in range(len(list(raroc_results['Load Factor']))):
        if raroc_results['Contract Price per kWh'][lf_x] == '':
            contractprice_list.append('')
        else:
            contractprice_list.append("₱{:,.2f}".format(float(raroc_results['Contract Price per kWh'][lf_x])/1000))

        if raroc_results['Line Rental Cap per kWh'][lf_x] == '':
            lrcap_list.append('')
        else:
            lrcap_list.append("₱{:,.2f}".format(float(raroc_results['Line Rental Cap per kWh'][lf_x])/1000))


        if type(raroc_results['Load Factor'][lf_x]) == float:
            raroc_lf_list_check.append("{:.0%}".format(raroc_results['Load Factor'][lf_x]))
        else:
            raroc_lf_list_check.append('')



    raroc_results['Load Factor']=raroc_lf_list_check
    raroc_results['Contract Price per kWh']=contractprice_list
    raroc_results['Line Rental Cap per kWh']=lrcap_list

    raroc_results['Cumulative RAROC']=["{:.0%}".format(x) for x in raroc_results['Cumulative RAROC']]
    raroc_results['Cumulative NPV']=["₱{:,.2f} M".format(x/10**6) for x in raroc_results['Cumulative NPV']]
    raroc_results['Cumulative VAR']=["₱{:,.2f} M".format(x/10**6) for x in raroc_results['Cumulative VAR']]
    raroc_results['Cumulative 5th Percentile']=["₱{:,.2f} M".format(x/10**6).replace('₱-','-₱') for x in raroc_results['Cumulative 5th Percentile']]

    raroc_results.at[0,'Contract Price per kWh'] =  '₱'+f'{contract_price_0:0.2f}'
    raroc_results.at[0,'Line Rental Cap per kWh'] =  '₱0.00'
    raroc_results.at[0,'Load Factor'] =  str(round(load_factor_0*100)) + '%'

    return raroc_results[['Customer', 'Start Date','End Date', 'Tenor (Years)',
       'Contract Price per kWh', 'Line Rental Cap per kWh', 'Peak Load (MW)',
       'Load Factor', 'Cumulative RAROC', 'Cumulative NPV', 'Cumulative VAR',
       'Cumulative 5th Percentile']]

raroc=raroc_results(0,'Portfolio as of ' + date_today_reformat, 0)
#For the first input above "raroc", key-in the column number
#of the last contract that is currently on-going in CORE

#To check the list of contracts that have net present values after step 7,
#feel free to key-in "npv_db.columns"

raroc=raroc.replace(0, '')


# raroc=raroc.replace('₱0.00', 'LR Exc')

# raroc=raroc.replace('₱42.00', 'LR Exc')

# raroc=raroc.replace('Japan 25MW', 'Minebea Mitsumi')

# raroc=raroc.replace('Portfolio as of 230711', "Portfolio as of July 31, 2023")

raroc['Line Rental Cap per kWh'] = 'LR EX'

# raroc['Contract Price per kWh'] = raroc['Contract Price per kWh'].replace('₱', '')

customer_db1 = customer_db
supplier_db1 = supplier_db
customer_list = list(raroc['Customer'])

supply_list = []
failed_toappend_list = []
failed_load_factor_list = []

for i in customer_list:

    try:
        enddate =str(customer_db1[customer_db1['CCName'] == str(i)].iloc[0]['EndDate']).strip()[:10]
        indexdate = raroc[raroc['Customer']==str(i)].index[0]
        raroc.at[indexdate, 'End Date'] = enddate
    except:
        supply_list.append(str(i))
        continue

for i in supply_list:
    try:
        enddate =str(supplier_db1[supplier_db1['SupplierName'] == str(i)].iloc[0]['EndDate']).strip()[:10]
        indexdate = raroc[raroc['Customer']==str(i)].index[0]
        raroc.at[indexdate, 'End Date'] = enddate
    except:
        failed_toappend_list.append(str(i))
        continue

for i in supply_list:
    try:
        loadfactor1 = str(round((np.mean(solar_pac_load_profiles[str(i)])/np.max(solar_pac_load_profiles[str(i)]))*100)) + '%'
        indexdate = raroc[raroc['Customer']==str(i)].index[0]
        raroc.at[indexdate, 'Load Factor'] = loadfactor1
    except:
        failed_load_factor_list.append(str(i))
        continue

print(failed_toappend_list)
print(failed_load_factor_list)

raroc['Contract Price per kWh'] =raroc['Contract Price per kWh'].str.replace('₱','')


raroc['Cumulative NPV'] =raroc['Cumulative NPV'].str.replace('₱','').str.replace(' M','')
raroc['Cumulative VAR'] =raroc['Cumulative VAR'].str.replace('₱','').str.replace(' M','')
raroc['Cumulative 5th Percentile'] =raroc['Cumulative 5th Percentile'].str.replace('₱','').str.replace(' M','')


raroc = raroc.rename(columns = {'Contract Price per kWh':'Contract Price PHP per kWh','Cumulative NPV':'Cumulative NPV (PHP Mil)', 'Cumulative VAR':'Cumulative VAR (PHP Mil)',
       'Cumulative 5th Percentile':'Cumulative 5th Percentile (PHP Mil)'})

for i in list(supplier_db['SupplierName']):
    try:
        supply_index = raroc[raroc['Customer'] == str(i)].index[0]

#         raroc.at[supply_index, 'Peak Load (MW)']

        # raroc.at[supply_index,'Peak Supply (MW)'] = raroc.at[supply_index, 'Peak Load (MW)']
        raroc.at[supply_index,'Peak Supply (MW)'] = round(np.max(solar_pac_load_profiles[str(i)]),2)

        raroc.at[supply_index,'Peak Load (MW)'] = ''

    except:
        print(f'Failed to change {i}')
        continue


raroc['Peak Supply (MW)'] = raroc['Peak Supply (MW)'].replace(np.nan, '')

raroc = raroc[['Customer', 'Start Date', 'End Date', 'Tenor (Years)',
       'Contract Price PHP per kWh', 'Line Rental Cap per kWh',
       'Peak Load (MW)', 'Peak Supply (MW)', 'Load Factor', 'Cumulative RAROC',
       'Cumulative NPV (PHP Mil)', 'Cumulative VAR (PHP Mil)',
       'Cumulative 5th Percentile (PHP Mil)']]

# raroc = raroc.sort_values(by='Start Date')

# raroc['Start Date'] = pd.to_datetime(raroc['Start Date'])
# raroc['End Date'] = pd.to_datetime(raroc['End Date'])

# raroc['Tenor (Years)'] = round((raroc['End Date'] - raroc['Start Date']).dt.days / 365, 1)

# raroc.to_excel(f'raroc {date_today_reformat}.xlsx',index = False)


raroc1 = raroc
# raroc1 = pd.read_parquet(fr'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\{date_today_reformat} NPVDatabase ({run_type}).parquet')
# print(f"{date_today_reformat} NPVDatabase ({run_type})- DONE")


dr = raroc1[['Customer','Cumulative NPV (PHP Mil)','Cumulative 5th Percentile (PHP Mil)']]

raroc_list = list(dr['Customer'])

dr['Cumulative 5th Percentile (PHP Mil)'] = dr['Cumulative 5th Percentile (PHP Mil)'].str.replace(',','').astype(float)

dr['NPV Value'] = 0

dr['5th Percentile Value (PHP Mil)'] = 0

dr['Contracted'] = 'a'

dr['Pipeline'] = 'P1'

npv_value = float(dr[dr['Customer'] == list(dr['Customer'])[0]]['Cumulative NPV (PHP Mil)'][0])

dr.at[0, 'NPV Value'] = npv_value * 1000000

value= float(dr[dr['Customer'] == list(dr['Customer'])[0]]['Cumulative 5th Percentile (PHP Mil)'][0])

dr.at[0, '5th Percentile Value (PHP Mil)'] = value * 1000000

dr.at[0, 'Contracted'] = list(dr['Customer'])[0]

# dr.at[0, 'Pipeline'] ='P1'

cc_list = [item for item in Signed_CCs if item not in Pipelines]

cc_list

# # sup_list =list(['TVI', 'LWEC', 'SSREC','SEM-Calaca-5MW'])

sup_list = Signed_Supplys

sup_list
# # pipe_list =  list(['IMCC-1','IMCC-2','EMS A','Park Centrale Tower'])

pipe_list = Pipelines

pipe_list

index_value = 0

for i in raroc_list:

    dr.at[index_value, 'NPV Value'] = np.mean(npv_db[str(i)])
    index_value = index_value + 1


index_value = 0

for i in raroc_list:

    value1 = float((dr[dr['Customer'] == raroc_list[int(index_value)]]['Cumulative 5th Percentile (PHP Mil)'][int(index_value)]))

    value2 = float((dr[dr['Customer'] == raroc_list[int(index_value) + int(1)]]['Cumulative 5th Percentile (PHP Mil)'][int(index_value) + int(1)]))


#         value1 = float((dr[dr['Customer'] == raroc_list[int(index_value)]]['Cumulative 5th Percentile (PHP Mil)'][int(index_value)]).strip().replace(',',''))

#         value2 = float((dr[dr['Customer'] == raroc_list[int(index_value) + int(1)]]['Cumulative 5th Percentile (PHP Mil)'][int(index_value) + int(1)]).strip().replace(',',''))

    dr.at[index_value + int(1), '5th Percentile Value (PHP Mil)'] = ((value2) - (value1))*1000000

#         npv_value1 = float(dr[dr['Customer'] == raroc_list[int(index_value)]]['Cumulative NPV'][int(index_value)].strip().replace('₱','').replace(' M',''))

#         npv_value2 = float(dr[dr['Customer'] == raroc_list[int(index_value) + int(1)]]['Cumulative NPV'][int(index_value) + int(1)].strip().replace('₱','').replace(' M',''))

#         dr.at[index_value + int(1), 'NPV Value'] = ((npv_value2) - (npv_value1))*1000000

        # print(f'done {i}')

        # if i in cc_list:
        #     dr.at[int(index_value), 'Contracted'] = str(i)
        #     dr.at[int(index_value), 'Pipeline'] ='P1'

    if i in sup_list:
        dr.at[int(index_value), 'Contracted'] = str(i)
        dr.at[int(index_value), 'Pipeline'] ='P1'
        print(index_value)
        # elif i in pipe_list:
        #     dr.at[int(index_value), 'Contracted'] = 'C1'

        #     dr.at[int(index_value), 'Pipeline'] = str(i)

    print(f'success-{i}')
    index_value = index_value + 1


#     except:

# #         value1 = float((dr[dr['Customer'] == raroc_list[int(index_value)]]['Cumulative 5th Percentile (PHP Mil)'][int(index_value)]).strip().replace(',',''))

# # #         value2 = float((dr[dr['Customer'] == raroc_list[int(index_value) + int(1)]]['Cumulative 5th Percentile (PHP Mil)'][int(index_value) + int(1)]).strip().replace(',',''))
# #         value2 = 0
# #         dr.at[index_value , '5th Percentile Value (PHP Mil)'] = ((value1))*1000000

# #         if i in cc_list:
# #             dr.at[int(index_value) , 'Contracted'] = str(i)

# #             dr.at[int(index_value), 'Pipeline'] ='P1'
# #         elif i in sup_list:

# #             dr.at[int(index_value) , 'Contracted'] = str(i)

# #             dr.at[int(index_value) , 'Pipeline'] ='P1'
# #         elif i in pipe_list:
# #             dr.at[int(index_value) , 'Contracted'] = 'C1'
# #             dr.at[int(index_value) , 'Pipeline'] = str(i)

#         print(f'failed-{i}')
#         index_value = index_value + 1
#         continue

"""# Executive Corporate Planning Report Calculation

## WESM Plus Computation
"""

df=sales_dashboard_source[ list(['Date', 'Billing Year', 'Billing Month', 'Day', 'Hour', 'MonthCountID',
       'ID', 'ID_Load', 'Year', 'Month', 'YearMonthIntervalID', 'VECForecasts',
       'LantauForecasts']) + list(Pipelines)] # PIPELINE CONTRACTS

df_admin = pd.read_excel(r'C:\Users\jason.paquibulan\Desktop\Python_Model_Parquet_Files\adminfee.xlsx')

wesm_list = list(df_admin['NAME'])

for i in wesm_list:
    df[f'{i}-Fee'] = (df_admin[df_admin['NAME'] == str(i)]['ADMIN FEE PESO/ KWH'] * 1000).values[0] * df[str(i)]
    print(i)

wesm_fee_list = ['GFCC-W-Fee', 'EMS-W-Fee', 'HEVALAPAZ-W-Fee', 'HELIX AGG-W-Fee',
       'CALYPSO1-W-Fee', 'CALYPSO2-W-Fee', 'CITIPLAS PLASTIC-W-Fee',
       'MULTI-PACK-W-Fee', 'ASIAN PLASTIC-W-Fee', 'LEE CHOU TIAM-W-Fee']

df['WESM Purchases in MWh'] = np.sum(df[wesm_list], axis =1)
df['WESM Purchases in Php'] = df['WESM Purchases in MWh'] *df['VECForecasts']
df['WESM+ Customer Fee in PHP'] = np.sum(df[wesm_fee_list], axis =1)

list_1 = list(['WESM Purchases in MWh','WESM Purchases in Php','WESM+ Customer Fee in PHP'])

df = df.reset_index()

df1 = df.groupby(df['Date'].dt.strftime('%Y-%m')).agg({col: 'sum' for col in list_1})
