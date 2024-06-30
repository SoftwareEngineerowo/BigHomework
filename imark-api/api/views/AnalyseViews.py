from api import models
from rest_framework.views import APIView
from rest_framework.response import Response
from ext import Code




code=Code.SUCCESS_CODE
msg=''


#添加基本分析结果分数
class ScoreAnalyseView(APIView):
    def get(self,request):
        examId=request.query_params.dict().get("examId")
        paperId=request.query_params.dict().get("paperId")
        data=models.Paper_Score_Sheet.objects.filter(examId=examId,paperId=paperId)
        if not data:
            code=Code.ERROR_CODE
            msg='该examId&paperId对应的记录不存在'
            data={}
        else:
            perfect_count = 0  # 优秀  90-100
            good_count = 0  # 良好  70-89
            normal_count = 0  # 正常  60-69
            poor_count = 0  # 较差  0-59

            score_list = []
            for item in data:
                score_list.append(item.finalScore)
                if item.finalScore >= 90:
                    perfect_count += 1
                elif (item.finalScore >= 70) and (item.finalScore < 90):
                    good_count += 1
                elif (item.finalScore >= 60) and (item.finalScore < 70):
                    normal_count += 1
                elif (item.finalScore >= 0) and (item.finalScore < 60):
                    poor_count += 1

            max_score = max(score_list)
            min_score = min(score_list)
            avg_score = sum(score_list) / len(score_list)

            count = {
                "perfect_count": perfect_count,
                "good_count": good_count,
                "normal_count": normal_count,
                "poor_count": poor_count,
            }

            data = {
                "count": count,
                "max_score": max_score,
                "min_score": min_score,
                "avg_score": avg_score,
            }

            code = Code.SUCCESS_CODE
            msg = '试卷分析成功'


        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)
