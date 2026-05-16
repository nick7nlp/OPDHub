import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib
matplotlib.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
matplotlib.rcParams['font.size'] = 10

# Fine-grained data — updated for 146 papers (V3, May 2026)
size_buckets = ['120M', '0.5B', '0.6-1.1B', '1.5-2B', '3-4B', '7-8B', '9-14B', '27-32B', '70B+']
families = ['Qwen3', 'Qwen2.5', 'Llama-3.x', 'Gemma-2', 'GPT-2', 'DeepSeek', 'T5/OPT', 'Other']

# Student data (fine-grained) — 146 papers
student_data = np.array([
    [0, 3, 0, 21, 22, 27, 5, 2, 0],   # Qwen3
    [0, 3, 0, 6, 4, 6, 1, 0, 0],      # Qwen2.5
    [0, 0, 2, 0, 1, 9, 1, 0, 0],      # Llama-3.x
    [0, 0, 0, 4, 3, 0, 1, 0, 0],      # Gemma-2
    [2, 1, 0, 0, 0, 0, 0, 0, 0],      # GPT-2
    [1, 0, 0, 5, 0, 2, 0, 0, 0],      # DeepSeek
    [1, 5, 2, 2, 0, 0, 0, 0, 0],      # T5/OPT
    [1, 0, 1, 0, 1, 6, 0, 1, 0],      # Other
])

# Teacher data (fine-grained) — Self/Multi-teacher excluded (71 papers)
teacher_data = np.array([
    [0, 0, 0, 0, 3, 15, 1, 16, 5],    # Qwen3
    [0, 0, 0, 1, 0, 6, 1, 0, 3],      # Qwen2.5
    [0, 0, 0, 0, 0, 4, 1, 0, 4],      # Llama-3.x
    [0, 0, 0, 0, 0, 1, 0, 3, 0],      # Gemma-2
    [0, 0, 1, 2, 0, 0, 0, 0, 5],      # GPT-2
    [2, 0, 0, 0, 0, 4, 0, 0, 0],      # DeepSeek
    [0, 0, 0, 0, 2, 1, 1, 0, 0],      # T5/OPT
    [0, 0, 0, 0, 2, 5, 0, 0, 0],      # Other
])

# Colormaps
colors_s = ['#f5f5f5', '#bbdefb', '#42a5f5', '#1565c0', '#0d47a1']
cmap_s = LinearSegmentedColormap.from_list('student', colors_s, N=256)
colors_t = ['#f5f5f5', '#ffcdd2', '#e53935', '#b71c1c', '#4a0000']
cmap_t = LinearSegmentedColormap.from_list('teacher', colors_t, N=256)

# Top model annotations (updated for 146 papers)
student_annotations = {
    (0, 3): 'Qwen3-1.7B',            # Qwen3, 1.5-2B (21)
    (0, 4): 'Qwen3-4B',              # Qwen3, 3-4B (22)
    (0, 5): 'Qwen3-8B',              # Qwen3, 7-8B (27) — hottest!
    (0, 6): 'Qwen3-14B',             # Qwen3, 9-14B (5)
    (1, 3): 'Qw2.5-1.5B',            # Qwen2.5, 1.5-2B (6)
    (1, 5): 'Qw2.5-7B',              # Qwen2.5, 7-8B (6)
    (2, 5): 'Llama-3.1-8B',          # Llama, 7-8B (9)
    (3, 3): 'Gemma-2-2B',            # Gemma, 1.5-2B (4)
    (3, 4): 'Gemma-3/4B',            # Gemma, 3-4B (3)
    (5, 3): 'DS-R1-1.5B',            # DeepSeek, 1.5-2B (5)
}

teacher_annotations = {
    (0, 5): 'Qwen3-8B',              # Qwen3, 7-8B (15) — king teacher
    (0, 7): 'Qwen3-32B',             # Qwen3, 27-32B (16) — biggest Qwen3 teacher
    (0, 8): 'Qwen3-235B',            # Qwen3, 70B+ (5)
    (1, 5): 'Qw2.5-Math-7B',         # Qwen2.5, 7-8B (6)
    (1, 8): 'Qw2.5-72B',             # Qwen2.5, 70B+ (3)
    (2, 5): 'Llama-3.1-8B',          # Llama, 7-8B (4)
    (2, 8): 'Llama-70B',             # Llama, 70B+ (4)
    (4, 8): 'GPT-4/5 API',           # GPT, 70B+ (5)
    (5, 5): 'DS-R1-7B',              # DeepSeek, 7-8B (4)
}

