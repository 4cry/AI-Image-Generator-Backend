import os
import sys
import glob

_dir = os.path.dirname(os.path.abspath(__file__))
_model_dir = os.path.join(_dir, "models", "nsfw_onnx")
_model_path = os.path.join(_model_dir, "model.onnx")
_marker = os.path.join(_model_dir, ".done")


def ensure_model():
    if os.path.exists(_marker):
        if os.path.exists(_model_path):
            return True

    parts = sorted(glob.glob(os.path.join(_model_dir, "model.onnx.part_*")))
    if not parts:
        if os.path.exists(_model_path):
            with open(_marker, "w") as f:
                f.write("done")
            return True
        print("ERROR: No model parts found.")
        return False

    print(f"Assembling NSFW model from {len(parts)} parts...")
    with open(_model_path, "wb") as out:
        for part in parts:
            with open(part, "rb") as f:
                out.write(f.read())

    for part in parts:
        os.remove(part)

    with open(_marker, "w") as f:
        f.write("done")
    print("Model ready.")
    return True


if __name__ == "__main__":
    ok = ensure_model()
    sys.exit(0 if ok else 1)
