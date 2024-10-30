# CVE Analysis System

The **CVE Analysis System** is a web-based application designed for analyzing Common Vulnerabilities and Exposures (CVEs). This tool uses MongoDB to store CVE data, Groq for AI-powered vulnerability analysis, and Plotly for data visualization. It provides a dashboard with a CVSS score analysis, impact distributions, and a search interface to retrieve CVE-specific insights.

## Features

- **CVE Search**: Search for specific CVEs and analyze them with Groq's AI for vulnerability insights.
- **Dashboard Visualization**: Visualizations for CVSS scores and impact distribution based on Confidentiality, Integrity, and Availability.
- **Interactive UI**: User-friendly interface with navigation, filtering, and search capabilities.

## Flowchart

![Flowchart](https://github.com/user-attachments/assets/dd115cca-03e4-45da-a3ff-dbd124c884af)


## Prerequisites

- **Python 3.x**
- **MongoDB**: Set up a MongoDB database and collection to store CVE data.
- **Groq API Key**: Needed to interact with the Groq model for generating CVE analyses.
- **Environment Variables**:
  - `MONGO_URI`: MongoDB connection string.
  - `GROQ_API_KEY`: API key for accessing Groq's services.

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/d01mittal/NLP-Project.git
   cd NLP-Project
2. **Install Required Libraries**: Use `pip` to install the required dependencies.
   ```bash
   pip install -r requirements.txt
3. **Configure Environment Variables**:
   ```bash
   export MONGO_URI='your_mongodb_uri'
   export GROQ_API_KEY='your_groq_api_key'
4. **Database Setup**: Ensure your MongoDB collection (`NLP_project.CSV_data`) is populated with CVE data. The data is uploaded above and the google drive link of the data is here as well: https://drive.google.com/file/d/13m3C67nP-wUJcs2x-1NeQTj_G-9LSaCG/view?usp=drive_link. The required fields in the database include:
   ```bash
   export MONGO_URI='your_mongodb_uri'
   export GROQ_API_KEY='your_groq_api_key'
 - `id`
 - `description`
 - `cvssScore`
 - `publishedDate`
 - `affectedProduct`
 - `authenticationRequired`
 - `accessComplexity`
 - `confidentialityImpact`
 - `integrityImpact`
 - `availabilityImpact`

The data should be stored like this in MongoDB:
![DataBase photo](https://github.com/user-attachments/assets/81c9f23d-bc90-4ced-b193-b9bb104bb952)

5. **Run the Application**: Start the Flask server:
   ```bash
   flask run
  The application will be available at `http://127.0.0.1:5000`.

## Application Structure

- **app.py**: The main Flask application file with routes for CVE search, dashboard, and Groq analysis.
- **templates/**: Contains HTML templates for the dashboard and main page (`dashboard.html`, `index.html`).
- **static/**: Static files such as `styles.css` for custom styling.
- **MongoDB**: Used to store and query CVE data for analysis.

## Usage

1. **Navigate to the CVE Search Page**: Go to `http://127.0.0.1:5000/`.
   - Enter a CVE ID (e.g., `CVE-1999-0095`) and click Analyze CVE.
   - A Groq-powered analysis will be displayed, with details on severity and mitigation.
2. **Access the Dashboard**: Go to `http://127.0.0.1:5000/dashboard`.
   - Filter data by specifying CVE ID range.
   - View CVSS score distributions and impact breakdowns.

## Deployment

To deploy the application, configure the environment variables on your hosting platform and ensure MongoDB is accessible.

## Key Features

1. Access to comprehensive CVE data up to August 2024.
2. Integrated AI capabilities for smarter data insights.
3. Interactive data visualization with multiple plot types, allowing users to customize data ranges for a tailored view.

## Collaborators

- [d01mittal](https://github.com/d01mittal)
- [Karthic-Elangovan](https://github.com/Karthic-Elangovan)
- [Gangatharangurusamy](https://github.com/Gangatharangurusamy)
- [riyajadhav06](https://github.com/riyajadhav06)
- [soumyajitjalua1](https://github.com/soumyajitjalua1)
