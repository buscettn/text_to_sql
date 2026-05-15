import uuid
from typing import AsyncGenerator, Dict, Any
from core.interfaces import SQLRequest, SQLResponse
from graph.workflow import create_workflow

class TextToSQLEngine:
    def __init__(self):
        # Initialize the LangGraph app once
        self.app = create_workflow()

    async def ainvoke(self, request: SQLRequest) -> SQLResponse:
        """
        Single-turn execution. Waits for the workflow to complete and returns the final response.
        """
        thread_id = request.thread_id or str(uuid.uuid4())
        initial_state = {
            "messages": [{"role": "user", "content": request.query}],
            "requested_domain": request.data_domain,
            "data_domain": {},
            "schema_context": [],
            "few_shot_context": [],
            "grounding_context": [],
            "generated_sql": None,
            "validation_errors": None,
            "generation_attempts": 0,
            "status": "pending",
            "agent_message": None
        }
        config = {"configurable": {"thread_id": thread_id}}
        
        # Invoke the workflow
        final_state = await self.app.ainvoke(initial_state, config=config)
        
        # Concatenate domain names for the final response
        data_domain_scores = final_state.get("data_domain") or {}
        concatenated_domains = ", ".join(data_domain_scores.keys()) if data_domain_scores else None

        return SQLResponse(
            sql=final_state.get("generated_sql"),
            message=final_state.get("agent_message", "No response generated."),
            status=final_state.get("status", "error"),
            data_domain=concatenated_domains,
            thread_id=thread_id
        )

    async def astream(self, request: SQLRequest) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Streaming execution. Yields status updates for the UI/CLI, and finally yields the SQLResponse.
        """
        thread_id = request.thread_id or str(uuid.uuid4())
        initial_state = {
            "messages": [{"role": "user", "content": request.query}],
            "requested_domain": request.data_domain,
            "data_domain": {},
            "schema_context": [],
            "few_shot_context": [],
            "grounding_context": [],
            "generated_sql": None,
            "validation_errors": None,
            "generation_attempts": 0,
            "status": "pending",
            "agent_message": None
        }
        config = {"configurable": {"thread_id": thread_id}}
        
        final_state = initial_state.copy()
        
        # Stream the workflow output
        async for output in self.app.astream(initial_state, config=config, stream_mode="updates"):
            # Update final_state with the latest updates from the node
            for node_name, updates in output.items():
                if isinstance(updates, dict):
                    # We only need to track the fields that are used in the SQLResponse.
                    # Since these fields don't have custom LangGraph reducers, 
                    # a simple dict.update is sufficient.
                    final_state.update(updates)
            
            yield output
            
        # Concatenate domain names for the final response
        data_domain_scores = final_state.get("data_domain") or {}
        concatenated_domains = ", ".join(data_domain_scores.keys()) if data_domain_scores else None

        yield SQLResponse(
            sql=final_state.get("generated_sql"),
            message=final_state.get("agent_message", "No response generated."),
            status=final_state.get("status", "error"),
            data_domain=concatenated_domains,
            thread_id=thread_id
        )
