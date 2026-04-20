"""
Health Companion Chatbot - Main Application
All Features: ML + RAG + Weather + Voice + PDF + Bilingual
Clean Streamlit Version - No HTML
"""

import streamlit as st
from datetime import datetime
import itertools
import re

from weather_module import WeatherModule
from hybrid_chatbot_lightweight import LightweightHybridChatbot
from ui_components import (
    render_sidebar, render_voice_input, 
    render_severity_slider, generate_pdf_report, get_text
)

# ============================================
# UNIQUE KEY GENERATOR
# ============================================
key_gen = itertools.count()

def get_key(prefix="btn"):
    return f"{prefix}_{next(key_gen)}"

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Swastya Sathi | Health Companion",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'location' not in st.session_state:
    st.session_state.location = ""
if 'current_disease' not in st.session_state:
    st.session_state.current_disease = None
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'severity_slider' not in st.session_state:
    st.session_state.severity_slider = 5
if 'last_input' not in st.session_state:
    st.session_state.last_input = ""
if 'action_triggered' not in st.session_state:
    st.session_state.action_triggered = None
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'weather_module' not in st.session_state:
    st.session_state.weather_module = None
if 'conversation_context' not in st.session_state:
    st.session_state.conversation_context = {
        'last_disease': None,
        'asked_followups': [],
        'user_concern_level': 'moderate'
    }

# ============================================
# INITIALIZE MODULES
# ============================================
@st.cache_resource
def init_modules():
    wm = WeatherModule()
    wm.clear_cache()
    return wm, LightweightHybridChatbot()

if st.session_state.weather_module is None:
    weather_module, chatbot = init_modules()
    st.session_state.weather_module = weather_module
    st.session_state.chatbot = chatbot
else:
    weather_module = st.session_state.weather_module
    chatbot = st.session_state.chatbot

# ============================================
# EMPATHETIC RESPONSE HELPERS
# ============================================
def get_empathetic_opening(severity_level, user_symptoms):
    """Generate empathetic opening based on severity and symptoms"""
    
    if severity_level == 'high':
        responses = [
            "I hear how difficult this is for you. Thank you for sharing this with me. Let's figure this out together, step by step.",
            "That sounds very challenging. I'm glad you reached out. Your health matters, and I'm here to help you through this.",
            "I can sense you're going through a tough time. You're not alone in this. Let me help you understand what might be happening."
        ]
    elif severity_level == 'moderate':
        responses = [
            "Thank you for telling me how you're feeling. I appreciate you being open about your symptoms.",
            "I understand this is concerning for you. Let's look at what might be going on, shall we?",
            "Thanks for sharing that with me. I'm here to support you and help you feel better."
        ]
    else:
        responses = [
            "Thanks for letting me know. It's always good to pay attention to how we're feeling.",
            "I appreciate you sharing that. Small changes in how we feel can tell us important things.",
            "Thank you for being attentive to your health. Let me help you understand this better."
        ]
    
    return responses[hash(user_symptoms) % len(responses)]

def get_validating_response(disease_name):
    """Validate user's concerns without over-diagnosing"""
    
    validations = [
        f"Many people experience {disease_name} at some point. What you're describing is valid, and there are ways to manage it.",
        f"I hear your concern about {disease_name}. Let me share what's typically known about this condition.",
        f"Thank you for trusting me with this. Based on what you've shared, {disease_name} is one possibility we should discuss."
    ]
    return validations[hash(disease_name) % len(validations)]

def get_followup_question(context):
    """Generate natural follow-up questions to build conversation"""
    
    followups = {
        'duration': [
            "How long have you been experiencing these symptoms?",
            "When did you first notice this starting?",
            "Has this been going on for a few days or longer?"
        ],
        'impact': [
            "How is this affecting your daily activities?",
            "Is this interfering with your sleep or work?",
            "What makes these symptoms better or worse?"
        ],
        'care': [
            "Have you tried anything to feel better?",
            "Have you taken any medication for this?",
            "Has anything helped relieve your symptoms?"
        ]
    }
    
    import random
    category = random.choice(list(followups.keys()))
    return random.choice(followups[category])

# ============================================
# ACTION FUNCTIONS
# ============================================
def add_precautions():
    disease = st.session_state.current_disease
    if disease:
        disease_name = disease.get('disease_name', '')
        precautions = disease.get('precautions', [])
        
        response = f"""**💊 Precautions for {disease_name}**

Here are some steps that can help you feel better:

{chr(10).join([f"{i}. {p}" for i, p in enumerate(precautions[:5], 1)])}

---
🌿 *Remember: These are general guidelines. Listen to your body and rest when you need to.*"""
        
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.session_state.action_triggered = 'precautions'

