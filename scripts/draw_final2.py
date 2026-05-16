import re
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import matplotlib
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import font_manager

font_manager.fontManager.addfont('/usr/share/fonts/tex-gyre/texgyrepagella-regular.otf')
font_manager.fontManager.addfont('/usr/share/fonts/tex-gyre/texgyrepagella-bold.otf')

matplotlib.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['TeX Gyre Pagella', 'Palatino', 'serif'],
    'font.size': 38,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'axes.linewidth': 1.2,
})

readme_path = '/tmp/awesome-opd/README.md'
with open(readme_path) as f:
    readme = f.read()

paper_configs = []
for m in re.finditer(r'🟢 \[([^\]]+)\]\((https://arxiv\.org/abs/[\d.]+)\).*?📐\s*([^<]+)</sub>', readme):
    paper_configs.append((m.group(1), m.group(2), m.group(3).strip()))

def extract_size_val(s):
    m = re.search(r'(\d+\.?\d*)\s*([BM])', s)
    if m:
        v = float(m.group(1))
        return v/1000 if m.group(2)=='M' else v
    return None

CANONICAL = {
    'GPT-2 120M\u2013760M':'GPT-2 (sm)','GPT-2 120M':'GPT-2 (sm)','GPT-2 0.1B\u20130.3B':'GPT-2 (sm)',
    'GPT-2':'GPT-2 (sm)','GPT-2 (student)':'GPT-2 (sm)',
    'GPT-2 XL':'GPT-2 1.5B','GPT-2 1.5B':'GPT-2 1.5B',
    'TinyLLaMA-1.1B':'TinyLLaMA 1.1B','TinyLLaMA':'TinyLLaMA 1.1B',
    'OPT-125M':'OPT 125M','OPT-6.7B':'OPT 6.7B','OPT-13B':'OPT 13B',
    'LLaMA-68M':'LLaMA 68M','LLaMA-7B':'LLaMA 7B','LLaMA2-7B':'LLaMA 7B','LLaMA-6.7B':'LLaMA 7B',
    'Llama-13B':'Llama 13B','Llama-70B':'Llama 70B',
    'Pythia-410M':'Pythia 410M','Pythia-2.8B':'Pythia 2.8B',
    'Qwen3-0.6B':'Qwen3 0.6B','Qwen3-1.7B':'Qwen3 1.7B','Qwen3-4B':'Qwen3 4B',
    'Qwen3-4B-Instruct':'Qwen3 4B','Qwen3-4B-Non-Thinking':'Qwen3 4B',
    'Qwen3-8B':'Qwen3 8B','Qwen3-14B':'Qwen3 14B',
    'Qwen3-30B-A3B':'Qwen3 30B','Qwen3-32B':'Qwen3 32B',
    'Qwen3-Next-80B-A3B-Thinking':'Qwen3 80B',
    'Qwen3-VL-2B':'Qwen3-VL 2B','Qwen3-VL-8B':'Qwen3-VL 8B','Qwen3-VL-32B':'Qwen3-VL 32B',
    'Qwen2-0.5B-Instruct':'Qwen2 0.5B','Qwen2-1.5B':'Qwen2 1.5B',
    'Qwen2.5-1.5B-Instruct':'Qwen2.5 1.5B','Qwen2.5-1.5B':'Qwen2.5 1.5B',
    'Qwen2.5-Math-1.5B-Instruct':'Qwen2.5M 1.5B','Qwen2.5-Math-1.5B':'Qwen2.5M 1.5B',
    'Qwen2.5-3B-Instruct':'Qwen2.5 3B','Qwen2.5-3B':'Qwen2.5 3B',
    'Qwen2-7B':'Qwen2 7B','Qwen2-7B-Instruct':'Qwen2 7B',
    'Qwen2.5-7B':'Qwen2.5 7B','Qwen2.5-7B-Instruct':'Qwen2.5 7B',
    'Qwen2.5-Math-7B':'Qwen2.5M 7B','Qwen2.5-14B':'Qwen2.5 14B',
    'DeepSeek-R1-Distill-Qwen-1.5B':'R1-Distill 1.5B','R1-Distill-Qwen-1.5B':'R1-Distill 1.5B',
    'DeepSeek-R1-Distill-7B':'R1-Distill 7B','R1-Distill-Qwen-7B':'R1-Distill 7B',
    'Gemma-2-2B':'Gemma2 2B','Gemma-2-2B-IT':'Gemma2 2B',
    'Gemma-2-9B':'Gemma2 9B','Gemma-2-27B':'Gemma2 27B',
    'Gemma-2B':'Gemma 2B','Gemma-7B':'Gemma 7B','Gemma3-4B':'Gemma3 4B',
    'Llama-3.1-8B':'Llama3.1 8B','Llama-3.1-8B-Instruct':'Llama3.1 8B',
    'Llama-3-8B':'Llama3.1 8B','Llama-3.2-1B':'Llama3.2 1B','Llama-3.2-3B':'Llama3.2 3B',
    'Llama-3.3-70B':'Llama3.3 70B','LLaMA-3.2-3B':'Llama3.2 3B',
    'QwQ-32B':'QwQ 32B','Phi-4-mini':'Phi-4 mini',
    'SkyWork-OR1-7B':'SkyWork-OR1 7B','SkyWork-OR1-Math-7B':'SkyWork-OR1 7B',
    'Mistral-7B':'Mistral 7B','Danube2-1.8B':'Danube2 1.8B',
    'InternLM-2.5-7B-Chat':'InternLM 7B','GPT-5-Chat':'GPT-5','GPT-5.2':'GPT-5',
    'ChatGPT':'ChatGPT','DeepSeek-R1 671B':'DeepSeek-R1 671B',
    'OpenLLaMA-7B':'OpenLLaMA 7B','OpenLLaMA2-7B':'OpenLLaMA 7B','OpenLLaMA2-3B':'OpenLLaMA 3B',
    'OpenThinker3-7B':'OpenThinker 7B','T5-XL 3B':'T5-XL 3B','T5-Large 780M':'T5-Large',
    'FLAN-T5-XL 3B':'T5-XL 3B','PaLM-540B':'PaLM 540B','GPT-J 6B':'GPT-J 6B',
    'gpt-oss-120b':'gpt-oss 120B','Qwen-7B':'Qwen 7B','Llama-3.1-3B':'Llama3.1 3B',
}

