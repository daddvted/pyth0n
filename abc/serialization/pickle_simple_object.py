import pickle

# A python dict object
test_dict = {"hello": "world"}

# Serialization
with open("test.pickle", "wb") as outfile:
    pickle.dump(test_dict, outfile)

# Deserialization
with open("test.pickle", "rb") as infile:
    test_dict_reconstructured = pickle.load(infile)

print(f"Reconstructed object: {test_dict_reconstructured}")

assert test_dict == test_dict_reconstructured


