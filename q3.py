import re
import os
import pandas as pd
from tqdm import tqdm
from q2 import download_audio, cut_audio
from typing import List
import json


def filter_df(csv_path: str, label: str) -> pd.DataFrame:
    """
    Write a function that takes the path to the processed csv from q1 and returns a df of only the rows 
    that contain the human readable label passed as argument
    """
    # TODO
    df = pd.read_csv(csv_path)
    
    # Use the exact column name from the CSV
    label_col = 'label_names'
    
    # Filter rows containing the label - use exact matching in pipe-separated list
    def contains_label_func(label_str, target_label):
        if pd.isna(label_str):
            return False
        labels_list = str(label_str).split('|')
        return target_label in labels_list
    
    mask = df[label_col].apply(lambda x: contains_label_func(x, label))
    return df[mask]


def data_pipeline(csv_path: str, label: str) -> None:
    """
    Using your previously created functions, write a function that takes a processed csv and for each video with the given label:
    """
    # TODO
    df = filter_df(csv_path, label)
    
    if df.empty:
        print(f"No rows found for label: {label}")
        return
    
    # Create directories
    raw_dir = f"{label}_raw"
    cut_dir = f"{label}_cut"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(cut_dir, exist_ok=True)
    
    for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Processing {label}"):
        try:
            # Get YTID - use exact column name
            ytid = str(row['# YTID'])
            
            # Get start and end times - use exact column names with spaces
            start = float(row[' start_seconds'])
            end = float(row[' end_seconds'])
            
            raw_path = os.path.join(raw_dir, f"{ytid}.mp3")
            cut_path = os.path.join(cut_dir, f"{ytid}.mp3")
            
            download_audio(ytid, raw_path)
            cut_audio(raw_path, cut_path, start, end)
            
        except Exception as e:
            print(f"Error processing {ytid}: {e}")
            continue


def rename_files(path_cut: str, csv_path: str) -> None:
    """
    Write a function that renames the existing files to include start and end times.
    """
    # TODO
    if not os.path.exists(path_cut):
        return
    
    df = pd.read_csv(csv_path)
    
    # Get YTID column - use exact column name
    ytid_col = '# YTID'
    
    for filename in os.listdir(path_cut):
        if not filename.endswith('.mp3'):
            continue
        
        # Extract YTID from filename (remove .mp3 extension)
        ytid = filename[:-4]
        
        # Find matching row in dataframe
        matching_rows = df[df[ytid_col] == ytid]
        if matching_rows.empty:
            continue
        
        row = matching_rows.iloc[0]
        
        # Get start and end times - use exact column names with spaces
        start = int(float(row[' start_seconds']))  
        end = int(float(row[' end_seconds']))
        length = end - start
        
        new_filename = f"{ytid}_{start}_{end}_{length}.mp3"
        
        old_path = os.path.join(path_cut, filename)
        new_path = os.path.join(path_cut, new_filename)
        
        try:
            # Check if target file already exists, remove it first
            if os.path.exists(new_path):
                os.remove(new_path)
            if old_path != new_path:
                os.rename(old_path, new_path)
        except Exception as e:
            print(f"Error renaming {filename}: {e}")