def canonicalize(raw):
    raw = raw.strip()
    raw = re.sub(r'\s*\([^)]*\)\s*$', '', raw)
    raw = re.sub(r'\s*[;·].*$', '', raw)
    if raw in CANONICAL: return CANONICAL[raw]
    base = re.sub(r'-Inst(ruct)?$', '', raw)
    if base in CANONICAL: return CANONICAL[base]
    if extract_size_val(raw) and len(raw) < 25: return raw
    return None

pair_count = defaultdict(int)
for title, url, config in paper_configs:
    if '→' not in config: continue
    parts = config.split('→')
    if len(parts) != 2: continue
    student_raw = parts[0].strip()
    teacher_raw = re.sub(r'\s*[;·].*$', '', parts[1].strip())
    students = [s.strip() for s in re.split(r'\s*/\s*', student_raw)]
    teachers = [t.strip() for t in re.split(r'\s*/\s*', teacher_raw)]
    for s in students:
        s_can = canonicalize(s)
        if not s_can: continue
        for t in teachers:
            if 'Self' in t or 'self' in t:
                pair_count[(s_can, s_can)] += 1
            else:
                t_can = canonicalize(t)
                if not t_can: continue
                pair_count[(t_can, s_can)] += 1

all_models = set()
for (t, s) in pair_count: all_models.add(t); all_models.add(s)
model_freq = defaultdict(int)
for (t, s), cnt in pair_count.items():
    model_freq[t] += cnt
    if t != s: model_freq[s] += cnt

filtered = [m for m in all_models if model_freq[m] >= 3]
filtered = [m for m in filtered if not re.match(r'^\d+B(-Base)?$', m)]

FAMILY_COLORS = {
    'GPT': '#d32f2f', 'T5': '#c2185b', 'OPT': '#7b1fa2', 'Pythia': '#512da8',
    'LLaMA': '#1565c0', 'Llama-3': '#0277bd', 'Mistral': '#00838f',
    'Gemma': '#00695c', 'Qwen': '#2e7d32', 'DeepSeek': '#e65100', 'Other': '#616161',
}

