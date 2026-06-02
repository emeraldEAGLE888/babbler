from babbler import SafeMultiWikiBabbler

philosophy_topics = [
    "Philosophy", "Metaphysics", "Epistemology", "Ontology", "Logic", "Truth", 
    "Knowledge", "Belief", "Justification (epistemology)", "Causality", "Identity", 
    "Objectivity (philosophy)", "Subjectivity", "Realism", "Idealism", "Determinism", 
    "Free Will", "Philosophy of Mind", "Consciousness", "Mind", "Intentionality", 
    "Qualia", "Mental Representation", "Theory of Mind", "Self-Awareness", 
    "Personal Identity", "Cognitive Science", "Cognitive Psychology", "Perception", 
    "Attention", "Memory", "Concept", "Abstraction", "Categorization", "Decision-Making", 
    "Reasoning", "Problem Solving", "Intelligence", "Creativity", "Systems and Complexity", 
    "Systems Theory", "System", "Complex System", "Emergence", "Self-Organization", 
    "Feedback", "Adaptation", "Network Science", "Cybernetics", "Dynamic System", 
    "Information", "Information Theory", "Communication", "Signal", "Semantics", 
    "Pragmatics", "Symbol", "Linguistics", "Language", "Representation", "Model", 
    "Structure", "Pattern", "Relation", "Classification", "Semiotics", 
    "Theoretical Computer Science", "Computation", "Algorithm", "Space", "Time", 
    "Entropy", "Order and Disorder", "Complexity"
]

print("Building secondary database: wiki_philosophy_pool.db...")
bot = SafeMultiWikiBabbler(db_path="wiki_philosophy_pool.db")
bot.fetch_and_train_pool(philosophy_topics)