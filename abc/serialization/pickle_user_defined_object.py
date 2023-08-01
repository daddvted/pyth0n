import pickle


class NewClass:
    def __init__(self, data) -> None:
        print(data)
        self.data = data

new_class = NewClass(6)

# Serialize and deserialize
pickled_data = pickle.dumps(new_class)
reconstructed_data = pickle.loads(pickled_data)

print(type(reconstructed_data))
print(reconstructed_data.data)