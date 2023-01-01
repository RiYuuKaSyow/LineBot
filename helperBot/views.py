from django.shortcuts import render
from django.conf import settings
from django.http import (
    HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseForbidden
)
from .models import Reply
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import configparser
import logging
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import(
    MessageEvent, TextMessage,
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
        return HttpResponseForbidden()
    return HttpResponse('OK')

@handler.add(event=MessageEvent,message=TextMessage)
def handle_message(event):
    msg = event.message.text.split('#') 
    if msg[0] != '':
        cmd = msg[0]
        if len(msg) < 4:
            duration = 3
        if len(msg) < 3:
            location = ''
        rpy = Reply(cmd=cmd, auth=settings.WEATHER_AUTH, location=location, duration=duration)
        if rpy.exist == False:
            return
        rpy.reply(event,lbApi)
    return

#    lbApi.reply_message(
#        reply_token=event.reply_token,
#        messages=TextSendMessage(text=event.messages.text)
#    )
#    return