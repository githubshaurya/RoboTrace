# RoboTrace: Low-Cost Robustness and Deployment-Stress Evaluation for VLA-Style Robot Learning

- Generated UTC: `2026-06-26T06:55:41.614182+00:00`
- Root: `/kaggle/working/RoboTrace`
- Dataset: `lerobot/pusht`
- Split: `train`

## Executive summary

RoboTrace is a Kaggle-friendly evaluation toolkit for low-cost Vision-Language-Action and robot-learning traces. It focuses on robustness and deployment-stress evidence rather than pretending a notebook is a robot lab.

The completed run evaluated `lerobot/pusht` through dataset probing, action trace metrics, visual perturbation severity, symbolic instruction sensitivity, async deployment-stress simulation, and lightweight action-only baselines.

The strongest result is from Stage 6: **action horizon mismatch** was the highest-risk deployment failure mode in this run. This gives the project a real systems story: control-loop and action-horizon mismatches can strongly distort recorded robot action traces even before a learned policy or hardware deployment is involved.

## Completed stages

| stage                          | status   |   warnings |   errors |
|:-------------------------------|:---------|-----------:|---------:|
| stage0_env_probe               | PASS     |          0 |        0 |
| stage1_core                    | present  |          0 |        0 |
| stage2_dataset_probe           | PASS     |          0 |        0 |
| stage3_trace_metrics           | PASS     |          0 |        0 |
| stage4_visual_robustness       | PASS     |          0 |        0 |
| stage5_instruction_sensitivity | PASS     |          1 |        0 |
| stage6_async_simulation        | PASS     |          0 |        0 |
| stage7_optional_policy_eval    | PASS     |          0 |        0 |

## Key metrics

| stage                          | metric                             | value                                        | interpretation                               |
|:-------------------------------|:-----------------------------------|:---------------------------------------------|:---------------------------------------------|
| stage0_env_probe               | overall_status                     | PASS                                         | Kaggle environment probe status              |
| stage0_env_probe               | python                             |                                              | Python runtime                               |
| stage0_env_probe               | cuda_available                     |                                              | CUDA availability                            |
| stage1_core                    | tests_ok                           | True                                         | Core unit tests                              |
| stage1_core                    | num_project_files                  | 46                                           | Created/indexed project files                |
| stage2_dataset_probe           | selected_dataset                   | lerobot/pusht                                | Dataset selected for staged probe            |
| stage2_dataset_probe           | dataset_status                     | loaded                                       | Dataset loading status                       |
| stage2_dataset_probe           | num_sample_rows_loaded             | 80                                           | Rows sampled for schema probe                |
| stage2_dataset_probe           | num_episode_groups                 | 1                                            | Episode groups observed                      |
| stage3_trace_metrics           | num_usable_episodes                | 4                                            | Episodes with usable action traces           |
| stage3_trace_metrics           | num_step_metric_rows               | 512                                          | Per-step metric rows                         |
| stage3_trace_metrics           | smoothness_mean_l2_step_delta_mean | 8.219304659792309                            | Dataset-level action trace metric            |
| stage3_trace_metrics           | trajectory_drift_l2_mean           | 181.0955104827881                            | Dataset-level action trace metric            |
| stage3_trace_metrics           | action_magnitude_l2_mean_mean      | 368.27360229314803                           | Dataset-level action trace metric            |
| stage3_trace_metrics           | num_steps_mean                     | 128.0                                        | Dataset-level action trace metric            |
| stage4_visual_robustness       | num_images                         | 12                                           | Real frames sampled for visual perturbations |
| stage4_visual_robustness       | image_source                       | hf_repo_video_file                           | Visual frame source                          |
| stage4_visual_robustness       | num_metric_rows                    | 144                                          | Visual perturbation metric rows              |
| stage4_visual_robustness       | policy_drift_measured              | False                                        | Policy drift intentionally not measured      |
| stage5_instruction_sensitivity | num_raw_instruction_records        | 512                                          | Instruction-like raw records                 |
| stage5_instruction_sensitivity | num_natural_language_unique        | 0                                            | Natural-language instruction count           |
| stage5_instruction_sensitivity | symbolic_fallback_used             | True                                         | Whether symbolic task fallback was used      |
| stage5_instruction_sensitivity | num_perturbation_rows              | 4                                            | Instruction perturbation rows                |
| stage6_async_simulation        | num_episodes                       | 4                                            | Episodes used in async simulator             |
| stage6_async_simulation        | num_scenarios                      | 26                                           | Async scenario count                         |
| stage6_async_simulation        | num_raw_rows                       | 104                                          | Raw async simulation rows                    |
| stage6_async_simulation        | top_mode_by_drift                  | action_horizon_mismatch                      | Worst async mode by normalized drift         |
| stage6_async_simulation        | top_mode_normalized_mean_l2_drift  | 0.3330325318685965                           | Normalized drift for worst mode              |
| stage6_async_simulation        | top_risk_scenario_mode             | action_horizon_mismatch                      | Highest-risk async scenario                  |
| stage6_async_simulation        | top_risk_scenario_params           | {"actual_horizon": 8, "expected_horizon": 4} | Highest-risk async scenario params           |
| stage6_async_simulation        | top_risk_scenario_mean_l2_drift    | 138.2900505065918                            | Highest-risk mean action drift               |
| stage7_optional_policy_eval    | num_baselines                      | 8                                            | Baseline count                               |
| stage7_optional_policy_eval    | num_eval_rows                      | 32                                           | Baseline evaluation rows                     |
| stage7_optional_policy_eval    | real_policy_loaded                 | False                                        | Real policy status                           |
| stage7_optional_policy_eval    | top_baseline_by_quality            | replay_oracle                                | Best baseline by quality proxy               |
| stage7_optional_policy_eval    | top_baseline_quality_score         | 1.0                                          | Best baseline quality proxy                  |
| stage7_optional_policy_eval    | worst_baseline_by_risk             | first_action_hold                            | Worst baseline by risk                       |
| stage7_optional_policy_eval    | worst_baseline_mean_l2_drift       | 183.9531135559082                            | Worst baseline drift                         |

