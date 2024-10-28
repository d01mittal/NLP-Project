from flask import Flask, request, jsonify, render_template
from plotly.utils import PlotlyJSONEncoder 
from pymongo import MongoClient
import plotly.express as px
from groq import Groq
import pandas as pd
import plotly
import json
import os

# Initialize Flask app
app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

# MongoDB connection setup
mongo_uri = os.getenv("MONGO_URI")
try:
    # Connect to MongoDB using the URI from the environment
    client = MongoClient(mongo_uri)
    db = client["NLP_project"]
    collection = db["CSV_data"]
    print("MongoDB connection successful.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Initialize Groq client
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

groq_client = Groq(api_key=GROQ_API_KEY)

def fetch_data_from_mongodb(data_id):
    try:
        data = collection.find_one({"id": data_id})
        if data:
            data['_id'] = str(data['_id'])
            return data
        return None
    except Exception as e:
        print(f"Database Error: {e}")
        return None

def generate_groq_response(data):
    try:
        prompt = f"""As a cybersecurity expert, analyze this CVE (Common Vulnerabilities and Exposures) data:

CVE ID: {data['id']}
Description: {data['description']}
CVSS Score: {data['cvssScore']}
Published: {data['publishedDate']}
Product: {data['affectedProduct']}

Security Details:
- Authentication Required: {data['authenticationRequired']}
- Access Complexity: {data['accessComplexity']}
- Confidentiality Impact: {data['confidentialityImpact']}
- Integrity Impact: {data['integrityImpact']}
- Availability Impact: {data['availabilityImpact']}

Provide a detailed analysis with the following sections:

# Vulnerability Summary
# Technical Impact Analysis
# Exploitation Potential
# Mitigation Steps
# Risk Assessment
"""

        # Make request to Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert analyzing CVE data."},
                {"role": "user", "content": prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=4096,
            top_p=0.95
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Groq API Error: {e}")
        return f"Error generating response: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Get filter parameters from query string
    start = int(request.args.get('start', 0))
    end = int(request.args.get('end', 1000))

    # Fetch data from MongoDB based on the range
    cve_data = list(collection.find().skip(start).limit(end - start))
    df = pd.DataFrame(cve_data)

    # Generate CVSS Score bar chart
    fig_bar = px.bar(df, x="id", y="cvssScore", title="CVSS Scores for CVE IDs",
                     color="cvssScore", labels={"id": "CVE ID", "cvssScore": "CVSS Score"}, height=400)
    
    # Generate impact distribution data
    impact_data = pd.DataFrame({
        "Impact": ["Confidentiality", "Integrity", "Availability"],
        "Complete": [
            sum(df['confidentialityImpact'] == "Complete"),
            sum(df['integrityImpact'] == "Complete"),
            sum(df['availabilityImpact'] == "Complete")
        ],
        "Partial": [
            sum(df['confidentialityImpact'] == "Partial"),
            sum(df['integrityImpact'] == "Partial"),
            sum(df['availabilityImpact'] == "Partial")
        ],
        "None": [
            sum(df['confidentialityImpact'] == "None"),
            sum(df['integrityImpact'] == "None"),
            sum(df['availabilityImpact'] == "None")
        ]
    })

    # Create three separate pie charts
    fig_pie_complete = px.pie(impact_data, names="Impact", values="Complete", 
                             title="Complete Impact Distribution",
                             color_discrete_sequence=px.colors.sequential.Magenta)
    fig_pie_partial = px.pie(impact_data, names="Impact", values="Partial", 
                             title="Partial Impact Distribution",
                             color_discrete_sequence=px.colors.sequential.turbid)
    fig_pie_none = px.pie(impact_data, names="Impact", values="None", 
                         title="None Impact Distribution",
                         color_discrete_sequence=px.colors.sequential.RdBu)

    # Convert all charts to JSON
    charts_json = {
        'bar_chart': json.dumps(fig_bar.to_dict(), cls=plotly.utils.PlotlyJSONEncoder),
        'pie_chart_complete': json.dumps(fig_pie_complete.to_dict(), cls=plotly.utils.PlotlyJSONEncoder),
        'pie_chart_partial': json.dumps(fig_pie_partial.to_dict(), cls=plotly.utils.PlotlyJSONEncoder),
        'pie_chart_none': json.dumps(fig_pie_none.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)
    }

    return render_template('dashboard.html', **charts_json)



@app.route('/generate-response', methods=['POST'])
def generate_response_endpoint():
    try:
        data = request.get_json()
        data_id = data.get('id')

        if not data_id:
            return jsonify({"error": "ID is required"}), 400

        cve_data = fetch_data_from_mongodb(data_id)
        if not cve_data:
            return jsonify({"error": "CVE not found"}), 404

        response = generate_groq_response(cve_data)
        return jsonify({"response": response, "cve_data": cve_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
