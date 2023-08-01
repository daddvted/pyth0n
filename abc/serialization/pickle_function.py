import pickle

def hello():
    return "hello world"


# Serialize and deserialize
pickled_function = pickle.dumps(hello)
reconstructed_function = pickle.loads(pickled_function)


print(reconstructed_function())