## Dataset probe

- Selected dataset: `lerobot/pusht`
- Dataset status: `loaded`
- Dataset split: `train`
- Sample rows loaded: `80`
- Episode groups: `1`

The project did not require LeRobot installation for dataset probing, which is important for Kaggle stability.

## Stage 3: Action trace metrics

|   episode_id |   num_steps |   action_dim |   smoothness_mean_l2_step_delta |   trajectory_drift_l2 |   trajectory_path_l2 |   action_magnitude_l2_mean |   timestamp_gap_mean |
|-------------:|------------:|-------------:|--------------------------------:|----------------------:|---------------------:|---------------------------:|---------------------:|
|            0 |         161 |            2 |                         8.13005 |               292.262 |             1300.81  |                    369.591 |                  0.1 |
|            1 |         118 |            2 |                         9.53785 |               141.481 |             1115.93  |                    379.044 |                  0.1 |
|            2 |         141 |            2 |                         6.45899 |               163.982 |              904.259 |                    278.534 |                  0.1 |
|            3 |          92 |            2 |                         8.75033 |               126.657 |              796.28  |                    445.926 |                  0.1 |

Stage 3 established the reference action traces used later by the async simulator and baseline evaluation.

## Stage 4: Visual robustness

- Images sampled: `12`
- Image source: `hf_repo_video_file`
- Visual metric rows: `144`
- Policy drift measured: `False`

