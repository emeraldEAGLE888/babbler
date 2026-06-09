import os
from babbler import SafeMultiWikiBabbler

# Setup paths
books_folder = "hp_books"
db_file = "harry_potter_pool.db"

# Smart Fallback: Checks if the folder was accidentally left inside 'templates'
if not os.path.exists(books_folder) and os.path.exists("templates/hp_books"):
    books_folder = "templates/hp_books"

# Guardrail check to make sure the folder actually exists and has files
if not os.path.exists(books_folder) or not os.listdir(books_folder):
    print(f"❌ Error: Please create the '{books_folder}' folder and drop your HP .txt files inside it first!")
    exit()

bot = SafeMultiWikiBabbler(db_path=db_file)
print("\nStarting training (Harry Potter)")

# Loop through every text file in your folder
for filename in os.listdir(books_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(books_folder, filename)
        print(f"Training on: {filename}...")
        
        # Open the file using errors="ignore" to bypass any smart-quote encoding crashes
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            raw_text = file.read()
            
            # 🎯 THE PARAGRAPH NORMALIZATION PATCH:
            # Step 1: Convert true paragraph blank lines (\n\n) into a single clean token
            formatted_text = raw_text.replace("\n\n", " [LINEBREAK] ")
            
            # Step 2: Convert stray single newlines (accidental mid-sentence margins) into normal spaces
            formatted_text = formatted_text.replace("\n", " ")
            
            # Feed the perfectly cleaned book text into your Markov engine
            bot.train_chunk(formatted_text)

print("\nTraining complete.")