import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from sklearn.cluster import KMeans

st.set_page_config(layout="wide", page_title="لوحة معلومات هيئة الصحة العامة بنجران", page_icon="images/R (1).png")

# Initialize session state for health data if not already set
if 'health_df' not in st.session_state:
    st.session_state.health_df = pd.DataFrame({
        'الشهر': ['يناير 2025', 'فبراير 2025', 'مارس 2025', 'أبريل 2025', 'مايو 2025', 'يونيو 2025',
                  'يوليو 2025', 'أغسطس 2025', 'سبتمبر 2025', 'أكتوبر 2025', 'نوفمبر 2025', 'ديسمبر 2025'],
        'عدد العابرين الوديعة': [181780, 197288, 160940, 103974, 83564, 101927, 152316, 28219, 0, 0, 0, 0],
        'عدد العابرين الخضراء': [766, 671, 722, 744, 780, 674, 761, 115, 0, 0, 0, 0],
        'عدد العابرين المطار': [3180, 2723, 1629, 1956, 2329, 2215, 3144, 625, 0, 0, 0, 0],
        'عدد العابرين': [185726, 200682, 163291, 106674, 86673, 104816, 156221, 28959, 0, 0, 0, 0],
        'عدد المعتمرين': [88806, 120930, 96027, 4316, 0, 17697, 49127, 12116, 0, 0, 0, 0],
        'عدد الحجاج': [0, 0, 0, 0, 12951, 0, 0, 0, 0, 0, 0, 0],
        'عيادة الطبيب الوديعة': [877, 664, 468, 573, 565, 549, 747, 130, 0, 0, 0, 0],
        'عيادة الطبيب المطار': [1613, 1465, 1172, 789, 658, 466, 501, 91, 0, 0, 0, 0],
        'زيارات العيادة': [2490, 2129, 1640, 1362, 1223, 1015, 1248, 221, 0, 0, 0, 0],
        'النقل الإسعافي المطار': [1, 2, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0],
        'النقل الإسعافي الوديعة': [6, 6, 2, 4, 14, 10, 7, 6, 0, 0, 0, 0],
        'حالات النقل الإسعافي': [7, 8, 3, 5, 16, 11, 8, 6, 0, 0, 0, 0],
        'حالات الإشتباه': [0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0],
        'الجولات الإشرافية': [2, 3, 2, 1, 2, 2, 2, 2, 0, 0, 0, 0],
        'شلل الأطفال': [57838, 63979, 37725, 28915, 36680, 38330, 68770, 14600, 0, 0, 0, 0],
        'مخية شوكية': [34487, 29023, 19789, 18200, 17078, 20135, 13733, 2285, 0, 0, 0, 0],
        'ثلاثي فيروسي': [12405, 16854, 10371, 6355, 8389, 4280, 5634, 1672, 0, 0, 0, 0],
        'مجموع التطعيمات': [104730, 109856, 67885, 53470, 62147, 62745, 88137, 18557, 0, 0, 0, 0],
        'المجموع الكلي': [674714, 746283, 561667, 327339, 313071, 354873, 540359, 107606, 0, 0, 0, 0]
    })

# Add combined column for emergency and suspicion cases
st.session_state.health_df['حالات النقل الإسعافي وحالات الإشتباه'] = st.session_state.health_df['حالات النقل الإسعافي'] + st.session_state.health_df['حالات الإشتباه']

# Initialize session state for auto-refresh settings
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'refresh_rate' not in st.session_state:
    st.session_state.refresh_rate = 30

# Define default analysis settings
analysis_type = "شامل"
time_period = "جميع الأشهر"
viz_type = ["خطي", "أعمدة", "دائري"]
show_predictions = True
show_correlations = True
show_clusters = False

# Function to update quarterly data in the DataFrame
def update_quarter_data(quarter, index, new_data):
    st.session_state.health_df.at[index, 'عدد العابرين الوديعة'] = new_data['عدد العابرين الوديعة']
    st.session_state.health_df.at[index, 'عدد العابرين الخضراء'] = new_data['عدد العابرين الخضراء']
    st.session_state.health_df.at[index, 'عدد العابرين المطار'] = new_data['عدد العابرين المطار']
    st.session_state.health_df.at[index, 'عدد العابرين'] = new_data['عدد العابرين']
    st.session_state.health_df.at[index, 'عدد المعتمرين'] = new_data['عدد المعتمرين']
    st.session_state.health_df.at[index, 'عدد الحجاج'] = new_data['عدد الحجاج']
    st.session_state.health_df.at[index, 'عيادة الطبيب الوديعة'] = new_data['عيادة الطبيب الوديعة']
    st.session_state.health_df.at[index, 'عيادة الطبيب المطار'] = new_data['عيادة الطبيب المطار']
    st.session_state.health_df.at[index, 'زيارات العيادة'] = new_data['زيارات العيادة']
    st.session_state.health_df.at[index, 'النقل الإسعافي المطار'] = new_data['النقل الإسعافي المطار']
    st.session_state.health_df.at[index, 'النقل الإسعافي الوديعة'] = new_data['النقل الإسعافي الوديعة']
    st.session_state.health_df.at[index, 'حالات النقل الإسعافي'] = new_data['حالات النقل الإسعافي']
    st.session_state.health_df.at[index, 'حالات الإشتباه'] = new_data['حالات الإشتباه']
    st.session_state.health_df.at[index, 'الجولات الإشرافية'] = new_data['الجولات الإشرافية']
    st.session_state.health_df.at[index, 'شلل الأطفال'] = new_data['شلل الأطفال']
    st.session_state.health_df.at[index, 'مخية شوكية'] = new_data['مخية شوكية']
    st.session_state.health_df.at[index, 'ثلاثي فيروسي'] = new_data['ثلاثي فيروسي']
    total_vaccinations = new_data['شلل الأطفال'] + new_data['مخية شوكية'] + new_data['ثلاثي فيروسي']
    st.session_state.health_df.at[index, 'مجموع التطعيمات'] = total_vaccinations
    st.session_state.health_df.at[index, 'المجموع الكلي'] = (
        new_data['عدد العابرين'] + new_data['عدد المعتمرين'] + new_data['عدد الحجاج'] +
        new_data['زيارات العيادة'] + new_data['حالات النقل الإسعافي'] + new_data['حالات الإشتباه'] +
        new_data['الجولات الإشرافية'] + total_vaccinations
    )
    # Update combined column
    st.session_state.health_df.at[index, 'حالات النقل الإسعافي وحالات الإشتباه'] = new_data['حالات النقل الإسعافي'] + new_data['حالات الإشتباه']