| perturbation     |   severity |   num_samples |   mae_mean |    mse_mean |   psnr_mean |   brightness_shift_mean |   contrast_ratio_mean |   edge_energy_ratio_mean |
|:-----------------|-----------:|--------------:|-----------:|------------:|------------:|------------------------:|----------------------:|-------------------------:|
| blur             |       1    |            12 | 0.00922355 | 0.000838782 |     30.7646 |            -1.59691e-05 |              0.903525 |                 0.593312 |
| blur             |       2    |            12 | 0.0121627  | 0.00129584  |     28.8751 |             0.000488063 |              0.843261 |                 0.496794 |
| brightness       |       0.2  |            12 | 0.00847423 | 0.000518669 |     32.8522 |             0.00847419  |              0.805141 |                 0.618853 |
| brightness       |       0.5  |            12 | 0.0142057  | 0.0018613   |     27.302  |             0.0142057   |              0.558261 |                 0.413632 |
| center_crop      |       0.75 |            12 | 0.0324084  | 0.0105355   |     19.7737 |            -0.0108216   |              1.2986   |                 0.867987 |
| contrast         |       0.2  |            12 | 0.00427946 | 0.000281143 |     35.5108 |            -0.00390635  |              1.18626  |                 1.17487  |
| contrast         |       0.5  |            12 | 0.0105407  | 0.0017325   |     27.6133 |            -0.00993048  |              1.46283  |                 1.43494  |
| jpeg             |       0.5  |            12 | 0.00330454 | 8.19164e-05 |     40.8811 |             0.00220539  |              0.978788 |                 1.0317   |
| jpeg             |       0.75 |            12 | 0.00571008 | 0.000248298 |     36.0614 |            -0.000474274 |              1.04288  |                 1.30191  |
| random_occlusion |       0.15 |            12 | 0.00358092 | 0.00127963  |     28.9293 |             0.00316824  |              0.922018 |                 0.97702  |
| random_occlusion |       0.3  |            12 | 0.0100065  | 0.00332455  |     24.7827 |             0.00757887  |              0.757585 |                 0.774563 |
| resolution_drop  |       0.5  |            12 | 0.00662704 | 0.0014559   |     28.3708 |             0.00259613  |              0.983064 |                 0.608931 |

Stage 4 used real frames extracted from Hugging Face repository video files. It measured visual severity only; it did not claim policy action drift.

## Stage 5: Instruction sensitivity

- Raw instruction-like records: `512`
- Natural-language unique records: `0`
- Symbolic fallback used: `True`
- Perturbation rows: `4`

Important limitation: `lerobot/pusht` did not expose natural-language instructions in the sampled rows. Stage 5 therefore produced symbolic task-label perturbations only. This should not be marketed as natural-language instruction robustness.

| perturbation        | kind                | is_natural_language   |   num_rows |   mean_word_count_delta |   mean_char_count_delta |   mean_lexical_overlap |
|:--------------------|:--------------------|:----------------------|-----------:|------------------------:|------------------------:|-----------------------:|
| original            | identity            | False                 |          1 |                       0 |                       0 |                    1   |
| symbolic_ambiguous  | symbolic_ambiguity  | False                 |          1 |                       0 |                      -3 |                    0   |
| symbolic_distractor | symbolic_distractor | False                 |          1 |                       1 |                      24 |                    0.5 |
| symbolic_mask       | symbolic_masking    | False                 |          1 |                       1 |                       7 |                    0   |

## Stage 6: Async deployment-stress simulation

- Episodes: `4`
- Scenarios: `26`
- Raw rows: `104`

Top mode by normalized drift:

- Mode: `action_horizon_mismatch`
- Normalized mean L2 drift: `0.3330325318685965`
- Mean L2 drift: `121.46199913024903`
- Recovery delay proxy: `123.4`

Top risk scenario:

- Mode: `action_horizon_mismatch`
- Params: `{"actual_horizon": 8, "expected_horizon": 4}`
- Risk score proxy: `2.5562635495893855`
- Mean L2 drift: `138.2900505065918`
- Quality score proxy: `0.727326073641731`

