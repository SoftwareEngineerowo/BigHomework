import asyncio
import json
import uuid

from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from erniebot_agent.memory import HumanMessage, AIMessage, SystemMessage, FunctionMessage

from aibot.models import AIBot, AIBotSerializer
from ocr.models import OCRModel
from server.settings import MSG_LENGTH, ERNIE_MODEL
from util.encoder import Encoder
from util.prompts import ASSISTANT, mkCommentPrompt, COMMENT, mkMarkPrompt, MARK
from util.tools import functions


class AIBotViewSet(viewsets.ModelViewSet):
    queryset = AIBot.objects.all()
    serializer_class = AIBotSerializer

    @action(methods=['put'], detail=False, url_path='assistant')
    def assistant(self, request):
        """AI 助手实现"""
        data = dict(request.data.copy())
        print(">>> assistant::data:", data)
        if 'sysId' not in data.keys():
            return Response('sysId Required', status=status.HTTP_400_BAD_REQUEST)
        if data['sysId'] == '' or data['sysId'] is None:
            return Response('sysId Required', status=status.HTTP_400_BAD_REQUEST)

        sysId = data['sysId'][0]
        fresh = int(data['fresh'][0])
        num = getNum(sysId)
        hu_msg = {'sysId': str(data['sysId'][0]),
                  'num': int(num),
                  'typ': 1,
                  'content': str(data['content'][0])
                  }

        addMsg(self, hu_msg)

        msgHistory = []
        fresh = 1
        if fresh == 0:
            # load msg history
            msgs = getHistory(sysId, 1)
            print(">>> msgs len:", len(msgs))
            if len(msgs) % 2 == 1:
                pt = 0
                for msg in msgs:
                    print(msg.__dict__)
                    pt += 1
                    if (pt % 2 == 0 and msg.__dict__['typ'] == 1) or (
                            pt % 2 == 1 and msg.__dict__['typ'] == 0):  # 偶数项必须是 AI MSG
                        break
                    prompt = msg.__dict__['content']
                    if msg.__dict__['typ'] == 0:
                        msgHistory.append(AIMessage(prompt))
                    else:
                        msgHistory.append(HumanMessage(prompt))
        else:
            prompt = hu_msg['content']
            print(">>> prompt:", prompt)
            msgHistory = [HumanMessage(prompt)]
        msgHistory.reverse()

        resp = asyncio.run(talk(msgHistory, ASSISTANT.content, functions))
        print(">>> resp:", resp)

        # add ai msg
        ai_msg = {'sysId': sysId,
                  'num': int(num + 1),
                  'typ': 0,
                  'content': str(resp.content)
                  }
        addMsg(self, ai_msg)

        return Response(str(resp.content), status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='history')
    def history(self, request):
        """返回历史记录"""
        # 获取数据
        data = request.data.copy()
        sysId = str(data['sysId'])
        pageNum = int(data['pageNum'])
        if sysId is None:
            return Response('sysId Required', status=status.HTTP_400_BAD_REQUEST)
        if pageNum is None:
            return Response('pageNum Required', status=status.HTTP_400_BAD_REQUEST)

        # 查询
        res = getHistory(sysId, pageNum)
        print(">>> history::res:", res)
        history = res
        if res is not None:
            history.reverse()
        print(">>> history::resp:", history, '\n>>> type:', type(history))
        history = json.dumps(history, cls=Encoder, ensure_ascii=False)
        return HttpResponse(history, content_type='application/json', status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='comment')
    def mkComment(self, request):
        """获取 AI 评价"""
        data = dict(request.data.copy())
        crt = None
        cnt = int(data['count'][0])  # 评价数量
        ques = str(data['question'])  # 问题
        ans = str(data['answer'])  # 学生作答
        if 'crt' in data.keys():
            crt = str(data['correct'])  # 参考答案
        msgs = [HumanMessage(mkCommentPrompt(ques, ans, crt, cnt))]
        resp = asyncio.run(talk(msgs, COMMENT.content, [])).content.replace('\n', '').replace('\r', '').replace(
            '\t', '').replace('\\', '').replace(' ', '')
        resp = resp.split('```json')[1].split('```')[0]
        print(">>> resps:", resp)
        return HttpResponse(resp, content_type='application/json', status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='mark')
    def mkMark(self, request):
        """AI 评分"""
        data = dict(request.data.copy())
        ques = str(data['question'])  # 问题
        ans = str(data['answer'])  # 作答
        full = str(data['full'])  # 总分
        crt = None
        if 'crt' in data.keys():
            crt = str(data['correct'])  # 参考答案
        msgs = [HumanMessage(mkMarkPrompt(ques, ans, crt, full))]
        resp = ''
        while '```json ' not in resp:
            resp = asyncio.run(talk(msgs, MARK.content, [])).content.replace('\n', ' ').replace('\r', ' ').replace('\t',
                                                                                                                   ' ')
        resp = resp.split('```json ')[1].split(' ```')[0]
        print(">>> resp:", resp)
        return HttpResponse(resp, content_type='application/json', status=status.HTTP_200_OK)


async def talk(msgs, system, funcs):
    print(">>> talk:", msgs)
    ai_message = await ERNIE_MODEL.chat(messages=msgs, system=system, functions=funcs)
    print(">>> ai_message:", ai_message)
    return ai_message


def addMsg(self, data):
    """添加聊天记录"""
    ser = self.get_serializer(data=data)
    ser.is_valid(raise_exception=False)
    print(">>> addMsg::data:", data)
    self.create(ser)


def getHistory(sysId, pageNum):
    """获取聊天历史记录(逆序)"""
    print(">>> getHistory::sysId:", sysId)
    if pageNum <= 0 or pageNum is None:
        pageNum = 1
    begin = int(MSG_LENGTH * (pageNum - 1))
    sql = f"select id,num,typ,content,time from aibot_aibot where sysId='{sysId}' order by time desc limit {begin},{MSG_LENGTH}"
    print(">>> sql:", sql)
    msgs = list(AIBot.objects.raw(sql))
    return msgs


def getNum(sysId) -> int:
    """获取消息条数"""
    num = 1
    sysId = str(sysId)
    print(sysId)
    sql = f"select id,max(num) as num from aibot_aibot where sysId='{sysId}'"
    latest = AIBot.objects.raw(sql)[0].__dict__['num']
    if latest is not None:
        num = latest + 1
    return num
