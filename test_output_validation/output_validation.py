#!/usr/bin/env python3
"""
output_validation.py

Reads LST_output_<LABEL>_run<N>.json files from the same directory,
validates and visualises output stability across labels and runs.

Labels : SONIC_GPU, SONIC_CPU, local_GPU, local_CPU
Runs   : 1 – 5  (missing files are silently skipped)

Outputs
-------
plot1_nTrackCandidates.png
plot2_pixelSeedIndex_overlap.png
plot3_trackCandidateType_overlap.png
plot4_hitIndices_event<NN>_<LABEL>.png   (one per event × label combination)
"""

import json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")           # non-interactive backend for batch use
import matplotlib.pyplot as plt

# ── Configuration ─────────────────────────────────────────────────────────────

DATA_DIR  = Path(__file__).parent          # same folder as this script
LABELS    = ["SONIC_GPU", "SONIC_CPU", "local_GPU", "local_CPU"]
RUNS      = [1, 2, 3, 4, 5]
N_EVENTS  = 10

STYLE = {
    "SONIC_GPU": {"color": "green", "marker": "o"},
    "SONIC_CPU": {"color": "red",   "marker": "o"},
    "local_GPU": {"color": "green", "marker": "^"},
    "local_CPU": {"color": "red",   "marker": "^"},
}

# Font sizes
TITLE_FS  = 14
LABEL_FS  = 12
TICK_FS   = 11
LEGEND_FS = 11
TABLE_FS  = 9

# Small horizontal nudge per label so stacked markers are individually visible
X_OFFSET = {
    "SONIC_GPU": -0.15,
    "SONIC_CPU": -0.05,
    "local_GPU": +0.05,
    "local_CPU": +0.15,
}

# ── Data loading ──────────────────────────────────────────────────────────────

def load_data():
    """Return data[label][run] = list-of-N_EVENTS event dicts."""
    data = {label: {} for label in LABELS}
    for label in LABELS:
        for run in RUNS:
            fpath = DATA_DIR / f"LST_output_{label}_run{run}.json"
            if not fpath.exists():
                continue
            with open(fpath) as f:
                raw = json.load(f)
            data[label][run] = raw["data"]
            print(f"Loaded  {fpath.name}  ({len(raw['data'])} events)")
    return data

# ── Jaccard overlap helper ────────────────────────────────────────────────────

def jaccard(vecA, vecB):
    """Multiset Jaccard overlap: 1 = identical, 0 = no overlap."""
    cA, cB = Counter(vecA), Counter(vecB)
    intersection = sum((cA & cB).values())
    union        = sum((cA | cB).values())
    return intersection / union if union > 0 else 1.0

# ── Two-level table helper ────────────────────────────────────────────────────