| mode                        | params_json                                  |   mean_l2_drift_mean |   normalized_mean_l2_drift_mean |   smoothness_degradation_mean |   recovery_delay_proxy_mean |   compute_saving_proxy_mean |   quality_score_proxy_mean |   risk_score_proxy |
|:----------------------------|:---------------------------------------------|---------------------:|--------------------------------:|------------------------------:|----------------------------:|----------------------------:|---------------------------:|-------------------:|
| action_horizon_mismatch     | {"actual_horizon": 8, "expected_horizon": 4} |            138.29    |                       0.377663  |                     -4.51917  |                      127    |                      0.875  |                   0.727326 |            2.55626 |
| action_chunk_reuse          | {"chunk_size": 16}                           |             52.1962  |                       0.142225  |                     -1.87024  |                      126.75 |                      0.9375 |                   0.87557  |            2.45953 |
| reduced_inference_frequency | {"frequency_divisor": 16}                    |             52.1962  |                       0.142225  |                     -1.87024  |                      126.75 |                      0.9375 |                   0.87557  |            2.45953 |
| action_horizon_mismatch     | {"actual_horizon": 2, "expected_horizon": 8} |            114.339   |                       0.317278  |                     -0.757125 |                      121    |                      0.5    |                   0.760002 |            2.41387 |
| action_horizon_mismatch     | {"actual_horizon": 4, "expected_horizon": 8} |            108.893   |                       0.298481  |                     -0.757125 |                      121    |                      0.75   |                   0.770605 |            2.41027 |
| action_horizon_mismatch     | {"actual_horizon": 4, "expected_horizon": 2} |            134.766   |                       0.367552  |                     -4.41449  |                      127    |                      0.75   |                   0.732706 |            2.40553 |
| action_horizon_mismatch     | {"actual_horizon": 2, "expected_horizon": 4} |            111.023   |                       0.304189  |                     -0.306532 |                      121    |                      0.5    |                   0.767245 |            2.2833  |
| action_chunk_reuse          | {"chunk_size": 8}                            |             26.727   |                       0.072854  |                     -0.873878 |                      123.75 |                      0.875  |                   0.932145 |            2.249   |
| frame_skip                  | {"skip": 8}                                  |             26.727   |                       0.072854  |                     -0.873878 |                      123.75 |                      0.875  |                   0.932145 |            2.249   |
| reduced_inference_frequency | {"frequency_divisor": 8}                     |             26.727   |                       0.072854  |                     -0.873878 |                      123.75 |                      0.875  |                   0.932145 |            2.249   |
| action_chunk_reuse          | {"chunk_size": 4}                            |             11.9396  |                       0.0326472 |                     -0.344993 |                      119    |                      0.75   |                   0.968395 |            2.01045 |
| frame_skip                  | {"skip": 4}                                  |             11.9396  |                       0.0326472 |                     -0.344993 |                      119    |                      0.75   |                   0.968395 |            2.01045 |
| reduced_inference_frequency | {"frequency_divisor": 4}                     |             11.9396  |                       0.0326472 |                     -0.344993 |                      119    |                      0.75   |                   0.968395 |            2.01045 |
| observation_delay           | {"delay_steps": 8}                           |             58.2029  |                       0.158927  |                     -0.344207 |                      126.5  |                      0      |                   0.86301  |            1.53242 |
| action_chunk_reuse          | {"chunk_size": 2}                            |              4.09747 |                       0.0111841 |                     -0.101    |                       94    |                      0.5    |                   0.988941 |            1.48035 |

This is the main systems contribution of the current run: recorded action traces can be stress-tested under realistic deployment distortions without needing paid APIs or robot hardware.

## Stage 7: Optional baseline / policy evaluation

- Baselines: `8`
- Evaluation rows: `32`
- Real policy loaded: `False`
- Real policy attempted: `False`

Top baseline by quality:

- Baseline: `replay_oracle`
- Quality score proxy: `1.0`
- Normalized drift: `0.0`

Worst baseline by risk:

- Baseline: `first_action_hold`
- Risk score proxy: `2.791916523575783`
- Mean L2 drift: `183.9531135559082`

