import sys
import pytest
from unittest.mock import patch
from io import StringIO
from cli.main import run_cli

def test_cli_execution_no_stream():
    # Patch sys.argv to simulate CLI arguments
    test_args = ["main.py", "Show me test users"]
    
    with patch.object(sys, 'argv', test_args):
        # Capture stdout
        with patch('sys.stdout', new=StringIO()) as fake_out:
            run_cli()
            output = fake_out.getvalue()
            
            assert "Processing query: 'Show me test users'" in output
            assert "Final Response:" in output
            assert "Status: success" in output

def test_cli_execution_with_stream():
    # Patch sys.argv to simulate CLI arguments
    test_args = ["main.py", "Show me streaming users", "--stream"]
    
    with patch.object(sys, 'argv', test_args):
        # Capture stdout
        with patch('sys.stdout', new=StringIO()) as fake_out:
            run_cli()
            output = fake_out.getvalue()
            
            assert "Processing query: 'Show me streaming users'" in output
            assert "[Stream] Finished node:" in output
            assert "Final Response:" in output
            assert "Status: success" in output
