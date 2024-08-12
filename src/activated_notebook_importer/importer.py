import nbformat
import json
from typing import Dict, Any, Optional
from nbparameterise import (
    extract_parameters, replace_definitions, parameter_values
)
import types
import sys
import logging

# Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def import_notebook_from_string(notebook_string: str, module_name: str = "notebook_module") -> types.ModuleType:
    """
    Import a Jupyter notebook from a string representation as a Python module.
    
    Args:
        notebook_string (str): A string containing the JSON of a Jupyter notebook
        module_name (str): Name to give to the created module
    
    Returns:
        types.ModuleType: The imported module
    
    Raises:
        json.JSONDecodeError: If the notebook string is not valid JSON
        ValueError: If the notebook structure is invalid
        SyntaxError: If there's a syntax error in the notebook code
    """
    try:
        # Parse the notebook JSON
        notebook = json.loads(notebook_string)
        
        # Create a new module
        module = types.ModuleType(module_name)
        
        # Compile all code cells into a single code object
        code_cells = [cell['source'] for cell in notebook['cells'] if cell['cell_type'] == 'code']
        combined_code = '\n'.join(''.join(cell) for cell in code_cells)
        code_object = compile(combined_code, f"<{module_name}>", 'exec')
        
        # Execute the compiled code in the module's namespace
        exec(code_object, module.__dict__)
        
        # Add the module to sys.modules
        sys.modules[module_name] = module
        
        logger.info(f"Successfully imported notebook as module: {module_name}")
        return module
    
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse notebook JSON: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid notebook structure: {e}")
        raise
    except SyntaxError as e:
        logger.error(f"Syntax error in notebook code: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during notebook import: {e}")
        raise

def read_notebook(notebook_path: str) -> nbformat.NotebookNode:
    """
    Read a Jupyter notebook from a file.
    
    Args:
        notebook_path (str): Path to the notebook file
    
    Returns:
        nbformat.NotebookNode: The parsed notebook
    
    Raises:
        FileNotFoundError: If the notebook file is not found
        nbformat.reader.NotJSONError: If the file is not a valid JSON notebook
    """
    try:
        with open(notebook_path) as f:
            return nbformat.read(f, as_version=4)
    except FileNotFoundError:
        logger.error(f"Notebook file not found: {notebook_path}")
        raise
    except nbformat.reader.NotJSONError:
        logger.error(f"Invalid notebook file: {notebook_path}")
        raise

def process_notebook(nb: nbformat.NotebookNode, params: Optional[Dict[str, Any]] = None) -> str:
    """
    Process a notebook by replacing parameters and removing excluded cells.
    
    Args:
        nb (nbformat.NotebookNode): The notebook to process
        params (Optional[Dict[str, Any]]): Parameters to replace in the notebook
    
    Returns:
        str: JSON string of the processed notebook
    """
    orig_parameters = extract_parameters(nb)
    if params:
        params = parameter_values(orig_parameters, params)
        nb = replace_definitions(nb, params)
    
    # Remove cells with tag 'import-exclude'
    nb['cells'] = [cell for cell in nb['cells'] if 'import-exclude' not in cell.get('metadata', {}).get('tags', [])]
    
    return json.dumps(nb)

def import_notebook(notebook_path: str, params: Optional[Dict[str, Any]] = None) -> types.ModuleType:
    """
    Import a Jupyter notebook from a file as a Python module.
    
    Args:
        notebook_path (str): Path to the notebook file
        params (Optional[Dict[str, Any]]): Parameters to replace in the notebook
    
    Returns:
        types.ModuleType: The imported module
    """
    try:
        nb = read_notebook(notebook_path)
        processed_nb = process_notebook(nb, params)
        return import_notebook_from_string(processed_nb)
    except Exception as e:
        logger.error(f"Failed to import notebook {notebook_path}: {e}")
        raise