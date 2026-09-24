# Portable execution additions

The upstream study/original methods are retained. Deployment settings can be
provided as a JSON object via `AF2_CONFIG`; keys are the path settings in
`structure_prediction/libconfig_af.py`, `data_dir`, and `max_template_date`.
Unknown keys are rejected. Keep machine-specific settings outside the repository.
State runs use the corresponding `mmcif_active_db_path` or `mmcif_inactive_db_path`.

The wrapper now forwards `--random_seed`, `--model_names` (indices 0–4),
`--db_preset`, `--msa_path`, `--cpu`, and `--no_relax`. It uses the current Python
interpreter and propagates a failing child exit status. `AF2_STEREO_CHEMICAL_PROPS`
can point to the separately downloaded stereo-chemical data, keeping source clean.
Explicit memory settings are preserved. Set `CUDA_VISIBLE_DEVICES` and verify
actual GPU computation before a prediction; upstream otherwise selects CPU.

`reduced_dbs`, supplied MSAs, skipping relaxation, and current database versions
must be recorded as deviations when comparing to the historical paper. An active
state argument selects receptor-state templates, not a ligand conformation.

Lightweight checks: `python -m unittest discover -s tests -v`.

For headless Kalign 3.2.2 jobs, set `AF2_KALIGN_STDIN=1`. That release also
reads inherited nonterminal stdin when `-i` is present; an empty stdin can cause
all template realignments to fail. The opt-in sends the same FASTA through one
stdin stream and omits the duplicate file input. No alignment parameters or
software versions change. Record this compatibility setting with the run.
