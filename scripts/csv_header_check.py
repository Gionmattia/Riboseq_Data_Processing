import pandas as pd
import numpy as np
import sys

def load_csv(path):
    '''
    Loads the .csv, given as an argument to the script in the terminal, as a dataframe (df).
    '''

    df = pd.read_csv(path)
    
    return(df)


def header_check(df):
    '''
    Checks whether the .csv file already has an header with the labels required or not.
    '''
    
    has_header = True
    df_columns = list(df.columns)
    needed_columns = ["Run", "Submission", "download_path", "ScientificName"]
    for each in needed_columns:
        if each not in df_columns:
            has_header = False
            
    return has_header


def check_col_order(df):
    '''
    Checks if the columns in the .csv file without header are in the usual order (the one displayed by RUnInfo.csv files) or not.
    '''

    first_check = df.iat[0,1] # SRR value. Must start with SRR.
    second_check = df.iat[0,10] # Download path. Must start with "https://".
    third_check =df.iat[0,29] # Must be a string.
    
    # First check: 
    formatted = True
    try:
        first_check.index("SRR")
    except:
        formatted = False
        pass

    # Second check:
    try:
        second_check.index("https://")
    except:
        formatted = False
        pass
    # Third check:
    try: 
        isinstance(third_check, str)
    except:
        formatted = False
        pass
        
    return (formatted)


def assign_all_col_names(df):
    '''
    Assigns column names to a headless .csv, assuming the columns follow the usual order ((the one displayed by RUnInfo.csv files).
    '''

    runInfo_colnames = ['Unnamed: 0', 'Run', 'ReleaseDate', 'LoadDate', 'spots', 'bases',
    'spots_with_mates', 'avgLength', 'size_MB', 'AssemblyName',
    'download_path', 'Experiment', 'LibraryName', 'LibraryStrategy',
    'LibrarySelection', 'LibrarySource', 'LibraryLayout', 'InsertSize',
    'InsertDev', 'Platform', 'Model', 'SRAStudy', 'BioProject',
    'Study_Pubmed_id', 'ProjectID', 'Sample', 'BioSample', 'SampleType',
    'TaxID', 'ScientificName', 'SampleName', 'g1k_pop_code', 'source',
    'g1k_analysis_group', 'Subject_ID', 'Sex', 'Disease', 'Tumor',
    'Affection_Status', 'Analyte_Type', 'Histological_Type', 'Body_Site',
    'CenterName', 'Submission', 'dbgap_study_accession', 'Consent','RunHash', 'ReadHash']
    
    df.columns = runInfo_colnames
    
    return (df)

 
def assing_blank_names(df):
    '''
    Assigns temporary names (BLNK#) to the columns.
    '''

    runInfo_blnk_colnames = ["BLNK"+str(x) for x in range(48)]
    df.columns = runInfo_blnk_colnames
    
    return (df)


def find_and_rename_columns_needed(df):
    '''
    Checks the columns in the df for the 4 columns of interest (Run, Submission, ScientificName and download_path) and assings them the correct label.
    '''

    SRR = False
    SRA = False
    Donwload_path = False
    ScientificName = False
    
  # Assign names to columns of interest, if present in the df.

    for each in range(0,48):
        df_cell = df.iat[0,each]
        co_name = df.columns[each]
        if type(df_cell) == str:
            
            if "SRR" in df_cell and "-" not in df_cell:
                # print("FOUND SRR!", df_cell)
                df = df.rename(columns={co_name:"Run"})
                SRR = True

            if "SRA" in df_cell:
                # print("FOUND SRA!", df_cell)
                df = df.rename(columns={co_name:"Submission"})
                SRA = True
            
            if "https" in df_cell:
                # print("FOUND LINK!", df_cell)      
                df = df.rename(columns={co_name:"download_path"})
                Donwload_path = True
            
            if df_cell[0].isupper and " " in df_cell and ((":" or "-") not in df_cell):
                words = df_cell.split(" ")
                if words[1][0].islower():
                    # print("FOUND NAME!!", df_cell)
                    df = df.rename(columns={co_name:"ScientificName"})
                    ScientificName = True
    
    
    # Check if the 4 columns of interested were all found in the df
    if SRR == False:
        raise Exception("SRR values are missing from the .csv file")
    if SRA == False:
        raise Exception("SRA values are missing from the .csv file")
    if Donwload_path == False:
        raise Exception("Donwload paths are missing from the .csv file")    
    if ScientificName == False:
        raise Exception("Scientific Names are missing from the .csv file")
        
    return (df)


def save_with_new_name(df):
    '''
    Saves the df as a new .csv file <previous name> + "_with_header.csv"
    '''

    csv_file = sys.argv[1]
    name_as_list = csv_file.split(".")
    new_name = name_as_list[0] + "_with_header.csv"
    df.to_csv(new_name, index=False)
    
    return


# First checks whether the loaded csv has an header or not. If yes, the file is returned with the new name.
# If not, checks whether the columns are in the "usual" order displayed by RunInfo.csv files or not.
# If yes, the header with all names is attached. If not, only the 4 columns of interest are labelled.
# In both cases, the output is a new .csv file.
# 
if __name__ == "__main__":
    df = load_csv(sys.argv[1])
    if header_check == True:
        df = save_with_new_name(df)
        print(header_check)
    else:
        if check_col_order(df):
            df = assign_all_col_names(df)
            df = save_with_new_name(df)
        elif not check_col_order(df):
            df = assing_blank_names(df)
            df = find_and_rename_columns_needed(df)
            df = save_with_new_name(df)