#!/usr/bin/env python3
"""Tables and plots of individual contig lengths for the optimal assemblies.

Input (made by contig_lengths.sh):
  velvet_k81_contig_lengths.tsv, oases_k71_contig_lengths.tsv
Output:
  contig_summary_table.csv          summary statistics for both assemblies
  velvet_k81_contig_table.csv       rank, contig name, length (all contigs)
  oases_k71_contig_table.csv
  fig5_contig_lengths_ranked.png    every contig's length, longest to shortest
  fig6_cumulative_length.png        cumulative assembly length vs contig rank
  fig7_length_histogram.png         distribution of contig lengths
"""
import csv
import statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GENOME = 4_641_652                       # E. coli K-12 MG1655 genome size (bp)
ASM = [("Velvet (k=81)", "velvet_k81", "#2a6fb0"),
       ("Oases (k=71)",  "oases_k71",  "#d9822b")]


def read_lengths(prefix):
    rows = []
    with open(f"{prefix}_contig_lengths.tsv") as fh:
        for line in fh:
            name, length = line.rstrip("\n").rsplit("\t", 1)
            rows.append((name, int(length)))
    rows.sort(key=lambda r: -r[1])
    return rows


def n50(lengths):
    half, running = sum(lengths) / 2, 0
    for L in sorted(lengths, reverse=True):
        running += L
        if running >= half:
            return L
    return 0


data = {label: read_lengths(prefix) for label, prefix, _ in ASM}

# ---------- Table 1: summary statistics ----------
cols = ["Assembly", "Contigs", "Total length (bp)", "x genome size",
        "Longest (bp)", "Shortest (bp)", "Mean (bp)", "Median (bp)", "N50 (bp)",
        ">=1 kb", ">=10 kb", ">=100 kb"]
summary = []
for label, _, _ in ASM:
    L = [r[1] for r in data[label]]
    summary.append([label, len(L), sum(L), f"{sum(L)/GENOME:.2f}", max(L), min(L),
                    round(statistics.mean(L)), round(statistics.median(L)), n50(L),
                    sum(x >= 1_000 for x in L), sum(x >= 10_000 for x in L),
                    sum(x >= 100_000 for x in L)])
with open("contig_summary_table.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(cols)
    w.writerows(summary)

print("\n== Contig summary ==")
for c, *vals in zip(cols, *summary):
    print(f"{c:<20}" + "".join(f"{str(v):>18}" for v in vals))

# ---------- Tables 2-3: every contig (for the appendix) ----------
for label, prefix, _ in ASM:
    with open(f"{prefix}_contig_table.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Rank", "Contig", "Length (bp)"])
        for i, (name, length) in enumerate(data[label], 1):
            w.writerow([i, name, length])


def style(ax, title, xlabel, ylabel):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)


# ---------- Fig 5: every contig's length, ranked ----------
fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=200)
for label, _, c in ASM:
    L = [r[1] for r in data[label]]
    ax.plot(range(1, len(L) + 1), L, "-o", color=c, ms=2.5, lw=1.5,
            label=f"{label}: {len(L)} contigs")
ax.set_yscale("log")
style(ax, "Length of each contig in the optimal assemblies",
      "Contig rank (longest = 1)", "Contig length (bp, log scale)")
fig.tight_layout(); fig.savefig("fig5_contig_lengths_ranked.png"); plt.close(fig)

# ---------- Fig 6: cumulative length ----------
fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=200)
for label, _, c in ASM:
    L = [r[1] for r in data[label]]
    cum, s = [], 0
    for x in L:
        s += x
        cum.append(s / 1e6)
    ax.plot(range(1, len(L) + 1), cum, color=c, lw=2, label=label)
ax.axhline(GENOME / 1e6, ls="--", color="grey", lw=1.2,
           label="E. coli genome size (4.64 Mb)")
style(ax, "Cumulative assembly length (contigs added longest first)",
      "Number of contigs", "Cumulative length (Mb)")
fig.tight_layout(); fig.savefig("fig6_cumulative_length.png"); plt.close(fig)

# ---------- Fig 7: histogram of contig lengths ----------
edges = [200, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 2_000_000]
names = ["200-500", "0.5-1k", "1-5k", "5-10k", "10-50k", "50-100k",
         "100-500k", ">500k"]
fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=200)
width = 0.4
for i, (label, _, c) in enumerate(ASM):
    L = [r[1] for r in data[label]]
    counts = [sum(lo <= x < hi for x in L) for lo, hi in zip(edges, edges[1:])]
    pos = [j + (i - 0.5) * width for j in range(len(counts))]
    bars = ax.bar(pos, counts, width, color=c, label=label)
    ax.bar_label(bars, fontsize=7, padding=1)
ax.set_xticks(range(len(names)), names)
style(ax, "Distribution of contig lengths", "Contig length (bp)",
      "Number of contigs")
fig.tight_layout(); fig.savefig("fig7_length_histogram.png"); plt.close(fig)

print("\nSaved: contig_summary_table.csv, velvet_k81_contig_table.csv, "
      "oases_k71_contig_table.csv,\n       fig5_contig_lengths_ranked.png, "
      "fig6_cumulative_length.png, fig7_length_histogram.png")