def add_doctor_info():
    disease = st.session_state.current_disease
    if disease:
        disease_name = disease.get('disease_name', '')
        when_to_see = disease.get('when_to_see_doctor', 'Consult a healthcare provider if symptoms persist.')
        
        severity = st.session_state.get('current_severity', 'moderate')
        
        urgency_note = ""
        if severity == 'high':
            urgency_note = "\n\n⚠️ **Please consider seeking medical attention soon.** Your symptoms warrant professional evaluation."
        elif severity == 'moderate':
            urgency_note = "\n\n⚠️ **Monitor your symptoms closely.** If they worsen, don't hesitate to see a doctor."
        
        response = f"""**🏥 When to See a Doctor - {disease_name}**

{when_to_see}{urgency_note}

---
💚 *Trust your instincts about your health. You know your body best.*"""
        
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.session_state.action_triggered = 'doctor'

def add_symptoms():
    disease = st.session_state.current_disease
    if disease:
        disease_name = disease.get('disease_name', '')
        symptoms = disease.get('symptoms', [])
        
        response = f"""**🔍 Common Symptoms of {disease_name}**

{chr(10).join([f"• {s}" for s in symptoms[:7]])}

---
📝 *Keep track of which symptoms bother you most. This helps doctors understand your situation better.*"""
        
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.session_state.action_triggered = 'symptoms'

def add_full_details():
    disease = st.session_state.current_disease
    if disease:
        disease_name = disease.get('disease_name', '')
        summary = disease.get('summary', '')
        symptoms = '\n'.join([f"• {s}" for s in disease.get('symptoms', [])[:7]])
        precautions = '\n'.join([f"• {p}" for p in disease.get('precautions', [])[:4]])
        when_to_see = disease.get('when_to_see_doctor', '')
        
        response = f"""**📋 {disease_name} - Complete Overview**

**What you should know:**
{summary}

**Common Symptoms to Watch For:**
{symptoms}

**Helpful Precautions:**
{precautions}

**When Professional Care is Recommended:**
{when_to_see}

---
💙 *This information is for educational purposes. Your healthcare provider can give you personalized advice.*"""
        
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.session_state.action_triggered = 'details'

def clear_conversation():
    st.session_state.messages = []
    st.session_state.current_disease = None
    st.session_state.last_input = ""
    st.session_state.action_triggered = 'clear'
    st.session_state.conversation_context = {
        'last_disease': None,
        'asked_followups': [],
        'user_concern_level': 'moderate'
    }
    if hasattr(chatbot, 'last_disease'):
        chatbot.last_disease = None

# ============================================
# LANGUAGE SELECTOR
# ============================================
with st.sidebar:
    st.markdown("### 🌐 Bhasha / Language")
    lang_options = ['English', 'हिंदी', 'Bilingual']
    
    current_lang = st.session_state.language
    if current_lang == 'en':
        idx = 0
    elif current_lang == 'hi':
        idx = 1
    else:
        idx = 2
    
    selected_lang = st.radio(
        "Select Language",
        lang_options,
        index=idx,
        horizontal=True,
        label_visibility="collapsed",
        key=get_key("lang")
    )
    
    lang_map = {'English': 'en', 'हिंदी': 'hi', 'Bilingual': 'bi'}
    st.session_state.language = lang_map[selected_lang]
    ui_lang = 'en' if st.session_state.language in ['en', 'bi'] else 'hi'

# ============================================
# SIDEBAR
# ============================================
location, low_bandwidth = render_sidebar(weather_module, chatbot, ui_lang)
if location:
    st.session_state.location = location

# New conversation button
st.sidebar.button(
    get_text(ui_lang, 'new_conversation'), 
    on_click=clear_conversation,
    use_container_width=True,
    key=get_key("new_conv")
)

