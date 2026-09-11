import os
import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

_dir = os.path.dirname(os.path.abspath(__file__))
_model_dir = os.path.join(_dir, "models", "nsfw_onnx")

from download_model import ensure_model
ensure_model()

_model_path = os.path.join(_model_dir, "model.onnx")
_tokenizer_path = os.path.join(_model_dir, "tokenizer.json")

print("Loading NSFW detector (ONNX)...")
_tokenizer = Tokenizer.from_file(_tokenizer_path)
_tokenizer.enable_padding(length=128, pad_id=0)
_tokenizer.enable_truncation(max_length=128)
_options = ort.SessionOptions()
_options.inter_op_num_threads = 2
_options.intra_op_num_threads = 4
_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
_session = ort.InferenceSession(_model_path, _options, providers=["CPUExecutionProvider"])
_input_name = _session.get_inputs()[0].name
_attention_name = _session.get_inputs()[1].name
_ids_buf = np.zeros((1, 128), dtype=np.int64)
_mask_buf = np.zeros((1, 128), dtype=np.int64)
print("NSFW detector ready.")


def check_prompt(text):
    enc = _tokenizer.encode(text)
    n = len(enc.ids)
    _ids_buf[0, :n] = enc.ids
    _mask_buf[0, :n] = enc.attention_mask
    outputs = _session.run(None, {_input_name: _ids_buf, _attention_name: _mask_buf})
    logits = outputs[0][0]
    exp = np.exp(logits - logits.max())
    probs = exp / exp.sum()
    label = "NSFW" if probs[1] > probs[0] else "SFW"
    return {"label": label, "confidence": float(probs.max())}
