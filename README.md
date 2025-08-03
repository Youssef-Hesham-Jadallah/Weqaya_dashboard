# Najran Public Health Authority Dashboard

## Overview
The *Najran Public Health Authority Dashboard* is an advanced, interactive web application developed using *Streamlit* and *Plotly* to provide comprehensive analytics and visualizations for public health performance at border crossings in Najran for the year 2025. The dashboard offers real-time insights into key health metrics, including traveler counts, pilgrim and hajj activities, clinic visits, emergency cases, vaccinations, and supervisory inspections. It supports data input, advanced analytics, and predictive modeling to aid decision-making.

## Features
- *Interactive Visualizations*: Includes bar charts, line charts, pie charts, heatmaps, and 3D scatter plots to visualize monthly and quarterly health data.
- *Data Input Forms*: Allows users to input and update data for Q3 and Q4 of 2025, with automatic calculations for total vaccinations and overall totals.
- *Real-Time Analytics*: Displays key performance indicators (KPIs), quarterly analysis, and predictive trends for travelers and clinic visits.
- *Custom Styling*: Utilizes a modern, glassmorphism-inspired design with Arabic fonts (Cairo and Amiri) and dynamic animations for an enhanced user experience.
- *Responsive Design*: Optimized for desktop and mobile devices with adaptive layouts and scrollable content.
- *Advanced Analytics*: Includes correlation heatmaps and predictive modeling with a 5% growth rate assumption for future projections.

## Technologies Used
- *Python*: Core programming language.
- *Streamlit*: Framework for building the interactive web application.
- *Plotly*: Used for creating dynamic and interactive charts.
- *Pandas*: For data manipulation and storage.
- *NumPy*: For numerical computations.
- *CSS*: Custom styles for a modern, visually appealing interface.
- *HTML*: Embedded in Streamlit for custom UI components.

## Installation
1. *Clone the Repository*:
   bash
   git clone https://github.com/your-repo/najran-health-dashboard.git
   cd najran-health-dashboard
   

2. *Install Dependencies*:
   Ensure you have Python 3.8+ installed, then run:
   bash
   pip install -r requirements.txt
   

3. *Requirements File*:
   Create a requirements.txt with the following:
   
   streamlit==1.25.0
   pandas==2.0.3
   numpy==1.24.3
   plotly==5.15.0
   

4. *Run the Application*:
   bash
   streamlit run dashboard.py
   

## Usage
1. *Access the Dashboard*: Open the application in a web browser (default: http://localhost:8501).
2. *Navigate Sections*:
   - *Main KPIs*: View total travelers, pilgrims, clinic visits, and emergency cases.
   - *Total Analysis*: Explore monthly and quarterly totals via bar and pie charts.
   - *Vaccination Analysis*: Analyze vaccination trends with line charts, pie charts, and heatmaps.
   - *Emergency & Clinic Visits*: Visualize clinic visits and emergency cases with combined bar and line charts.
   - *Quarterly Analysis*: Dive into detailed Q1 and Q2 data, and input data for Q3 and Q4.
   - *3D Gauges*: Monitor clinic efficiency, emergency response, vaccination rates, and inspection efficiency.
   - *Advanced Analytics*: Review correlation heatmaps and predictive trends for 2026.
3. *Data Input*: Use forms in Q3 and Q4 tabs to update health metrics, which are automatically saved to the session state.
4. *Export Options*: Download charts as PNG or export data as CSV for further analysis.

## Folder Structure

najran-health-dashboard/
├── dashboard.py          # Main Streamlit application script
├── requirements.txt      # Python dependencies
├── images/               # Folder for icons (e.g., R (1).png for favicon)
└── README.md             # This documentation file


## Data Structure
The dashboard uses a Pandas DataFrame (health_df) stored in the Streamlit session state with the following columns:
- الشهر (Month): Month names for 2025.
- عدد العابرين (Travelers): Number of border crossing travelers.
- عدد المعتمرين (Pilgrims): Number of Umrah pilgrims.
- عدد الحجاج (Hajj Pilgrims): Number of Hajj pilgrims.
- زيارات العيادة (Clinic Visits): Number of clinic visits.
- حالات النقل الإسعافي وحالات الإشتباه (Emergency Cases): Emergency and suspected cases.
- الجولات الإشرافية (Inspections): Number of supervisory inspections.
- شلل الأطفال (Polio): Polio vaccinations.
- مخية شوكية (Meningitis): Meningitis vaccinations.
- ثلاثي فيروسي (Triple Viral): Triple viral vaccinations.
- مجموع التطعيمات (Total Vaccinations): Sum of all vaccinations.
- المجموع الكلي (Grand Total): Sum of all metrics per month.

## Customization
- *Styling*: Modify the CSS in the st.markdown section to adjust colors, fonts, or animations.
- *Data*: Update the initial DataFrame in dashboard.py to include new metrics or time periods.
- *Visualizations*: Extend Plotly charts by adding new traces or modifying layouts in the respective sections.
- *Predictions*: Adjust the growth_rate variable in the predictions section for different forecasting scenarios.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -m "Add new feature").
4. Push to the branch (git push origin feature-branch).
5. Open a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For inquiries or support, contact the Najran Public Health Authority Analytics Team at [email@example.com].

---

Developed by the *Najran Public Health Authority Analytics Team*  
Last Updated: August 3, 2025


### Instructions to Save the File
To save this content as a `README.md` file:
1. **Manual Save**:
   - Copy the above Markdown content.
   - Create a new file named `README.md` in your project directory (e.g., `najran-health-dashboard/`).
   - Paste the content into the file and save it.

