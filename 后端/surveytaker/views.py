from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.views import View
import json

from django.views.decorators.csrf import csrf_exempt

from surveytaker import models


class ResponseView(View):
    @csrf_exempt
    def post(self, request):
        """
       Add Response
       router：POST /api/v1/survey
       """

        json_bytes = request.body

        if not json_bytes:
            return HttpResponse(status=404)
        try:
            json_str = json_bytes.decode()
            response_dict = json.loads(json_str)
            if not response_dict.get("survey_id") or not response_dict.get("question_id"):
                return HttpResponse("Parameter not complete", status=500)

            response = models.Response.objects.create(
                survey_id=response_dict.get("survey_id"),
                question_id=response_dict.get("question_id"),
                contact_info=response_dict.get("contact_info"),
                content=response_dict.get("content"),
                identifier=response_dict.get("identifier")
            )

            if response:
                return JsonResponse({"data": "success"}, status=200)
            else:
                return JsonResponse({"data": "failed"}, status=500)
        except ValueError:
            return HttpResponse("Request mal-formatted", status=500)


class SurveyAPIView(View):
    @csrf_exempt
    def get(self, request):
        """
       Get specific survey
       Router: GET /api/v1/survey/{surveyID}
       """
        # Wait for group A finish their work

        json_str = """
               {
    "id": 5,
    "name": "Survey One!",
    "rtl": false,
    "totalNum": 5,
    "timelimitMinutes": -1,
    "active": true,
    "consent_required": true,
    "consentText": "This is the consent Text. If you agree with our protocol, you are allowed to proceed.",
    "block": [
        {
            "title": "QUESTION BLOCK 1",
            "questions": [
                {
                    "img": "https://storage.googleapis.com/soft3888/123.jpeg",
                    "newsTitle": "Sample News",
                    "newsDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ultrices eros in cursus turpis. Nibh venenatis cras sed felis eget velit aliquet sagittis id. Interdum posuere lorem ipsum dolor sit amet. Tristique senectus et netus et malesuada fames. Odio ut sem nulla pharetra diam sit amet. Netus et malesuada fames ac turpis egestas. Sit amet facilisis magna etiam. Praesent tristique magna sit amet purus. Viverra justo nec ultrices dui sapien eget mi.",
                    "name": "Question 1",
                    "type": "LIKERT",
                    "Required": false,
                    "order": 1,
                    "description": "How do you think the importance of these factors?",
                    "tableHead": [
                        {
                            "key": "category",
                            "title": "Category"
                        },
                        {
                            "key": "extreme",
                            "title": "Extreme Important"
                        },
                        {
                            "key": "very",
                            "title": "Very Important"
                        },
                        {
                            "key": "slight",
                            "title": "Slight Important"
                        },
                        {
                            "key": "not",
                            "title": "Not Important"
                        }
                    ],
                    "tableData": [
                        {
                            "category": "Your prior knowledge",
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio"
                        },
                        {
                            "category": "News source",
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio"
                        },
                        {
                            "category": "Headline claim",
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio"
                        },
                        {
                            "category": "Image associated with post",
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio"
                        },
                        {
                            "category": "Others",
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio",
                            "other_content": ""
                        }
                    ]
                },
                {
                    "img": "https://storage.googleapis.com/soft3888/morrison.jpeg",
                    "newsTitle": "Sample News",
                    "newsDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ultrices eros in cursus turpis. Nibh venenatis cras sed felis eget velit aliquet sagittis id. Interdum posuere lorem ipsum dolor sit amet. Tristique senectus et netus et malesuada fames. Odio ut sem nulla pharetra diam sit amet. Netus et malesuada fames ac turpis egestas. Sit amet facilisis magna etiam. Praesent tristique magna sit amet purus. Viverra justo nec ultrices dui sapien eget mi.",
                    "name": "Question 2",
                    "type": "SCALE",
                    "Required": false,
                    "order": 2,
                    "surveyTitle": "survey title",
                    "questionContents": "Please rank",
                    "rankNumber": 10
                },
                {
                    "img": "https://storage.googleapis.com/soft3888/trump.jpeg",
                    "newsTitle": "Sample News",
                    "newsDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ultrices eros in cursus turpis. Nibh venenatis cras sed felis eget velit aliquet sagittis id. Interdum posuere lorem ipsum dolor sit amet. Tristique senectus et netus et malesuada fames. Odio ut sem nulla pharetra diam sit amet. Netus et malesuada fames ac turpis egestas. Sit amet facilisis magna etiam. Praesent tristique magna sit amet purus. Viverra justo nec ultrices dui sapien eget mi.",
                    "name": "Question 3",
                    "type": "DRAG",
                    "Required": true,
                    "order": 3,
                    "description": "According to the material above, please classify whether the listed news are fake or authentic.",
                    "isExpanded": true,
                    "panels": [
                        {
                            "info": "News Waiting for classification",
                            "id": 0
                        },
                        {
                            "info": "Authentic class",
                            "id": 1
                        },
                        {
                            "info": "Fake class",
                            "id": 2
                        }
                    ],
                    "items": [
                        {
                            "id": 0,
                            "title": "People aged from 18 to 35 spend approximate 15 hours on average playing e-games every week",
                            "list": 0
                        },
                        {
                            "id": 1,
                            "title": "People aged from 36 to 45 spend approximate 15 hours on average playing e-games every week",
                            "list": 0
                        },
                        {
                            "id": 2,
                            "title": "People aged from 46 to 60 spend approximate 15 hours on average playing e-games every week",
                            "list": 0
                        }
                    ]
                },
                {
                    "img": "https://storage.googleapis.com/soft3888/uk.jpeg",
                    "newsTitle": "Sample News",
                    "newsDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ultrices eros in cursus turpis. Nibh venenatis cras sed felis eget velit aliquet sagittis id. Interdum posuere lorem ipsum dolor sit amet. Tristique senectus et netus et malesuada fames. Odio ut sem nulla pharetra diam sit amet. Netus et malesuada fames ac turpis egestas. Sit amet facilisis magna etiam. Praesent tristique magna sit amet purus. Viverra justo nec ultrices dui sapien eget mi.",
                    "name": "Question 4",
                    "type": "BTN",
                    "Required": false,
                    "order": 4,
                    "description": "After reading the news, do you want to share with your friends or like the contents or skip the news or even want to check the news? Click the button to make a decision",
                    "question_button": [
                        {
                            "title": "share"
                        },
                        {
                            "title": "like"
                        },
                        {
                            "title": "skip"
                        },
                        {
                            "title": "check"
                        }
                    ]
                },
                {
                    "img": "https://storage.googleapis.com/soft3888/123.jpeg",
                    "newsTitle": "Sample News",
                    "newsDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ultrices eros in cursus turpis. Nibh venenatis cras sed felis eget velit aliquet sagittis id. Interdum posuere lorem ipsum dolor sit amet. Tristique senectus et netus et malesuada fames. Odio ut sem nulla pharetra diam sit amet. Netus et malesuada fames ac turpis egestas. Sit amet facilisis magna etiam. Praesent tristique magna sit amet purus. Viverra justo nec ultrices dui sapien eget mi.",
                    "name": "Question 5",
                    "type": "MCQ",
                    "Required": true,
                    "order": 5,
                    "questionContents": "Q4 Description",
                    "options": [
                        {
                            "id": 0,
                            "option": "I think sharing the news improves my personal image",
                            "textField": "false"
                        },
                        {
                            "id": 1,
                            "option": "I want to share the news to my friends",
                            "textField": "false"
                        },
                        {
                            "id": 2,
                            "option": "I think the news is true",
                            "textField": "false"
                        },
                        {
                            "id": 3,
                            "option": "Other reasons",
                            "textField": "true"
                        }
                    ]
                }
            ]
        }
    ]
}
               """

        json_str2 = """
                       {
    "id": 5,
    "name": "Survey Two!",
    "rtl": true,
    "totalNum": 5,
    "timelimitMinutes": 2,
    "active": true,
    "consent_required": true,
    "consentText": "This is the consent Text. If you agree with our protocol, you are allowed to proceed.",
    "block": [
        {
            "title": "QUESTION BLOCK 1",
            "questions": [
                {
                    "img": "https://storage.googleapis.com/soft3888/123.jpeg",
                    "newsTitle": "عينة من الأخبار",
                    "newsDescription": "نيولا باراياتيور. أيكسسيبتيور ساينت أوككايكات كيوبايداتات نون بروايدينت ,سيونت ان كيولبا أيوتي أريري دولار إن ريبريهينديرأيت فوليوبتاتي فيلايت أيسسي كايلليوم دولار أيو فيجايت لوريم ايبسوم دولار سيت أميت ,كونسيكتيتور أدايبا يسكينج أليايت,سيت دو أيوسمود تيمبور أنكايديديونتيوت لابوري ات دولار ماجنا أليكيوا . يوت انيم أد مينيم فينايم,كيواس نوستريد أكسير سيتاشن يللأمكو لابورأس نيسي يت أليكيوب أكس أيا كوممودو كونسيكيوات . ديواس كيو أوفيسيا ديسيريونتموليت انيم أيدي ايست لابوريوم",
                    "name": "Question 1",
                    "type": "LIKERT",
                    "Required": true,
                    "order": 1,
                    "description": "كيف ترى أهمية هذه العوامل؟",
                    "tableHead": [
                        {
                            "key": "extreme",
                            "title": "مهم للغاية"
                        },
                        {
                            "key": "very",
                            "title": "مهم جدا"
                        },
                        {
                            "key": "slight",
                            "title": "طفيف مهم"
                        },
                        {
                            "key": "not",
                            "title": "غير مهم"
                        },
                        {
                            "key": "category",
                            "title": "فئة"
                        }
                    ],
                    "tableData": [
                        {
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio",
                            "category": "معرفتك المسبقة"
                        },
                        {
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio",
                            "category": "مصدر الأخبار"
                        },
                        {
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio",
                            "category": "مطالبة العنوان"
                        },
                        {
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio",
                            "category": "الصورة المرتبطة بالمشاركة"
                        },
                        {
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio",
                            "other_content": "",
                            "category": "آحرون"
                        }
                    ]
                },
                {
                    "img": "https://storage.googleapis.com/soft3888/morrison.jpeg",
                    "newsTitle": "Sample News",
                    "newsDescription": "نيولا باراياتيور. أيكسسيبتيور ساينت أوككايكات كيوبايداتات نون بروايدينت ,سيونت ان كيولبا أيوتي أريري دولار إن ريبريهينديرأيت فوليوبتاتي فيلايت أيسسي كايلليوم دولار أيو فيجايت لوريم ايبسوم دولار سيت أميت ,كونسيكتيتور أدايبا يسكينج أليايت,سيت دو أيوسمود تيمبور أنكايديديونتيوت لابوري ات دولار ماجنا أليكيوا . يوت انيم أد مينيم فينايم,كيواس نوستريد أكسير سيتاشن يللأمكو لابورأس نيسي يت أليكيوب أكس أيا كوممودو كونسيكيوات . ديواس كيو أوفيسيا ديسيريونتموليت انيم أيدي ايست لابوريوم",
                    "name": "Question 2",
                    "type": "SCALE",
                    "Required": false,
                    "order": 2,
                    "surveyTitle": "survey title",
                    "questionContents": "Please rank",
                    "rankNumber": 10
                },
                {
                    "img": "https://storage.googleapis.com/soft3888/uk.jpeg",
                    "newsTitle": "عينة من الأخبار",
                    "newsDescription": "نيولا باراياتيور. أيكسسيبتيور ساينت أوككايكات كيوبايداتات نون بروايدينت ,سيونت ان كيولبا أيوتي أريري دولار إن ريبريهينديرأيت فوليوبتاتي فيلايت أيسسي كايلليوم دولار أيو فيجايت لوريم ايبسوم دولار سيت أميت ,كونسيكتيتور أدايبا يسكينج أليايت,سيت دو أيوسمود تيمبور أنكايديديونتيوت لابوري ات دولار ماجنا أليكيوا . يوت انيم أد مينيم فينايم,كيواس نوستريد أكسير سيتاشن يللأمكو لابورأس نيسي يت أليكيوب أكس أيا كوممودو كونسيكيوات . ديواس كيو أوفيسيا ديسيريونتموليت انيم أيدي ايست لابوريوم.",
                    "type": "BTN",
                    "Required": true,
                    "order": 3,
                    "right_to_left": false,
                    "description": "بعد قراءة الخبر ، هل تريد مشاركته مع أصدقائك أو الإعجاب بالمحتويات أو تخطي الأخبار أو حتى تريد الاطلاع على الأخبار؟ انقر فوق الزر لاتخاذ قرار",
                    "question_button": [
                        {
                            "title": "شارك"
                        },
                        {
                            "title": "مثل"
                        },
                        {
                            "title": "يتخطى"
                        },
                        {
                            "title": "التحقق من"
                        },
                        {
                            "title": "تصميم حسب الطلب"
                        }
                    ]
                },
                {
                    "img": "https://storage.googleapis.com/soft3888/123.jpeg",
                    "newsTitle": "Sample News",
                    "newsDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ultrices eros in cursus turpis. Nibh venenatis cras sed felis eget velit aliquet sagittis id. Interdum posuere lorem ipsum dolor sit amet. Tristique senectus et netus et malesuada fames. Odio ut sem nulla pharetra diam sit amet. Netus et malesuada fames ac turpis egestas. Sit amet facilisis magna etiam. Praesent tristique magna sit amet purus. Viverra justo nec ultrices dui sapien eget mi.",
                    "name": "Question 4",
                    "type": "MCQ",
                    "Required": true,
                    "order": 4,
                    "questionContents": "Q4 Description",
                    "options": [
                        {
                            "id": 0,
                            "option": "I think sharing the news improves my personal image",
                            "textField": "false"
                        },
                        {
                            "id": 1,
                            "option": "I want to share the news to my friends",
                            "textField": "false"
                        },
                        {
                            "id": 2,
                            "option": "I think the news is true",
                            "textField": "false"
                        },
                        {
                            "id": 3,
                            "option": "Other reasons",
                            "textField": "true"
                        }
                    ]
                },
                {
                    "img": "https://storage.googleapis.com/soft3888/trump.jpeg",
                    "newsTitle": "Sample News",
                    "newsDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ultrices eros in cursus turpis. Nibh venenatis cras sed felis eget velit aliquet sagittis id. Interdum posuere lorem ipsum dolor sit amet. Tristique senectus et netus et malesuada fames. Odio ut sem nulla pharetra diam sit amet. Netus et malesuada fames ac turpis egestas. Sit amet facilisis magna etiam. Praesent tristique magna sit amet purus. Viverra justo nec ultrices dui sapien eget mi.",
                    "name": "Question 5",
                    "type": "DRAG",
                    "Required": true,
                    "order": 5,
                    "description": "According to the material above, please classify whether the listed news are fake or authentic.",
                    "isExpanded": true,
                    "panels": [
                        {
                            "info": "News Waiting for classification",
                            "id": 0
                        },
                        {
                            "info": "Authentic class",
                            "id": 1
                        },
                        {
                            "info": "Fake class",
                            "id": 2
                        }
                    ],
                    "items": [
                        {
                            "id": 0,
                            "title": "People aged from 18 to 35 spend approximate 15 hours on average playing e-games every week",
                            "list": 0
                        },
                        {
                            "id": 1,
                            "title": "People aged from 36 to 45 spend approximate 15 hours on average playing e-games every week",
                            "list": 0
                        },
                        {
                            "id": 2,
                            "title": "People aged from 46 to 60 spend approximate 15 hours on average playing e-games every week",
                            "list": 0
                        }
                    ]
                }
            ]
        }
    ]
}
                       """

        json_str2 = """
                       {
    "id": 5,
    "name": "Survey Two!",
    "rtl": true,
    "totalNum": 5,
    "timelimitMinutes": 5,
    "active": true,
    "consent_required": true,
    "consentText": "This is the consent Text. If you agree with our protocol, you are allowed to proceed.",
    "block": [
        {
            "title": "QUESTION BLOCK 1",
            "questions": [
                {
                    "img": "https://storage.googleapis.com/soft3888/123.jpeg",
                    "newsTitle": "عينة من الأخبار",
                    "newsDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ultrices eros in cursus turpis. Nibh venenatis cras sed felis eget velit aliquet sagittis id. Interdum posuere lorem ipsum dolor sit amet. Tristique senectus et netus et malesuada fames. Odio ut sem nulla pharetra diam sit amet. Netus et malesuada fames ac turpis egestas. Sit amet facilisis magna etiam. Praesent tristique magna sit amet purus. Viverra justo nec ultrices dui sapien eget mi.",
                    "name": "Question 1",
                    "type": "LIKERT",
                    "Required": true,
                    "order": 1,
                    "description": "كيف ترى أهمية هذه العوامل؟",
                    "tableHead": [
                        {
                            "key": "extreme",
                            "title": "مهم للغاية"
                        },
                        {
                            "key": "very",
                            "title": "مهم جدا"
                        },
                        {
                            "key": "slight",
                            "title": "طفيف مهم"
                        },
                        {
                            "key": "not",
                            "title": "غير مهم"
                        },
                        {
                            "key": "category",
                            "title": "فئة"
                        }
                    ],
                    "tableData": [
                        {
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio",
                            "category": "معرفتك المسبقة"
                        },
                        {
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio",
                            "category": "مصدر الأخبار"
                        },
                        {
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio",
                            "category": "مطالبة العنوان"
                        },
                        {
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio",
                            "category": "الصورة المرتبطة بالمشاركة"
                        },
                        {
                            "extreme": "radio",
                            "very": "radio",
                            "slight": "radio",
                            "not": "radio",
                            "other_content": "",
                            "category": "آحرون"
                        }
                    ]
                },
                {
                    "img": "https://storage.googleapis.com/soft3888/morrison.jpeg",
                    "newsTitle": "Sample News",
                    "newsDescription": "نيولا باراياتيور. أيكسسيبتيور ساينت أوككايكات كيوبايداتات نون بروايدينت ,سيونت ان كيولبا أيوتي أريري دولار إن ريبريهينديرأيت فوليوبتاتي فيلايت أيسسي كايلليوم دولار أيو فيجايت لوريم ايبسوم دولار سيت أميت ,كونسيكتيتور أدايبا يسكينج أليايت,سيت دو أيوسمود تيمبور أنكايديديونتيوت لابوري ات دولار ماجنا أليكيوا . يوت انيم أد مينيم فينايم,كيواس نوستريد أكسير سيتاشن يللأمكو لابورأس نيسي يت أليكيوب أكس أيا كوممودو كونسيكيوات . ديواس كيو أوفيسيا ديسيريونتموليت انيم أيدي ايست لابوريوم",
                    "name": "Question 2",
                    "type": "SCALE",
                    "Required": false,
                    "order": 2,
                    "surveyTitle": "survey title",
                    "questionContents": "Please rank",
                    "rankNumber": 10
                },
                {
                    "img": "https://storage.googleapis.com/soft3888/uk.jpeg",
                    "newsTitle": "عينة من الأخبار",
                    "newsDescription": "نيولا باراياتيور. أيكسسيبتيور ساينت أوككايكات كيوبايداتات نون بروايدينت ,سيونت ان كيولبا أيوتي أريري دولار إن ريبريهينديرأيت فوليوبتاتي فيلايت أيسسي كايلليوم دولار أيو فيجايت لوريم ايبسوم دولار سيت أميت ,كونسيكتيتور أدايبا يسكينج أليايت,سيت دو أيوسمود تيمبور أنكايديديونتيوت لابوري ات دولار ماجنا أليكيوا . يوت انيم أد مينيم فينايم,كيواس نوستريد أكسير سيتاشن يللأمكو لابورأس نيسي يت أليكيوب أكس أيا كوممودو كونسيكيوات . ديواس كيو أوفيسيا ديسيريونتموليت انيم أيدي ايست لابوريوم.",
                    "type": "BTN",
                    "Required": true,
                    "order": 3,
                    "right_to_left": false,
                    "description": "بعد قراءة الخبر ، هل تريد مشاركته مع أصدقائك أو الإعجاب بالمحتويات أو تخطي الأخبار أو حتى تريد الاطلاع على الأخبار؟ انقر فوق الزر لاتخاذ قرار",
                    "question_button": [
                        {
                            "title": "شارك"
                        },
                        {
                            "title": "مثل"
                        },
                        {
                            "title": "يتخطى"
                        },
                        {
                            "title": "التحقق من"
                        },
                        {
                            "title": "تصميم حسب الطلب"
                        }
                    ]
                },
                {
                    "img": "https://storage.googleapis.com/soft3888/123.jpeg",
                    "newsTitle": "Sample News",
                    "newsDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ultrices eros in cursus turpis. Nibh venenatis cras sed felis eget velit aliquet sagittis id. Interdum posuere lorem ipsum dolor sit amet. Tristique senectus et netus et malesuada fames. Odio ut sem nulla pharetra diam sit amet. Netus et malesuada fames ac turpis egestas. Sit amet facilisis magna etiam. Praesent tristique magna sit amet purus. Viverra justo nec ultrices dui sapien eget mi.",
                    "name": "Question 4",
                    "type": "MCQ",
                    "Required": true,
                    "order": 4,
                    "questionContents": "Q4 Description",
                    "options": [
                        {
                            "id": 0,
                            "option": "I think sharing the news improves my personal image",
                            "textField": "false"
                        },
                        {
                            "id": 1,
                            "option": "I want to share the news to my friends",
                            "textField": "false"
                        },
                        {
                            "id": 2,
                            "option": "I think the news is true",
                            "textField": "false"
                        },
                        {
                            "id": 3,
                            "option": "Other reasons",
                            "textField": "true"
                        }
                    ]
                },
                {
                    "img": "https://storage.googleapis.com/soft3888/trump.jpeg",
                    "newsTitle": "Sample News",
                    "newsDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ultrices eros in cursus turpis. Nibh venenatis cras sed felis eget velit aliquet sagittis id. Interdum posuere lorem ipsum dolor sit amet. Tristique senectus et netus et malesuada fames. Odio ut sem nulla pharetra diam sit amet. Netus et malesuada fames ac turpis egestas. Sit amet facilisis magna etiam. Praesent tristique magna sit amet purus. Viverra justo nec ultrices dui sapien eget mi.",
                    "name": "Question 5",
                    "type": "DRAG",
                    "Required": true,
                    "order": 5,
                    "description": "According to the material above, please classify whether the listed news are fake or authentic.",
                    "isExpanded": true,
                    "panels": [
                        {
                            "info": "News Waiting for classification",
                            "id": 0
                        },
                        {
                            "info": "Authentic class",
                            "id": 1
                        },
                        {
                            "info": "Fake class",
                            "id": 2
                        }
                    ],
                    "items": [
                        {
                            "id": 0,
                            "title": "People aged from 18 to 35 spend approximate 15 hours on average playing e-games every week",
                            "list": 0
                        },
                        {
                            "id": 1,
                            "title": "People aged from 36 to 45 spend approximate 15 hours on average playing e-games every week",
                            "list": 0
                        },
                        {
                            "id": 2,
                            "title": "People aged from 46 to 60 spend approximate 15 hours on average playing e-games every week",
                            "list": 0
                        }
                    ]
                }
            ]
        }
    ]
}
                       """

        link = request.get_full_path().replace("/api/st/survey/", "")

        try:
            survey = models.LinkGeneration.objects.get(link=link)
            if survey.survey_id == 1:
                print("2333333")
                return JsonResponse(json.loads(json_str), status=200)
            elif survey.survey_id == 2:
                return JsonResponse(json.loads(json_str2), status=200)
        except models.LinkGeneration.DoesNotExist:
            return HttpResponse(status=404)
