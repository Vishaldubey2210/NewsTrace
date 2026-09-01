import time
from app.nlp.emotion_analyzer import emotion_analyzer

def benchmark():
    sample = "The government celebrated a breakthrough triumph."
    start = time.time()
    for _ in range(1000):
        emotion_analyzer.analyze_emotions(sample)
    duration = time.time() - start
    print(f"⚡ NLP Benchmark: 1000 emotion classifications in {duration:.3f}s ({1000/duration:.1f} ops/sec)")

if __name__ == '__main__':
    benchmark()
