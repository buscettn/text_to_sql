import sqlglot
from sqlglot import errors
from typing import Tuple

def validate_and_fix_sql(sql: str) -> Tuple[bool, str]:
    """
    Validates the SQL syntactically and transpiles it to the Impala dialect.
    Uses 'hive' as a fallback dialect if 'impala' is not directly supported by the installed sqlglot version.
    
    Args:
        sql: The SQL string to validate and transpile.
        
    Returns:
        A tuple containing:
        - A boolean indicating whether the validation/transpilation was successful.
        - The transpiled SQL string if successful, or the error message if not.
    """
    if not sql or not sql.strip():
        return False, "Empty SQL query"
        
    try:
        try:
            # Try to transpile to impala directly
            transpiled = sqlglot.transpile(sql, write="impala", identify=True)
        except ValueError as e:
            if "Unknown dialect 'impala'" in str(e):
                # Fallback to hive which is closest to impala in sqlglot
                transpiled = sqlglot.transpile(sql, write="hive", identify=True)
            else:
                raise e

        if not transpiled:
             return False, "Failed to transpile SQL"
        
        # Join multiple statements if present
        fixed_sql = ";\n".join(transpiled)
        return True, fixed_sql
    except errors.ParseError as e:
        return False, f"SQL Parse Error: {str(e)}"
    except errors.SqlglotError as e:
        return False, f"SQL Error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected Error: {str(e)}"