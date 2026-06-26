import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re
import os

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(DATA_DIR, "plots")
os.makedirs(OUT_DIR, exist_ok=True)

FILES = {
    "local_cpu":  ("local_cpu_async_event1.csv",  "red",   "^", "Local CPU"),
    "local_gpu":  ("local_gpu_async_event1.csv",  "green", "^", "Local GPU"),
    "remote_cpu": ("remote_cpu_async_event1.csv", "red",   "o", "Remote CPU"),
    "remote_gpu": ("remote_gpu_async_event1.csv", "green", "o", "Remote GPU"),
}

def parse_gpu_util(val):
    """Extract first numeric value from e.g. 'GPU-xxx:0.362881;'"""
    if pd.isna(val):
        return float("nan")
    m = re.search(r":([0-9.eE+\-]+)", str(val))
    return float(m.group(1)) if m else float("nan")

def load(fname):
    path = os.path.join(DATA_DIR, fname)
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    df = df.sort_values("Concurrency").reset_index(drop=True)
    if "Avg GPU Utilization" in df.columns:
        df["Avg GPU Utilization"] = df["Avg GPU Utilization"].apply(parse_gpu_util)
    return df

dfs = {key: load(fname) for key, (fname, *_) in FILES.items()}

METRICS = [
    ("Inferences/Second",       "Inferences / Second"),
    ("Client Send",             "Client Send (µs)"),
    ("Network+Server Send/Recv","Network + Server Send/Recv (µs)"),
    ("Server Queue",            "Server Queue (µs)"),
    ("Server Compute Input",    "Server Compute Input (µs)"),
    ("Server Compute Infer",    "Server Compute Infer (µs)"),
    ("Server Compute Output",   "Server Compute Output (µs)"),
    ("Client Recv",             "Client Recv (µs)"),
    ("p50 latency",             "p50 Latency (µs)"),
    ("p90 latency",             "p90 Latency (µs)"),
    ("p95 latency",             "p95 Latency (µs)"),
    ("p99 latency",             "p99 Latency (µs)"),
    ("request/response",        "Request/Response (µs)"),
    ("response wait",           "Response Wait (µs)"),
    ("Avg GPU Utilization",     "Avg GPU Utilization (%)"),
]

for col, ylabel in METRICS:
    fig, ax = plt.subplots(figsize=(8, 5))
    for key, (_, color, marker, label) in FILES.items():
        if col == "Avg GPU Utilization" and "cpu" in key:
            continue
        df = dfs[key]
        if col not in df.columns:
            print(f"  skipping {key}: column '{col}' not found")
            continue
        ax.plot(
            df["Concurrency"], df[col],
            color=color, marker=marker, label=label,
            linestyle="-", linewidth=1.5, markersize=8,
        )
    ax.set_xlabel("Concurrent Requests")
    ax.set_ylabel(ylabel)
    ax.set_title(ylabel + " vs Concurrent Requests")
    ax.legend(title="LST alpaka")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    if col == "Avg GPU Utilization":
        ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)
    safe = re.sub(r"[^A-Za-z0-9_]+", "_", col).strip("_")
    out = os.path.join(OUT_DIR, f"{safe}.png")
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Saved {out}")

print("Done.")
