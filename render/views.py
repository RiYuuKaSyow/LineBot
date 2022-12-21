from django.shortcuts import render
from django.conf import settings
from django.http import (
    HttpResponse, HttpRequest, HttpResponseBadRequest
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import configparser
import logging
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import(
    MessageEvent, TextMessage, TextSendMessage,
)
#
lbApi = LineBotApi(settings.LINE_TOKEN)
handler = WebhookHandler(settings.LINE_SECRET)

def index(request):
    return HttpResponse(request)
    #return render( request, )

@csrf_exempt
@require_POST
def callback(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        return HttpResponseBadRequest()
    return HttpResponse('OK')

@handler.add(event=MessageEvent,message=TextMessage)
def handle_message(event):
    lbApi.reply_message(
        reply_token=event.reply_token,
        messages=TextSendMessage(text=event.messages.text)
    )