# Extracted Benchmark Data from Papers

## DeepSeek-R1 Distillation Results (Table 15 from paper)
| Model | AIME 2024 pass@1 | AIME cons@64 | MATH-500 pass@1 | GPQA Diamond pass@1 | LiveCodeBench pass@1 | Codeforces rating |
|---|---|---|---|---|---|---|
| GPT-4o-0513 | 9.3 | 13.4 | 74.6 | 49.9 | 32.9 | 759 |
| Claude-3.5-Sonnet-1022 | 16.0 | 26.7 | 78.3 | 65.0 | 38.9 | 717 |
| R1-Distill-Qwen-1.5B | 28.9 | 52.7 | 83.9 | 33.8 | 16.9 | 954 |
| R1-Distill-Qwen-7B | 55.5 | 83.3 | 92.8 | 49.1 | 37.6 | 1189 |
| R1-Distill-Qwen-14B | 69.7 | 80.0 | 93.9 | 59.1 | 53.1 | 1481 |
| R1-Distill-Qwen-32B | 72.6 | 83.3 | 94.3 | 62.1 | 57.2 | 1691 |
| R1-Distill-Llama-8B | 50.4 | 80.0 | 89.1 | 49.0 | 39.6 | 1205 |
| R1-Distill-Llama-70B | 70.0 | 86.7 | 94.5 | 65.2 | 57.5 | 1633 |

## Distillation vs RL (Table 16)
| Model | AIME pass@1 | AIME cons@64 | MATH-500 | GPQA Diamond | LiveCodeBench |
|---|---|---|---|---|---|
| QwQ-32B-Preview | 50.0 | 60.0 | 90.6 | 54.5 | 41.9 |
| Qwen2.5-32B-Zero (RL only) | 47.0 | 60.0 | 91.6 | 55.0 | 40.2 |
| R1-Distill-Qwen-32B | 72.6 | 83.3 | 94.3 | 62.1 | 57.2 |

Key insight: Distillation from R1 CRUSHES pure RL on smaller models.
32B distilled model beats 32B RL-trained model by 25.6 points on AIME.

## RLKD Results (2505.16142)
On AIME24, DeepSeek-R1-Distill-Qwen-7B-RLKD achieves 53.3% pass@1 (vs 50.0% baseline)
Using only 3.2K RL steps on top of 800K SFT data.
Qwen2.5-Math-7B-RLKD-Zero: 23.3% with 0 SFT + 3.2K RL steps (vs 16.7% for full Instruct pipeline)

## GKD (2306.13649) Results
- T5 models on XSum summarization
- On-policy GKD outperforms ImitKD, f-distill, Supervised KD
- On-policy GKD + RL achieves highest ROUGE-2
- JSD (0.9) is the optimal divergence for GKD

## MiniLLM (2306.08543) Results
- Teacher→Student: GPT-2-1.5B→GPT-2 (125M/340M/760M), GPT-J 6B→(760M/1.5B/2.7B), OPT 13B→(1.3B/2.7B/6.7B)
- MiniLLM consistently outperforms SeqKD across all teacher-student pairs
- Average GPT-4 score: MiniLLM > SeqKD by 3-5 points on average

## DistiLLM (2402.03898) Results
- GPT-2 XL→GPT-2, OPT-2.7B→OPT-1.3B, OLLaMA2-7B→OLLaMA2-3B
- DistiLLM outperforms GKD and MiniLLM on instruction following
- GKD and MiniLLM's SGO can hurt smaller students
- 1.5-3x training speedup via adaptive off-policy approach

## DeepSeek-R1 Distillation Details
- 800K samples from DeepSeek-R1 (long CoT reasoning traces)
- Base models: Qwen2.5-Math-1.5B/7B, Qwen2.5-14B/32B, Llama-3.1-8B, Llama-3.3-70B
- Training: 2-3 epochs, cosine LR (5e-5 to 1e-4), batch size 64, max 32K tokens
- Key insight: 1.5B distilled model BEATS GPT-4o and Claude-3.5-Sonnet on math!
- Key insight: Distillation >> RL for small models (but RL needed to push frontier)
