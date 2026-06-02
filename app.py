from flask import Flask, render_template, jsonify, request
from babbler import SafeMultiWikiBabbler

app = Flask(__name__)

# Three completely isolated database engine configurations
engines = {
    "general": SafeMultiWikiBabbler(db_path="wiki_large_pool.db"),
    "philosophy": SafeMultiWikiBabbler(db_path="wiki_philosophy_pool.db"),
    "lyrics": SafeMultiWikiBabbler(db_path="wiki_lyrics_pool.db"),
    "kaggle_lyrics": SafeMultiWikiBabbler(db_path="kaggle_lyrics_pool.db"),
    "hogwarts": SafeMultiWikiBabbler(db_path="harry_potter_pool.db")
}

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/babble')
def babble():
   model_choice = request.args.get('model', default='general', type=str)
   num_words = request.args.get('num_words', default=80, type=int)
   temperature = request.args.get('temperature', default=1.0, type=float)
   order = request.args.get('order', default=2, type=int)
  
   bot = engines.get(model_choice, engines['general'])
   text = bot.babble(num_words=num_words, temperature=temperature, order=order)
   
   # Post-Generation Cleanup: Turn the text token into a clean HTML line break
   # Cleaning up surrounding whitespace keeps things perfectly left-aligned
   text = text.replace(" [LINEBREAK] ", "<br>").replace("[LINEBREAK] ", "<br>").replace(" [LINEBREAK]", "<br>").replace("[LINEBREAK]", "<br>")
   
   return jsonify({'text': text})

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)