# Emergency button
st.sidebar.markdown("---")
if st.sidebar.button(
    get_text(ui_lang, 'emergency_button'),
    use_container_width=True,
    type="primary",
    key=get_key("emergency")
):
    emergency_texts = {
        'en': """
🚨 **EMERGENCY CONTACTS - INDIA**

📞 **Ambulance:** 108 / 102
📞 **Health Helpline:** 104
📞 **Women Helpline:** 1091
📞 **Child Helpline:** 1098

*Call immediately if you're experiencing a medical emergency.*
        """,
        'hi': """
🚨 **आपातकालीन संपर्क - भारत**

📞 **एम्बुलेंस:** 108 / 102
📞 **स्वास्थ्य हेल्पलाइन:** 104
📞 **महिला हेल्पलाइन:** 1091
📞 **चाइल्ड हेल्पलाइन:** 1098

*यदि आपातकालीन स्थिति हो तो तुरंत कॉल करें।*
        """
    }
    st.sidebar.info(emergency_texts.get(ui_lang, emergency_texts['en']))

# ============================================
# MAIN CHAT HEADER
# ============================================
private_text = get_text(ui_lang, 'private')
verified_text = get_text(ui_lang, 'verified')
rural_text = get_text(ui_lang, 'rural')

st.caption(f"{private_text} • {verified_text} • {rural_text}")

app_title = get_text(ui_lang, 'app_title')
subtitle = get_text(ui_lang, 'subtitle')

st.title(app_title)
st.caption(subtitle)

# Voice Input
voice_text = render_voice_input(ui_lang)

# Severity Slider
slider_value = render_severity_slider(ui_lang)
st.session_state.severity_slider = slider_value

# Welcome message
if len(st.session_state.messages) == 0:
    weather_data = weather_module.get_current_conditions(location) if location else None
    
    location_str = f"📍 {location}" if location else "📍 Your location"
    weather_str = ""
    if weather_data:
        weather_str = f"🌡️ {weather_data['temperature']:.1f}°C | 💧 {weather_data['humidity']:.0f}% | 😷 AQI: {weather_data.get('aqi', 'N/A')}"
    
    greetings = {
        'en': "👋 Hello. I'm your health companion, and I'm here to listen. How are you feeling today?",
        'hi': "👋 नमस्ते। मैं आपका स्वास्थ्य साथी हूं, और मैं सुनने के लिए यहां हूं। आप आज कैसा महसूस कर रहे हैं?"
    }
    
    st.info(f"**{greetings.get(ui_lang, greetings['en'])}**\n\n{location_str}\n{weather_str}\n\n💬 *Share what's on your mind - I'm here to support you.*")

# ============================================
# DISPLAY CHAT HISTORY
# ============================================
for msg in st.session_state.messages:
    if msg['role'] == 'user':
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# ============================================
# PROCESS USER INPUT
# ============================================
def process_user_input(user_input: str):
    """Process user input with empathetic, conversational response"""
    
    # Detect language
    is_hindi = bool(re.search(r'[\u0900-\u097F]', user_input))
    
    if st.session_state.language == 'en':
        resp_lang = 'en'
    elif st.session_state.language == 'hi':
        resp_lang = 'hi'
    else:
        resp_lang = 'hi' if is_hindi else 'en'
    
    # Check for follow-up questions from previous context
    if hasattr(chatbot, 'is_asking_about_last_disease') and chatbot.is_asking_about_last_disease(user_input):
        if hasattr(chatbot, 'handle_followup'):
            response = chatbot.handle_followup(user_input, resp_lang)
            if response:
                return response
    
    # Main processing
    result = chatbot.process(user_input)
    
    disease = result.get('disease') or {}
    severity = float(result.get('confidence', 0.0))
    
    # Determine severity level
    if st.session_state.severity_slider >= 8:
        severity_level = 'high'
    elif st.session_state.severity_slider >= 5:
        severity_level = 'moderate'
    else:
        severity_level = 'low'
    
    # Override with ML confidence if available
    ml_confidence = float(result.get('confidence', 0.0))
    if ml_confidence > 0.7:
        severity_level = 'moderate'
    elif ml_confidence > 0.85:
        severity_level = 'high'
    
    st.session_state.current_disease = disease
    st.session_state.current_severity = severity_level
    
    # Extract disease info safely
    disease_name = disease.get('disease_name', 'a common condition')
    summary = disease.get('summary', 'I want to help you understand what might be going on.')
    source = result.get('source', 'Health analysis')
    
    # Build empathetic response
    response_parts = []
    
    # 1. Empathetic opening based on symptoms and severity
    empathetic_opening = get_empathetic_opening(severity_level, user_input)
    response_parts.append(empathetic_opening)
    response_parts.append("")  # spacing
    
    # 2. Validate their concerns
    validation = get_validating_response(disease_name)
    response_parts.append(validation)
    response_parts.append("")
    
    # 3. Share relevant health information (gentle, not alarming)
    if severity_level == 'high':
        response_parts.append(f"**What I'm noticing:** {summary[:300]}")
        response_parts.append("")
        response_parts.append(f"**Confidence in this assessment:** {ml_confidence:.0%}")
    else:
        response_parts.append(f"**What this might mean:** {summary[:250]}")
    
    response_parts.append("")
    
    # 4. Environmental context if available (helps understand triggers)
    if st.session_state.location:
        weather_data = weather_module.get_current_conditions(st.session_state.location)
        if weather_data:
            aqi = weather_data.get('aqi', 100)
            temp = weather_data.get('temperature', 25)
            humidity = weather_data.get('humidity', 50)
            
            risk, warnings = weather_module.calculate_risk(temp, aqi, humidity)
            
            response_parts.append("**🌤️ Environmental factors to consider:**")
            response_parts.append(f"• Temperature: {temp:.1f}°C | Humidity: {humidity:.0f}% | Air Quality: {aqi}")
            if warnings:
                response_parts.append(f"• {warnings[0]}")
            response_parts.append("")
    
    # 5. Natural follow-up question (builds conversation)
    followup = get_followup_question(st.session_state.conversation_context)
    response_parts.append(f"**To better understand:** {followup}")
    response_parts.append("")
    
    # 6. Gentle closing that invites more sharing
    closing = "💬 *Feel free to share more details when you're ready. I'm here to listen and help.*"
    response_parts.append(closing)
    
    return "\n\n".join(response_parts)

