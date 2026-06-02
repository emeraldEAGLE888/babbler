import urllib.request
import urllib.parse
import json
import time
from babbler import SafeMultiWikiBabbler

# 60 Iconic Tracks curated to mix completely different lyrical structures
tracklist = [
    # --- The Original Starter 12 ---
    ("Queen", "Bohemian Rhapsody"),
    ("The Beatles", "Hey Jude"),
    ("Michael Jackson", "Billie Jean"),
    ("Taylor Swift", "Blank Space"),
    ("Eminem", "Lose Yourself"),
    ("Nirvana", "Smells Like Teen Spirit"),
    ("Led Zeppelin", "Stairway to Heaven"),
    ("David Bowie", "Heroes"),
    ("Bob Dylan", "Like a Rolling Stone"),
    ("Billie Eilish", "Bad Guy"),
    ("Pink Floyd", "Comfortably Numb"),
    ("Kendrick Lamar", "Humble"),

    # --- Classic Rock & Anthems ---
    ("Eagles", "Hotel California"),
    ("Guns N' Roses", "Sweet Child O' Mine"),
    ("Billy Joel", "Piano Man"),
    ("Elton John", "Rocket Man"),
    ("The Rolling Stones", "Sympathy for the Devil"),
    ("Fleetwood Mac", "Dreams"),
    ("Oasis", "Wonderwall"),
    ("Bon Jovi", "Livin' on a Prayer"),
    ("Journey", "Don't Stop Believin'"),
    ("AC/DC", "Back in Black"),
    ("The Police", "Every Breath You Take"),
    ("Queen", "Don't Stop Me Now"),

    # --- Pop & Dance Classics ---
    ("Michael Jackson", "Thriller"),
    ("Britney Spears", "Toxic"),
    ("Adele", "Rolling in the Deep"),
    ("Lady Gaga", "Bad Romance"),
    ("ABBA", "Dancing Queen"),
    ("Beyoncé", "Single Ladies"),
    ("Rihanna", "Umbrella"),
    ("Bruno Mars", "Just the Way You Are"),
    ("Maroon 5", "Sugar"),
    ("Madonna", "Like a Virgin"),

    # --- Modern Pop & Radio Hits ---
    ("Taylor Swift", "Cruel Summer"),
    ("The Weeknd", "Blinding Lights"),
    ("Harry Styles", "As It Was"),
    ("Dua Lipa", "Levitating"),
    ("Olivia Rodrigo", "Drivers License"),
    ("Billie Eilish", "Happier Than Ever"),
    ("Kate Bush", "Running Up That Hill"),

    # --- Alternative, Grunge & Metal ---
    ("The Killers", "Mr. Brightside"),
    ("The White Stripes", "Seven Nation Army"),
    ("Hozier", "Take Me to Church"),
    ("Coldplay", "Viva La Vida"),
    ("Green Day", "Basket Case"),
    ("Linkin Park", "In the End"),
    ("Radiohead", "Creep"),
    ("Metallica", "Master of Puppets"),
    ("Foo Fighters", "Everlong"),

    # --- Country & Soul Narratives ---
    ("Dolly Parton", "Jolene"),
    ("Johnny Cash", "Ring of Fire"),
    ("John Denver", "Take Me Home, Country Roads"),
    ("Whitney Houston", "I Will Always Love You"),
    ("Amy Winehouse", "Back to Black"),

    # --- Disney & Musical Theatre (Rich, expressive storytelling vocabulary) ---
    ("Idina Menzel", "Let It Go"),
    ("Lin-Manuel Miranda", "We Don't Talk About Bruno"),
    ("Elton John", "Circle of Life"),
    ("Judy Garland", "Over the Rainbow"),

    # --- Synth-Pop & New Wave (Distinct rhythmic phrasing) ---
    ("A-ha", "Take On Me"),
    ("Tears for Fears", "Everybody Wants to Rule the World"),
    ("Rick Astley", "Never Gonna Give You Up"),
    ("Eurythmics", "Sweet Dreams"),
    ("Men At Work", "Down Under"),

    # --- Clean Pop & Radio Anthems ---
    ("Pharrell Williams", "Happy"),
    ("Justin Timberlake", "Can't Stop the Feeling!"),
    ("Owl City", "Fireflies"),
    ("Carly Rae Jepsen", "Call Me Maybe"),
    ("OneRepublic", "Counting Stars"),
    ("Lorde", "Royals"),
    ("Imagine Dragons", "Radioactive"),
    ("Ed Sheeran", "Perfect"),

    # --- Folk, Soul & Acoustic Classics ---
    ("Simon & Garfunkel", "The Sound of Silence"),
    ("Bill Withers", "Lean on Me"),
    ("Stevie Wonder", "Superstition"),
    ("The Beatles", "Yesterday"),
    ("Ben E. King", "Stand by Me"),
    ("Neil Diamond", "Sweet Caroline"),
    ("Louis Armstrong", "What a Wonderful World"),

    # --- Alternative & Indie (Great abstract sentence transitions) ---
    ("Coldplay", "Yellow"),
    ("Vance Joy", "Riptide"),
    ("Bastille", "Pompeii"),
    ("Gotye", "Somebody That I Used to Know"),
    ("Twenty One Pilots", "Stressed Out"),
    ("The Lumineers", "Ho Hey")
]

db_file = "wiki_lyrics_pool.db"
bot = SafeMultiWikiBabbler(db_path=db_file)

print(f"--- Starting Live Download of {len(tracklist)} Songs ---")

for index, (artist, track) in enumerate(tracklist, 1):
    encoded_artist = urllib.parse.quote(artist)
    encoded_track = urllib.parse.quote(track)
    
    url = f"https://lrclib.net/api/get?artist_name={encoded_artist}&track_name={encoded_track}"
    
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'MarkovLyricsBot/1.0 (educational_project@example.com)'}
    )
    
    try:
        print(f"[{index}/{len(tracklist)}] Fetching: '{track}' by {artist}...")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            lyrics_text = data.get('plainLyrics')
            
            if not lyrics_text:
                print(f"   -> Warning: No plain lyrics found for '{track}'. Skipping.")
                continue
            
            # Convert structural layout newlines into a safe word token before babbler.py strips them
            formatted_lyrics = lyrics_text.replace("\n", " [LINEBREAK] ")
                
            word_count = len(formatted_lyrics.split())
            bot.train_chunk(formatted_lyrics)
            print(f"   -> Success! Trained matrix configurations with {word_count} tokens.")
            
    except Exception as e:
        print(f"   -> Failed to process '{track}'. Error: {e}")
        
    # Crucial 1-second pause to prevent getting blocked by the free API
    time.sleep(1.0)

print("\n--- Lyrics Database Matrix Generation Complete! ---")