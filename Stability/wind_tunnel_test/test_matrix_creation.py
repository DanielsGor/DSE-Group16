import itertools as it
import numpy as np
import pandas as pd


 
alpha_short = [0, 4, 8]
alpha_long = [0, 4, 8, 10, 12]

V_pp_short = [0, 9, 12]
V_pp_long = [0, 6, 9, 12]

"""
V_pp_short = [12]
V_pp_long = [12]
"""

f_burst_short = [10, 50, 200]
f_burst_long = [10, 20, 50, 100, 200, 500]

duty_cycle_short = [0.1, 0.5, 0.9]
duty_cycle_long = [0.1, 0.3, 0.5, 0.7, 0.9]



def test_1(alpha = alpha_long, V_pp=V_pp_short, f_burst=f_burst_short, duty_cycle=duty_cycle_short):
    df_test_1 = pd.DataFrame(columns=['alpha', 'V_pp', 'f_burst', 'duty_cycle'])
    for a  in alpha:
        for v in V_pp:
            for f in f_burst:
                for d in duty_cycle:
                    df_test_1 = pd.concat([df_test_1, pd.DataFrame([[a, v, f, d]], columns=['alpha', 'V_pp', 'f_burst', 'duty_cycle'])])

    print('break')
    return df_test_1

def test_2(alpha = alpha_short, V_pp=V_pp_long, f_burst=f_burst_short, duty_cycle=duty_cycle_short):
    df_test_2 = pd.DataFrame(columns=['alpha', 'V_pp', 'f_burst', 'duty_cycle'])
    for a in alpha:
        for v in V_pp:
            for f in f_burst:
                for d in duty_cycle:
                    df_test_2 = pd.concat([df_test_2, pd.DataFrame([[a, v, f, d]], columns=['alpha', 'V_pp', 'f_burst', 'duty_cycle'])])
    print('break')  
    return df_test_2

def test_3(alpha = alpha_short, V_pp=V_pp_short, f_burst=f_burst_long, duty_cycle=duty_cycle_short):
    df_test_3 = pd.DataFrame(columns=['alpha', 'V_pp', 'f_burst', 'duty_cycle'])
    for a in alpha:
        for v in V_pp:
            for f in f_burst:
                for d in duty_cycle:
                    df_test_3 = pd.concat([df_test_3, pd.DataFrame([[a, v, f, d]], columns=['alpha', 'V_pp', 'f_burst', 'duty_cycle'])])
    print('break')   
    return df_test_3

def test_4(alpha = alpha_short, V_pp=V_pp_short, f_burst=f_burst_short, duty_cycle=duty_cycle_long):
    df_test_4 = pd.DataFrame(columns=['alpha', 'V_pp', 'f_burst', 'duty_cycle'])
    for a in alpha:
        for v in V_pp:
            for f in f_burst:
                for d in duty_cycle:
                    df_test_4 = pd.concat([df_test_4, pd.DataFrame([[a, v, f, d]], columns=['alpha', 'V_pp', 'f_burst', 'duty_cycle'])])
    print('break')
    return df_test_4

def combined_test(test_1=test_1(), test_2=test_2(), test_3=test_3(), test_4=test_4()):
    df_combined = pd.concat([test_1, test_2, test_3, test_4])
    # Remove duplicates from df_combined
    df_combined = df_combined.drop_duplicates()
    df_combined = df_combined.reset_index(drop=True)

    # Given that every test takes 3 minutes, how long will it take to run all tests?
    time_per_test = 2 # minutes
    print('Number of tests: ', len(df_combined))
    print('Time to run all tests: ', len(df_combined)*time_per_test/60, ' hours')
    print('break')

    df_combined.to_excel('Stability\\wind_tunnel_test\\wind_tunnel_test_matrix.xlsx', index=False)
    return df_combined

def main():
    test = test_4()
    df_combined = combined_test()
    
if __name__ == '__main__':
    main()
