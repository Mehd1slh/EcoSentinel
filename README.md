<div align="center">
  <img src="Platform/EcoS/static/EcoS_vertical.png" alt="EcoSentinel Logo" width="300"/>
  <h1>EcoSentinel AI</h1>
  <p><em>Smart Pollution and Carbon Response Orchestrator</em></p>
</div>

##  Overview
EcoSentinel is an AI-powered environmental alert system that combines satellite imagery analysis with citizen participation and automated workflows to detect urban waste accumulation and water pollution. It enables real-time monitoring and response through AI classification, risk scoring, and stakeholder alerting.

##  The Problem
Local governments and communities often lack the real-time intelligence and automation needed to respond to environmental threats. EcoSentinel bridges that gap by leveraging AI and automation to **Dépolluer, Décarboner, and Régénérer** our cities.

##  Key Features
- **Real-Time Monitoring:** Detects trash buildup in urban zones (e.g., Sala Al Jadida) using Sentinel-2 imagery.
- **Water Quality Analysis:** Analyzes the Oued Abou Regreg river (Rabat to Salé) using NDWI, NDMI, SWIR, and true color composites to estimate pollution levels.
- **Citizen Participation:** Allows citizens to submit geo-tagged incident reports via web and mobile platforms.
- **Smart Alerts:** Automatically alerts stakeholders (e.g., Ridal company) with cleanup requests based on severity thresholds.
- **Interactive Dashboard:** Offers a comprehensive dashboard featuring alerts, citizen submissions, severity filters, and exportable summaries.
- **Hybrid Intelligence:** Merges human reports with AI vision for a highly accurate and tiered alert system to manage resources efficiently.

##  AI Capabilities
EcoSentinel heavily relies on state-of-the-art AI models:
- **Image Classification:** Hugging Face Vision models detect illegal dumps, deforestation, and water pollution from drone and satellite images.
- **Text Summarization:** OpenAI GPT-4 summarizes large environmental reports and pollution alerts.
- **Named Entity Recognition (NER) & Sentiment Analysis:** Extracts relevant locations, pollutants, and analyzes public feedback from citizen-submitted reports.
- **Risk Scoring:** Custom algorithms classify incidents into low, medium, or high urgency cases.

##  Tech Stack
- **Frontend:** Angular, Tailwind CSS (also compatible with React/Vue.js)
- **Backend:** Flask (Python)
- **AI Orchestration:** n8n
- **AI Models:** Hugging Face (Transformers), OpenAI (GPT-4)
- **Data Sources:** Sentinel-2 API, Google Earth Engine, Google Maps, OpenAQ, MeteoBlue, Drone/Camera imagery
- **Database:** PostgreSQL
- **Hosting & Deployment:** Render, Vercel, Docker

##  Automated Workflow
EcoSentinel uses **n8n** to orchestrate the entire process:
1. **Trigger:** Scheduled pipeline runs every 6 hours.
2. **API Integration:** Fetches pollution data (OpenAQ) and recent satellite images.
3. **AI Processing:** Classifies environmental damage using Hugging Face and generates summaries/recommendations via GPT-4.
4. **Action:** If pollution levels exceed thresholds, the system updates the live map, emails stakeholders, logs to the database, and dispatches SMS/Telegram alerts.

##  Impact
EcoSentinel provides a scalable civic tech solution for smart cities, championing a participatory governance model. It empowers municipalities with a real-time dashboard and automated interventions, ensuring a sustainable and rapid response to environmental hazards.
