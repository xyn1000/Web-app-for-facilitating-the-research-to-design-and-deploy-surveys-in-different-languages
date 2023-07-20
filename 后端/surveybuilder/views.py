from django.shortcuts import render
from services.articledata import extract_article_metadata
from django.http.response import JsonResponse 
from rest_framework.parsers import JSONParser 
from rest_framework.renderers import JSONRenderer 
from rest_framework.decorators import api_view
from rest_framework import status

from surveybuilder.models import Survey, Block, Question, SocialPostQuestion, ButtonRowQuestion, ButtonQuestion, TextboxQuestionNumber, TextboxQuestionText, MultiChoiceQuestion, MultiChoice, NumberScaleQuestion, DragAndDropQuestion, DragAndDropChoice, DragAndDropCard
from surveybuilder.serializers import SurveySerializer, BlockSerializer, QuestionSerializer, SocialPostQuestionSerializer, ButtonRowQuestionSerializer, ButtonQuestionSerializer, TextboxQuestionNumberSerializer, TextboxQuestionTextSerializer, MultiChoiceSerializer, MultiChoiceQuestionSerializer, NumberScaleQuestionSerializer, DragAndDropChoiceSerializer, DragAndDropQuestionSerializer, DragAndDropCardSerializer

from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas

questionTypeSerializer = {
    "News post": SocialPostQuestionSerializer,
    "Button row": ButtonRowQuestionSerializer,
    "buttonquestion": ButtonQuestionSerializer,
    "Number entry": TextboxQuestionNumberSerializer,
    "Text entry": TextboxQuestionTextSerializer,
    "Multiple choice": MultiChoiceQuestionSerializer,
    "multichoice": MultiChoiceSerializer,
    "Number scale": NumberScaleQuestionSerializer,
    "Drag and drop": DragAndDropQuestionSerializer,
    "Drag and drop card": DragAndDropCardSerializer,
    "Drag and drop choice": DragAndDropChoiceSerializer
}

questionTypeModel = {
    "News post": SocialPostQuestion,
    "Button row": ButtonRowQuestion,
    "buttonquestion": ButtonQuestion,
    "Number entry": TextboxQuestionNumber,
    "Text entry": TextboxQuestionText,
    "Multiple choice": MultiChoiceQuestion,
    "multichoice": MultiChoice,
    "Number scale": NumberScaleQuestion,
    "Drag and drop": DragAndDropQuestion,
    "Drag and drop choice": DragAndDropChoice,
    "Drag and drop card": DragAndDropCard 
}

########## Survey related API function calls ##########

