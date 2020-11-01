import h5py
filename = "neural/model.h5"

with h5py.File(filename, "r") as f:
    # List all groups
    print("Keys: {}: {}".format(f.keys(), f.values()))
    a_group_key = list(f.keys())[2]

    # Get the data
    data = list(f[a_group_key])
    print(data)