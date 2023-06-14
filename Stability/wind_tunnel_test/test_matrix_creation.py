import itertools as it
import numpy as np
import pandas as pd


 
alpha_short = [-2, 0, 2, 5, 8]
alpha_long = [-8, -5, -2, 0, 2, 5, 8, 10, 12]


V_pp_short = [0, 12]
V_pp_long = [0, 12]


f_burst_short = [10, 50, 200]
f_burst_long = [2, 5, 10, 20, 50, 100] #500 is unrealistic
# remove the 200, 500 by more in between values or removing them

duty_cycle_short = [0.1, 0.5, 1]
duty_cycle_long = [0.1, 0.3, 0.5, 0.7, 1]



def test_1(alpha = alpha_long, V_pp=V_pp_short, f_burst=f_burst_short, duty_cycle=duty_cycle_short):
    df_test_1 = pd.DataFrame(columns=['test series', 'alpha', 'V_pp', 'f_burst', 'duty_cycle'])
    for a in alpha:
        for v in V_pp:
            if v == 0:
                f = 'X'
                d = 'X'
                df_test_1 = pd.concat([df_test_1, pd.DataFrame([[1, a, v, f, d]], columns=['test series', 'alpha', 'V_pp', 'f_burst', 'duty_cycle'])])
            else:
                for f in f_burst:
                    for d in duty_cycle:
                        df_test_1 = pd.concat([df_test_1, pd.DataFrame([[1, a, v, f, d]], columns=['test series', 'alpha', 'V_pp', 'f_burst', 'duty_cycle'])])
    print('break')
    return df_test_1

def test_3(alpha = alpha_short, V_pp=V_pp_short, f_burst=f_burst_long, duty_cycle=duty_cycle_short):
    df_test_3 = pd.DataFrame(columns=['test series', 'alpha', 'V_pp', 'f_burst', 'duty_cycle'])
    for a in alpha:
        for v in V_pp:
            if v == 0:
                f = 'X'
                d = 'X'
                df_test_3 = pd.concat([df_test_3, pd.DataFrame([[3, a, v, f, d]], columns=['test series', 'alpha', 'V_pp', 'f_burst', 'duty_cycle'])])
            else:
                for f in f_burst:
                    for d in duty_cycle:
                        df_test_3 = pd.concat([df_test_3, pd.DataFrame([[3, a, v, f, d]], columns=['test series', 'alpha', 'V_pp', 'f_burst', 'duty_cycle'])])
    print('break')   
    return df_test_3

def test_4(alpha = alpha_short, V_pp=V_pp_short, f_burst=f_burst_short, duty_cycle=duty_cycle_long):
    df_test_4 = pd.DataFrame(columns=['test series', 'alpha', 'V_pp', 'f_burst', 'duty_cycle'])
    for a in alpha:
        for v in V_pp:
            if v == 0:
                f = 'X'
                d = 'X'
                df_test_4 = pd.concat([df_test_4, pd.DataFrame([[4, a, v, f, d]], columns=['test series', 'alpha', 'V_pp', 'f_burst', 'duty_cycle'])])
            else:
                for f in f_burst:
                    for d in duty_cycle:
                        df_test_4 = pd.concat([df_test_4, pd.DataFrame([[4, a, v, f, d]], columns=['test series', 'alpha', 'V_pp', 'f_burst', 'duty_cycle'])])
    print('break')
    return df_test_4

def combined_test(test_1=test_1(), test_3=test_3(), test_4=test_4()):
    df_combined = pd.concat([test_1, test_3, test_4])
    # Remove duplicates from df_combined
    #df_combined = df_combined.drop_duplicates(subset=['alpha', 'V_pp', 'f_burst', 'duty_cycle'])
    # get rid of duplicates when V_pp = 0 #check if this is still correct!!!!!!!!!!!
    #df_combined = df_combined[~((df_combined['V_pp'] == 0) & (df_combined.duplicated(subset=['alpha'], keep='first')))]


     # Check for duplicates, ignoring 'test series' column
    df_combined = df_combined.reset_index(drop=True)
    #duplicates = df_combined[df_combined.duplicated(subset=df_combined.columns.difference(['test series']), keep=False)]
    df_combined = df_combined.sort_values(by=df_combined.columns.difference(['test series']).tolist())

    

    #df_combined = df_combined.reset_index(drop=True)

    # Given that every test takes 1 minutes, how long will it take to run all tests?
    time_per_test = 1 # minutes
    print('Number of tests: ', len(df_combined))
    print('Time to run all tests: ', len(df_combined)*time_per_test/60, ' hours')
    print('break')

    df_combined.to_excel('Stability\\wind_tunnel_test\\wind_tunnel_test_matrix.xlsx', index=True)
    return df_combined

def main():
    test = test_4()
    df_combined = combined_test()
    
if __name__ == '__main__':
    main()