# ============================================
# CHAT INPUT
# ============================================
placeholder = get_text(ui_lang, 'input_placeholder')
user_input = st.chat_input(placeholder, key=get_key("chat_input"))

if voice_text and not user_input:
    user_input = voice_text

if user_input and user_input != st.session_state.last_input:
    st.session_state.last_input = user_input
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    
    with st.spinner("💭 Listening and understanding..."):
        response = process_user_input(user_input)
    
    st.session_state.messages.append({'role': 'assistant', 'content': response})
    st.rerun()

# ============================================
# QUICK ACTION BUTTONS
# ============================================
if st.session_state.current_disease and len(st.session_state.messages) > 0:
    st.divider()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.button(
            "💊 Precautions", 
            on_click=add_precautions,
            use_container_width=True,
            key=get_key("prec"),
            help="See steps that might help you feel better"
        )
    
    with col2:
        st.button(
            "🏥 Doctor Guidance", 
            on_click=add_doctor_info,
            use_container_width=True,
            key=get_key("doc"),
            help="Know when to seek professional care"
        )
    
    with col3:
        st.button(
            "🔍 Symptoms List", 
            on_click=add_symptoms,
            use_container_width=True,
            key=get_key("symp"),
            help="View common symptoms to track"
        )
    
    with col4:
        st.button(
            "📋 Full Details", 
            on_click=add_full_details,
            use_container_width=True,
            key=get_key("details"),
            help="Complete information about this condition"
        )
    
    with col5:
        if st.button("📄 PDF Report", use_container_width=True, key=get_key("pdf")):
            try:
                from fpdf import FPDF
                
                weather_data = None
                if st.session_state.location:
                    weather_data = weather_module.get_current_conditions(st.session_state.location)
                
                last_symptoms = "N/A"
                if len(st.session_state.messages) >= 2:
                    last_symptoms = st.session_state.messages[-2]['content']
                
                disease = st.session_state.current_disease
                pdf_path = generate_pdf_report(
                    disease, last_symptoms, 
                    st.session_state.get('current_severity', 'moderate'),
                    st.session_state.location, weather_data, ui_lang
                )
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download",
                        f,
                        file_name=f"health_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        key=get_key("download")
                    )
            except ImportError:
                st.warning("📦 PDF generation requires fpdf2. Run: `pip install fpdf2`")
            except Exception as e:
                st.warning(f"⚠️ Could not generate PDF: {str(e)}")

# ============================================
# FOOTER
# ============================================
disclaimer1 = get_text(ui_lang, 'disclaimer')
disclaimer2 = get_text(ui_lang, 'disclaimer2')
footer_text = get_text(ui_lang, 'footer')

st.divider()
st.caption(disclaimer1)
st.caption(disclaimer2)
st.caption(footer_text)