2. **Using Python** (if you prefer programmatically):
   python
   with open('README.md', 'w', encoding='utf-8') as f:
       f.write("""# Najran Public Health Authority Dashboard

## Overview
The *Najran Public Health Authority Dashboard* is an advanced, interactive web application developed using *Streamlit* and *Plotly* to provide comprehensive analytics and visualizations for public health performance at border crossings in Najran for the year 2025. The dashboard offers real-time insights into key health metrics, including traveler counts, pilgrim and hajj activities, clinic visits, emergency cases, vaccinations, and supervisory inspections. It supports data input, advanced analytics, and predictive modeling to aid decision-making.

## Features
- *Interactive Visualizations*: Includes bar charts, line charts, pie charts, heatmaps, and 3D scatter plots to visualize monthly and quarterly health data.
- *Data Input Forms*: Allows users to input and update data for Q3 and Q4 of 2025, with automatic calculations for total vaccinations and overall totals.
- *Real-Time Analytics*: Displays key performance indicators (KPIs), quarterly analysis, and predictive trends for travelers and clinic visits.
- *Custom Styling*: Utilizes a modern, glassmorphism-inspired design with Arabic fonts (Cairo and Amiri) and dynamic animations for an enhanced user experience.
- *Responsive Design*: Optimized for desktop and mobile devices with adaptive layouts and scrollable content.
- *Advanced Analytics*: Includes correlation heatmaps and predictive modeling with a 5% growth rate assumption for future projections.

## Technologies Used
- *Python*: Core programming language.
- *Streamlit*: Framework for building the interactive web application.
- *Plotly*: Used for creating dynamic and interactive charts.
- *Pandas*: For data manipulation and storage.
- *NumPy*: For numerical computations.
- *CSS*: Custom styles for a modern, visually appealing interface.
- *HTML*: Embedded in Streamlit for custom UI components.

## Installation
1. *Clone the Repository*:
   bash
   git clone https://github.com/your-repo/najran-health-dashboard.git
   cd najran-health-dashboard
   

2. *Install Dependencies*:
   Ensure you have Python 3.8+ installed, then run:
   bash
   pip install -r requirements.txt
   

3. *Requirements File*:
   Create a requirements.txt with the following:
   
   streamlit==1.25.0
   pandas==2.0.3
   numpy==1.24.3
   plotly==5.15.0
   

4. *Run the Application*:
   bash
   streamlit run dashboard.py
   

## Usage
1. *Access the Dashboard*: Open the application in a web browser (default: http://localhost:8501).
2. *Navigate Sections*:
   - *Main KPIs*: View total travelers, pilgrims, clinic visits, and emergency cases.
   - *Total Analysis*: Explore monthly and quarterly totals via bar and pie charts.
   - *Vaccination Analysis*: Analyze vaccination trends with line charts, pie charts, and heatmaps.
   - *Emergency & Clinic Visits*: Visualize clinic visits and emergency cases with combined bar and line charts.
   - *Quarterly Analysis*: Dive into detailed Q1 and Q2 data, and input data for Q3 and Q4.
   - *3D Gauges*: Monitor clinic efficiency, emergency response, vaccination rates, and inspection efficiency.
   - *Advanced Analytics*: Review correlation heatmaps and predictive trends for 2026.
3. *Data Input*: Use forms in Q3 and Q4 tabs to update health metrics, which are automatically saved to the session state.
4. *Export Options*: Download charts as PNG or export data as CSV for further analysis.

## Folder Structure

najran-health-dashboard/
├── dashboard.py          # Main Streamlit application script
├── requirements.txt      # Python dependencies
├── images/               # Folder for icons (e.g., R (1).png for favicon)
└── README.md             # This documentation file


## Data Structure
The dashboard uses a Pandas DataFrame (health_df) stored in the Streamlit session state with the following columns:
- الشهر (Month): Month names for 2025.
- عدد العابرين (Travelers): Number of border crossing travelers.
- عدد المعتمرين (Pilgrims): Number of Umrah pilgrims.
- عدد الحجاج (Hajj Pilgrims): Number of Hajj pilgrims.
- زيارات العيادة (Clinic Visits): Number of clinic visits.
- حالات النقل الإسعافي وحالات الإشتباه (Emergency Cases): Emergency and suspected cases.
- الجولات الإشرافية (Inspections): Number of supervisory inspections.
- شلل الأطفال (Polio): Polio vaccinations.
- مخية شوكية (Meningitis): Meningitis vaccinations.
- ثلاثي فيروسي (Triple Viral): Triple viral vaccinations.
- مجموع التطعيمات (Total Vaccinations): Sum of all vaccinations.
- المجموع الكلي (Grand Total): Sum of all metrics per month.

## Customization
- *Styling*: Modify the CSS in the st.markdown section to adjust colors, fonts, or animations.
- *Data*: Update the initial DataFrame in dashboard.py to include new metrics or time periods.
- *Visualizations*: Extend Plotly charts by adding new traces or modifying layouts in the respective sections.
- *Predictions*: Adjust the growth_rate variable in the predictions section for different forecasting scenarios.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -m "Add new feature").
4. Push to the branch (git push origin feature-branch).
5. Open a pull request with a detailed description of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For inquiries or support, contact the Najran Public Health Authority Analytics Team at [email@example.com].

---

Developed by the *Najran Public Health Authority Analytics Team*  
Last Updated: August 3, 2025
""")
   ```
   Run this Python code in your project directory to generate the README.md file.

### Notes
- The file is encoded in UTF-8 to support Arabic text correctly.
- If you meant a different format (e.g., HTML, JSON, or another structure), please specify the format or provide an example.
- If you want the file to be written to a specific directory or with additional content, let me know.
- The repository URL (https://github.com/your-repo/najran-health-dashboard.git) and contact email ([hgereino@gmail.com]) are placeholders. Replace them with actual values if needed.

Let me know if you need further assistance or a different approach!