def get_family(model):
    families = [
        ('GPT-2','GPT'),('GPT-J','GPT'),('GPT-5','GPT'),('ChatGPT','GPT'),('gpt-oss','GPT'),
        ('T5','T5'),('OPT','OPT'),('Pythia','Pythia'),('PaLM','Other'),
        ('LLaMA','LLaMA'),('TinyLLaMA','LLaMA'),
        ('Llama','Llama-3'),('OpenLLaMA','Llama-3'),
        ('Danube','Other'),('Mistral','Mistral'),('Phi','Other'),
        ('Gemma','Gemma'),
        ('Qwen','Qwen'),('QwQ','Qwen'),
        ('DeepSeek','DeepSeek'),('R1-Distill','DeepSeek'),
        ('SkyWork','Other'),('OpenThinker','Other'),('InternLM','Other'),
    ]
    for prefix, fam in families:
        if model.startswith(prefix): return fam
    return 'Other'

def family_sort_key(model):
    order = {'GPT':0,'T5':1,'OPT':2,'Pythia':3,'LLaMA':4,'Llama-3':5,
             'Mistral':6,'Gemma':7,'Qwen':8,'DeepSeek':9,'Other':10}
    fam = get_family(model)
    return (order.get(fam, 50), extract_size_val(model) or 0, model)

filtered = sorted(filtered, key=family_sort_key)
n = len(filtered)

matrix = np.zeros((n, n))
for i, t in enumerate(filtered):
    for j, s in enumerate(filtered):
        matrix[i, j] = pair_count.get((t, s), 0)

sorted_by_freq = sorted(filtered, key=lambda m: -model_freq[m])
model_rank = {m: i+1 for i, m in enumerate(sorted_by_freq)}

# Discrete color scale
boundaries = [0.5, 1.5, 2.5, 4.5, 7.5, 12.5, 20]
colors_discrete = ['#e8f5e9', '#a5d6a7', '#4caf50', '#2e7d32', '#1b5e20', '#0a3a10']
cmap_discrete = ListedColormap(colors_discrete)
norm_d = BoundaryNorm(boundaries, cmap_discrete.N)

# Figure
cell_px = 1.55
fig_size = n * cell_px + 6
fig, ax = plt.subplots(figsize=(fig_size, fig_size))
fig.patch.set_facecolor('white')
ax.set_facecolor('#fafafa')

im = ax.imshow(np.where(matrix > 0, matrix, np.nan), cmap=cmap_discrete, norm=norm_d,
               aspect='equal', interpolation='nearest')

# Diagonal band — self-distillation with orange color scale
# Orange gradient matching the green boundaries: 1/2/3-4/5-7/8-12/13+
orange_colors = ['#fff3e0', '#ffcc80', '#ff9800', '#e65100', '#bf360c', '#6d1b00']
for i in range(n):
    ax.add_patch(plt.Rectangle((i-0.5, i-0.5), 1, 1,
                 facecolor='#fff8e1', edgecolor='none', zorder=0))
    val = int(matrix[i, i])
    if val > 0:
        # Map value to orange tier
        if val >= 13: oidx = 5
        elif val >= 8: oidx = 4
        elif val >= 5: oidx = 3
        elif val >= 3: oidx = 2
        elif val >= 2: oidx = 1
        else: oidx = 0
        ax.add_patch(plt.Rectangle((i-0.5, i-0.5), 1, 1,
                     facecolor=orange_colors[oidx], edgecolor='#e65100', linewidth=3, zorder=1))

# Cell numbers — white on dark cells, black on light cells
for i in range(n):
    for j in range(n):
        val = int(matrix[i, j])
        if val > 0:
            # Use white text on darker cells (val >= 5)
            txt_color = '#ffffff' if val >= 5 else '#1a1a1a'
            ax.text(j, i, str(val), ha='center', va='center',
                   fontsize=50 if val >= 5 else 44, fontweight='bold',
                   color=txt_color, zorder=10)

# Labels colored by family
ax.set_xticks(range(n))
ax.set_xticklabels(filtered, rotation=55, ha='left', fontsize=46, fontweight='bold')
ax.set_yticks(range(n))
ax.set_yticklabels(filtered, fontsize=46, fontweight='bold')
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')

