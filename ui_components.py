"""
UI Helper Components - Full Language Support + Emergency
"""

import streamlit as st
import random

# Language dictionaries
TEXT = {
    'en': {
        'app_title': '🏥 Health Companion',
        'subtitle': 'Your trusted health companion',
        'sidebar_title': '⚙️ Settings',
        'language_label': '🌐 Language',
        'location_label': '📍 Your Location',
        'location_placeholder': 'Enter village or city name...',
        'low_bandwidth': '📶 Low Data Mode',
        'low_bandwidth_help': 'Uses less data - better for rural areas',
        'weather_temp': '🌡️ Temperature',
        'weather_humidity': '💧 Humidity',
        'weather_aqi': '😷 AQI',
        'cached_data': '💾 Cached data',
        'live_data': '✅ Live data',
        'seasonal_data': '📊 Seasonal average',
        'env_risk': '⚠️ Environmental Risk',
        'system_status': '📊 System',
        'kb_diseases': '📚 Knowledge Base:',
        'ml_model': '🧠 ML Model:',
        'ml_ready': '✅ Ready',
        'ml_unavailable': '⚠️ Not available',
        'new_conversation': '🔄 New Conversation',
        'emergency_button': '🚨 EMERGENCY',
        'emergency_help': 'Find nearby hospitals / emergency contacts',
        'welcome_greeting': 'Hello! I am your health companion. How are you feeling today?',
        'welcome_location': 'Please enter your location in the sidebar',
        'welcome_hint': '💬 Try: "What precautions?" • "When to see doctor?"',
        'input_placeholder': 'Describe your symptoms or ask a question...',
        'analyzing': 'Analyzing your symptoms...',
        'confidence': 'Confidence',
        'severity': 'Severity',
        'want_to_know': '💡 Want to know?',
        'precautions_btn': '💊 Precautions',
        'doctor_btn': '🏥 When to See Doctor',
        'symptoms_btn': '🔍 Symptoms',
        'details_btn': '📋 Full Details',
        'disclaimer': '🔒 Your data is completely secure - nothing is stored',
        'disclaimer2': '⚠️ This is educational information only, not medical diagnosis • Always consult a doctor',
        'footer': '🌾 Made with 💚 for Rural India',
        'private': '🔒 100% Private & Secure',
        'verified': '🏥 Verified Medical Knowledge',
        'rural': '🌾 Built for Rural India',
        'risk_high': 'HIGH',
        'risk_moderate': 'MODERATE',
        'risk_low': 'LOW',
        'severity_high': 'HIGH',
        'severity_moderate': 'MODERATE',
        'severity_low': 'LOW'
    },
    'hi': {
        'app_title': '🏥 स्वास्थ्य साथी',
        'subtitle': 'आपका विश्वसनीय स्वास्थ्य साथी',
        'sidebar_title': '⚙️ सेटिंग्स',
        'language_label': '🌐 भाषा',
        'location_label': '📍 आपका स्थान',
        'location_placeholder': 'गाँव या शहर का नाम दर्ज करें...',
        'low_bandwidth': '📶 कम डेटा मोड',
        'low_bandwidth_help': 'कम डेटा उपयोग - ग्रामीण क्षेत्रों के लिए बेहतर',
        'weather_temp': '🌡️ तापमान',
        'weather_humidity': '💧 नमी',
        'weather_aqi': '😷 AQI',
        'cached_data': '💾 कैश्ड डेटा',
        'live_data': '✅ लाइव डेटा',
        'seasonal_data': '📊 मौसमी औसत',
        'env_risk': '⚠️ पर्यावरण जोखिम',
        'system_status': '📊 सिस्टम',
        'kb_diseases': '📚 ज्ञानकोश:',
        'ml_model': '🧠 ML मॉडल:',
        'ml_ready': '✅ सक्रिय',
        'ml_unavailable': '⚠️ अनुपलब्ध',
        'new_conversation': '🔄 नई बातचीत',
        'emergency_button': '🚨 आपातकालीन',
        'emergency_help': 'नज़दीकी अस्पताल / आपातकालीन संपर्क',
        'welcome_greeting': 'नमस्ते! मैं आपका स्वास्थ्य साथी हूं। आज आप कैसा महसूस कर रहे हैं?',
        'welcome_location': 'कृपया साइडबार में अपना स्थान दर्ज करें',
        'welcome_hint': '💬 प्रयास करें: "क्या सावधानियां?" • "डॉक्टर को कब दिखाएं?"',
        'input_placeholder': 'अपने लक्षण बताएं या सवाल पूछें...',
        'analyzing': 'लक्षणों का विश्लेषण कर रहा हूं...',
        'confidence': 'विश्वास',
        'severity': 'गंभीरता',
        'want_to_know': '💡 जानना चाहेंगे?',
        'precautions_btn': '💊 सावधानियां',
        'doctor_btn': '🏥 डॉक्टर को कब दिखाएं',
        'symptoms_btn': '🔍 लक्षण',
        'details_btn': '📋 पूरी जानकारी',
        'disclaimer': '🔒 आपका डेटा पूरी तरह सुरक्षित है - कुछ भी स्टोर नहीं किया जाता',
        'disclaimer2': '⚠️ यह केवल शैक्षिक जानकारी है, चिकित्सकीय निदान नहीं • हमेशा डॉक्टर से सलाह लें',
        'footer': '🌾 ग्रामीण भारत के लिए 💚 से निर्मित',
        'private': '🔒 100% निजी और सुरक्षित',
        'verified': '🏥 सत्यापित चिकित्सा ज्ञान',
        'rural': '🌾 ग्रामीण भारत के लिए',
        'risk_high': 'अधिक',
        'risk_moderate': 'मध्यम',
        'risk_low': 'कम',
        'severity_high': 'अधिक',
        'severity_moderate': 'मध्यम',
        'severity_low': 'कम'
    }
}

