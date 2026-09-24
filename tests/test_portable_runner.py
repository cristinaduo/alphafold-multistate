"""CLI contract tests: no scientific environment required."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / 'structure_prediction'
sys.path.insert(0, str(SOURCE))
import run


class PortableRunnerTests(unittest.TestCase):
    def test_study_keeps_masking_and_forwards_seed_and_state_coordinates(self):
        with patch.object(run.sp, 'call', return_value=0) as call:
            self.assertEqual(run.main(['sample.fa', '--preset', 'study', '--state', 'active',
                '--random_seed', '20260924', '--model_names', '0', '--db_preset', 'reduced_dbs']), 0)
        args = call.call_args[0][0]
        self.assertEqual(args[0], sys.executable)
        for expected in ['--random_seed=20260924', '--model_names=0', '--db_preset=reduced_dbs',
                         '--remove_msa_for_template_aligned=true', '--use_templates=true', '--use_msa=true']:
            self.assertIn(expected, args)
        self.assertIn('--template_mmcif_dir=' + run.libconfig_af.mmcif_active_db_path, args)

    def test_original_and_failure_are_not_reported_as_study_success(self):
        with patch.object(run.sp, 'call', return_value=9) as call:
            self.assertEqual(run.main(['sample.fa', '--preset', 'original']), 9)
        self.assertNotIn('--remove_msa_for_template_aligned=true', call.call_args[0][0])
        self.assertIn('--db_preset=full_dbs', call.call_args[0][0])

    def test_bad_model_list_stops_before_execution(self):
        with patch.object(run.sp, 'call') as call:
            with self.assertRaises(ValueError):
                run.main(['sample.fa', '--model_names', 'model_1'])
            call.assert_not_called()

    def test_json_configuration_rejects_unknown_keys(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'config.json'
            env = dict(os.environ, AF2_CONFIG=str(path), PYTHONPATH=str(SOURCE))
            path.write_text(json.dumps({'data_dir': '/example/data'}))
            result = subprocess.run([sys.executable, '-c', 'import libconfig_af; print(libconfig_af.data_dir)'],
                                    env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), '/example/data')
            path.write_text(json.dumps({'typo_data_dir': '/example/data'}))
            result = subprocess.run([sys.executable, '-c', 'import libconfig_af'], env=env, capture_output=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
