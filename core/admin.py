from django.contrib import admin
from .models import ChatbotEntry, PredictionRecord

@admin.register(ChatbotEntry)
class ChatbotEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'timestamp')

@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'symptoms', 'result', 'risk_level', 'timestamp')

