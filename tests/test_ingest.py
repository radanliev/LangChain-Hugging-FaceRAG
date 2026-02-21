pypytest suite and CI and the index artifact

import subprocess
import sys
import os

def test_ingest_creates_index(tmp_path):
    # prepare sample data
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    sample = data_dir / "sample.txt"
    sample.write_text("This is a small CI test document. Hello world.")

    index_path = tmp_path / "test_index.pkl"

    # run ingest script
    ingest_script = os.path.join(os.path.dirname(__file__), "..", "src", "ingest.py")
    cmd = [sys.executable, ingest_script, "--data-dir", str(data_dir), "--index-path", str(index_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    print(res.stderr, file=sys.stderr)
    assert res.returncode == 0, "Ingest script failed"

    assert index_path.exists(), "Index file was not created"