| baseline                    |   mean_l2_drift_mean |   normalized_mean_l2_drift_mean |   quality_score_proxy_mean |   smoothness_degradation_mean |   hold_fraction_mean |   recovery_delay_proxy_mean |   risk_score_proxy |
|:----------------------------|---------------------:|--------------------------------:|---------------------------:|------------------------------:|---------------------:|----------------------------:|-------------------:|
| first_action_hold           |            183.953   |                       0.521917  |                   0.665165 |                    -8.2193    |            1         |                      127    |          2.79192   |
| mean_action                 |            105.182   |                       0.289828  |                   0.775969 |                    -8.2193    |            1         |                      127    |          2.55983   |
| chunk_replay_8              |             26.727   |                       0.072854  |                   0.932145 |                    -0.873878  |            0.878259  |                      123.75 |          2.18861   |
| nearest_neighbor_time_50pct |            133.079   |                       0.362933  |                   0.735204 |                    -4.39077   |            0.507576  |                      127    |          2.14051   |
| chunk_replay_4              |             11.9396  |                       0.0326472 |                   0.968395 |                    -0.344993  |            0.755943  |                      119    |          1.97859   |
| lag1_hold                   |              8.15124 |                       0.0223112 |                   0.978179 |                    -0.0236031 |            0.0524306 |                       94    |          1.01474   |
| linear_extrapolation        |              3.73067 |                       0.0102885 |                   0.989817 |                     1.21192   |            0.0468864 |                       50.5  |          0.562175  |
| replay_oracle               |              0       |                       0         |                   1        |                     0         |            0.0463351 |                        0    |          0.0463351 |

Stage 7 did not load a real VLA policy. That is intentional. The current artifact is a robust evaluation scaffold plus sanity baselines, not a policy benchmark.

## Evidence index