def attach_two_level_table(ax_tbl, all_cols, cell_data, row_labels):
    """
    Render a table on ax_tbl with a two-level header:
      Row 0 : full label names, visually merged across each label's columns
      Row 1 : "Run N" for each column
      Row 2+ : cell_data rows

    all_cols  : list of (label, run) pairs in display order
    cell_data : list[list[str]]  — N_EVENTS rows × len(all_cols) cols
    row_labels: list[str]        — one entry per event
    """
    # Group column indices by label (preserving order)
    label_groups = {}
    for idx, (lb, _) in enumerate(all_cols):
        label_groups.setdefault(lb, []).append(idx)

    # Build the two header rows that become part of cellText
    label_row = [""] * len(all_cols)   # filled in after table creation
    run_row   = [f"Run {r}" for _, r in all_cols]

    all_rows       = [label_row, run_row] + list(cell_data)
    row_labels_ext = ["", ""] + list(row_labels)   # blank labels for the two header rows

    # Equal column widths: each data column gets an identical share of the axes width.
    # 0.85 leaves ~15 % for the row-label column; the rest is split evenly.
    col_w = 0.85 / len(all_cols)

    ax_tbl.axis("off")
    tbl = ax_tbl.table(
        cellText=all_rows,
        rowLabels=row_labels_ext,
        loc="center",
        cellLoc="center",
        colWidths=[col_w] * len(all_cols),
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(TABLE_FS)

    # Style label row: simulate merged cells by hiding internal vertical borders
    # and placing the label text in the middle cell of each group.
    # (Without colLabels the first cellText row lands at table row index 0.)
    for lb in LABELS:
        if lb not in label_groups:
            continue
        indices = label_groups[lb]
        n_grp   = len(indices)
        mid_col = indices[n_grp // 2]

        for i, col_idx in enumerate(indices):
            cell = tbl[0, col_idx]
            cell.get_text().set_text("")          # clear; label text set below
            if n_grp > 1:
                if i == 0:
                    cell.visible_edges = "TBL"    # left boundary of the group
                elif i == n_grp - 1:
                    cell.visible_edges = "TBR"    # right boundary of the group
                else:
                    cell.visible_edges = "TB"     # interior — no vertical lines

        # Place full label name centred in the middle cell
        mid_cell = tbl[0, mid_col]
        mid_cell.get_text().set_text(lb)
        mid_cell.get_text().set_fontweight("bold")
        mid_cell.get_text().set_fontsize(TABLE_FS)

    return tbl


# ── Plot 1: nTrackCandidates per event ────────────────────────────────────────

def plot_ntrack(data):
    event_nums = list(range(1, N_EVENTS + 1))

    all_cols   = [(lb, r) for lb in LABELS for r in RUNS if r in data[lb]]
    row_labels = [f"Ev {i+1}" for i in range(N_EVENTS)]
    cell_data  = [
        [str(data[lb][r][i]["nTrackCandidates"][0]) if i < len(data[lb][r]) else "—"
         for lb, r in all_cols]
        for i in range(N_EVENTS)
    ]

    n_cols    = len(all_cols)
    tbl_width = max(4, n_cols * 0.85)
    fig, (ax, ax_tbl) = plt.subplots(
        1, 2, figsize=(13 + tbl_width, 6),
        gridspec_kw={"width_ratios": [13, tbl_width]},
        layout="constrained",
    )

    # ── Scatter ──
    for label in LABELS:
        s, dx = STYLE[label], X_OFFSET[label]
        first = True
        for run in RUNS:
            if run not in data[label]:
                continue
            evs = data[label][run]
            ys  = [evs[i]["nTrackCandidates"][0] for i in range(len(evs))]
            xs  = [e + dx for e in event_nums[:len(ys)]]
            ax.scatter(xs, ys, color=s["color"], marker=s["marker"], s=60, alpha=0.85,
                       label=label if first else "_nolegend_")
            first = False
    ax.set_xlabel("Event", fontsize=LABEL_FS)
    ax.set_ylabel("nTrackCandidates", fontsize=LABEL_FS)
    ax.set_title("Number of Track Candidates per Event  (all labels × runs 1–5)",
                 fontsize=TITLE_FS)
    ax.set_xticks(event_nums)
    ax.tick_params(labelsize=TICK_FS)
    ax.legend(framealpha=0.9, fontsize=LEGEND_FS)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    # ── Table ──
    attach_two_level_table(ax_tbl, all_cols, cell_data, row_labels)

    out = DATA_DIR / "plot1_nTrackCandidates.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Saved  {out.name}")

# ── Plot 2 & 3: Jaccard overlap per event (each run vs run1, same label) ─────

def plot_overlap(data, field, filename, title):
    event_nums = list(range(1, N_EVENTS + 1))

    # ── Build table data ──
    all_cols   = [(lb, r) for lb in LABELS if 1 in data[lb]
                           for r in RUNS[1:] if r in data[lb]]
    row_labels = [f"Ev {i+1}" for i in range(N_EVENTS)]
    cell_data  = []
    for i in range(N_EVENTS):
        row = []
        for lb, r in all_cols:
            run1 = data[lb][1]
            runN = data[lb][r]
            if i < min(len(run1), len(runN)):
                row.append(f"{jaccard(run1[i][field], runN[i][field]):.4f}")
            else:
                row.append("—")
        cell_data.append(row)

    n_cols    = len(all_cols)
    tbl_width = max(4, n_cols * 1.05)
    fig, (ax, ax_tbl) = plt.subplots(
        1, 2, figsize=(13 + tbl_width, 6),
        gridspec_kw={"width_ratios": [13, tbl_width]},
        layout="constrained",
    )

    # ── Scatter ──
    for label in LABELS:
        if 1 not in data[label]:
            continue
        run1_events = data[label][1]
        s, dx = STYLE[label], X_OFFSET[label]
        first = True
        for run in RUNS[1:]:
            if run not in data[label]:
                continue
            runN_events = data[label][run]
            n = min(len(run1_events), len(runN_events))
            ys = [jaccard(run1_events[i][field], runN_events[i][field]) for i in range(n)]
            xs = [e + dx for e in event_nums[:n]]
            ax.scatter(xs, ys, color=s["color"], marker=s["marker"], s=60, alpha=0.85,
                       label=f"{label}  (runs 2–5 vs run1)" if first else "_nolegend_")
            first = False
    ax.set_xlabel("Event", fontsize=LABEL_FS)
    ax.set_ylabel("Jaccard Overlap", fontsize=LABEL_FS)
    ax.set_ylim(-0.05, 1.05)
    ax.set_title(title, fontsize=TITLE_FS)
    ax.set_xticks(event_nums)
    ax.tick_params(labelsize=TICK_FS)
    ax.legend(framealpha=0.9, fontsize=LEGEND_FS)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    # ── Table ──
    attach_two_level_table(ax_tbl, all_cols, cell_data, row_labels)

    out = DATA_DIR / filename
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Saved  {out.name}")

# ── Plot 4: hitIndices distribution per (event, label) ───────────────────────
# Values > 4e9 are placeholder sentinels and go into a separate overflow panel.

OVERFLOW_THRESHOLD = 4_000_000_000   # 4 × 10^9


def plot_hitindices(data):
    for ev_idx in range(N_EVENTS):
        for label in LABELS:
            available_runs = sorted(data[label].keys())
            if not available_runs:
                continue

            # Two panels: main histogram (normal values) + overflow bar chart
            fig, (ax_main, ax_ovf) = plt.subplots(
                1, 2, figsize=(13, 4),
                gridspec_kw={"width_ratios": [5, 1], "wspace": 0.35},
                layout="constrained",
            )

            ovf_counts = []
            for run in available_runs:
                events = data[label][run]
                if ev_idx >= len(events):
                    ovf_counts.append(0)
                    continue
                hits   = events[ev_idx]["hitIndices"]
                normal = [h for h in hits if h <= OVERFLOW_THRESHOLD]
                n_ovf  = len(hits) - len(normal)
                ovf_counts.append(n_ovf)

                if normal:
                    ax_main.hist(normal, bins=100,
                                 histtype="step", linewidth=1.2, label=f"run{run}")

            # Overflow bar: one bar per run
            ax_ovf.bar(range(len(available_runs)), ovf_counts,
                       color="gray", alpha=0.7)
            ax_ovf.set_xticks(range(len(available_runs)))
            ax_ovf.set_xticklabels([f"run{r}" for r in available_runs],
                                   rotation=45, ha="right", fontsize=8)
            ax_ovf.set_ylabel("Count", fontsize=LABEL_FS)
            ax_ovf.set_title("Overflow\n(> 4×10⁹)", fontsize=TITLE_FS - 2)
            ax_ovf.tick_params(labelsize=TICK_FS)

            ax_main.set_xlabel("hitIndex value", fontsize=LABEL_FS)
            ax_main.set_ylabel("Count", fontsize=LABEL_FS)
            ax_main.set_title("Normal hits  (≤ 4×10⁹)", fontsize=TITLE_FS - 2)
            ax_main.legend(framealpha=0.9, fontsize=LEGEND_FS)
            ax_main.tick_params(labelsize=TICK_FS)

            fig.suptitle(f"hitIndices Distribution  —  {label},  Event {ev_idx + 1}",
                         fontsize=TITLE_FS)
            fname = f"plot4_hitIndices_event{ev_idx + 1:02d}_{label}.png"
            out = DATA_DIR / fname
            fig.savefig(out, dpi=120)
            plt.close(fig)
            print(f"Saved  {fname}")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    data = load_data()

    plot_ntrack(data)

    plot_overlap(data,
                 field    = "pixelSeedIndex",
                 filename = "plot2_pixelSeedIndex_overlap.png",
                 title    = "pixelSeedIndex  Jaccard Overlap  (each run vs run1, same label)")

    plot_overlap(data,
                 field    = "trackCandidateType",
                 filename = "plot3_trackCandidateType_overlap.png",
                 title    = "trackCandidateType  Jaccard Overlap  (each run vs run1, same label)")

    plot_hitindices(data)
    print("Done.")


if __name__ == "__main__":
    main()
