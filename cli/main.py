import argparse
import asyncio
import sys
from sdk import TextToSQLEngine, SQLRequest, SQLResponse

async def execute_query(query: str, domain: str = None, stream: bool = False):
    engine = TextToSQLEngine()
    request = SQLRequest(query=query, data_domain=domain)
    
    print(f"Processing query: '{query}'")
    if domain:
        print(f"Domain: {domain}")
    print("-" * 40)
    
    if stream:
        async for output in engine.astream(request):
            if isinstance(output, SQLResponse):
                print("\n" + "=" * 40)
                print("Final Response:")
                print(f"Status: {output.status}")
                print(f"Message: {output.message}")
                if output.sql:
                    print(f"SQL:\n{output.sql}")
                print("=" * 40)
            else:
                for node_name, updates in output.items():
                    print(f"[Stream] Finished node: {node_name}")
    else:
        response = await engine.ainvoke(request)
        print("=" * 40)
        print("Final Response:")
        print(f"Status: {response.status}")
        print(f"Message: {response.message}")
        if response.sql:
            print(f"SQL:\n{response.sql}")
        print("=" * 40)

def run_cli():
    parser = argparse.ArgumentParser(description="Text-to-SQL CLI")
    parser.add_argument("query", type=str, help="The natural language query to translate to SQL")
    parser.add_argument("--domain", type=str, default=None, help="The specific data domain to target")
    parser.add_argument("--stream", action="store_true", help="Enable streaming progress updates")
    
    args = parser.parse_args()
    
    try:
        asyncio.run(execute_query(args.query, args.domain, args.stream))
    except KeyboardInterrupt:
        print("\nExecution interrupted by user.")
        sys.exit(1)

if __name__ == "__main__":
    run_cli()
