# test_graphrag.py

import asyncio

# Corrected: Import everything directly from the top-level sdk
from graphrag_sdk import PipelineWorkflowConfig, PipelineWorkflowStep, run_pipeline_with_config


async def main():
    """
    A simple test script to demonstrate GraphRAG functionality.
    """
    print("Starting GraphRAG test...")

    # 1. Define a simple configuration for the indexing pipeline
    # This part of the code remains the same
    config = PipelineWorkflowConfig(
        workflow=[
            PipelineWorkflowStep(
                verb="index",
                args={
                    "storage_type": "memory", # Use in-memory storage for this test
                    "graph_name": "miku_test_graph",
                    "document_collection": "miku_docs",
                    "extraction": {
                        "strategy": {
                            "type": "graph_intelligence",
                            "llm": {
                                "type": "static_response", # Use a fake LLM for speed
                                "response": "()" # A dummy response
                            }
                        }
                    }
                },
            )
        ]
    )
    
    # 2. Define your input data
    documents = [
        {"id": 1, "text": "Hatsune Miku is a virtual singer."},
        {"id": 2, "text": "Miku's signature color is turquoise."},
        {"id": 3, "text": "Her most famous song is 'World is Mine'."},
    ]

    # 3. Run the indexing pipeline
    print("Building knowledge graph from documents...")
    result = await run_pipeline_with_config(config, documents=documents)
    
    if result.is_success():
        print("Knowledge graph built successfully!")
        
    else:
        print("Failed to build knowledge graph.")
        print("Error:", result.errors)


if __name__ == "__main__":
    asyncio.run(main())