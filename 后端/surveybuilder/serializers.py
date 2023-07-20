from rest_framework import serializers
from surveybuilder.models import Survey, Block, Question, SocialPostQuestion, ButtonRowQuestion, ButtonQuestion, TextboxQuestionDecimal, TextboxQuestionNumber, TextboxQuestionText, MultiChoiceQuestion, MultiChoice, NumberScaleQuestion, DragAndDropQuestion, DragAndDropChoice, DragAndDropCard

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'name', 'language', 'consentText', 'timelimitMinutes', 'active']

class BlockSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(max_value=2147483647, min_value=0, required=True)

    class Meta:
        model = Block
        fields = ['id', 'survey', 'title', 'description', 'order']
        extra_kwargs = {'description': {'required': False}}

class QuestionSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(max_value=2147483647, min_value=0, required=True)
    
    class Meta:
        model = Question
        fields = ['id', 'block', 'name', 'type', 'description', 'required', 'order']

class SocialPostQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialPostQuestion
        fields = ['id', 'question', 'articleURL', 
            'articleTitle', 'articleSource', 'articleImageLink', 'articleStyle',
            'articleSnippet', 'articleLikes', 'articleComments', 'articleShares',
            'articleCommentsOn', 'articleSharesOn', 'articleLikesOn']

class ButtonRowQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ButtonRowQuestion
        fields = ['id', 'question', 'numberButtons']

class ButtonQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ButtonQuestion
        fields = ['id', 'buttonRow', 'buttonText', 
            'buttonType', 'buttonIcon', 'answered']

class TextboxQuestionNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextboxQuestionNumber
        fields = ['id', 'question', 'query', 
            'textboxMax', 'textboxMin']

class TextboxQuestionTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextboxQuestionText
        fields = ['id', 'question', 'query', 
            'textboxMax', 'textboxMin']

class TextboxQuestionDecimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextboxQuestionDecimal
        fields = ['id', 'question', 'query', 
            'textboxMax', 'textboxMin']

class MultiChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiChoice
        fields = ['id', 'question', 'order', 'title']

class MultiChoiceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultiChoiceQuestion
        fields = ['id', 'question', 'options', 'isDropDown',
            'isCheckbox', 'textboxMax', 'textboxMin']

class NumberScaleQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumberScaleQuestion
        fields = ['id', 'question', 'minTitle', 'middleTitle',
            'maxTitle', 'interval', 'numberMax', 'numberMin']

class DragAndDropChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DragAndDropChoice
        fields = ['id', 'question', 'order', 'title']

class DragAndDropCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DragAndDropCard
        fields = ['id', 'question', 'order', 'title']

class DragAndDropQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DragAndDropQuestion
        fields = ['id', 'question', 'choices', 'cards', 
            'textboxMax', 'textboxMin'] 