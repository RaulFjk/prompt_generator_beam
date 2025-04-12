import requests
import json

def test_prompt_generation():
    url = "http://localhost:8000/generate_prompt"

    data = {
        "api_key": "HERE COMES THE KEY",
        "extraction_task": "Prompt that extracts total gross, total net, business name and a list of items including product name and price data as a JSON structure",
        "doc_type": None
    }

    print(f"Sending test request to {url} ...")
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)

    if response.status_code == 200:
        result = response.json()
        print("Response JSON:\n", json.dumps(result, indent=2))

        # Print the final prompt
        print("\nFinal Prompt:\n", result["final_prompt"])

        # Basic info
        print("\nIdentified Doc Type:", result["identified_doc_type"])
        print("Check Result:", result["check_result"])
        print("Check Reason:", result["check_reason"])

        # If there's an adjusted_prompt, let's also show it
        if "adjusted_prompt" in result and result["adjusted_prompt"] is not None:
            print("\nADJUSTED PROMPT:\n", result["adjusted_prompt"])
    else:
        print("Error response:", response.text)

if __name__ == "__main__":
    test_prompt_generation()
