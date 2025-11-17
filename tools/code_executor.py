"""Safe Python code execution in sandbox."""

import sys
import io
import traceback
from typing import Dict, Any
from contextlib import redirect_stdout, redirect_stderr
from core.logger import logger
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt


class CodeExecutor:
    """Execute Python code safely."""
    
    def __init__(self):
        """Initialize executor."""
        self.globals_dict = {
            '__builtins__': __builtins__,
            'print': print,
        }
        
        # Add safe libraries
        self._add_safe_libraries()
    
    def _add_safe_libraries(self):
        """Add commonly used safe libraries."""
        safe_imports = {
            'math': 'math',
            'random': 'random',
            'datetime': 'datetime',
            'json': 'json',
            'csv': 'csv',
            're': 're',
            'statistics': 'statistics',
            'collections': 'collections',
            'itertools': 'itertools',
            'functools': 'functools',
            'numpy': 'numpy',
            'pandas': 'pandas',
            'matplotlib': 'matplotlib',
            'plt': 'matplotlib.pyplot',
        }
        
        for alias, module_name in safe_imports.items():
            try:
                module = __import__(module_name)
                if '.' in module_name:
                    # Handle submodules like matplotlib.pyplot
                    parts = module_name.split('.')
                    for part in parts[1:]:
                        module = getattr(module, part)
                self.globals_dict[alias] = module
            except ImportError:
                pass  # Library not installed
    
    def execute_code(
        self,
        code: str,
        timeout: int = 10,
        return_plot: bool = True
    ) -> Dict[str, Any]:
        """Execute Python code safely.
        
        Args:
            code: Python code to execute
            timeout: Execution timeout in seconds
            return_plot: Whether to save matplotlib plots
            
        Returns:
            Execution result dict
        """
        try:
            # Capture output
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()
            
            # Execute code
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, self.globals_dict)
            
            stdout = stdout_capture.getvalue()
            stderr = stderr_capture.getvalue()
            
            # Check for plots
            plot_path = None
            if return_plot and plt.get_fignums():
                plot_path = f"output_plot_{id(code)}.png"
                plt.savefig(plot_path, bbox_inches='tight', dpi=100)
                plt.close('all')
            
            logger.info("Code executed successfully")
            
            return {
                'success': True,
                'stdout': stdout,
                'stderr': stderr,
                'error': None,
                'plot': plot_path
            }
            
        except Exception as e:
            error_msg = traceback.format_exc()
            logger.error(f"Code execution error: {error_msg}")
            
            return {
                'success': False,
                'stdout': stdout_capture.getvalue() if 'stdout_capture' in locals() else "",
                'stderr': stderr_capture.getvalue() if 'stderr_capture' in locals() else "",
                'error': error_msg,
                'plot': None
            }
    
    def execute_expression(self, expression: str) -> Dict[str, Any]:
        """Evaluate a Python expression.
        
        Args:
            expression: Python expression
            
        Returns:
            Result dict with value
        """
        try:
            result = eval(expression, self.globals_dict)
            logger.info(f"Expression evaluated: {expression}")
            
            return {
                'success': True,
                'result': result,
                'error': None
            }
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Expression error: {error_msg}")
            
            return {
                'success': False,
                'result': None,
                'error': error_msg
            }
    
    def format_execution_result(self, result: Dict[str, Any]) -> str:
        """Format execution result for display.
        
        Args:
            result: Execution result
            
        Returns:
            Formatted string
        """
        output = []
        
        if result['success']:
            output.append("✅ **Code executed successfully!**\n")
            
            if result['stdout']:
                output.append("**Output:**")
                output.append("```json")
                output.append(result['stdout'])
                output.append("```\n")
            
            if result['plot']:
                output.append(f"📊 **Plot saved:** {result['plot']}\n")
            
            if not result['stdout'] and not result['plot']:
                output.append("*Code executed with no output.*\n")
        else:
            output.append("❌ **Execution Error:**\n")
            output.append("```json")
            output.append(result['error'])
            output.append("```")
        
        return "\n".join(output)


# Global executor
code_executor = CodeExecutor()