def draw_panel(ax, data, families, title, cmap, max_val, annotations=None):
    im = ax.imshow(data, cmap=cmap, aspect='auto', vmin=0, vmax=max_val)
    
    ax.set_xticks(range(len(size_buckets)))
    ax.set_xticklabels(size_buckets, fontsize=9, fontweight='bold', rotation=30, ha='right')
    ax.set_yticks(range(len(families)))
    ax.set_yticklabels(families, fontsize=11, fontweight='bold')
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    
    # Text in cells
    for i in range(len(families)):
        for j in range(len(size_buckets)):
            val = data[i, j]
            if val > 0:
                color = 'white' if val > max_val * 0.5 else '#333333'
                fontsize = 12 if val >= 10 else 10
                
                # Check for annotation
                if annotations and (i, j) in annotations:
                    ax.text(j, i, str(val), ha='center', va='center',
                           fontsize=fontsize, fontweight='bold', color=color)
                    # Small annotation below
                    ax.text(j, i + 0.32, annotations[(i,j)], ha='center', va='center',
                           fontsize=6.5, color=color, alpha=0.85)
                else:
                    ax.text(j, i, str(val), ha='center', va='center',
                           fontsize=fontsize, fontweight='bold', color=color)
    
    # Grid
    ax.set_xticks(np.arange(-0.5, len(size_buckets), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(families), 1), minor=True)
    ax.grid(which='minor', color='#bdbdbd', linewidth=0.8)
    ax.tick_params(which='minor', size=0)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=25)
    
    return im

# Create figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 5.8),
                                gridspec_kw={'width_ratios': [1, 1]})

max_val = max(student_data.max(), teacher_data.max())

im1 = draw_panel(ax1, student_data, families, 
                 "As Student (distilled into)", cmap_s, max_val, student_annotations)
im2 = draw_panel(ax2, teacher_data, families,
                 "As Teacher (distilled from)", cmap_t, max_val, teacher_annotations)

# Colorbars
cbar1 = fig.colorbar(im1, ax=ax1, shrink=0.75, pad=0.02, aspect=25)
cbar1.set_label('Papers', fontsize=9)
cbar2 = fig.colorbar(im2, ax=ax2, shrink=0.75, pad=0.02, aspect=25)
cbar2.set_label('Papers', fontsize=9)

# Main title
fig.suptitle("On-Policy Distillation — Model Usage Atlas  (146 papers, 9 size tiers, 8 families)", 
             fontsize=13, fontweight='bold', y=1.0)

# Footnotes
fig.text(0.5, -0.04, 
         "Self-distillation (71 papers) excluded from teacher counts.  |  "
         "Cell annotations show the dominant model in that cell.  |  "
         "Data: Awesome-LLM-On-Policy-Distillation, May 2026.",
         ha='center', fontsize=8.5, color='#616161', style='italic')

plt.tight_layout(rect=[0, 0.02, 1, 0.96])

outpath = "/tmp/awesome-opd/assets/model-atlas-heatmap.png"
plt.savefig(outpath, dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {outpath}")

# PDF version
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 5.8),
                                gridspec_kw={'width_ratios': [1, 1]})
im1 = draw_panel(ax1, student_data, families,
                 "As Student (distilled into)", cmap_s, max_val, student_annotations)
im2 = draw_panel(ax2, teacher_data, families,
                 "As Teacher (distilled from)", cmap_t, max_val, teacher_annotations)
cbar1 = fig.colorbar(im1, ax=ax1, shrink=0.75, pad=0.02, aspect=25)
cbar1.set_label('Papers', fontsize=9)
cbar2 = fig.colorbar(im2, ax=ax2, shrink=0.75, pad=0.02, aspect=25)
cbar2.set_label('Papers', fontsize=9)
fig.suptitle("On-Policy Distillation — Model Usage Atlas  (146 papers, 9 size tiers, 8 families)",
             fontsize=13, fontweight='bold', y=1.0)
fig.text(0.5, -0.04,
         "Self-distillation (71 papers) excluded from teacher counts.  |  "
         "Cell annotations show the dominant model in that cell.  |  "
         "Data: Awesome-LLM-On-Policy-Distillation, May 2026.",
         ha='center', fontsize=8.5, color='#616161', style='italic')
plt.tight_layout(rect=[0, 0.02, 1, 0.96])
outpdf = outpath.replace('.png', '.pdf')
plt.savefig(outpdf, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved: {outpdf}")
