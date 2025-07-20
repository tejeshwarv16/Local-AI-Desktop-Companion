# test_sdk.py

import asyncio
from graphrag_sdk.tool import run

async def main():
    print("Starting GraphRAG SDK test...")

    # 1. Define your input data
    documents = [
        {"id": "doc1", "text": "Hatsune Miku is a virtual singer from Japan."},
        {"id": "doc2", "text": "Miku's primary color is a distinct turquoise or cyan."},
        {"id": "doc3", "text": "A famous song performed by Miku is 'World is Mine'."},
    ]

    # 2. Run the pipeline using the simple SDK 'run' command
    # This will use our new .yml file for configuration by default.
    result = await run(documents, ".")

    # 3. Print the results
    # We can now see the extracted entities and relationships
    print("\n--- Extraction Results ---")
    print(result.output)
    print("\nGraphRAG SDK test completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())