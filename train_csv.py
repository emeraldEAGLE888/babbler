import os
import csv
import time
import re
import kagglehub
from babbler import SafeMultiWikiBabbler

print("Connecting to Kaggle... Stream-downloading dataset files...")
dataset_folder_path = kagglehub.dataset_download("d3stron/english-music-lyrics-5-genres-500k")

full_csv_path = None
for file in os.listdir(dataset_folder_path):
    if file.endswith(".csv"):
        full_csv_path = os.path.join(dataset_folder_path, file)
        if "train" in file.lower():
            break

if not full_csv_path:
    print("❌ Error: No CSV file found.")
    exit()

db_file = "kaggle_lyrics_pool.db"
bot = SafeMultiWikiBabbler(db_path=db_file)

print("\nStarting training (Songs)")

with open(full_csv_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    lyrics_key = None
    possible_keys = ['lyrics', 'lyric', 'text', 'lyrics_clean']
    
    if reader.fieldnames:
        for field in reader.fieldnames:
            if field.lower() in possible_keys or field.strip().lower() in possible_keys:
                lyrics_key = field
                break
                
    if not lyrics_key:
        print(f"Error: Could not find lyrics column.")
        exit()
        
    count = 0
    start_time = time.time()
    
    for row in reader:
        raw_lyrics = row.get(lyrics_key) 
        
        if raw_lyrics: 
            # Find any space followed by a Capital Letter, and prepend [LINEBREAK] token
            formatted_lyrics = re.sub(r'\s+([A-Z])', r' [LINEBREAK] \1', raw_lyrics)
            
            # Feed the newly structured text into Markov chain
            bot.train_chunk(formatted_lyrics)
            count += 1
            
            if count % 10 == 0:
                elapsed = time.time() - start_time
                print(f" Digested {count} songs... (Running for {int(elapsed)} seconds)", flush=True)
                
        # Stopping at 3000 songs
        if count >= 3000: 
            break

print(f"\nSuccessfully mported {count} songs")