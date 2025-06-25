from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, ChatbotForm
from .models import ChatbotEntry, PredictionRecord


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def chatbot(request):
    answer = None
    if request.method == 'POST':
        form = ChatbotForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            responses = {
                "hello": "Hi! How can I assist you today?",
                "fever": "Please stay hydrated and consider seeing a doctor if fever persists.",
                "cough": "Try warm fluids and rest. If severe, consult a doctor.",
                "headache": "Headaches can be due to stress or dehydration. Rest and stay hydrated.",
            }
            response = next((resp for key, resp in responses.items() if key in question.lower()),
                            "I'm sorry, I can't answer that yet. Please consult a healthcare professional.")
            ChatbotEntry.objects.create(user=request.user, question=question, answer=response)
            answer = response
    else:
        form = ChatbotForm()
    return render(request, 'chatbot.html', {'form': form, 'answer': answer})


@login_required
def prediction(request):
    prediction = None
    advice = ""
    severity = "mild"
    emoji = "🟢"

    all_symptom_suggestions = [
        "Fever", "Cold", "Cough", "Headache", "Flu", "Body Ache", "Fatigue",
        "Sore Throat", "Shortness of Breath", "Chest Pain", "Dengue", "COVID-19",
        "Typhoid", "Pneumonia", "Heart Problem", "Heart Attack", "Cancer", "Migraine",
        "Rash", "Joint Pain", "Diarrhea", "Sweating", "Nausea", "Vomiting", "Abdominal Pain"
    ]

    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "").lower()

        conditions = {
            "Fever": ["fever", "temperature", "high temp", "warm body", "hot forehead"],
            "Viral Fever (वायरल बुखार)": ["viral fever", "sore throat", "fatigue", "runny nose", "body ache", "high temperature", "flu"],
            "Bacterial Fever": ["bacterial fever", "pus", "chills", "sweating", "headache", "persistent fever", "infection"],
            "Flu (Influenza)": ["flu", "cold", "fever", "cough", "chills", "body ache"],
            "COVID-19": ["covid", "corona", "loss of smell", "loss of taste", "sore throat", "breathless"],
            "Dengue": ["dengue", "rash", "joint pain", "muscle pain", "high fever", "platelets"],
            "Malaria": ["malaria", "sweating", "vomiting", "chills", "diarrhea"],
            "Typhoid": ["typhoid", "abdominal pain", "constipation", "weakness"],
            "Viral Infection": ["headache", "fatigue", "sneeze", "cold", "weakness", "viral"],
            "Chikungunya": ["chikungunya", "rash", "joint pain", "headache", "fever"],
            "Asthma": ["short breath", "tight chest", "wheezing", "asthma"],
            "Migraine": ["migraine", "nausea", "light sensitivity", "severe headache"],
            "Pneumonia": ["pneumonia", "chest pain", "wet cough", "breathing issue", "breath", "lung infection"],
            "Heart Problem": ["chest pain", "shortness of breath", "pressure", "left arm pain", "sweating"],
            "Heart Attack": ["chest pain", "left arm pain", "sweating", "pressure", "nausea"],
            "COPD": ["breath", "chronic cough", "fatigue"],
            "Food Poisoning": ["vomiting", "diarrhea", "stomach pain", "spoiled food", "nausea"],
            "Sinusitis": ["sinus", "nasal congestion", "facial pain", "pressure in head"],
            "Tuberculosis": ["persistent cough", "weight loss", "night sweats", "tb"],
            "Kidney Stones": ["side pain", "blood in urine", "pain while urinating"],
            "Appendicitis": ["lower abdominal pain", "vomiting", "no appetite"],
            "Chickenpox": ["blisters", "itching", "fatigue", "rash"],
            "Measles": ["measles", "rash", "runny nose", "fever"],
            "Hepatitis": ["jaundice", "yellow eyes", "fatigue", "abdominal swelling"],
            "Bronchitis": ["chest discomfort", "dry cough", "fatigue"],
            "Cancer (Possible Warning Signs)": ["unexplained weight loss", "lump", "fatigue", "persistent pain"],
            "Depression": ["hopeless", "sad", "loss of interest", "sleep issue"],
            "Anxiety": ["shaking", "sweating", "panic", "fear", "nervous"],
            "Diabetes": ["frequent urination", "thirst", "blurred vision", "slow healing"],
            "Hypertension": ["high bp", "dizziness", "nosebleeds", "blurred vision"],
            "Hypotension": ["low bp", "fainting", "blurred vision", "dizziness"],
            "Stroke": ["numbness", "slurred speech", "vision issue", "sudden confusion"],
            "Lupus": ["joint pain", "rash", "fatigue", "fever"],
            "Psoriasis": ["scaly rash", "itching", "red patches", "skin peeling"],
            "Eczema": ["dry skin", "itchy", "redness", "flare ups"],
        }

        matched = None
        for disease, keywords in conditions.items():
            match_count = sum(1 for keyword in keywords if keyword in symptoms)
            if match_count >= 2 or (match_count == 1 and disease.lower() in symptoms):
                matched = disease
                break

        if matched:
            prediction = f"🧠 Based on your symptoms, you might have <strong>{matched}</strong>. Please consult a doctor. Stay healthy!"

            if matched.lower() in ["heart attack", "heart problem", "cancer (possible warning signs)"]:
                severity = "danger"
                emoji = "🔴"
            elif matched.lower() in ["covid-19", "dengue", "pneumonia"]:
                severity = "warning"
                emoji = "🟡"
            else:
                severity = "mild"
                emoji = "🟢"

            if matched == "Dengue":
                advice += "🔍 Example: Fever, rash, joint pain → Likely Dengue<br>"
            if matched == "Pneumonia":
                advice += "🔍 Example: Cough, chest pain, breath → Likely Pneumonia<br>"
            if matched == "Heart Problem":
                advice += "🔍 Example: chest pain, short breath → Likely Heart Problem<br>"

            if "chest pain" in symptoms and "short" in symptoms or matched in ["Heart Attack", "Heart Problem", "Asthma", "Pneumonia", "COPD"]:
                advice += (
                    "<br><br>❤️ <strong>Important Note:</strong> Chest pain and shortness of breath could indicate serious issues like heart attack, angina, pneumonia, asthma, anxiety, or pulmonary embolism.<br>"
                    "👉 Seek immediate help if pain is severe or with nausea, sweating, or radiating to arm/neck."
                )
        else:
            prediction = "⚠️ We couldn't match your symptoms with a known disease. Please consult a doctor for diagnosis. Stay healthy!"

        if "fatigue" in symptoms or "headache" in symptoms:
            advice += (
                "<br><br>🧪 <strong>Note:</strong> Fatigue (थकान) and headache (सिरदर्द) are common in many viral infections like flu, dengue, COVID-19 etc.<br>"
                "• <strong>Fatigue is a common viral symptom.</strong><br>"
                "• <strong>Headache is also common in viral fevers.</strong>"
            )

        if "fever" in symptoms:
            advice += (
                "<br><br>🌡️ <strong>Fever</strong> means the body temperature is above 98.6°F (37°C).<br>"
                "It can be caused by infections (viral, bacterial), heat stroke, or other issues.<br>"
                "<strong>Hindi:</strong> बुखार शरीर का तापमान सामान्य से अधिक होने पर होता है। यह वायरस, बैक्टीरिया या अन्य कारणों से हो सकता है।"
            )

        PredictionRecord.objects.create(
            user=request.user,
            symptoms=symptoms,
            result=prediction,
            risk_level=severity.capitalize()
        )

    return render(request, 'prediction.html', {
        'prediction': f"{emoji} {prediction}" if prediction else None,
        'advice': advice,
        'severity': severity,
        'suggestions': all_symptom_suggestions
    })


@login_required
def map_view(request):
    return render(request, 'map.html')


@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    users = User.objects.all()
    chatbot_entries = ChatbotEntry.objects.all().order_by('-timestamp')[:10]
    predictions = PredictionRecord.objects.all().order_by('-timestamp')[:10]
    return render(request, 'dashboard.html', {
        'users': users,
        'chatbot_entries': chatbot_entries,
        'predictions': predictions
    })


@login_required
def profile(request):
    return render(request, 'profile.html')