| stage                          | label                           | kind       | exists   | path                                                                                                    |
|:-------------------------------|:--------------------------------|:-----------|:---------|:--------------------------------------------------------------------------------------------------------|
| stage0_env_probe               | env_probe_json                  | saved_file | True     | /kaggle/working/RoboTrace/env_probe/env_probe.json                                                      |
| stage0_env_probe               | nvidia_smi_txt                  | saved_file | True     | /kaggle/working/RoboTrace/env_probe/nvidia_smi.txt                                                      |
| stage0_env_probe               | pip_freeze_txt                  | saved_file | True     | /kaggle/working/RoboTrace/env_probe/pip_freeze.txt                                                      |
| stage2_dataset_probe           | dataset_schema_md               | report     | True     | /kaggle/working/RoboTrace/case_studies/dataset_probe/dataset_schema.md                                  |
| stage2_dataset_probe           | dataset_probe_json              | saved_file | True     | /kaggle/working/RoboTrace/case_studies/dataset_probe/dataset_probe.json                                 |
| stage2_dataset_probe           | dataset_sample_jsonl            | saved_file | True     | /kaggle/working/RoboTrace/results/raw/stage2_dataset_sample_rows.jsonl                                  |
| stage2_dataset_probe           | episode_summary_csv             | saved_file | True     | /kaggle/working/RoboTrace/results/summaries/stage2_episode_probe_summary.csv                            |
| stage3_trace_metrics           | trace_report_md                 | report     | True     | /kaggle/working/RoboTrace/case_studies/trace_metrics/stage3_trace_metrics_report.md                     |
| stage3_trace_metrics           | dataset_summary_json            | saved_file | True     | /kaggle/working/RoboTrace/results/summaries/stage3_dataset_summary.json                                 |
| stage3_trace_metrics           | episode_metrics_jsonl           | saved_file | True     | /kaggle/working/RoboTrace/results/raw/stage3_episode_metrics.jsonl                                      |
| stage3_trace_metrics           | episode_summary_csv             | saved_file | True     | /kaggle/working/RoboTrace/results/summaries/stage3_episode_summary.csv                                  |
| stage3_trace_metrics           | episode_traces_npz              | saved_file | True     | /kaggle/working/RoboTrace/results/raw/stage3_episode_traces.npz                                         |
| stage3_trace_metrics           | step_metrics_jsonl              | saved_file | True     | /kaggle/working/RoboTrace/results/raw/stage3_step_metrics.jsonl                                         |
| stage4_visual_robustness       | preview_grid                    | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage4_visual_preview_grid.png                                |
| stage4_visual_robustness       | severity_bar                    | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage4_visual_severity_bar.png                                |
| stage4_visual_robustness       | severity_heatmap                | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage4_visual_severity_heatmap.png                            |
| stage4_visual_robustness       | visual_report_md                | report     | True     | /kaggle/working/RoboTrace/case_studies/visual_robustness/stage4_visual_robustness_report.md             |
| stage4_visual_robustness       | frame_manifest_json             | saved_file | True     | /kaggle/working/RoboTrace/case_studies/visual_robustness/stage4_extracted_frame_manifest.json           |
| stage4_visual_robustness       | manifest_json                   | saved_file | True     | /kaggle/working/RoboTrace/results/raw/stage4_visual_perturbation_manifest.json                          |
| stage4_visual_robustness       | repo_visual_candidates_json     | saved_file | True     | /kaggle/working/RoboTrace/case_studies/visual_robustness/stage4_repo_visual_file_candidates.json        |
| stage4_visual_robustness       | stage4_summary_json             | saved_file | True     | /kaggle/working/RoboTrace/case_studies/visual_robustness/stage4_summary.json                            |
| stage4_visual_robustness       | visual_metrics_jsonl            | saved_file | True     | /kaggle/working/RoboTrace/results/raw/stage4_visual_metrics.jsonl                                       |
| stage4_visual_robustness       | visual_summary_csv              | saved_file | True     | /kaggle/working/RoboTrace/results/summaries/stage4_visual_summary.csv                                   |
| stage4_visual_robustness       | visual_summary_json             | saved_file | True     | /kaggle/working/RoboTrace/results/summaries/stage4_visual_summary.json                                  |
| stage5_instruction_sensitivity | length_shift                    | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage5_instruction_length_shift.png                           |
| stage5_instruction_sensitivity | perturbation_counts             | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage5_instruction_perturbation_counts.png                    |
| stage5_instruction_sensitivity | instruction_report_md           | report     | True     | /kaggle/working/RoboTrace/case_studies/instruction_sensitivity/stage5_instruction_sensitivity_report.md |
| stage5_instruction_sensitivity | instruction_manifest_json       | saved_file | True     | /kaggle/working/RoboTrace/results/raw/stage5_instruction_manifest.json                                  |
| stage5_instruction_sensitivity | instruction_perturbations_jsonl | saved_file | True     | /kaggle/working/RoboTrace/results/raw/stage5_instruction_perturbations.jsonl                            |
| stage5_instruction_sensitivity | instruction_records_jsonl       | saved_file | True     | /kaggle/working/RoboTrace/results/raw/stage5_instruction_records.jsonl                                  |
| stage5_instruction_sensitivity | instruction_summary_csv         | saved_file | True     | /kaggle/working/RoboTrace/results/summaries/stage5_instruction_summary.csv                              |
| stage5_instruction_sensitivity | instruction_summary_json        | saved_file | True     | /kaggle/working/RoboTrace/results/summaries/stage5_instruction_summary.json                             |
| stage5_instruction_sensitivity | stage5_summary_json             | saved_file | True     | /kaggle/working/RoboTrace/case_studies/instruction_sensitivity/stage5_summary.json                      |
| stage6_async_simulation        | drift_by_mode                   | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage6_async_drift_by_mode.png                                |
| stage6_async_simulation        | latency_quality                 | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage6_latency_quality_tradeoff.png                           |
| stage6_async_simulation        | metric_heatmap                  | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage6_async_metric_heatmap.png                               |
| stage6_async_simulation        | recovery_delay                  | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage6_recovery_delay_proxy.png                               |
| stage6_async_simulation        | smoothness_by_mode              | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage6_async_smoothness_degradation_by_mode.png               |
| stage6_async_simulation        | trace_overlay                   | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage6_trace_overlay_first_episode.png                        |
| stage6_async_simulation        | async_report_md                 | report     | True     | /kaggle/working/RoboTrace/case_studies/async_simulation/async_report.md                                 |
| stage6_async_simulation        | async_candidate_traces_npz      | saved_file | True     | /kaggle/working/RoboTrace/results/raw/stage6_async_candidate_traces.npz                                 |
| stage6_async_simulation        | async_dataset_summary_json      | saved_file | True     | /kaggle/working/RoboTrace/results/summaries/async_dataset_summary.json                                  |
| stage6_async_simulation        | async_raw_jsonl                 | saved_file | True     | /kaggle/working/RoboTrace/results/raw/async_raw.jsonl                                                   |
| stage6_async_simulation        | async_summary_csv               | saved_file | True     | /kaggle/working/RoboTrace/results/summaries/async_summary.csv                                           |
| stage6_async_simulation        | stage6_summary_json             | saved_file | True     | /kaggle/working/RoboTrace/case_studies/async_simulation/stage6_summary.json                             |
| stage7_optional_policy_eval    | baseline_drift                  | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage7_baseline_mean_drift.png                                |
| stage7_optional_policy_eval    | baseline_heatmap                | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage7_baseline_metric_heatmap.png                            |
| stage7_optional_policy_eval    | baseline_quality                | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage7_baseline_quality_score.png                             |
| stage7_optional_policy_eval    | baseline_recovery               | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage7_baseline_recovery_delay.png                            |
| stage7_optional_policy_eval    | trace_overlay                   | figure     | True     | /kaggle/working/RoboTrace/results/figures/stage7_baseline_trace_overlay.png                             |
| stage7_optional_policy_eval    | policy_eval_report_md           | report     | True     | /kaggle/working/RoboTrace/case_studies/optional_policy_eval/stage7_policy_eval_report.md                |
| stage7_optional_policy_eval    | baseline_raw_jsonl              | saved_file | True     | /kaggle/working/RoboTrace/results/raw/stage7_baseline_eval_raw.jsonl                                    |
| stage7_optional_policy_eval    | baseline_rollouts_npz           | saved_file | True     | /kaggle/working/RoboTrace/results/raw/stage7_baseline_rollouts.npz                                      |
| stage7_optional_policy_eval    | baseline_summary_csv            | saved_file | True     | /kaggle/working/RoboTrace/results/summaries/stage7_baseline_summary.csv                                 |
| stage7_optional_policy_eval    | policy_eval_summary_json        | saved_file | True     | /kaggle/working/RoboTrace/results/summaries/stage7_policy_eval_summary.json                             |
| stage7_optional_policy_eval    | stage7_summary_json             | saved_file | True     | /kaggle/working/RoboTrace/case_studies/optional_policy_eval/stage7_summary.json                         |

