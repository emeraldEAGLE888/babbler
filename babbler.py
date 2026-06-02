import sqlite3
import random
import os
import json
import urllib.request
import urllib.parse
import time
from collections import defaultdict

class SafeMultiWikiBabbler:
    def __init__(self, db_path="wiki_large_pool.db"):
        self.db_path = db_path
        self._setup_database()

    def _setup_database(self):
        #Initializes the SQLite database with multi-order matrix schema tracking.
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transitions (
                    chain_order INTEGER,
                    state TEXT,
                    next_word TEXT,
                    frequency INTEGER,
                    PRIMARY KEY (chain_order, state, next_word)
                )
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_state_order ON transitions (chain_order, state)")
            conn.commit()

    def train_chunk(self, text_chunk):
        #Trains the model simultaneously across Orders 1-4 with punctuation attached to words.
        # Clean formatting while keeping periods, commas, and sentence structure glued to words
        clean_text = text_chunk.replace("\n", " ").replace('"', '').replace("'", "")
        words = clean_text.split()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            for order in range(1, 5):
                if len(words) <= order:
                    continue

                chunk_transitions = defaultdict(int)
                for i in range(len(words) - order):
                    state = " ".join(words[i : i + order])
                    next_word = words[i + order]
                    chunk_transitions[(state, next_word)] += 1

                query = """
                    INSERT INTO transitions (chain_order, state, next_word, frequency) 
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(chain_order, state, next_word) 
                    DO UPDATE SET frequency = frequency + EXCLUDED.frequency
                """
                data = [(order, state, next_word, freq) for (state, next_word), freq in chunk_transitions.items()]
                cursor.executemany(query, data)
            
            conn.commit()

    def fetch_and_train_pool(self, topics):
        """Automatically downloads text via Wikipedia's API with rate-limiting built-in."""
        total_topics = len(topics)
        print(f"--- Starting Live Download of {total_topics} Articles ---")
        
        for index, topic in enumerate(topics, 1):
            encoded_topic = urllib.parse.quote(topic)
            url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles={encoded_topic}&format=json&origin=*&redirects=1"
            
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'MarkovLargePoolBot/2.5 (educational_project@example.com)'}
            )
            
            try:
                print(f"[{index}/{total_topics}] Downloading: '{topic}'...")
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    pages = data['query']['pages']
                    page_id = list(pages.keys())[0]
                    
                    if page_id == "-1":
                        print(f"   -> Warning: '{topic}' not found. Skipping.")
                        continue
                        
                    page_text = pages[page_id]['extract']
                    word_count = len(page_text.split())
                    
                    self.train_chunk(page_text)
                    print(f"   -> Success! Trained matrix configurations with {word_count} words.")
                    
            except Exception as e:
                print(f"   -> Failed to process '{topic}'. Error: {e}")
            
            if index < total_topics:
                time.sleep(1.0)
                
        print("\n--- All Training Complete! Database Matrix Is Ready ---")

    def _get_next_word_probabilities(self, state_text, order):
        """Queries DB to get possible words tailored to the specific Markov Order."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT next_word, frequency FROM transitions WHERE chain_order = ? AND state = ?", 
                (order, state_text)
            )
            results = cursor.fetchall()
            
        if not results:
            return None, None
            
        words = [row[0] for row in results]
        weights = [row[1] for row in results]
        return words, weights

    def _get_random_state(self, order):
        """Grabs a completely random seed state restricted to the target configuration order."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT state FROM transitions WHERE chain_order = ? ORDER BY RANDOM() LIMIT 1", (order,))
            res = cursor.fetchone()
            return res[0] if res else None

    def babble(self, num_words=100, temperature=1.0, order=2):
        """Generates text using backoff routines while ensuring sentences finish cleanly at word limits."""
        current_state_text = self._get_random_state(order)
        if not current_state_text:
            return f"The database matrix is empty for Order {order}. Please train the model first."

        output = current_state_text.split()
        
        # Extend past word count ceiling up to 40 words extra to find a natural sentence finale
        max_tokens = num_words + 40
        sentence_endings = (".", "!", "?")

        while len(output) < num_words or (not output[-1].endswith(sentence_endings) and len(output) < max_tokens):
            words, weights = self._get_next_word_probabilities(current_state_text, order)

            if words and weights:
                safe_temp = max(temperature, 0.01)
                adjusted_weights = [w ** (1.0 / safe_temp) for w in weights]
                next_word = random.choices(words, weights=adjusted_weights, k=1)[0]
                output.append(next_word)
                current_state_text = " ".join(output[-order:])
            else:
                # SAFE BACKOFF SEQUENCE: Drops down an order securely since words hold their punctuation context
                fallback_order = order - 1
                backed_off = False
                
                while fallback_order >= 1:
                    fallback_state = " ".join(output[-fallback_order:])
                    words, weights = self._get_next_word_probabilities(fallback_state, fallback_order)
                    if words and weights:
                        safe_temp = max(temperature, 0.01)
                        adjusted_weights = [w ** (1.0 / safe_temp) for w in weights]
                        next_word = random.choices(words, weights=adjusted_weights, k=1)[0]
                        output.append(next_word)
                        current_state_text = " ".join(output[-order:])
                        backed_off = True
                        break
                    fallback_order -= 1
                
                if not backed_off:
                    # Original Teleportation: Triggers only if an entire chain completely breaks mid-thought
                    teleport_state = self._get_random_state(order)
                    if not teleport_state:
                        break
                    output.extend(teleport_state.split())
                    current_state_text = " ".join(output[-order:])

        # Force a period at the absolute end if the generation window clipped off mid-sentence
        if not output[-1].endswith(sentence_endings):
            output[-1] = output[-1] + "."

        return " ".join(output)

if __name__ == "__main__":
    bot = SafeMultiWikiBabbler(db_path="wiki_large_pool.db")
    my_custom_list = [
        "Albert Einstein", "Isaac Newton", "Leonardo da Vinci", "William Shakespeare", 
        "Napoleon", "Julius Caesar", "Abraham Lincoln", "Adolf Hitler", 
        "Michael Jackson", "Taylor Swift", "United States", "China", "India", "Russia", 
        "United Kingdom", "Germany", "France", "Japan", "World War II", "World War I", 
        "Cold War", "French Revolution", "American Civil War", "Russian Revolution", 
        "Physics", "Mathematics", "Theory of Relativity", "Quantum Mechanics", 
        "Evolution", "Natural Selection", "DNA", "Periodic Table", "Internet", 
        "World Wide Web", "Artificial Intelligence", "Machine Learning", "Google", 
        "Microsoft", "Star Wars", "The Lord of the Rings", "Doctor Who", "The Simpsons", 
        "Game of Thrones", "Minecraft", "World of Warcraft", "COVID-19", "Climate Change", 
        "FIFA World Cup", "Premier League", "ChatGPT"
    ]
    bot.fetch_and_train_pool(my_custom_list)