for i, label in enumerate(ax.get_yticklabels()):
    label.set_color(FAMILY_COLORS.get(get_family(filtered[i]), '#616161'))
for j, label in enumerate(ax.get_xticklabels()):
    label.set_color(FAMILY_COLORS.get(get_family(filtered[j]), '#616161'))

# Family separators
prev_fam = None
for i, m in enumerate(filtered):
    fam = get_family(m)
    if prev_fam is not None and fam != prev_fam:
        ax.axhline(y=i - 0.5, color='#455a64', linewidth=2.8, alpha=0.9, zorder=3)
        ax.axvline(x=i - 0.5, color='#455a64', linewidth=2.8, alpha=0.9, zorder=3)
    prev_fam = fam

# Grid
ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
ax.grid(which='minor', color='#e0e0e0', linewidth=0.5, zorder=2)
ax.tick_params(which='minor', size=0)

# Marginal sums
for i in range(n):
    row_sum = int(matrix[i].sum())
    if row_sum > 0:
        ax.text(n + 0.3, i, str(row_sum), ha='left', va='center',
               fontsize=34, color='#455a64', fontweight='bold')
    col_sum = int(matrix[:, i].sum())
    if col_sum > 0:
        ax.text(i, n + 0.3, str(col_sum), ha='center', va='top',
               fontsize=34, color='#455a64', fontweight='bold')

# Title
ax.set_title("On-Policy Distillation — Teacher × Student Model Pair Heatmap\n"
             "119 papers  ·  cell = co-occurrence count  ·  diagonal = self-distillation",
             fontsize=44, fontweight='bold', color='#212121', pad=30, linespacing=1.6)
ax.set_xlabel('← Student Model', fontsize=48, fontweight='bold', color='#333', labelpad=22)
ax.set_ylabel('Teacher Model →', fontsize=48, fontweight='bold', color='#333', labelpad=22)

# --- SPREAD-OUT LEGEND: one wide row across full width ---
legend_elements = [
    mpatches.Patch(facecolor=colors_discrete[0], edgecolor='#999', label='1 paper'),
    mpatches.Patch(facecolor=colors_discrete[1], edgecolor='#999', label='2 papers'),
    mpatches.Patch(facecolor=colors_discrete[2], edgecolor='#999', label='3–4'),
    mpatches.Patch(facecolor=colors_discrete[3], edgecolor='#999', label='5–7'),
    mpatches.Patch(facecolor=colors_discrete[4], edgecolor='#999', label='8–12'),
    mpatches.Patch(facecolor=colors_discrete[5], edgecolor='#999', label='13+'),
    mpatches.Patch(facecolor='#ffe0b2', edgecolor='#e65100', linewidth=2, label='Self-Distill'),
]

families_seen = []
for m in filtered:
    fam = get_family(m)
    if fam not in [f for f,_ in families_seen]:
        families_seen.append((fam, FAMILY_COLORS.get(fam,'#616161')))
fam_patches = [mpatches.Patch(facecolor=c, edgecolor='#444', label=name) for name,c in families_seen]

# Combine all into one big legend, spread across full width
all_handles = legend_elements + [mpatches.Patch(facecolor='none', edgecolor='none', label='     ')] + fam_patches

plt.tight_layout(rect=[0, 0.045, 1, 0.97])

fig.legend(handles=all_handles, loc='lower center',
          bbox_to_anchor=(0.5, -0.005), 
          ncol=len(all_handles),  # ALL in one row
          fontsize=30, framealpha=0.95, edgecolor='#bdbdbd',
          columnspacing=2.5, handlelength=2.8, borderpad=1.2,
          handletextpad=0.8)

outpath = "/tmp/awesome-opd/assets/model-atlas-heatmap.png"
plt.savefig(outpath, dpi=150, bbox_inches='tight', facecolor='white', pad_inches=0.5)
plt.savefig(outpath.replace('.png', '.pdf'), bbox_inches='tight', facecolor='white', pad_inches=0.5)
plt.close()

from PIL import Image; import os
img = Image.open(outpath)
print(f"✅ {img.size[0]}x{img.size[1]} px, {os.path.getsize(outpath)/1024:.0f} KB")
