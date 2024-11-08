import pandas as pd
def pull_data_from_excel(p,columns_to_pull):
    #p = 'InventoryValuation.xlsx'
    data = pd.read_excel(p) 
    df = pd.DataFrame(data, columns=columns_to_pull)
    L = df.values.tolist() #this is a list of itemId matched with BBVT Warehouse (Value)
    return L
