import json
import sys
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

def normalize_frame(frame):
    f = np.array(frame).flatten()
    return f / (np.linalg.norm(f) + 1e-6)


def flatten(seq):
    return [np.array(f).flatten() for f in seq]

action = sys.argv[1]
# with open(f"data/{action}.json") as f:
#     ref = json.load(f)
with open(f"data/{action}.json") as f:
    ref_data = json.load(f)

ref = ref_data["landmarks"]

with open("child.json") as f:
    child = json.load(f)

print(type(ref))
print(ref)

ref_seq = [normalize_frame(f) for f in ref]
child_seq = [normalize_frame(f) for f in child]

ref_seq = ref_seq[::2]     
child_seq = child_seq[::2]


print("Ref length:", len(ref_seq))
print("Child length:", len(child_seq))

distance, _ = fastdtw(ref_seq, child_seq, dist=euclidean)

score = np.exp(-distance / 50) * 100


print("DTW Distance:", distance)
print("Similarity Score:", score)

if score > 75:
    result = "Correct"
elif score > 50:
    result = "Almost Correct"
else:
    result = "Incorrect"

print(result)

with open("result.json", "w") as f:
    json.dump({
        "result": result,
        "score": float(score)
    }, f)