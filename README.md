# ActivatedNotebookImporter

ActivatedNotebookImporter is a Python package developed and used internally by Activated AI (https://activated-ai.com) that allows you to import Jupyter notebooks as Python modules. This package is designed to seamlessly integrate Jupyter notebooks into your Python workflows.

## Key Features

- Import Jupyter notebooks as Python modules
- Support for parameter substitution, enabling dynamic parameter setting
- Ability to exclude specific cells from execution using tags
- Automatic parameter detection from the first cell and cells tagged with "parameters"

## Use Case

ActivatedNotebookImporter is particularly useful for workflows where you want to use Jupyter notebooks as reusable modules. Instead of converting your Jupyter notebooks to Python scripts, you can use them directly in your workflows:

1. Set parameters using the `params` argument when importing the notebook
2. Exclude specific cells in the notebook by tagging them with 'import-exclude'
3. Import the notebook as a module
4. Call functions from the imported module with your desired parameters
5. Get the results directly, without intermediate steps

This approach allows for more flexible and maintainable code, keeping your exploratory work and reusable code closely aligned.

## Installation

You can install ActivatedNotebookImporter using pip:

```
pip install activated-notebook-importer
```

## Usage

Here's a basic example of how to use ActivatedNotebookImporter:

```python
from activated_notebook_importer import import_notebook

# Import a notebook with parameter substitution
module = import_notebook('path/to/your/notebook.ipynb', 
                         {'param1': 'value1', 'param2': 'value2'})

# Assuming your notebook defines a 'my_function' function
result = module.my_function()
print(result)
```

In your Jupyter notebook:

```python
# In the first cell or in cells tagged with "parameters"
param1 = 'default1'
param2 = 'default2'

# In a code cell
def my_function(param1=param1, param2=param2):
    # Your code here
    return some_result

# In another cell, tag this with 'import-exclude' in Jupyter
# This cell won't be executed when the notebook is imported
my_function()
```

Note: 
- The first cell of the notebook is assumed to contain parameters, which can be overwritten with the `params` argument when importing.
- You can also tag cells with the "parameters" tag for them to be considered as parameter cells.

## Example: Hyperparameter Search

One potential use case is for hyperparameter search in machine learning models:

```python
from activated_notebook_importer import import_notebook

hyperparameters = [
    {'learning_rate': 0.01, 'batch_size': 32},
    {'learning_rate': 0.001, 'batch_size': 64},
    {'learning_rate': 0.0001, 'batch_size': 128}
]

results = []
for params in hyperparameters:
    module = import_notebook('model_training.ipynb', params)
    results.append(module.train())

# Process and analyze results
```

## Internal Use at Activated AI

ActivatedNotebookImporter is a tool used in various workflows at Activated AI. We use it to:
- Integrate notebook-based code into larger systems
- Easily reuse and parameterize notebook code
- Maintain consistency between our exploratory notebooks and reusable code

By using this tool, we've improved our ability to leverage work done in Jupyter notebooks in our broader Python ecosystem.

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## About Activated AI

ActivatedNotebookImporter is developed and maintained by Activated AI. Visit our website at https://activated-ai.com to learn more about our AI research and development.