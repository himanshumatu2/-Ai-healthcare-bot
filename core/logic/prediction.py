def predict_disease(symptoms):
    symptoms = symptoms.lower()

    # VERY basic mock logic – replace with real ML model if needed
    if 'fever' in symptoms and 'cough' in symptoms:
        return "Flu", "Medium"
    elif 'headache' in symptoms and 'dizziness' in symptoms:
        return "Migraine", "Low"
    elif 'chest pain' in symptoms and 'shortness of breath' in symptoms:
        return "Heart Disease", "High"
    elif 'rash' in symptoms:
        return "Skin Allergy", "Low"
    else:
        return "Unknown", "Low"
