from django.db import models

class Survey(models.Model):
    name = models.CharField(max_length=5000, blank=True, default='')
    language = models.CharField(max_length=5000, blank=True, default='')
    consentText = models.CharField(max_length=10000, blank=True, default='')
    timelimitMinutes = models.IntegerField(default=60)
    active = models.BooleanField(default=True)

class Block(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    description = models.CharField(max_length=15000, blank=True, default='')
    title = models.CharField(max_length=5000, blank=True, default='')
    order = models.IntegerField(default=None)

class Question(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    name = models.CharField(max_length=5000, blank=True, default='')
    type = models.CharField(max_length=5000, blank=True, default='')
    description = models.CharField(max_length=5000, blank=True, default='')
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=None)

class SocialPostQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    articleURL = models.URLField(max_length=5000, blank=True, default='')
    articleTitle = models.CharField(max_length=5000, blank=True, default='')
    articleSource = models.CharField(max_length=5000, blank=True, default='')
    articleImageLink = models.CharField(max_length=5000, blank=True, default='')
    articleStyle = models.CharField(max_length=5000, blank=True, default='Twitter')
    articleSnippet = models.CharField(max_length=5000, blank=True, default='')
    articleLikes = models.IntegerField(default=0)
    articleComments = models.IntegerField(default=0)
    articleShares = models.IntegerField(default=0)
    articleCommentsOn = models.BooleanField(default=False)
    articleSharesOn = models.BooleanField(default=False)
    articleLikesOn = models.BooleanField(default=False)

class ButtonRowQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    numberButtons = models.IntegerField(default=0)

class ButtonQuestion(models.Model):
    buttonRow = models.ForeignKey(ButtonRowQuestion, on_delete=models.CASCADE)
    buttonText = models.CharField(max_length=5000, blank=True, default='')
    buttonType = models.CharField(max_length=5000, blank=True, default='')
    buttonIcon = models.CharField(max_length=5000, blank=True, default='')
    answered = models.BooleanField(default=False)

class TextboxQuestionNumber(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    query = models.IntegerField(default=0)
    textboxMax = models.IntegerField(default=0)
    textboxMin = models.IntegerField(default=0)

class TextboxQuestionText(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    query = models.CharField(max_length=5000, blank=True, default='')
    validate = models.BooleanField(default=False)
    textboxMax = models.IntegerField(default=0)
    textboxMin = models.IntegerField(default=0)

class TextboxQuestionDecimal(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    query = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    textboxMax = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    textboxMin = models.DecimalField(default=0, decimal_places=2, max_digits=8)

class MultiChoiceQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    options = models.IntegerField(default=0)
    isDropDown = models.BooleanField(default=False)
    isCheckbox = models.BooleanField(default=False)
    textboxMax = models.IntegerField(default=1)
    textboxMin = models.IntegerField(default=1)

class MultiChoice(models.Model):
    question = models.ForeignKey(MultiChoiceQuestion, on_delete=models.CASCADE)
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=True, default='')

class NumberScaleQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    minTitle = models.CharField(max_length=5000, blank=True, default='') 
    middleTitle = models.CharField(max_length=5000, blank=True, default='') 
    maxTitle = models.CharField(max_length=5000, blank=True, default='') 
    interval = models.IntegerField(default=0)
    numberMax = models.IntegerField(default=0)
    numberMin = models.IntegerField(default=0)

# not prioritsing the likert scale for now - will come back if we have time
"""
class LikertScaleQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    numberRows = models.IntegerField(default=None)
    numberChoices = models.IntegerField(default=None)
    #entry = models.CharField(max_length=500, blank=False, default='')
    #minTitle = models.CharField(max_length=5000, blank=False, default='') 
    #middleTitle = models.CharField(max_length=5000, blank=False, default='') 
    #maxTitle = models.CharField(max_length=5000, blank=False, default='') 

class LikertScaleRow(models.Model):
    question = models.ForeignKey(LikertScaleQuestion, on_delete=models.CASCADE) # associated with a likert q
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=False, default='')

class LikertScaleChoices(models.Model):
    question = models.ForeignKey(LikertScaleRow, on_delete=models.CASCADE) # associated with a likert q row
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=False, default='')
"""

class DragAndDropQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # choices are the categories for cards to be sorted into
    choices = models.IntegerField(default=0)
    # cards are the items that will be dragged and sorted
    cards = models.IntegerField(default=0)
    textboxMax = models.IntegerField(default=1)
    textboxMin = models.IntegerField(default=1)

class DragAndDropCard(models.Model):
    question = models.ForeignKey(DragAndDropQuestion, on_delete=models.CASCADE)
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=True, default='')

class DragAndDropChoice(models.Model):
    question = models.ForeignKey(DragAndDropQuestion, on_delete=models.CASCADE)
    order = models.IntegerField(default=None)
    title = models.CharField(max_length=5000, blank=True, default='')