@api_view(['GET', 'POST'])
def survey_list(request):
    """
    get:
    Return all surveys within the database

    post:
    Include a new survey to the database
    """
    if request.method == 'GET':
        # GET all surveys
        surveys = Survey.objects.all()
        survey_serialized = SurveySerializer(surveys, many=True)
        return JsonResponse(survey_serialized.data, safe=False)
    elif request.method == 'POST':
        # POST a new survey!

        parsed_request = JSONParser().parse(request)
        survey_serialized = SurveySerializer(data = parsed_request)

        if survey_serialized.is_valid():
            survey_serialized.save()
            return JsonResponse(survey_serialized.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(survey_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def survey_data(request, id):
    """
    get:
    Get a specific survey and all nested data. This includes blocks, questions, questions types, and all relevant data.
    """
    try: 
        survey = Survey.objects.get(pk=id)
        blocks = Block.objects.filter(survey=survey.id)
    except Survey.DoesNotExist: 
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND) 
    
    # Transform data into python native
    survey_serialized = SurveySerializer(survey)
    blocks_serialized = BlockSerializer(blocks, many=True)
    # Extract data
    survey_data = survey_serialized.data
    survey_data['blocks'] = blocks_serialized.data[:]
    # Includes all question data
    for (i, bloc) in enumerate(blocks):
        questions = Question.objects.filter(block=bloc.id)
        questions_serialized = QuestionSerializer(questions, many=True)
        survey_data['blocks'][i]['questions'] = questions_serialized.data[:]
        # Includes all question subtype data
        for (i, ques) in enumerate(survey_data['blocks'][i]['questions']):
            questiontype = questionTypeModel[ques['type']].objects.get(question=ques['id'])
            questiontype_serialized = questionTypeSerializer[ques['type']](questiontype)
            ques['typedata'] = questiontype_serialized.data

            if ques['type'] == 'Multiple choice':
                multichoice = MultiChoiceQuestion.objects.get(question=ques['id'])
                choices = MultiChoice.objects.filter(question=multichoice.id)
                choicesSerialized = MultiChoiceSerializer(choices, many=True)
                ques['choices'] = choicesSerialized.data[:]
            elif ques['type'] == 'Button row':
                buttonrow = ButtonRowQuestion.objects.get(question=ques['id'])
                buttons = ButtonQuestion.objects.filter(buttonRow=buttonrow.id)
                buttonsSerialized = ButtonQuestionSerializer(buttons, many=True)
                ques['buttons'] = buttonsSerialized.data[:]

        
    return JsonResponse(survey_data, safe=False)

@api_view(['GET', 'PATCH', 'DELETE'])
def survey_info(request, id):
    """
    get:
    Get a specific survey by its ID

    patch:
    Update a specific survey by its ID

    delete:
    Remove a specific survey by its ID
    """
    try: 
        survey = Survey.objects.get(pk=id)
    except Survey.DoesNotExist: 
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET':
        # GET a specific survey

        survey_serialized = SurveySerializer(survey)
        return JsonResponse(survey_serialized.data)
    elif request.method == 'DELETE':
        # DELETE a specific survey

        survey.delete()
        return JsonResponse({'Message': 'The survey has been deleted.'}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PATCH':
        # UPDATE a specific survey

        parsed_request = JSONParser().parse(request)
        survey_serialized = SurveySerializer(survey, data=parsed_request, partial=True)
        
        if survey_serialized.is_valid():
            survey_serialized.save()
            return JsonResponse(survey_serialized.data) 
        return JsonResponse(survey_serialized.errors, status=status.HTTP_400_BAD_REQUEST) 

########## Block related API function calls ##########

@api_view(['GET', 'POST'])
def block_list(request, id):
    """
    get:
    Get all blocks within a survey

    post:
    Include a block to a given survey
    """
    try: 
        # Needs to include some sort of authentication check here
        survey = Survey.objects.get(pk=id)
    except Survey.DoesNotExist: 
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET':
        # GET list of blocks in a given survey
        
        blocks = Block.objects.filter(survey=survey.id)
        blocks_serialized = BlockSerializer(blocks, many=True)
        return JsonResponse(blocks_serialized.data, safe=False)
    elif request.method == 'POST':
        # POST a new block
        
        parsed_request = JSONParser().parse(request)
        parsed_request["survey"] = survey.id

        block_serialized = BlockSerializer(data = parsed_request)
        
        if block_serialized.is_valid():
            block_serialized.save()
            return JsonResponse(block_serialized.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(block_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PATCH'])
def block_info(request, id):
    """
    get:
    Get a specific blocks information by ID

    delete:
    Delete a specific block by ID

    patch:
    Update a blocks information
    """
    try:
        blocks = Block.objects.get(pk = id)
    except Block.DoesNotExist:
        return JsonResponse({'Message': 'The block can\'t be found.'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET':
        # GET a specific block
        block_serialized = BlockSerializer(blocks)
        return JsonResponse(block_serialized.data)

    elif request.method == 'DELETE':
        # DELETE a specific block
        blocks.delete()
        return JsonResponse({'Message': 'The block has been deleted.'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        # Update a specific block

        parsed_request = JSONParser().parse(request)
        block_serialized = BlockSerializer(blocks, data=parsed_request, partial=True)
        
        if block_serialized.is_valid():
            block_serialized.save()
            return JsonResponse(block_serialized.data) 
        return JsonResponse(block_serialized.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST'])
def duplication_block(request, id):
    """
    post:
    Takes an existing block ID and duplicates it
    {
      order: "include order for the new block object"
    }
    """
    try: 
        block = Block.objects.get(pk=id)
    except Block.DoesNotExist: 
        return JsonResponse({'Message': 'The block can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # parse request information to find new question order
        parsed_request = JSONParser().parse(request)

        # get all question references to the block
        questionsInBlock = Question.objects.filter(block = block.id)

        # save a new block with the desired order
        try:
            block.id = None
            block.order = parsed_request['order']
            block.save()
        except Exception as e:
            return JsonResponse({'Message': f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

        for question in questionsInBlock:
            print("New question being handled")
            
            # create a copy of the subtype information
            questionTypeInformation = questionTypeModel[question.type].objects.get(question = question.id)

            # if multi-choice or button-row get sub-sub-type information
            if (question.type == "Multiple choice"):
                # get a copy of all choices
                choices = MultiChoice.objects.filter(question = questionTypeInformation.id)
            elif (question.type == "Button row"):
                # get a copy of all buttons
                buttons = ButtonQuestion.objects.filter(buttonRow = questionTypeInformation.id)

            # create a copy of the question information
            question.id = None
            questionTypeInformation.id = None

            question.block = block

            try:
                question.save()
                questionTypeInformation.question = question
                questionTypeInformation.save()

                if (question.type == "Multiple choice"):
                    for entry in choices:
                        entry.id = None
                        entry.question = questionTypeInformation
                        entry.save()
                elif (question.type == "Button row"):
                    for entry in buttons:
                        entry.id = None
                        entry.buttonRow = questionTypeInformation
                        entry.save()

            except Exception as e:
                return JsonResponse({'Message': f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

        block_serialized = BlockSerializer(block)
        return JsonResponse(block_serialized.data, status=status.HTTP_201_CREATED, safe=False)


########## Question related API function calls ##########

@api_view(['GET', 'POST'])
def question_list(request, id):
    """
    get:
    Get all questions within a specific block

    post:
    Include a question into a specific block, this automatically creates the question subtype as well
    """
    try:
        # Needs to include some sort of authentication check here
        block = Block.objects.get(pk=id)
    except Block.DoesNotExist: 
        return JsonResponse({'Message': 'The block can\'t be found.'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'GET':
        # GET list of blocks in a block
        
        questions = Question.objects.filter(block=block.id)
        questions_serialized = QuestionSerializer(questions, many=True)
        return JsonResponse(questions_serialized.data, safe=False)
    elif request.method == 'POST':
        # POST new question to the block
        
        parsed_request = JSONParser().parse(request)
        parsed_request["block"] = block.id

        if parsed_request["type"] not in questionTypeSerializer:
            return JsonResponse({'Message': 'Incorrect question type.'}, status=status.HTTP_400_BAD_REQUEST) 

        question_serialized = QuestionSerializer(data = parsed_request)
        
        if question_serialized.is_valid():
            question_serialized.save()
        else:
            JsonResponse(question_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Create an empty question
        questionType_data = {"question": question_serialized.data['id']}
        # Try serialize it..
        questionType_serialized_data = questionTypeSerializer[question_serialized.data['type']](data = questionType_data)

        if questionType_serialized_data.is_valid():
            questionType_serialized_data.save() 
        else:
            return JsonResponse(questionType_serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse(question_serialized.data, status=status.HTTP_201_CREATED) 

@api_view(['POST'])
def duplication_question(request, id):
    """
    post:
    Takes an existing question ID and duplicates it
    {
      order: "include order for the new question object"
    }
    """
    try: 
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist: 
        return JsonResponse({'Message': 'The question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # parse request information to find new question order
        parsed_request = JSONParser().parse(request)

        # create a copy of the subtype information
        questionTypeInformation = questionTypeModel[question.type].objects.get(question = question.id)

        # if multi-choice or button-row get sub-sub-type information
        if (question.type == "Multiple choice"):
            # get a copy of all choices
            choices = MultiChoice.objects.filter(question = questionTypeInformation.id)
        elif (question.type == "Button row"):
            # get a copy of all buttons
            buttons = ButtonQuestion.objects.filter(buttonRow = questionTypeInformation.id)

        # create a copy of the question information
        question.id = None
        questionTypeInformation.id = None

        try:
            question.order = parsed_request['order']
            question.save()
            questionTypeInformation.question = question
            questionTypeInformation.save()
            if (question.type == "Multiple choice"):
                for entry in choices:
                    entry.id = None
                    entry.question = questionTypeInformation
                    entry.save()
            elif (question.type == "Button row"):
                for entry in buttons:
                    entry.id = None
                    entry.buttonRow = questionTypeInformation
                    entry.save()
        except Exception as e:
            return JsonResponse({'Message': f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

        question_serialized = QuestionSerializer(question)
        return JsonResponse(question_serialized.data, status=status.HTTP_201_CREATED, safe=False)
    

@api_view(['GET', 'PATCH', 'DELETE'])
def question_info(request, id):
    """
    get:
    Get all question information by a specific ID

    patch:
    Update a questions information given its ID

    delete:
    Remove a question by ID
    """
    try: 
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist: 
        return JsonResponse({'Message': 'The question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET':
        # GET a specific question

        question_serialized = QuestionSerializer(question)
        questiontype = questionTypeModel[question_serialized.data['type']].objects.get(question=question.id)
        questiontype_serialized = questionTypeSerializer[question_serialized.data['type']](questiontype)

        question_data = question_serialized.data
        question_data['type'] = questiontype_serialized.data

        return JsonResponse(question_data, safe=False)
    elif request.method == 'DELETE':
        # DELETE a specific question

        question.delete()
        return JsonResponse({'Message': 'The question has been deleted.'}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PATCH':
        # UPDATE a specific question

        parsed_request = JSONParser().parse(request)
        question_serialized = QuestionSerializer(question, data=parsed_request, partial=True)
        
        if question_serialized.is_valid():
            question_serialized.save()
            return JsonResponse(question_serialized.data) 
        return JsonResponse(question_serialized.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['PATCH'])
def question_inner(request, id):
    """
    patch:
    Update question subtype information by ID
    """
    try: 
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        return JsonResponse({'Message': 'The question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    # Parse the request passed through
    parsed_request = JSONParser().parse(request)
        
    # Associate the ID key to a questions data and find its type
    question_serialized = QuestionSerializer(question)
    questiontype = questionTypeModel[question_serialized.data['type']].objects.get(question=question.id)

    # Serialize the request 
    parsed_request_serialized = questionTypeSerializer[question_serialized.data['type']](questiontype, data = parsed_request, partial = True)

    if parsed_request_serialized.is_valid():
        parsed_request_serialized.save()
        return JsonResponse(parsed_request_serialized.data)
    return JsonResponse(parsed_request_serialized.errors, status=status.HTTP_400_BAD_REQUEST)         

########## SocialMedia Question related API function calls ##########

# Has to be a POST request due to issues in axios not being able to send data in GET
# See: https://stackoverflow.com/questions/46404051/send-object-with-axios-get-request

@api_view(['POST'])
def article_information(request):
    """
    post:
    Given a link, return all relevent metadata
    """
    try:
        parsed_request = JSONParser().parse(request)
        link = parsed_request['link']
    except Exception:
        return JsonResponse({'Message': 'Bad link.'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'POST':
        articleData = extract_article_metadata(link)
        return JsonResponse(articleData, safe=False)

########## Buttonrow Question related API function calls ##########

@api_view(['GET','POST','DELETE','PATCH'])
def buttonrow_data(request, id):
    """
    get:
    Given a buttonrow entity ID, return the entity and its buttons

    post:
    Include a new button entity to a buttonrow entity

    delete:
    Delete a button entity from a buttonrow entity

    patch:
    Update a button entity from a buttonrow entity
    """
    try:
        buttonrowQuestion = ButtonRowQuestion.objects.get(pk=id)
    except ButtonRowQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The buttonrow can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a buttonrow questions information
        buttonrowQuestionSerialized = ButtonRowQuestionSerializer(buttonrowQuestion)
        buttons = ButtonQuestion.objects.filter(buttonRow=id)
        buttonsSerialized = ButtonQuestionSerializer(buttons, many=True)

        # Include all button information to the buttonrow data
        buttonrow_data = buttonrowQuestionSerialized.data
        buttonrow_data['buttons'] = buttonsSerialized.data[:]

        return JsonResponse(buttonrow_data)
    elif request.method == 'POST':
        # POST a button to the buttonrow question

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['buttonRow'] = buttonrowQuestion.id
        button_serialized = ButtonQuestionSerializer(data = parsed_request)

        # save the button input
        if button_serialized.is_valid():
            button_serialized.save()
        else:
            return JsonResponse(button_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        # increment the buttonrow counter
        try:
            buttonrowQuestion.numberButtons += 1
            buttonrowQuestion.save()
            return JsonResponse(button_serialized.data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'Message': 'Couldnt increment buttonrow count.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE a button from the button row

        # Expects an object like such {"id": <to-be-deleted>} for the button
        parsed_request = JSONParser().parse(request)
        button_id = parsed_request['id']

        try:
            buttons = ButtonQuestion.objects.get(id=button_id)
            buttons.delete()
            buttonrowQuestion.numberButtons -= 1
            buttonrowQuestion.save()
        except:
            JsonResponse({'Message': 'Couldnt delete the button.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse({'Message': 'Successfully deleted the button'}, status=status.HTTP_204_NO_CONTENT) 

    elif request.method == 'PATCH':
        # UPDATE an existing button within the button row

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['buttonRow'] = buttonrowQuestion.id

        # fetch the preexisting object and check incoming request
        button = ButtonQuestion.objects.get(id=parsed_request['id'])
        button_serialized = ButtonQuestionSerializer(button, data = parsed_request)

        # save the button input
        if button_serialized.is_valid():
            button_serialized.save()
            return JsonResponse(button_serialized.data)
        else:
            return JsonResponse(button_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

########## Multi-choice Question related API function calls ##########

@api_view(['GET','POST','DELETE','PATCH'])
def choices_data(request, id):
    """
    get:
    Given a multiplechoice entity ID, return the entity and its choices

    post:
    Include a new choice entity to a multiplechoice entity

    delete:
    Delete a choice entity from a multiplechoice entity

    patch:
    Update a choice entity from a multiplechoice entity
    """
    try:
        multiChoiceQuestion = MultiChoiceQuestion.objects.get(pk=id)
    except MultiChoiceQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The multiplechoice question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a multichoice questions information
        multiChoiceQuestionSerialized = MultiChoiceQuestionSerializer(multiChoiceQuestion)

        choices = MultiChoice.objects.filter(question=id)
        choicesSerialized = MultiChoiceSerializer(choices, many=True)

        # Include all button information to the multichoice data
        multi_data = multiChoiceQuestionSerialized.data
        multi_data['choices'] = choicesSerialized.data[:]
        
        return JsonResponse(multi_data)
    elif request.method == 'POST':
        # POST a choice to the multiplechoice question

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = multiChoiceQuestion.id
        choice_serialized = MultiChoiceSerializer(data = parsed_request)

        # save the button input
        if choice_serialized.is_valid():
            choice_serialized.save()
        else:
            return JsonResponse(choice_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        # increment the buttonrow counter
        try:
            multiChoiceQuestion.options += 1
            multiChoiceQuestion.save()
            return JsonResponse(choice_serialized.data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'Message': 'Couldnt increment multichoice count.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE a button from the button row

        # Expects an object like such {"id": <to-be-deleted>} for the button
        parsed_request = JSONParser().parse(request)
        multichoice_id = parsed_request['id']

        try:
            choice = MultiChoice.objects.get(id=multichoice_id)
            choice.delete()
            multiChoiceQuestion.options -= 1
            multiChoiceQuestion.save()
        except:
            JsonResponse({'Message': 'Couldnt delete the choice.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse({'Message': 'Successfully deleted the choice'}, status=status.HTTP_204_NO_CONTENT) 

    elif request.method == 'PATCH':
        # UPDATE an existing button within the button row

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = multiChoiceQuestion.id

        # fetch the preexisting object and check incoming request
        choice = MultiChoice.objects.get(id=parsed_request['id'])
        choice_serialized = MultiChoiceSerializer(choice, data = parsed_request)

        # save the button input
        if choice_serialized.is_valid():
            choice_serialized.save()
            return JsonResponse(choice_serialized.data)
        else:
            return JsonResponse(choice_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


########## Drag and Drop Question related API function calls ##########

@api_view(['GET','POST','DELETE','PATCH'])
def dragdropcard_data(request, id):
    """
    get:
    Given a drag and drop entity ID, return the entity and its cards

    post:
    include a new card entity

    delete:
    delete a card entity

    patch:
    update a card entity
    """
    try:
        dragdropQuestion = DragAndDropQuestion.objects.get(pk=id)
    except DragAndDropQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The Drag and Drop question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a drag and drop question's card information
        dragAndDropQuestionSerialized = DragAndDropQuestionSerializer(dragdropQuestion)

        cards = DragAndDropChoice.objects.filter(question=id)
        cardsSerialized = DragAndDropCardSerializer(cards, many=True)

        # Include all choice information to the drag and drop data
        multi_data = dragAndDropQuestionSerialized.data
        multi_data['cards'] = cardsSerialized.data[:]
        
        return JsonResponse(multi_data)
    elif request.method == 'POST':
        # POST a card to the drag and drop question

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = dragdropQuestion.id
        card_serialized = DragAndDropCardSerializer(data = parsed_request)

        # save the button input
        if card_serialized.is_valid():
            card_serialized.save()
        else:
            return JsonResponse(card_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        # increment the buttonrow counter
        try:
            dragdropQuestion.cards += 1
            dragdropQuestion.save()
            return JsonResponse(card_serialized.data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'Message': 'Couldnt increment card count for drag and drop question.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE a choice from the drag and drop

        # Expects an object like such {"id": <to-be-deleted>} for the button
        parsed_request = JSONParser().parse(request)
        card_id = parsed_request['id']

        try:
            card = DragAndDropCard.objects.get(id=card_id)
            card.delete()
            dragdropQuestion.cards -= 1
            dragdropQuestion.save()
        except:
            JsonResponse({'Message': 'Couldnt delete the card from the drag and drop question.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse({'Message': 'Successfully deleted the card from the drag and drop question.'}, status=status.HTTP_204_NO_CONTENT) 

    elif request.method == 'PATCH':
        # UPDATE an existing card within the drag and drop question

        # parse the card input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = dragdropQuestion.id

        # fetch the preexisting object and check incoming request
        card = DragAndDropChoice.objects.get(id=parsed_request['id'])
        card_serialized = DragAndDropCardSerializer(card, data = parsed_request)

        # save the choice input
        if card_serialized.is_valid():
            card_serialized.save()
            return JsonResponse(card_serialized.data)
        else:
            return JsonResponse(card_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST','DELETE','PATCH'])
def dragdropchoice_data(request, id):
    """
    get:
    Given a drag and drop entity ID, return the entity and its choices 

    post:
    Include a new choice entity to a drag and drop entity

    delete:
    Delete a choice entity from a drag and drop entity

    patch:
    Update a choice entity from a drag and drop entity 
    """
    try:
        dragdropQuestion = DragAndDropQuestion.objects.get(pk=id)
    except DragAndDropQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The Drag and Drop question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a drag and drop question's choice information
        dragAndDropQuestionSerialized = DragAndDropQuestionSerializer(dragdropQuestion)

        choices = DragAndDropChoice.objects.filter(question=id)
        choicesSerialized = DragAndDropChoiceSerializer(choices, many=True)

        # Include all choice information to the drag and drop data
        multi_data = dragAndDropQuestionSerialized.data
        multi_data['choices'] = choicesSerialized.data[:]
        
        return JsonResponse(multi_data)
    elif request.method == 'POST':
        # POST a choice to the drag and drop question

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = dragdropQuestion.id
        choice_serialized = DragAndDropChoiceSerializer(data = parsed_request)

        # save the button input
        if choice_serialized.is_valid():
            choice_serialized.save()
        else:
            return JsonResponse(choice_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        # increment the buttonrow counter
        try:
            dragdropQuestion.choices += 1
            dragdropQuestion.save()
            return JsonResponse(choice_serialized.data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'Message': 'Couldnt increment choice count for drag and drop question.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE a choice from the drag and drop

        # Expects an object like such {"id": <to-be-deleted>} for the button
        parsed_request = JSONParser().parse(request)
        choice_id = parsed_request['id']

        try:
            choice = DragAndDropChoice.objects.get(id=choice_id)
            choice.delete()
            dragdropQuestion.choices -= 1
            dragdropQuestion.save()
        except:
            JsonResponse({'Message': 'Couldnt delete the choice from the drag and drop question.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse({'Message': 'Successfully deleted the choice from the drag and drop question.'}, status=status.HTTP_204_NO_CONTENT) 

    elif request.method == 'PATCH':
        # UPDATE an existing choice within the drag and drop question

        # parse the choice input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = dragdropQuestion.id

        # fetch the preexisting object and check incoming request
        choice = DragAndDropChoice.objects.get(id=parsed_request['id'])
        choice_serialized = DragAndDropChoiceSerializer(choice, data = parsed_request)

        # save the choice input
        if choice_serialized.is_valid():
            choice_serialized.save()
            return JsonResponse(choice_serialized.data)
        else:
            return JsonResponse(choice_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


########## Documentation API function call ##########

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    """
    get:
    API Documentation
    """
    generator = schemas.SchemaGenerator(title='Survey API')
    return response.Response(generator.get_schema(request=request))