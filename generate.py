import os
import sys
import json
from openai import OpenAI

# Fetch the key from the runner's secure environment memory
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY environment variable is missing.", file=sys.stderr)
    sys.exit(1)

client = OpenAI(api_key=api_key)

def build_project():
    print("Generating workspace assets...")
    
    prompt = (
        "Generate a complete layout. Provide your output as a single valid JSON object "
        "containing exactly two keys: 'html' (content for index.html) and 'js' (content for script.js). "
        "Output raw JSON only without markdown wrapping."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a front-end generation engine that outputs web source assets in structured JSON format."},
                {"role": "user", "content": prompt}
            ]
        )
        
        data = json.loads(response.choices.message.content)
        
        # Write files directly to the directory
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(data.get("html", "<h1>Default Page</h1>"))
            
        with open("script.js", "w", encoding="utf-8") as f:
            f.write(data.get("js", "// Default Script"))
            
        print("Success: Web assets generated safely.")
        
    except Exception as e:
        print(f"Pipeline failure: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    build_project()