# Custom CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@200;300;400;600;700;800&family=Amiri:wght@400;700&display=swap');
:root {
    --primary-gradient: linear-gradient(135deg, #22577A 0%, #38A3A5 100%);
    --secondary-gradient: linear-gradient(135deg, #57CC99 0%, #80ED99 100%);
    --tertiary-gradient: linear-gradient(135deg, #2794EB 0%, #BFF8D4 100%);
    --success-gradient: linear-gradient(135deg, #80ED99 0%, #BFF8D4 100%);
    --warning-gradient: linear-gradient(135deg, #57CC99 0%, #80ED99 100%);
    --danger-gradient: linear-gradient(135deg, #22577A 0%, #38A3A5 100%);
    --glass-bg: rgba(255, 255, 255, 0.05);
    --glass-border: rgba(255, 255, 255, 0.1);
    --dark-glass: rgba(0, 0, 0, 0.5);
    --shadow-glow: 0 8px 32px rgba(34, 87, 122, 0.37);
    --shadow-premium: 0 15px 35px rgba(0, 0, 0, 0.4);
    --text-primary: #BFF8D4;
    --text-secondary: rgba(255, 255, 255, 0.7);
    --text-accent: #80ED99;
    --radius-lg: 16px;
    --radius-md: 12px;
    --radius-sm: 8px;
    --transition-main: all 0.3s ease;
}
.stApp {
    background: 
        radial-gradient(circle at 20% 80%, #22577A 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, #38A3A5 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, #57CC99 0%, transparent 50%),
        linear-gradient(135deg, #0A0A0A 0%, #121212 50%, #1C2526 100%);
    background-size: 400% 400%;
    animation: backgroundShift 20s ease infinite;
    color: var(--text-primary);
    font-family: 'Cairo', sans-serif;
    direction: rtl;
    min-height: 100vh;
    padding: 0 !important;
    margin: 0 !important;
}
@keyframes backgroundShift {
    0%, 100% { background-position: 0% 50%; }
    33% { background-position: 100% 0%; }
    66% { background-position: 100% 100%; }
}
.main-header {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: 2rem 1rem;
    margin: 1rem 0;
    text-align: center;
    box-shadow: var(--shadow-glow);
    position: relative;
    overflow: hidden;
    animation: headerFloat 6s ease-in-out infinite;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.05), transparent);
    animation: shimmer 3s linear infinite;
}
@keyframes headerFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
@keyframes shimmer {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}
.metric-card {
    background: var(--glass-bg);
    backdrop-filter: blur(15px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-md);
    padding: 1rem;
    margin: 0.5rem 0;
    min-height: 180px;
    text-align: center;
    box-shadow: var(--shadow-glow);
    transition: var(--transition-main);
    position: relative;
    animation: cardSlideIn 0.8s ease-out;
}
.metric-card:hover {
    transform: translateY(-15px) scale(1.02);
    box-shadow: 0 20px 40px rgba(34, 87, 122, 0.5);
    border-color: var(--text-accent);
}
.metric-card.updated {
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0% { box-shadow: var(--shadow-glow); }
    50% { box-shadow: 0 0 20px rgba(128, 237, 153, 0.8); }
    100% { box-shadow: var(--shadow-glow); }
}
.metric-value {
    font-size: 2.5rem;
    font-weight: 800;
    background: var(--secondary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    animation: valueCount 2s ease-out;
}
.metric-label {
    font-size: 1.3rem;
    color: var(--text-secondary);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.metric-status {
    font-size: 0.9rem;
    padding: 0.4rem 1rem;
    border-radius: var(--radius-sm);
    display: inline-block;
}
.insight-badge, .warning-badge, .danger-badge {
    margin: 0.25rem;
    border-radius: var(--radius-sm);
    font-size: 0.9rem;
    padding: 0.4rem 1rem;
    font-weight: 600;
    transition: var(--transition-main);
}
.insight-badge { background: var(--success-gradient); color: #0A0A0A; }
.warning-badge { background: var(--warning-gradient); color: #0A0A0A; }
.danger-badge { background: var(--danger-gradient); color: #0A0A0A; }
.insight-badge:hover, .warning-badge:hover, .danger-badge:hover {
    transform: scale(1.1);
}
.chart-title {
    color: var(--text-primary);
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 1rem;
    text-align: center;
    border-bottom: 2px solid var(--text-accent);
    padding-bottom: 0.5rem;
}
.analysis-card {
    background: var(--dark-glass);
    backdrop-filter: blur(10px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-md);
    padding: 1rem;
    margin: 0.5rem 0;
    border-right: 4px solid var(--text-accent);
    box-shadow: var(--shadow-premium);
    animation: fadeInLeft 0.8s ease-out;
    min-height: 220px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.analysis-title {
    font-size: 1.2rem;
    color: var(--text-accent);
    font-weight: 600;
}
.analysis-text {
    font-size: 1.1rem;
    color: var(--text-secondary);
    line-height: 1.6;
    flex-grow: 1;
    max-height: 100px;
    overflow-y: auto;
}
.stButton > button {
    background: var(--primary-gradient);
    color: #0A0A0A;
    border: none;
    border-radius: var(--radius-md);
    padding: 0.8rem 1.5rem;
    font-weight: 600;
    transition: var(--transition-main);
    box-shadow: var(--shadow-premium);
}
.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 30px rgba(34, 87, 122, 0.4);
}
.section-divider {
    height: 2px;
    background: var(--primary-gradient);
    border: none;
    margin: 1rem 0;
    animation: dividerGlow 3s ease-in-out infinite;
}
.stTabs [data-baseweb="tab"] {
    background-color: #1C2526;
    color: var(--text-secondary);
    border: none;
    padding: 10px 20px;
    margin: 0 5px;
    border-radius: var(--radius-md);
    transition: all 0.3s ease;
    text-decoration: none;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #80ED99;
    color: #0A0A0A;
    font-weight: 600;
    box-shadow: var(--shadow-glow);
    border: none;
    outline: none;
    text-decoration: none;
}
.stTabs [data-baseweb="tab-list"] {
    border-bottom: none;
}
.stTabs [data-baseweb="tab-panel"] {
    border: none;
}
@keyframes dividerGlow {
    0%, 100% { box-shadow: 0 0 5px rgba(34, 87, 122, 0.5); }
    50% { box-shadow: 0 0 20px rgba(34, 87, 122, 0.8); }
}
@keyframes cardSlideIn {
    from { transform: translateY(50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
@keyframes fadeInLeft {
    from { transform: translateX(-30px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
@keyframes valueCount {
    from { transform: scale(0); }
    to { transform: scale(1); }
}
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: var(--dark-glass);
    border-radius: var(--radius-sm);
}
::-webkit-scrollbar-thumb {
    background: var(--primary-gradient);
    border-radius: var(--radius-sm);
}
::-webkit-scrollbar-thumb:hover {
    background: var(--secondary-gradient);
}
.gauge-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 0.001rem;
}
.gauge-container .plotly {
    max-height: 300px;
    transition: var(--transition-main);
}
.gauge-container:hover .plotly {
    transform: scale(1.05);
}
@media (max-width: 768px) {
    .main-header, .chart-container, .metric-card, .analysis-card {
        padding: 0.8rem;
        margin: 0.8rem 0;
    }
    .metric-value { font-size: 2rem; }
    .metric-label { font-size: 1.1rem; }
    .analysis-text { font-size: 0.95rem; max-height: 80px; }
    .gauge-container .plotly { max-height: 200px; }
}
@media (max-width: 480px) {
    .metric-value { font-size: 1.8rem; }
    .insight-badge, .warning-badge, .danger-badge {
        font-size: 0.8rem;
        padding: 0.3rem 0.8rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3rem; font-weight: 800; color: white;">
         وقاية
    </h1>
    <h5 style="font-size: 3rem; font-weight: 800; color: white;">
         لوحة معلومات هيئة الصحة العامة بمنطقة نجران
    </h5>
    <p style="font-size: 1.5rem; color: var(--text-secondary);">
        تحليلات متقدمة للأداء الصحي في المنافذ - 2025
    </p>
</div>
""", unsafe_allow_html=True)

# Floating stats
st.markdown(f"""
<div class="floating-stats" style="position: fixed; top: 100px; right: 20px; background: var(--glass-bg); backdrop-filter: blur(15px); border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 1.5rem; box-shadow: var(--shadow-glow); z-index: 1000; animation: floatUpDown 4s ease-in-out infinite; font-size: 1rem; color: var(--text-secondary);">
     إحصائيات سريعة<br>
     المجموع الكلي: {st.session_state.health_df['المجموع الكلي'].sum():,}<br>
     التطعيمات: {st.session_state.health_df['مجموع التطعيمات'].sum():,}<br>
     العابرين: {st.session_state.health_df['عدد العابرين'].sum():,}<br>
     العابرين الوديعة: {st.session_state.health_df['عدد العابرين الوديعة'].sum():,}<br>
     العابرين الخضراء: {st.session_state.health_df['عدد العابرين الخضراء'].sum():,}<br>
     العابرين المطار: {st.session_state.health_df['عدد العابرين المطار'].sum():,}
</div>
<style>
@keyframes floatUpDown {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-10px); }}
}}
</style>
""", unsafe_allow_html=True)

# Analysis settings
filtered_df = st.session_state.health_df
if time_period != "جميع الأشهر":
    if time_period == "الربع الأول":
        filtered_df = st.session_state.health_df.iloc[0:3]
    elif time_period == "الربع الثاني":
        filtered_df = st.session_state.health_df.iloc[3:6]
    elif time_period == "الربع الثالث":
        filtered_df = st.session_state.health_df.iloc[6:9]
    elif time_period == "الربع الرابع":
        filtered_df = st.session_state.health_df.iloc[9:12]
    elif time_period == "شهر واحد":
        month = st.selectbox("اختر الشهر:", st.session_state.health_df['الشهر'].unique())
        filtered_df = st.session_state.health_df[st.session_state.health_df['الشهر'] == month]

# Display analysis type
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> المؤشرات الرئيسية</div>', unsafe_allow_html=True)

# Create columns for key metrics
col1, col2, col3, col4 = st.columns(4)

# Displaying key metrics
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df['عدد العابرين'].sum():,}</div>
        <div class="metric-label">إجمالي العابرين</div>
        <div class="metric-status insight-badge">مستقر</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df['عدد المعتمرين'].sum() + filtered_df['عدد الحجاج'].sum():,}</div>
        <div class="metric-label">إجمالي المعتمرين والحجاج</div>
        <div class="metric-status warning-badge">موسمي</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df['زيارات العيادة'].sum():,}</div>
        <div class="metric-label">زيارات العيادة</div>
        <div class="metric-status insight-badge">مستقر</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df['حالات النقل الإسعافي'].sum():,}</div>
        <div class="metric-label">حالات الطوارئ</div>
        <div class="metric-status danger-badge">يحتاج متابعة</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Displaying total monthly sum
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> تحليل المجموع الكلي</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> المجموع الكلي لكل شهر</h4>', unsafe_allow_html=True)
    fig_total_monthly = go.Figure()
    fig_total_monthly.add_trace(go.Bar(
        x=filtered_df['الشهر'],
        y=filtered_df['المجموع الكلي'],
        name='المجموع الكلي',
        marker_color='#1A3D5C',
        text=filtered_df['المجموع الكلي'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
        textposition='auto',
        hovertemplate='الشهر: %{x}<br>المجموع الكلي: %{y:,}<extra></extra>'
    ))
    fig_total_monthly.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        yaxis_title='المجموع الكلي',
        height=600,
        transition={'duration': 1000, 'easing': 'cubic-in-out'}
    )
    st.plotly_chart(fig_total_monthly, use_container_width=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

with col2:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> المجموع الكلي لكل ربع</h4>', unsafe_allow_html=True)
    quarters_data = {
        'الربع': ['الربع الأول', 'الربع الثاني', 'الربع الثالث', 'الربع الرابع'],
        'المجموع الكلي': [
            st.session_state.health_df.iloc[0:3]['المجموع الكلي'].sum(),
            st.session_state.health_df.iloc[3:6]['المجموع الكلي'].sum(),
            st.session_state.health_df.iloc[6:9]['المجموع الكلي'].sum(),
            st.session_state.health_df.iloc[9:12]['المجموع الكلي'].sum()
        ]
    }
    quarters_data['المجموع الكلي'] = [max(1, val) for val in quarters_data['المجموع الكلي']]
    fig_total_quarterly = go.Figure(data=[go.Pie(
        labels=quarters_data['الربع'],
        values=quarters_data['المجموع الكلي'],
        hole=0.4,
        textinfo='percent+label',
        textfont_size=14,
        marker=dict(
            colors=['#22577A', '#38A3A5', '#57CC99', '#80ED99'],
            line=dict(color='#0A0A0A', width=2)
        ),
        hovertemplate='الربع: %{label}<br>المجموع الكلي: %{value:,}<br>النسبة: %{percent}<extra></extra>',
        pull=[0.1, 0, 0, 0]
    )])
    fig_total_quarterly.add_annotation(
        text=f"إجمالي<br>{sum(quarters_data['المجموع الكلي']):,}",
        x=0.5, y=0.5,
        font_size=18,
        font_color='var(--text-primary)',
        showarrow=False
    )
    fig_total_quarterly.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=600
    )
    st.plotly_chart(fig_total_quarterly, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# تحليل التطعيمات
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> تحليل التطعيمات</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> اتجاهات التطعيمات</h4>', unsafe_allow_html=True)
    filtered_vacc_df = filtered_df[filtered_df['شلل الأطفال'].notnull()]
    fig_vacc_trend = make_subplots(specs=[[{"secondary_y": True}]])
    fig_vacc_trend.add_trace(
        go.Scatter(
            x=filtered_vacc_df['الشهر'], 
            y=filtered_vacc_df['شلل الأطفال'],
            mode='lines+markers',
            name='شلل الأطفال',
            line=dict(color='#22577A', width=4),
            marker=dict(size=12),
            fill='tonexty',
            text=filtered_vacc_df['شلل الأطفال'].apply(lambda x: f'{x:,}'),
            textposition='top center'
        ),
        secondary_y=False,
    )
    fig_vacc_trend.add_trace(
        go.Scatter(
            x=filtered_vacc_df['الشهر'], 
            y=filtered_vacc_df['مخية شوكية'],
            mode='lines+markers',
            name='مخية شوكية',
            line=dict(color='#38A3A5', width=4),
            marker=dict(size=12),
            text=filtered_vacc_df['مخية شوكية'].apply(lambda x: f'{x:,}'),
            textposition='bottom center'
        ),
        secondary_y=True,
    )
    fig_vacc_trend.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        showlegend=True,
        height=600,
        transition={'duration': 1000, 'easing': 'cubic-in-out'}
    )
    fig_vacc_trend.update_yaxes(title_text="شلل الأطفال", secondary_y=False, title_font_color='var(--text-primary)')
    fig_vacc_trend.update_yaxes(title_text="مخية شوكية", secondary_y=True, title_font_color='var(--text-primary)')
    st.plotly_chart(fig_vacc_trend, use_container_width=True)

with col2:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> توزيع التطعيمات</h4>', unsafe_allow_html=True)
    vaccine_data = {
        'النوع': ['شلل الأطفال', 'مخية شوكية', 'ثلاثي فيروسي'],
        'الإجمالي': [
            filtered_vacc_df['شلل الأطفال'].sum(),
            filtered_vacc_df['مخية شوكية'].sum(),
            filtered_vacc_df['ثلاثي فيروسي'].sum()
        ]
    }
    vaccine_data['الإجمالي'] = [max(1, val) for val in vaccine_data['الإجمالي']]
    fig_vacc_pie = go.Figure(data=[go.Pie(
        labels=vaccine_data['النوع'],
        values=vaccine_data['الإجمالي'],
        hole=0.4,
        textinfo='percent+label',
        textfont_size=14,
        marker=dict(
            colors=['#22577A', '#38A3A5', '#57CC99'],
            line=dict(color='#0A0A0A', width=2)
        ),
        hovertemplate='%{label}<br>العدد: %{value:,}<br>النسبة: %{percent}<extra></extra>',
        pull=[0.1, 0, 0]
    )])
    fig_vacc_pie.add_annotation(
        text=f"إجمالي<br>{sum(vaccine_data['الإجمالي']):,}",
        x=0.5, y=0.5,
        font_size=18,
        font_color='var(--text-primary)',
        showarrow=False
    )
    fig_vacc_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=600
    )
    st.plotly_chart(fig_vacc_pie, use_container_width=True)

with col3:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> خريطة حرارية للتطعيمات</h4>', unsafe_allow_html=True)
    vacc_matrix = np.array([
        filtered_vacc_df['شلل الأطفال'].values,
        filtered_vacc_df['مخية شوكية'].values,
        filtered_vacc_df['ثلاثي فيروسي'].values
    ])
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=vacc_matrix,
        x=filtered_vacc_df['الشهر'],
        y=['شلل الأطفال', 'مخية شوكية', 'ثلاثي فيروسي'],
        colorscale=[[0, '#8CCCA4'], [0.5, '#3D8F6B'], [1, '#1A3D5C']],
        text=vacc_matrix,
        texttemplate="%{text:,}",
        textfont={"size": 16, "color": "white"},
        hoverongaps=False,
        hovertemplate='الشهر: %{x}<br>التطعيم: %{y}<br>العدد: %{z:,}<extra></extra>'
    ))
    fig_heatmap.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=600
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">تحليل الطوارئ والزيارات الطبية</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> زيارات العيادة</h4>', unsafe_allow_html=True)
    filtered_clinic_df = filtered_df[filtered_df['زيارات العيادة'].notnull()]
    fig_clinic = go.Figure()
    fig_clinic.add_trace(go.Bar(
        x=filtered_clinic_df['الشهر'],
        y=filtered_clinic_df['زيارات العيادة'],
        name='زيارات العيادة',
        marker_color='#2794EB',
        text=filtered_clinic_df['زيارات العيادة'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
        textposition='auto',
        hovertemplate='الشهر: %{x}<br>الزيارات: %{y:,}<extra></extra>'
    ))
    fig_clinic.add_trace(go.Scatter(
        x=filtered_clinic_df['الشهر'],
        y=filtered_clinic_df['زيارات العيادة'],
        mode='lines+markers',
        name='الاتجاه',
        line=dict(color='#80ED99', width=3),
        marker=dict(size=8)
    ))
    fig_clinic.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        yaxis_title='عدد الزيارات',
        height=600,
        transition={'duration': 1000, 'easing': 'cubic-in-out'}
    )
    st.plotly_chart(fig_clinic, use_container_width=True)

with col2:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> حالات النقل الإسعافي</h4>', unsafe_allow_html=True)
    filtered_emergency_df = filtered_df[filtered_df['حالات النقل الإسعافي'].notnull()]
    fig_emergency = go.Figure()
    fig_emergency.add_trace(go.Scatter(
        x=filtered_emergency_df['الشهر'],
        y=filtered_emergency_df['حالات النقل الإسعافي'],
        mode='lines+markers',
        fill='tonexty',
        name='النقل الإسعافي',
        line=dict(color='#BFF8D4', width=4),
        marker=dict(size=15, color='#57CC99'),
        text=filtered_emergency_df['حالات النقل الإسعافي'].apply(lambda x: f'{x}' if x > 0 else '0'),
        textposition='top center',
        hovertemplate='الشهر: %{x}<br>الحالات: %{y}<extra></extra>'
    ))
    fig_emergency.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=600,
        yaxis=dict(range=[0, max(25, filtered_emergency_df['حالات النقل الإسعافي'].max() * 1.2)])
    )
    st.plotly_chart(fig_emergency, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Quarterly analysis
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> تحليلات الأرباع</div>', unsafe_allow_html=True)

q1_tab, q2_tab, q3_tab, q4_tab = st.tabs(["الربع الأول", "الربع الثاني", "الربع الثالث", "الربع الرابع"])

with q1_tab:
    q1_df = filtered_df[filtered_df['الشهر'].isin(['يناير 2025', 'فبراير 2025', 'مارس 2025'])]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> تطور عدد العابرين والمعتمرين - الربع الأول</h4>', unsafe_allow_html=True)
        fig_q1_travelers = go.Figure()
        fig_q1_travelers.add_trace(go.Scatter(
            x=q1_df['الشهر'], 
            y=q1_df['عدد العابرين'],
            mode='lines+markers+text',
            name='العابرين',
            line=dict(color='#22577A', width=4),
            marker=dict(size=12, color='#38A3A5'),
            text=q1_df['عدد العابرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='top center',
            hovertemplate='الشهر: %{x}<br>العابرين: %{y:,}<br>المعتمرين: %{customdata:,}<extra></extra>',
            customdata=q1_df['عدد المعتمرين']
        ))
        fig_q1_travelers.add_trace(go.Scatter(
            x=q1_df['الشهر'], 
            y=q1_df['عدد المعتمرين'],
            mode='lines+markers+text',
            name='المعتمرين',
            line=dict(color='#57CC99', width=4),
            marker=dict(size=12, color='#80ED99'),
            text=q1_df['عدد المعتمرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='bottom center',
            hovertemplate='الشهر: %{x}<br>المعتمرين: %{y:,}<br>العابرين: %{customdata:,}<extra></extra>',
            customdata=q1_df['عدد العابرين']
        ))
        fig_q1_travelers.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=600,
            transition={'duration': 1000, 'easing': 'cubic-in-out'}
        )
        st.plotly_chart(fig_q1_travelers, use_container_width=True)
    
    with col2:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> زيارات العيادة والنقل الإسعافي - الربع الأول</h4>', unsafe_allow_html=True)
        fig_q1_medical = make_subplots(specs=[[{"secondary_y": True}]])
        fig_q1_medical.add_trace(
            go.Bar(x=q1_df['الشهر'], y=q1_df['زيارات العيادة'], 
                   name='زيارات العيادة', 
                   marker_color='#2794EB',
                   text=q1_df['زيارات العيادة'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
                   textposition='auto'),
            secondary_y=False,
        )
        fig_q1_medical.add_trace(
            go.Scatter(x=q1_df['الشهر'], y=q1_df['حالات النقل الإسعافي'], 
                      mode='lines+markers',
                      name='النقل الإسعافي',
                      line=dict(color='#BFF8D4', width=3),
                      marker=dict(size=10, color='#80ED99'),
                      text=q1_df['حالات النقل الإسعافي'].apply(lambda x: f'{x}' if x > 0 else '0'),
                      textposition='top center'),
            secondary_y=True,
        )
        fig_q1_medical.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600,
            transition={'duration': 1000, 'easing': 'cubic-in-out'}
        )
        fig_q1_medical.update_yaxes(title_text="زيارات العيادة", secondary_y=False, title_font_color='var(--text-primary)')
        fig_q1_medical.update_yaxes(title_text="النقل الإسعافي", secondary_y=True, title_font_color='var(--text-primary)')
        st.plotly_chart(fig_q1_medical, use_container_width=True)
    
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;">تحليل التطعيمات حسب النوع - الربع الأول</h4>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig_q1_vacc_3d = go.Figure()
        months = q1_df['الشهر']
        fig_q1_vacc_3d.add_trace(go.Scatter3d(
            x=months,
            y=['شلل الأطفال'] * len(months),
            z=q1_df['شلل الأطفال'],
            mode='markers+lines',
            marker=dict(size=8, color='#22577A', opacity=0.8),
            line=dict(color='#38A3A5', width=6),
            name='شلل الأطفال'
        ))
        fig_q1_vacc_3d.add_trace(go.Scatter3d(
            x=months,
            y=['مخية شوكية'] * len(months),
            z=q1_df['مخية شوكية'],
            mode='markers+lines',
            marker=dict(size=8, color='#57CC99', opacity=0.8),
            line=dict(color='#80ED99', width=6),
            name='مخية شوكية'
        ))
        fig_q1_vacc_3d.add_trace(go.Scatter3d(
            x=months,
            y=['ثلاثي فيروسي'] * len(months),
            z=q1_df['ثلاثي فيروسي'],
            mode='markers+lines',
            marker=dict(size=8, color='#2794EB', opacity=0.8),
            line=dict(color='#BFF8D4', width=6),
            name='ثلاثي فيروسي'
        ))
        fig_q1_vacc_3d.update_layout(
            scene=dict(
                xaxis_title='الشهر',
                yaxis_title='نوع التطعيم',
                zaxis_title='العدد',
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600
        )
        st.plotly_chart(fig_q1_vacc_3d, use_container_width=True)
    
    with col2:
        total_vacc_q1 = q1_df['مجموع التطعيمات'].sum()
        fig_q1_pie = go.Figure(data=[go.Pie(
            labels=['شلل الأطفال', 'مخية شوكية', 'ثلاثي فيروسي'],
            values=[max(1, q1_df['شلل الأطفال'].sum()), max(1, q1_df['مخية شوكية'].sum()), max(1, q1_df['ثلاثي فيروسي'].sum())],
            hole=0.4,
            textinfo='percent+label',
            textfont_size=14,
            marker=dict(colors=['#22577A', '#38A3A5', '#57CC99'], line=dict(color='#0A0A0A', width=2)),
            hovertemplate='%{label}<br>العدد: %{value:,}<br>النسبة: %{percent}<extra></extra>',
            rotation=90,
            pull=[0.1, 0, 0]
        )])
        fig_q1_pie.add_annotation(
            text=f"إجمالي<br>{total_vacc_q1:,}",
            x=0.5, y=0.5,
            font_size=18,
            font_color='var(--text-primary)',
            showarrow=False
        )
        fig_q1_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600
        )
        st.plotly_chart(fig_q1_pie, use_container_width=True)
    
    st.markdown('<h3 style="color: var(--text-accent); text-align: center;"> تحليلات الربع الأول</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> اتجاه العابرين</div>
            <div class="analysis-text">
                وصل عدد العابرين إلى ذروته في فبراير (200,682) ثم انخفض في مارس إلى 163,291. 
                يشير هذا إلى نشاط موسمي قوي في منتصف الربع الأول.
            </div>
            <span class="insight-badge">نمو 8.1% في فبراير</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> موسم العمرة</div>
            <div class="analysis-text">
                شهد فبراير أعلى معدل للمعتمرين (120,930) بزيادة 36% عن يناير، 
                مما يعكس الذروة الموسمية لأداء العمرة في هذه الفترة.
            </div>
            <span class="warning-badge">ذروة موسمية</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> برنامج التطعيم</div>
            <div class="analysis-text">
                تم تطعيم 282,471 جرعة في الربع الأول، مع تركيز كبير على تطعيم شلل الأطفال (62% من المجموع).
            </div>
            <span class="insight-badge">هدف محقق</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="analysis-card">
        <div class="analysis-title"> المجموع الكلي للربع الأول</div>
        <div class="analysis-text">
            المجموع الكلي: {q1_df['المجموع الكلي'].sum():,}
        </div>
    </div>
    """, unsafe_allow_html=True)

with q2_tab:
    q2_df = filtered_df[filtered_df['الشهر'].isin(['أبريل 2025', 'مايو 2025', 'يونيو 2025'])]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> مقارنة العابرين والمعتمرين - الربع الثاني</h4>', unsafe_allow_html=True)
        fig_q2_comparison = go.Figure()
        fig_q2_comparison.add_trace(go.Bar(
            x=q2_df['الشهر'],
            y=q2_df['عدد العابرين'],
            name='العابرين',
            marker_color='#22577A',
            text=q2_df['عدد العابرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='auto',
            hovertemplate='الشهر: %{x}<br>العابرين: %{y:,}<br>المعتمرين والحجاج: %{customdata:,}<extra></extra>',
            customdata=q2_df['عدد المعتمرين'] + q2_df['عدد الحجاج']
        ))
        fig_q2_comparison.add_trace(go.Bar(
            x=q2_df['الشهر'],
            y=q2_df['عدد المعتمرين'] + q2_df['عدد الحجاج'],
            name='المعتمرين والحجاج',
            marker_color='#38A3A5',
            text=(q2_df['عدد المعتمرين'] + q2_df['عدد الحجاج']).apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='auto',
            hovertemplate='الشهر: %{x}<br>المعتمرين والحجاج: %{y:,}<br>العابرين: %{customdata:,}<extra></extra>',
            customdata=q2_df['عدد العابرين']
        ))
        fig_q2_comparison.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600,
            transition={'duration': 1500, 'easing': 'cubic-in-out'}
        )
        st.plotly_chart(fig_q2_comparison, use_container_width=True)

    with col2:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> حالات النقل الإسعافي - الربع الثاني</h4>', unsafe_allow_html=True)
        fig_q2_emergency = go.Figure()
        fig_q2_emergency.add_trace(go.Scatter(
            x=q2_df['الشهر'],
            y=q2_df['حالات النقل الإسعافي'],
            mode='lines+markers',
            fill='tonexty',
            name='النقل الإسعافي',
            line=dict(color='#57CC99', width=4),
            marker=dict(size=15, color='#80ED99'),
            text=q2_df['حالات النقل الإسعافي'].apply(lambda x: f'{x}' if x > 0 else '0'),
            textposition='top center',
            hovertemplate='الشهر: %{x}<br>النقل الإسعافي: %{y}<extra></extra>'
        ))
        fig_q2_emergency.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600,
            yaxis=dict(range=[0, max(25, q2_df['حالات النقل الإسعافي'].max() * 1.2)])
        )
        st.plotly_chart(fig_q2_emergency, use_container_width=True)

    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> خريطة حرارية للتطعيمات - الربع الثاني</h4>', unsafe_allow_html=True)
    vacc_matrix = np.array([
        q2_df['شلل الأطفال'].values,
        q2_df['مخية شوكية'].values,
        q2_df['ثلاثي فيروسي'].values
    ])
    fig_q2_heatmap = go.Figure(data=go.Heatmap(
        z=vacc_matrix,
        x=q2_df['الشهر'],
        y=['شلل الأطفال', 'مخية شوكية', 'ثلاثي فيروسي'],
        colorscale=[[0, "#42AC69"], [0.5, "#3C8B69"], [1, '#22577A']],
        text=vacc_matrix,
        texttemplate="%{text:,}",
        textfont={"size": 16, "color": "white"},
        hoverongaps=False,
        hovertemplate='الشهر: %{x}<br>التطعيم: %{y}<br>العدد: %{z:,}<extra></extra>'
    ))
    fig_q2_heatmap.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=600
    )
    st.plotly_chart(fig_q2_heatmap, use_container_width=True)

    st.markdown('<h3 style="color: var(--text-accent); text-align: center;"> تحليلات الربع الثاني</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> انخفاض العابرين</div>
            <div class="analysis-text">
                انخفض عدد العابرين بشكل ملحوظ في مايو إلى 86,673، 
                وهو أدنى معدل في النصف الأول من العام، ثم تعافى جزئياً في يونيو.
            </div>
            <span class="warning-badge">انخفاض 19% في مايو</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> موسم الحج</div>
            <div class="analysis-text">
                ظهرت حالات الحج في مايو (12,951 حاج) مع توقف العمرة، 
                مما يعكس بداية الاستعدادات لموسم الحج الكبير.
            </div>
            <span class="insight-badge">بداية موسم الحج</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> ذروة الطوارئ</div>
            <div class="analysis-text">
                سجل شهر مايو أعلى معدل لحالات النقل الإسعافي (16 حالة)، 
                مما يستدعي تعزيز الخدمات الطبية الطارئة.
            </div>
            <span class="danger-badge">زيادة 220% في مايو</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="analysis-card">
        <div class="analysis-title"> المجموع الكلي للربع الثاني</div>
        <div class="analysis-text">
            المجموع الكلي: {q2_df['المجموع الكلي'].sum():,}
        </div>
    </div>
    """, unsafe_allow_html=True)

with q3_tab:
    q3_df = st.session_state.health_df.iloc[6:9]
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> تحليل بيانات الربع الثالث</h4>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> العابرين والمعتمرين - الربع الثالث</h4>', unsafe_allow_html=True)
        fig_q3_chart = go.Figure()
        fig_q3_chart.add_trace(go.Scatter(
            x=q3_df['الشهر'],
            y=q3_df['عدد العابرين'],
            mode='lines+markers+text',
            name='العابرين',
            line=dict(color='#22577A', width=4),
            marker=dict(size=12, color='#38A3A5'),
            text=q3_df['عدد العابرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='top center',
            hovertemplate='الشهر: %{x}<br>العابرين: %{y:,}<br>المعتمرين: %{customdata:,}<extra></extra>',
            customdata=q3_df['عدد المعتمرين']
        ))
        fig_q3_chart.add_trace(go.Scatter(
            x=q3_df['الشهر'],
            y=q3_df['عدد المعتمرين'],
            mode='lines+markers+text',
            name='المعتمرين',
            line=dict(color='#57CC99', width=4),
            marker=dict(size=12, color='#80ED99'),
            text=q3_df['عدد المعتمرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='bottom center',
            hovertemplate='الشهر: %{x}<br>المعتمرين: %{y:,}<br>العابرين: %{customdata:,}<extra></extra>',
            customdata=q3_df['عدد العابرين']
        ))
        fig_q3_chart.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            showlegend=True,
            height=600,
            transition={'duration': 1000, 'easing': 'cubic-in-out'}
        )
        st.plotly_chart(fig_q3_chart, use_container_width=True)
    
    with col2:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> خدمات العيادة والطوارئ - الربع الثالث</h4>', unsafe_allow_html=True)
        fig_q3_medical = make_subplots(specs=[[{"secondary_y": True}]])
        fig_q3_medical.add_trace(
            go.Bar(
                x=q3_df['الشهر'],
                y=q3_df['زيارات العيادة'],
                name='زيارات العيادة',
                marker_color='#2794EB',
                text=q3_df['زيارات العيادة'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
                textposition='auto'
            ),
            secondary_y=False,
        )
        fig_q3_medical.add_trace(
            go.Scatter(
                x=q3_df['الشهر'],
                y=q3_df['حالات النقل الإسعافي'],
                mode='lines+markers',
                name='النقل الإسعافي',
                line=dict(color='#BFF8D4', width=3),
                marker=dict(size=10, color='#80ED99'),
                text=q3_df['حالات النقل الإسعافي'].apply(lambda x: f'{x}' if x > 0 else '0'),
                textposition='top center'
            ),
            secondary_y=True,
        )
        fig_q3_medical.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600
        )
        fig_q3_medical.update_yaxes(title_text="زيارات العيادة", secondary_y=False, title_font_color='var(--text-primary)')
        fig_q3_medical.update_yaxes(title_text="النقل الإسعافي", secondary_y=True, title_font_color='var(--text-primary)')
        st.plotly_chart(fig_q3_medical, use_container_width=True)

    q3_total = q3_df['المجموع الكلي'].sum()
    st.markdown(f"""
    <div class="analysis-card">
        <div class="analysis-title">المجموع الكلي للربع الثالث</div>
        <div class="analysis-text">
            المجموع الكلي: {q3_total:,}
        </div>
        <span class="insight-badge">يوليو - سبتمبر 2025</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<p style="color: #FFCC00; text-align: center; font-weight: bold;">تنويه: البيانات للربع الثالث غير مكتملة حتى الآن (متاحة حتى أغسطس 2025 فقط، وسبتمبر غير متوفرة بعد).</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with q4_tab:
    q4_df = st.session_state.health_df.iloc[9:12]
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> تحليل بيانات الربع الرابع</h4>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> العابرين والمعتمرين - الربع الرابع</h4>', unsafe_allow_html=True)
        fig_q4_chart = go.Figure()
        fig_q4_chart.add_trace(go.Scatter(
            x=q4_df['الشهر'],
            y=q4_df['عدد العابرين'],
            mode='lines+markers+text',
            name='العابرين',
            line=dict(color='#22577A', width=4),
            marker=dict(size=12, color='#38A3A5'),
            text=q4_df['عدد العابرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='top center',
            hovertemplate='الشهر: %{x}<br>العابرين: %{y:,}<br>المعتمرين: %{customdata:,}<extra></extra>',
            customdata=q4_df['عدد المعتمرين']
        ))
        fig_q4_chart.add_trace(go.Scatter(
            x=q4_df['الشهر'],
            y=q4_df['عدد المعتمرين'],
            mode='lines+markers+text',
            name='المعتمرين',
            line=dict(color='#57CC99', width=4),
            marker=dict(size=12, color='#80ED99'),
            text=q4_df['عدد المعتمرين'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
            textposition='bottom center',
            hovertemplate='الشهر: %{x}<br>المعتمرين: %{y:,}<br>العابرين: %{customdata:,}<extra></extra>',
            customdata=q4_df['عدد العابرين']
        ))
        fig_q4_chart.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            showlegend=True,
            height=600,
            transition={'duration': 1000, 'easing': 'cubic-in-out'}
        )
        st.plotly_chart(fig_q4_chart, use_container_width=True)
    
    with col2:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> خدمات العيادة والطوارئ - الربع الرابع</h4>', unsafe_allow_html=True)
        fig_q4_medical = make_subplots(specs=[[{"secondary_y": True}]])
        fig_q4_medical.add_trace(
            go.Bar(
                x=q4_df['الشهر'],
                y=q4_df['زيارات العيادة'],
                name='زيارات العيادة',
                marker_color='#2794EB',
                text=q4_df['زيارات العيادة'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
                textposition='auto'
            ),
            secondary_y=False,
        )
        fig_q4_medical.add_trace(
            go.Scatter(
                x=q4_df['الشهر'],
                y=q4_df['حالات النقل الإسعافي'],
                mode='lines+markers',
                name='النقل الإسعافي',
                line=dict(color='#BFF8D4', width=3),
                marker=dict(size=10, color='#80ED99'),
                text=q4_df['حالات النقل الإسعافي'].apply(lambda x: f'{x}' if x > 0 else '0'),
                textposition='top center'
            ),
            secondary_y=True,
        )
        fig_q4_medical.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            height=600
        )
        fig_q4_medical.update_yaxes(title_text="زيارات العيادة", secondary_y=False, title_font_color='var(--text-primary)')
        fig_q4_medical.update_yaxes(title_text="النقل الإسعافي", secondary_y=True, title_font_color='var(--text-primary)')
        st.plotly_chart(fig_q4_medical, use_container_width=True)

    q4_total = q4_df['المجموع الكلي'].sum()
    st.markdown(f"""
    <div class="analysis-card">
        <div class="analysis-title">المجموع الكلي للربع الرابع</div>
        <div class="analysis-text">
            المجموع الكلي: {q4_total:,}
        </div>
        <span class="insight-badge">أكتوبر - ديسمبر 2025</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<p style="color: #FFCC00; text-align: center; font-weight: bold;">تنويه: لا توجد بيانات متاحة للربع الرابع حتى الآن (أكتوبر إلى ديسمبر 2025 غير متوفرة بعد).</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Travelers by entry point
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> العابرين حسب نقطة الدخول</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> عدد العابرين حسب نقطة الدخول</h4>', unsafe_allow_html=True)
    fig_travelers_entry = go.Figure()
    fig_travelers_entry.add_trace(go.Bar(
        x=filtered_df['الشهر'],
        y=filtered_df['عدد العابرين الوديعة'],
        name='الوديعة',
        marker_color='#22577A',
        text=filtered_df['عدد العابرين الوديعة'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
        textposition='auto',
        hovertemplate='الشهر: %{x}<br>الوديعة: %{y:,}<extra></extra>'
    ))
    fig_travelers_entry.add_trace(go.Bar(
        x=filtered_df['الشهر'],
        y=filtered_df['عدد العابرين الخضراء'],
        name='الخضراء',
        marker_color='#38A3A5',
        text=filtered_df['عدد العابرين الخضراء'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
        textposition='auto',
        hovertemplate='الشهر: %{x}<br>الخضراء: %{y:,}<extra></extra>'
    ))
    fig_travelers_entry.add_trace(go.Bar(
        x=filtered_df['الشهر'],
        y=filtered_df['عدد العابرين المطار'],
        name='المطار',
        marker_color='#57CC99',
        text=filtered_df['عدد العابرين المطار'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
        textposition='auto',
        hovertemplate='الشهر: %{x}<br>المطار: %{y:,}<extra></extra>'
    ))
    fig_travelers_entry.update_layout(
        barmode='stack',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        yaxis_title='عدد العابرين',
        height=600,
        transition={'duration': 1000, 'easing': 'cubic-in-out'}
    )
    st.plotly_chart(fig_travelers_entry, use_container_width=True)

with col2:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> زيارات العيادة حسب نقطة الدخول</h4>', unsafe_allow_html=True)
    fig_clinic_entry = go.Figure()
    fig_clinic_entry.add_trace(go.Bar(
        x=filtered_df['الشهر'],
        y=filtered_df['عيادة الطبيب الوديعة'],
        name='عيادة الوديعة',
        marker_color='#2794EB',
        text=filtered_df['عيادة الطبيب الوديعة'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
        textposition='auto',
        hovertemplate='الشهر: %{x}<br>عيادة الوديعة: %{y:,}<extra></extra>'
    ))
    fig_clinic_entry.add_trace(go.Bar(
        x=filtered_df['الشهر'],
        y=filtered_df['عيادة الطبيب المطار'],
        name='عيادة المطار',
        marker_color='#80ED99',
        text=filtered_df['عيادة الطبيب المطار'].apply(lambda x: f'{x:,}' if x > 0 else '0'),
        textposition='auto',
        hovertemplate='الشهر: %{x}<br>عيادة المطار: %{y:,}<extra></extra>'
    ))
    fig_clinic_entry.update_layout(
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        yaxis_title='عدد الزيارات',
        height=600,
        transition={'duration': 1000, 'easing': 'cubic-in-out'}
    )
    st.plotly_chart(fig_clinic_entry, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Correlation analysis
if show_correlations:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"> تحليل الارتباط</div>', unsafe_allow_html=True)
    
    correlation_matrix = filtered_df[['عدد العابرين', 'عدد المعتمرين', 'عدد الحجاج', 
                                     'زيارات العيادة', 'حالات النقل الإسعافي', 'مجموع التطعيمات',
                                     'عدد العابرين الوديعة', 'عدد العابرين الخضراء', 
                                     'عدد العابرين المطار', 'عيادة الطبيب الوديعة', 
                                     'عيادة الطبيب المطار']].corr()
    
    fig_correlation = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale=[[0, '#22577A'], [0.5, '#38A3A5'], [1, '#57CC99']],
        text=correlation_matrix.values.round(2),
        texttemplate="%{text}",
        textfont={"size": 12, "color": "white"},
        hoverongaps=False,
        hovertemplate='المتغير 1: %{x}<br>المتغير 2: %{y}<br>الارتباط: %{z:.2f}<extra></extra>'
    ))
    fig_correlation.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=600
    )
    st.plotly_chart(fig_correlation, use_container_width=True)
    
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> رؤى الارتباط</h4>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> العابرين والتطعيمات</div>
            <div class="analysis-text">
                ارتباط قوي بين عدد العابرين ومجموع التطعيمات 
                (معامل الارتباط: {correlation_matrix.loc['عدد العابرين', 'مجموع التطعيمات']:.2f})، 
                مما يشير إلى أن زيادة العابرين ترتبط بزيادة التطعيمات.
            </div>
            <span class="insight-badge">ارتباط إيجابي قوي</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> زيارات العيادة والطوارئ</div>
            <div class="analysis-text">
                ارتباط معتدل بين زيارات العيادة وحالات النقل الإسعافي 
                (معامل الارتباط: {correlation_matrix.loc['زيارات العيادة', 'حالات النقل الإسعافي']:.2f})، 
                مما يعكس الحاجة إلى تعزيز الخدمات الطبية.
            </div>
            <span class="warning-badge">ارتباط معتدل</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> العابرين والمعتمرين</div>
            <div class="analysis-text">
                ارتباط قوي بين عدد العابرين والمعتمرين 
                (معامل الارتباط: {correlation_matrix.loc['عدد العابرين', 'عدد المعتمرين']:.2f})، 
                مما يعكس تأثير موسم العمرة على حركة العابرين.
            </div>
            <span class="insight-badge">ارتباط موسمي</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Predictive analysis
if show_predictions:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"> تحليلات تنبؤية</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> تنبؤ العابرين</h4>', unsafe_allow_html=True)
        months = filtered_df['الشهر']
        travelers = filtered_df['عدد العابرين'].values
        future_months = ['أكتوبر 2025', 'نوفمبر 2025', 'ديسمبر 2025']
        predicted_travelers = [travelers[-1] * (1 + i * 0.05) for i in range(1, 4)]
        all_months = list(months) + future_months
        all_travelers = list(travelers) + predicted_travelers
        
        fig_pred_travelers = go.Figure()
        fig_pred_travelers.add_trace(go.Scatter(
            x=months,
            y=travelers,
            mode='lines+markers',
            name='العابرين (الفعلي)',
            line=dict(color='#22577A', width=4),
            marker=dict(size=12),
            text=[f'{x:,}' if x > 0 else '0' for x in travelers],
            textposition='top center'
        ))
        fig_pred_travelers.add_trace(go.Scatter(
            x=future_months,
            y=predicted_travelers,
            mode='lines+markers',
            name='العابرين (التنبؤ)',
            line=dict(color='#57CC99', width=4, dash='dash'),
            marker=dict(size=12),
            text=[f'{x:,.0f}' for x in predicted_travelers],
            textposition='top center'
        ))
        fig_pred_travelers.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            yaxis_title='عدد العابرين',
            height=600
        )
        st.plotly_chart(fig_pred_travelers, use_container_width=True)
    
    with col2:
        st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> تنبؤ التطعيمات</h4>', unsafe_allow_html=True)
        vaccinations = filtered_df['مجموع التطعيمات'].values
        predicted_vaccinations = [vaccinations[-1] * (1 + i * 0.03) for i in range(1, 4)]
        all_vaccinations = list(vaccinations) + predicted_vaccinations
        
        fig_pred_vaccinations = go.Figure()
        fig_pred_vaccinations.add_trace(go.Scatter(
            x=months,
            y=vaccinations,
            mode='lines+markers',
            name='التطعيمات (الفعلي)',
            line=dict(color='#38A3A5', width=4),
            marker=dict(size=12),
            text=[f'{x:,}' if x > 0 else '0' for x in vaccinations],
            textposition='top center'
        ))
        fig_pred_vaccinations.add_trace(go.Scatter(
            x=future_months,
            y=predicted_vaccinations,
            mode='lines+markers',
            name='التطعيمات (التنبؤ)',
            line=dict(color='#80ED99', width=4, dash='dash'),
            marker=dict(size=12),
            text=[f'{x:,.0f}' for x in predicted_vaccinations],
            textposition='top center'
        ))
        fig_pred_vaccinations.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_family='Cairo',
            font_color='var(--text-primary)',
            yaxis_title='عدد التطعيمات',
            height=600
        )
        st.plotly_chart(fig_pred_vaccinations, use_container_width=True)
    
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> رؤى تنبؤية</h4>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> توقعات العابرين</div>
            <div class="analysis-text">
                من المتوقع أن يرتفع عدد العابرين بنسبة 5% شهريًا في الربع الرابع، 
                ليصل إلى حوالي {predicted_travelers[-1]:,.0f} في ديسمبر 2025.
            </div>
            <span class="insight-badge">توقعات إيجابية</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> توقعات التطعيمات</div>
            <div class="analysis-text">
                من المتوقع أن تزداد التطعيمات بنسبة 3% شهريًا، 
                لتصل إلى حوالي {predicted_vaccinations[-1]:,.0f} في ديسمبر 2025.
            </div>
            <span class="insight-badge">نمو مطرد</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Clustering analysis
if show_clusters:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"> تحليل التجميع</div>', unsafe_allow_html=True)
    
    cluster_data = filtered_df[['عدد العابرين', 'مجموع التطعيمات']].dropna()
    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster_data['Cluster'] = kmeans.fit_predict(cluster_data)
    
    fig_clusters = go.Figure()
    for cluster in range(3):
        cluster_subset = cluster_data[cluster_data['Cluster'] == cluster]
        fig_clusters.add_trace(go.Scatter(
            x=cluster_subset['عدد العابرين'],
            y=cluster_subset['مجموع التطعيمات'],
            mode='markers',
            name=f'المجموعة {cluster + 1}',
            marker=dict(size=15, color=['#22577A', '#38A3A5', '#57CC99'][cluster], opacity=0.7),
            text=filtered_df.loc[cluster_subset.index, 'الشهر'],
            hovertemplate='الشهر: %{text}<br>العابرين: %{x:,}<br>التطعيمات: %{y:,}<extra></extra>'
        ))
    fig_clusters.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        xaxis_title='عدد العابرين',
        yaxis_title='مجموع التطعيمات',
        height=600
    )
    st.plotly_chart(fig_clusters, use_container_width=True)
    
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> رؤى التجميع</h4>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> المجموعة 1: نشاط مرتفع</div>
            <div class="analysis-text">
                تشمل الأشهر ذات العدد الكبير من العابرين والتطعيمات (مثل يناير وفبراير)، 
                مما يعكس الذروة الموسمية.
            </div>
            <span class="insight-badge">نشاط موسمي مرتفع</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="analysis-card">
            <div class="analysis-title"> المجموعة 2: نشاط منخفض</div>
            <div class="analysis-text">
                تشمل الأشهر ذات العدد المنخفض من العابرين والتطعيمات (مثل أغسطس)، 
                مما يعكس الهدوء الموسمي.
            </div>
            <span class="warning-badge">نشاط منخفض</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Gauge charts for key metrics
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> لوحات القياس</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

months = filtered_df['الشهر']
month_indices = list(range(len(months)))

with col1:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> كفاءة العيادات</h4>', unsafe_allow_html=True)
    fig_clinic_3d = go.Figure()
    fig_clinic_3d.add_trace(go.Scatter3d(
        x=month_indices,
        y=filtered_df['عدد العابرين'],
        z=filtered_df['زيارات العيادة'],
        mode='markers+lines',
        marker=dict(size=8, color='#22577A', opacity=0.8),
        line=dict(color='#38A3A5', width=6),
        name='زيارات العيادة',
        text=[f'الشهر: {m}<br>زيارات: {v:,}<br>عابرين: {t:,}' for m, v, t in zip(months, filtered_df['زيارات العيادة'], filtered_df['عدد العابرين'])],
        hovertemplate='%{text}<extra></extra>'
    ))
    fig_clinic_3d.update_layout(
        scene=dict(
            xaxis_title='الشهر',
            yaxis_title='عدد العابرين',
            zaxis_title='زيارات العيادة',
            xaxis=dict(tickvals=month_indices, ticktext=months),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )
    st.plotly_chart(fig_clinic_3d, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> كفاءة الاستجابة للطوارئ</h4>', unsafe_allow_html=True)
    fig_emergency_3d = go.Figure()
    fig_emergency_3d.add_trace(go.Scatter3d(
        x=month_indices,
        y=filtered_df['زيارات العيادة'],
        z=filtered_df['حالات النقل الإسعافي وحالات الإشتباه'],
        mode='markers+lines',
        marker=dict(size=8, color='#57CC99', opacity=0.8),
        line=dict(color='#80ED99', width=6),
        name='حالات الطوارئ',
        text=[f'الشهر: {m}<br>حالات طوارئ: {e}<br>زيارات: {v:,}' for m, e, v in zip(months, filtered_df['حالات النقل الإسعافي وحالات الإشتباه'], filtered_df['زيارات العيادة'])],
        hovertemplate='%{text}<extra></extra>'
    ))
    fig_emergency_3d.update_layout(
        scene=dict(
            xaxis_title='الشهر',
            yaxis_title='زيارات العيادة',
            zaxis_title='حالات الطوارئ',
            xaxis=dict(tickvals=month_indices, ticktext=months),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )
    st.plotly_chart(fig_emergency_3d, use_container_width=True, config={'displayModeBar': False})

with col3:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> معدل التطعيمات</h4>', unsafe_allow_html=True)
    fig_vacc_3d = go.Figure()
    fig_vacc_3d.add_trace(go.Scatter3d(
        x=month_indices,
        y=filtered_df['عدد العابرين'],
        z=filtered_df['مجموع التطعيمات'],
        mode='markers+lines',
        marker=dict(size=8, color='#2794EB', opacity=0.8),
        line=dict(color='#BFF8D4', width=6),
        name='التطعيمات',
        text=[f'الشهر: {m}<br>تطعيمات: {v:,}<br>عابرين: {t:,}' for m, v, t in zip(months, filtered_df['مجموع التطعيمات'], filtered_df['عدد العابرين'])],
        hovertemplate='%{text}<extra></extra>'
    ))
    fig_vacc_3d.update_layout(
        scene=dict(
            xaxis_title='الشهر',
            yaxis_title='عدد العابرين',
            zaxis_title='مجموع التطعيمات',
            xaxis=dict(tickvals=month_indices, ticktext=months),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )
    st.plotly_chart(fig_vacc_3d, use_container_width=True, config={'displayModeBar': False})

with col4:
    st.markdown('<h4 style="color: var(--text-primary); text-align: center;"> كفاءة الجولات الإشرافية</h4>', unsafe_allow_html=True)
    fig_inspection_3d = go.Figure()
    fig_inspection_3d.add_trace(go.Scatter3d(
        x=month_indices,
        y=filtered_df['عدد العابرين'],
        z=filtered_df['الجولات الإشرافية'],
        mode='markers+lines',
        marker=dict(size=8, color='#80ED99', opacity=0.8),
        line=dict(color='#57CC99', width=6),
        name='الجولات الإشرافية',
        text=[f'الشهر: {m}<br>جولات: {i}<br>عابرين: {t:,}' for m, i, t in zip(months, filtered_df['الجولات الإشرافية'], filtered_df['عدد العابرين'])],
        hovertemplate='%{text}<extra></extra>'
    ))
    fig_inspection_3d.update_layout(
        scene=dict(
            xaxis_title='الشهر',
            yaxis_title='عدد العابرين',
            zaxis_title='الجولات الإشرافية',
            xaxis=dict(tickvals=month_indices, ticktext=months),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )
    st.plotly_chart(fig_inspection_3d, use_container_width=True, config={'displayModeBar': False})

st.markdown('</div>', unsafe_allow_html=True)

# Gauge charts calculations (fixed)
clinic_efficiency = min((filtered_df['زيارات العيادة'].sum() / max(1, filtered_df['عدد العابرين'].sum())) * 100, 100)
emergency_response = min((filtered_df['حالات النقل الإسعافي وحالات الإشتباه'].sum() / max(1, filtered_df['زيارات العيادة'].sum())) * 100, 100)
vaccination_rate = min((filtered_df['مجموع التطعيمات'].sum() / max(1, filtered_df['عدد العابرين'].sum())) * 100, 100)
inspection_efficiency = min((filtered_df['الجولات الإشرافية'].sum() / max(1, len(filtered_df) * 2)) * 100, 100)  # Assuming target of 2 inspections per month

col1, col2, col3, col4 = st.columns(4)

with col1:
    fig_gauge_clinic = go.Figure(go.Indicator(
        mode="gauge+number",
        value=clinic_efficiency,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "كفاءة العيادات (%)", 'font': {'size': 16, 'color': 'var(--text-primary)'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'var(--text-primary)', 'tickfont': {'color': 'var(--text-primary)'}},
            'bar': {'color': '#22577A'},
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': 'var(--text-primary)',
            'steps': [
                {'range': [0, 50], 'color': '#BFF8D4'},
                {'range': [50, 75], 'color': '#57CC99'},
                {'range': [75, 100], 'color': '#38A3A5'}
            ],
            'threshold': {
                'line': {'color': '#80ED99', 'width': 4},
                'value': 80
            }
        }
    ))
    fig_gauge_clinic.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_gauge_clinic, use_container_width=True, config={'displayModeBar': False})

with col2:
    fig_gauge_emergency = go.Figure(go.Indicator(
        mode="gauge+number",
        value=emergency_response,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "كفاءة الاستجابة للطوارئ (%)", 'font': {'size': 16, 'color': 'var(--text-primary)'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'var(--text-primary)', 'tickfont': {'color': 'var(--text-primary)'}},
            'bar': {'color': '#38A3A5'},
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': 'var(--text-primary)',
            'steps': [
                {'range': [0, 50], 'color': '#BFF8D4'},
                {'range': [50, 75], 'color': '#57CC99'},
                {'range': [75, 100], 'color': '#22577A'}
            ],
            'threshold': {
                'line': {'color': '#80ED99', 'width': 4},
                'value': 90
            }
        }
    ))
    fig_gauge_emergency.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_gauge_emergency, use_container_width=True, config={'displayModeBar': False})

with col3:
    fig_gauge_vaccination = go.Figure(go.Indicator(
        mode="gauge+number",
        value=vaccination_rate,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "معدل التطعيمات (%)", 'font': {'size': 16, 'color': 'var(--text-primary)'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'var(--text-primary)', 'tickfont': {'color': 'var(--text-primary)'}},
            'bar': {'color': '#57CC99'},
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': 'var(--text-primary)',
            'steps': [
                {'range': [0, 50], 'color': '#BFF8D4'},
                {'range': [50, 75], 'color': '#38A3A5'},
                {'range': [75, 100], 'color': '#22577A'}
            ],
            'threshold': {
                'line': {'color': '#80ED99', 'width': 4},
                'value': 85
            }
        }
    ))
    fig_gauge_vaccination.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_gauge_vaccination, use_container_width=True, config={'displayModeBar': False})

with col4:
    fig_gauge_inspection = go.Figure(go.Indicator(
        mode="gauge+number",
        value=inspection_efficiency,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "كفاءة الجولات الإشرافية (%)", 'font': {'size': 16, 'color': 'var(--text-primary)'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'var(--text-primary)', 'tickfont': {'color': 'var(--text-primary)'}},
            'bar': {'color': '#2794EB'},
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': 'var(--text-primary)',
            'steps': [
                {'range': [0, 50], 'color': '#BFF8D4'},
                {'range': [50, 75], 'color': '#57CC99'},
                {'range': [75, 100], 'color': '#38A3A5'}
            ],
            'threshold': {
                'line': {'color': '#80ED99', 'width': 4},
                'value': 90
            }
        }
    ))
    fig_gauge_inspection.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_family='Cairo',
        font_color='var(--text-primary)',
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_gauge_inspection, use_container_width=True, config={'displayModeBar': False})

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# Key metrics for entry points
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> المؤشرات الرئيسية لنقاط الدخول</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df['عدد العابرين الوديعة'].sum():,}</div>
        <div class="metric-label">إجمالي العابرين - الوديعة</div>
        <div class="metric-status insight-badge">مستقر</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df['عدد العابرين الخضراء'].sum():,}</div>
        <div class="metric-label">إجمالي العابرين - الخضراء</div>
        <div class="metric-status insight-badge">مستقر</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{filtered_df['عدد العابرين المطار'].sum():,}</div>
        <div class="metric-label">إجمالي العابرين - المطار</div>
        <div class="metric-status insight-badge">مستقر</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Final summary
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"> ملخص الأداء السنوي</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="analysis-card">
        <div class="analysis-title"> إجمالي العابرين</div>
        <div class="analysis-text">
            تم تسجيل {filtered_df['عدد العابرين'].sum():,} عابر خلال الفترة، مع ذروة في فبراير وأدنى مستوى في أغسطس.
        </div>
        <span class="insight-badge">نشاط موسمي</span>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="analysis-card">
        <div class="analysis-title"> إجمالي التطعيمات</div>
        <div class="analysis-text">
            تم إعطاء {filtered_df['مجموع التطعيمات'].sum():,} جرعة تطعيم، مع تركيز على شلل الأطفال.
        </div>
        <span class="insight-badge">أداء قوي</span>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="analysis-card">
        <div class="analysis-title"> حالات الطوارئ</div>
        <div class="analysis-text">
            تم التعامل مع {filtered_df['حالات النقل الإسعافي'].sum()} حالة طوارئ، مع ذروة في مايو.
        </div>
        <span class="danger-badge">يحتاج متابعة</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 1rem; color: var(--text-secondary);'>
    <hr class="section-divider">
    <p>© 2025 هيئة الصحة العامة - نجران. جميع الحقوق محفوظة.</p>
    <p>تم تطوير لوحة المعلومات باستخدام Streamlit و Plotly.</p>
</div>
""", unsafe_allow_html=True)