Missing/optional evidence paths are excluded from the public evidence index and stored in:

- `/kaggle/working/RoboTrace/results/summaries/robotrace_missing_evidence_manifest.json`

## Claims allowed

- RoboTrace runs fully in Kaggle under the tested environment.
- The core package, metrics, perturbation logic, async simulator, and report writers pass CPU-safe tests.
- The run successfully probes `lerobot/pusht` without requiring LeRobot installation.
- The run computes action-trace metrics over 4 usable episodes and 512 step rows.
- The visual robustness suite perturbs real frames extracted from dataset repository video files.
- The instruction sensitivity stage found only symbolic task labels for this dataset, not natural language.
- The async simulator identifies action horizon mismatch as the highest-risk deployment-stress mode in this run.
- The optional policy stage provides action-only sanity baselines and explicitly records that no real policy was loaded.

## Claims not allowed

- Do not claim real robot hardware validation.
- Do not claim real VLA policy robustness.
- Do not claim natural-language instruction robustness for `lerobot/pusht` from this run.
- Do not claim task success or success-rate degradation.
- Do not claim measured serving latency; Stage 6 latency values are proxies.
- Do not claim SOTA benchmark status.

## Next stages

1. Stage 9: Prepare Hugging Face dataset/Space release folder, with dataset card and dashboard scaffold.
2. Stage 10: GitHub packaging and push, only after inspecting the generated report and avoiding large raw artifacts.
3. Optional later stage: isolated real-policy loading, but only in a separate notebook with pinned versions and fallback behavior.

## Final verdict

RoboTrace is currently a credible low-cost evaluation and deployment-stress toolkit artifact. Its strongest angle is not policy performance; it is careful, reproducible stress testing of action traces under practical deployment distortions.