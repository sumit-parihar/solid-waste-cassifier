import ollama

def analyze_waste(image_path):
    prompt = """
    You are an AI system for Smart Waste Management.

    Analyze the uploaded waste image and produce a professional report.

    Return the output in the following **Markdown format**.

    # 🧠 Smart Waste Analysis Report

    ### 🔍 Detected Item
    Provide the name of the waste item detected.

    ### ♻ Context-Aware Waste Classification
    Explain which waste category it belongs to:
    - Organic
    - Recyclable
    - Hazardous
    - E-Waste
    - Landfill

    ### 🧾 AI Explanation Layer
    Explain how the AI identified the object using visible characteristics.

    ### 🌍 Environmental Impact Feedback
    Explain the environmental impact if disposed incorrectly.

    ### 🔋 Energy Recovery Potential
    Explain if the waste can be converted to energy or reused.

    Make the explanation **clear, concise, and professional**.
    Only return the formatted report.
    """

    response = ollama.chat(
        model='minicpm-v',
        messages=[
            {
                'role': 'user',
                'content': prompt,
                'images': [image_path]
            }
        ],
        options={
            "num_predict": 150
        }
    )

    return response['message']['content']