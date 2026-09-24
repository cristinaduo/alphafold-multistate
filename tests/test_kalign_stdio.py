"""Test headless input transport without installing the scientific environment."""
import importlib
import logging
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'structure_prediction'))
with patch.dict(sys.modules,{'absl':types.SimpleNamespace(logging=logging)}):
    kalign=importlib.import_module('alphafold.data.tools.kalign')


class KalignStdinTest(unittest.TestCase):
    def test_headless_mode_supplies_one_input_and_preserves_sequences(self):
        with tempfile.TemporaryDirectory() as td:
            executable=Path(td)/'kalign'
            executable.write_text('''#!/usr/bin/env python3
import pathlib,sys
# Reproduce the relevant Kalign 3.2.2 nonterminal-input rule.
if '-i' in sys.argv: sys.exit(1)
data=sys.stdin.read()
if data.count('>')!=2:sys.exit(2)
pathlib.Path(sys.argv[sys.argv.index('-o')+1]).write_text(data)
''')
            executable.chmod(0o755)
            aligner=kalign.Kalign(binary_path=str(executable))
            with patch.dict(os.environ,{'AF2_KALIGN_STDIN':'0'}):
                with self.assertRaises(RuntimeError):aligner.align(['ACDEFGH','ACDEGH'])
            with patch.dict(os.environ,{'AF2_KALIGN_STDIN':'1'}):
                result=aligner.align(['ACDEFGH','ACDEGH'])
            self.assertEqual(result,'>sequence 1\nACDEFGH\n>sequence 2\nACDEGH\n')
