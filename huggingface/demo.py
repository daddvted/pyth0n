from transformers import pipeline


classifier = pipeline("sentiment-analysis")
print(classifier("I've been waiting for a HuggingFace course my whole life."))
print(classifier("I think the weather today sucks"))
print(classifier("天气不错"))
