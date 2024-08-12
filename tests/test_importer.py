import unittest
from unittest.mock import patch, mock_open
from activated_notebook_importer import import_notebook, import_notebook_from_string
import json

class TestActivatedNotebookImporter(unittest.TestCase):
    @patch('builtins.open')
    def test_import_notebook(self, mock_file):
        notebook_content = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "def test_func():\n",
                        "    return 'Hello, World!'"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {
                        "name": "ipython",
                        "version": 3
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.8.5"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(notebook_content)
        
        module = import_notebook('dummy_path.ipynb')
        self.assertTrue(hasattr(module, 'test_func'))
        self.assertEqual(module.test_func(), 'Hello, World!')

    def test_import_notebook_from_string(self):
        notebook_string = json.dumps({
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "def greet(name):\n",
                        "    return f'Hello, {name}!'"
                    ]
                }
            ],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 4
        })
        module = import_notebook_from_string(notebook_string)
        self.assertTrue(hasattr(module, 'greet'))
        self.assertEqual(module.greet('Alice'), 'Hello, Alice!')

if __name__ == '__main__':
    unittest.main()