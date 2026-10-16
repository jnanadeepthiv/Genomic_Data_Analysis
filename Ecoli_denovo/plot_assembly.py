#!/usr/bin/env python3
"""Plot Velvet vs Oases assembly metrics across k-mer sizes.
Usage: python3 plot_assembly.py   (reads velvet_summary.txt and oases_summary.txt
       produced by stats.sh, writes fig1-fig4 PNG files)"""
import re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GENOME = 4_641_652          # E. coli K-12 MG1655 reference genome size (bp)
VEL, OAS = "#2a6fb0", "#d9822b"

def read(path):
    rows = {}
    for line in open(path):
        k = int(re.search(r"k=(\d+)", line).group(1))
        vals = dict(re.findall(r"(\w+)=(\d+)", line.split("\t", 1)[1]))
        rows[k] = {key: int(v) for key, v in vals.items()}
    return rows

vel, oas = read("velvet_summary.txt"), read("oases_summary.txt")

def plot(metric, ylabel, title, fname, scale=1, logy=False, genome_line=False,
         best=None):
    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=200)
    for d, name, c in [(vel, "Velvet", VEL), (oas, "Oases", OAS)]:
        ks = [k for k in sorted(d) if not (logy and d[k][metric] <= 0)]
        ax.plot(ks, [d[k][metric] / scale for k in ks], "-o", color=c,
                lw=2, ms=5, label=name)
    if genome_line:
        ax.axhline(GENOME / scale, ls="--", color="grey", lw=1.2,
                   label="E. coli genome size (4.64 Mb)")
    if best:
        for k, d, c in best:
            ax.annotate(f"k={k}", (k, d[k][metric] / scale),
                        textcoords="offset points", xytext=(0, 9),
                        ha="center", fontsize=9, color=c, fontweight="bold")
    ax.margins(y=0.1)
    if logy:
        ax.set_yscale("log")
    ax.set_xticks(sorted(set(vel) | set(oas)))
    ax.set_xlabel("k-mer size")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(fname)
    plt.close(fig)

plot("N50", "N50 (kb)", "N50 vs k-mer size", "fig1_N50.png", scale=1000,
     best=[(81, vel, VEL), (71, oas, OAS)])
plot("contigs", "Number of contigs (log scale)", "Number of contigs vs k-mer size",
     "fig2_contigs.png", logy=True)
plot("longest", "Longest contig (kb)", "Longest contig vs k-mer size",
     "fig3_longest.png", scale=1000)
plot("total", "Total assembly length (Mb)", "Total assembly length vs k-mer size",
     "fig4_total_length.png", scale=1e6, genome_line=True)
print("Saved fig1_N50.png, fig2_contigs.png, fig3_longest.png, fig4_total_length.png")
