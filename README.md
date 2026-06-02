# Final Project - Markov Babbler

### Discussion

For our final project, we've created a Markov Babbler. This demonstration has been trained on several publicly available curated datasets. We used SQLite to make an index representing a sparse matrix. The generator uses Markov chains to model the words that most probably follow any given word from the dataset. 

### Linear Algebra Application

This babbler uses a transition matrix, where each entry represents the probability of moving from one state (word) to another. The matrix stores the relationships between states and is used to predict the next likely word(s) based on the current word. Iterating on these probabilities results in sentences that appear coherent but generally do not hold any real meaning.