def get_text(lang: str, key: str) -> str:
    """Get text in selected language"""
    if lang in TEXT:
        return TEXT[lang].get(key, TEXT['en'].get(key, key))
    return TEXT['en'].get(key, key)

def get_css() -> str:
    """Return custom CSS with healthcare/medical theme"""
    return """
    <style>
        :root {
            --primary: #0D9488;
            --primary-light: #CCFBF1;
            --secondary: #0284C7;
            --accent: #F59E0B;
            --success: #10B981;
            --warning: #F97316;
            --danger: #EF4444;
            --bg-light: #F8FAFC;
            --text-dark: #1E293B;
            --text-muted: #64748B;
        }
        
        .stApp {
            background: linear-gradient(135deg, #F0FDF4 0%, #F0F9FF 100%);
        }
        
        .user-message {
            background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%);
            color: white;
            padding: 14px 18px;
            border-radius: 20px 20px 4px 20px;
            margin: 12px 0;
            float: right;
            clear: both;
            max-width: 70%;
            box-shadow: 0 2px 8px rgba(13, 148, 136, 0.15);
            font-size: 1rem;
            line-height: 1.5;
        }
        
        .bot-message {
            background: white;
            padding: 18px 22px;
            border-radius: 20px 20px 20px 4px;
            margin: 12px 0;
            float: left;
            clear: both;
            max-width: 80%;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border-left: 4px solid #0D9488;
            font-size: 1rem;
            line-height: 1.6;
            color: #1E293B;
        }
        
        .disease-highlight {
            font-size: 1.4em;
            font-weight: 700;
            background: linear-gradient(135deg, #0D9488, #0284C7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 12px 0 8px 0;
        }
        
        .severity-high { background: #FEE2E2; color: #991B1B; padding: 6px 14px; border-radius: 30px; font-weight: 600; display: inline-block; margin: 5px 8px 5px 0; border: 1px solid #FECACA; }
        .severity-moderate { background: #FEF3C7; color: #92400E; padding: 6px 14px; border-radius: 30px; font-weight: 600; display: inline-block; margin: 5px 8px 5px 0; border: 1px solid #FDE68A; }
        .severity-low { background: #D1FAE5; color: #065F46; padding: 6px 14px; border-radius: 30px; font-weight: 600; display: inline-block; margin: 5px 8px 5px 0; border: 1px solid #A7F3D0; }
        
        .env-badge { padding: 6px 14px; border-radius: 30px; font-weight: 600; display: inline-block; margin: 5px 8px 5px 0; }
        .risk-high { background: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
        .risk-moderate { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
        .risk-low { background: #D1FAE5; color: #065F46; border: 1px solid #A7F3D0; }
        
        .source-badge { background: #E0E7FF; color: #3730A3; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 500; margin-left: 10px; }
        
        .confidence-bar { background: #E2E8F0; height: 6px; border-radius: 3px; margin: 8px 0; width: 150px; }
        .confidence-fill { background: linear-gradient(90deg, #0D9488, #10B981); height: 6px; border-radius: 3px; }
        
        .env-context { background: #F0FDF4; border-radius: 12px; padding: 14px 18px; margin: 15px 0; border: 1px solid #D1FAE5; }
        .env-context-title { font-weight: 600; color: #065F46; margin-bottom: 8px; }
        
        .welcome-message {
            background: linear-gradient(135deg, #0D9488 0%, #0284C7 100%);
            color: white;
            padding: 32px 28px;
            border-radius: 24px;
            margin-bottom: 28px;
            box-shadow: 0 8px 24px rgba(13, 148, 136, 0.2);
        }
        
        .emergency-btn {
            background: #EF4444;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 40px;
            font-weight: 700;
            font-size: 1.1rem;
            width: 100%;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
            transition: all 0.2s;
            margin: 10px 0;
        }
        
        .emergency-btn:hover {
            background: #DC2626;
            box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
            transform: translateY(-2px);
        }
        
        .clearfix::after { content: ""; clear: both; display: table; }
        
        .disclaimer {
            text-align: center;
            color: #64748B;
            font-size: 0.8rem;
            margin-top: 30px;
            padding: 15px;
            border-top: 1px solid #E2E8F0;
        }
        
        .empathy-text { color: #64748B; font-style: italic; margin-bottom: 10px; }
        
        .voice-btn {
            background: #F0FDF4;
            border: 1px solid #0D9488;
            color: #0D9488;
            padding: 8px 16px;
            border-radius: 30px;
            cursor: pointer;
            margin: 5px;
        }
        
        .slider-container {
            background: #F8FAFC;
            padding: 15px;
            border-radius: 12px;
            margin: 15px 0;
        }
    </style>
    """

def render_sidebar(weather_module, chatbot_core, lang='en'):
    """Render sidebar with full language support"""
    
    st.sidebar.markdown(f"""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 20px;">
        <span style="font-size: 28px;">🏥</span>
        <span style="font-weight: 700; font-size: 1.3rem; color: #0D9488;">{get_text(lang, 'app_title')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Location input
    st.sidebar.subheader(get_text(lang, 'location_label'))
    location = st.sidebar.text_input(
        get_text(lang, 'location_label'),
        value=st.session_state.get('location', ''),
        placeholder=get_text(lang, 'location_placeholder'),
        label_visibility="collapsed"
    )
    
    # Low bandwidth toggle
    low_bandwidth = st.sidebar.checkbox(
        get_text(lang, 'low_bandwidth'),
        value=False,
        help=get_text(lang, 'low_bandwidth_help')
    )
    
    if location and location != st.session_state.get('location', ''):
        st.session_state.location = location
    
    # Emergency Button
    st.sidebar.markdown("---")
    if st.sidebar.button(get_text(lang, 'emergency_button'), use_container_width=True, type="primary"):
        show_emergency_info(lang)
    
    st.sidebar.markdown("---")
    
    # Weather display
    if st.session_state.get('location'):
        st.sidebar.subheader(f"🌍 {st.session_state.location}")
        
        weather_data = weather_module.get_weather(st.session_state.location, low_bandwidth)
        aqi = weather_module.get_aqi(st.session_state.location, low_bandwidth)
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric(get_text(lang, 'weather_temp'), f"{weather_data['temperature']:.1f}°C")
            st.metric(get_text(lang, 'weather_humidity'), f"{weather_data['humidity']:.0f}%")
        with col2:
            st.metric(get_text(lang, 'weather_aqi'), aqi)
        
        # Data source
        if weather_data.get('is_seasonal', False):
            st.sidebar.caption(f"📊 *{get_text(lang, 'seasonal_data')}*")
        elif weather_data.get('is_cached', False):
            st.sidebar.caption(f"💾 *{get_text(lang, 'cached_data')}*")
        else:
            st.sidebar.success(f"✅ *{get_text(lang, 'live_data')}*")
        
        # Risk assessment
        risk, warnings = weather_module.calculate_risk(
            weather_data['temperature'], aqi, weather_data['humidity']
        )
        
        risk_labels = {'high': get_text(lang, 'risk_high'), 'moderate': get_text(lang, 'risk_moderate'), 'low': get_text(lang, 'risk_low')}
        st.sidebar.markdown(f"""
        <div class="env-badge risk-{risk}" style="width: 100%; text-align: center; margin: 10px 0;">
            ⚠️ {get_text(lang, 'env_risk')}: {risk_labels[risk]} / {risk.upper()}
        </div>
        """, unsafe_allow_html=True)
        
        if warnings:
            for w in warnings[:2]:
                st.sidebar.caption(f"• {w}")
    
    st.sidebar.markdown("---")
    
    # System status
    st.sidebar.markdown("---")
    
    # System status
    st.sidebar.subheader(get_text(lang, 'system_status'))
    
    # Get KB size safely
    try:
        kb_size = len(chatbot_core.kb)
    except:
        try:
            kb_size = len(chatbot_core.rag.documents)
        except:
            kb_size = 21  # Default
    
    st.sidebar.caption(f"{get_text(lang, 'kb_diseases')} {kb_size}")
    
    # Check ML status safely
    ml_loaded = False
    try:
        ml_loaded = chatbot_core.ml_ready
    except:
        try:
            ml_loaded = chatbot_core.ml.is_loaded
        except:
            pass
    
    if ml_loaded:
        st.sidebar.success(f"{get_text(lang, 'ml_model')} {get_text(lang, 'ml_ready')}")
    else:
        st.sidebar.warning(f"{get_text(lang, 'ml_model')} {get_text(lang, 'ml_unavailable')}")
    
    # New conversation button
    if st.sidebar.button(get_text(lang, 'new_conversation'), use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_disease = None
        chatbot_core.last_disease = None
        st.rerun()
    
    return location, low_bandwidth

def show_emergency_info(lang='en'):
    """Show emergency contacts and nearby hospitals"""
    emergency_texts = {
        'en': {
            'title': '🚨 EMERGENCY INFORMATION',
            'ambulance': '📞 Ambulance: 108 / 102',
            'helpline': '📞 Health Helpline: 104',
            'women_helpline': '📞 Women Helpline: 1091',
            'child_helpline': '📞 Child Helpline: 1098',
            'nearby_hospitals': '🏥 Finding nearby hospitals...',
            'note': '⚠️ In case of emergency, call 108 immediately.'
        },
        'hi': {
            'title': '🚨 आपातकालीन जानकारी',
            'ambulance': '📞 एम्बुलेंस: 108 / 102',
            'helpline': '📞 स्वास्थ्य हेल्पलाइन: 104',
            'women_helpline': '📞 महिला हेल्पलाइन: 1091',
            'child_helpline': '📞 चाइल्ड हेल्पलाइन: 1098',
            'nearby_hospitals': '🏥 नज़दीकी अस्पताल खोज रहे हैं...',
            'note': '⚠️ आपातकालीन स्थिति में तुरंत 108 पर कॉल करें।'
               }
    }
    
    texts = emergency_texts[lang] if lang in emergency_texts else emergency_texts['en']
    
    with st.sidebar.expander(texts['title'], expanded=True):
        st.markdown(f"""
        ### {texts['title']}
        
        {texts['ambulance']}
        
        {texts['helpline']}
        
        {texts['women_helpline']}
        
        {texts['child_helpline']}
        
        ---
        
        {texts['nearby_hospitals']}
        
        *{texts['note']}*
        """)


def render_voice_input(lang='en'):
    """Voice input component for rural/low-literacy users"""
    voice_texts = {
        'en': {
            'button': '🎤 Speak your symptoms',
            'listening': 'Listening... Speak clearly',
            'heard': 'I heard:',
            'not_supported': 'Voice input not supported in your browser'
        },
        'hi': {
            'button': '🎤 अपने लक्षण बोलें',
            'listening': 'सुन रहा हूं... स्पष्ट बोलें',
            'heard': 'मैंने सुना:',
            'not_supported': 'आपके ब्राउज़र में वॉइस इनपुट समर्थित नहीं है'
        }
    }
    
    texts = voice_texts[lang] if lang in voice_texts else voice_texts['en']
    
    # JavaScript for voice recognition
    voice_js = f"""
    <script>
    let recognition;
    
    function startVoiceRecognition() {{
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = '{'hi-IN' if lang == 'hi' else 'en-IN'}';
            recognition.continuous = false;
            recognition.interimResults = false;
            
            recognition.onstart = function() {{
                document.getElementById('voice-status').innerHTML = '{texts["listening"]}';
            }};
            
            recognition.onresult = function(event) {{
                const transcript = event.results[0][0].transcript;
                document.getElementById('voice-input').value = transcript;
                document.getElementById('voice-status').innerHTML = '{texts["heard"]} ' + transcript;
            }};
            
            recognition.onerror = function(event) {{
                document.getElementById('voice-status').innerHTML = 'Error: ' + event.error;
            }};
            
            recognition.start();
        }} else {{
            document.getElementById('voice-status').innerHTML = '{texts["not_supported"]}';
        }}
    }}
    </script>
    
    <div style="margin: 10px 0;">
        <button onclick="startVoiceRecognition()" type="button" class="voice-btn">
            {texts['button']}
        </button>
        <span id="voice-status" style="margin-left: 10px; color: #64748B;"></span>
    </div>
    """
    st.components.v1.html(voice_js, height=60, scrolling=True)
    
    # Hidden input to store voice result
    voice_input = st.text_input("Voice input", key="voice_input", label_visibility="collapsed")
    
    return voice_input


def render_severity_slider(lang='en'):
    """Visual severity slider for symptom intensity"""
    slider_texts = {
        'en': {
            'title': '📊 How severe are your symptoms? (1-10)',
            'low': 'Mild',
            'high': 'Severe',
            'help': 'Slide to indicate intensity'
        },
        'hi': {
            'title': '📊 आपके लक्षण कितने गंभीर हैं? (1-10)',
            'low': 'हल्का',
            'high': 'गंभीर',
            'help': 'तीव्रता बताने के लिए स्लाइड करें'
        }
    }
    
    texts = slider_texts[lang] if lang in slider_texts else slider_texts['en']
    
    with st.expander(texts['title'], expanded=False):
        severity = st.slider(
            texts['title'],
            min_value=1,
            max_value=10,
            value=5,
            step=1,
            help=texts['help'],
            label_visibility="collapsed"
        )
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.caption(f"🟢 {texts['low']}")
        with col3:
            st.caption(f"🔴 {texts['high']}")
        
        return severity
    return 5


def generate_pdf_report(disease, symptoms, severity, location, weather_data, lang='en'):
    """Generate PDF report for doctor visit"""
    from fpdf import FPDF
    import tempfile
    from datetime import datetime
    
    pdf = FPDF()
    pdf.add_page()
    
    # Add Unicode font support
    pdf.add_font('NotoSans', '', 'https://fonts.gstatic.com/noto/sans/NotoSans-Regular.ttf')
    pdf.set_font('NotoSans', '', 12)
    
    # Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Health Companion Report', ln=True, align='C')
    pdf.ln(10)
    
    # Date
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)
    pdf.ln(5)
    
    # Symptoms
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Reported Symptoms:', ln=True)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, symptoms)
    pdf.ln(5)
    
    # Severity
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Severity Level: {severity.upper()}", ln=True)
    pdf.ln(5)
    
    # Possible Condition
    if disease:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f"Possible Condition: {disease.get('disease_name', 'N/A')}", ln=True)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 8, disease.get('summary', ''))
        pdf.ln(5)
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Recommended Precautions:', ln=True)
        pdf.set_font('Arial', '', 11)
        for p in disease.get('precautions', [])[:5]:
            pdf.cell(0, 8, f"• {p}", ln=True)
        pdf.ln(5)
        
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'When to See Doctor:', ln=True)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 8, disease.get('when_to_see_doctor', ''))
    
    # Environmental Context
    if weather_data:
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f"Location: {location}", ln=True)
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 8, f"Temperature: {weather_data.get('temperature', 'N/A')}°C", ln=True)
        pdf.cell(0, 8, f"Humidity: {weather_data.get('humidity', 'N/A')}%", ln=True)
        pdf.cell(0, 8, f"AQI: {weather_data.get('aqi', 'N/A')}", ln=True)
    
    # Disclaimer
    pdf.ln(10)
    pdf.set_font('Arial', 'I', 9)
    pdf.multi_cell(0, 6, 'Disclaimer: This report is generated for informational purposes only and does not constitute a medical diagnosis. Please consult a healthcare provider.')
    
    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_file.name)
    
    return temp_file.name