"""
URL configuration for imark project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from api.views import  AddTestViews,SelectTestViews,AddMarkViews,AnalyseViews,SelectMarkViews,DeleteTestView,UserViews,DeleteMarkViews
urlpatterns = [


    ###################-----用户模块-------############################

    #注册
    path('registered/',UserViews.RegisteredView.as_view()),

    #登录
    path('login/',UserViews.LoginView.as_view()),

    #修改个人资料
    path('userInfo/update/',UserViews.UserInfoUpdateView.as_view()),



    ###################-----考试添加-------############################


    #添加试题类型
    path('quesKind/add/',AddTestViews.AddQuesKindView.as_view()),
    #添加试题
    path('ques/add/',AddTestViews.AddQuesView.as_view()),

    #更改考试试卷的答卷上传状态
    path('exam/changeHasAnswer/',AddTestViews.ExamChangeHasAnswerView.as_view()),



    #添加答题
    path('answer/add/',AddTestViews.AddAnswerView.as_view()),
    #添加准考证
    path('certify/add/',AddTestViews.AddCertifyView.as_view()),
    #添加试卷
    path('paper/add/',AddTestViews.AddPaperView.as_view()),
    #根据试卷id修改试卷状态
    path('paper/updatePaperStasus/',AddTestViews.UpdatePaperStatus.as_view()),


    #添加考试（躯壳）
    path('exam/beforeAdd/',AddTestViews.AddExambeforeView.as_view()),
    #添加考试(内容)
    path('exam/add/',AddTestViews.AddExamView.as_view()),
    #添加考试(取消)
    path('exam/cancel/',AddTestViews.AddExamCancelView.as_view()),



    ###################-----考试查询-------############################



    #显示所有试题
    path('showQues/all/',SelectTestViews.ShowAllQuesView.as_view()),
    #根据题型查询试题
    path('showQues/byQuesKindId/',SelectTestViews.ShowQuesByQuesKindIdView.as_view()),
    #根据试题id查询试题
    path('showQues/byQuesId/',SelectTestViews.ShowQuesByQuesIdView.as_view()),


    #显示所有考试
    path('showExam/all/',SelectTestViews.ShowAllExamView.as_view()),
    #根据考试id查询考试
    path('showExam/byExamId/',SelectTestViews.ShowExamByExamIdView.as_view()),
    #试卷名称模糊查询
    path('showPaper/fuzzyByPaperName/',SelectTestViews.ShowFuzzyPaperByPaperNameView.as_view()),
    #根据试卷id查询试卷
    path('showPaper/byPaperId/',SelectTestViews.ShowPaperByPaperIdView.as_view()),

    #根据hasAnswers分类查询考试试卷的答卷状态
    path('exam/selectHasAnswer/',SelectTestViews.ExamSelectHasAnswerView.as_view()),

    #显示所有试卷
    path('showPaper/all/',SelectTestViews.ShowAllPaperView.as_view()),

    #根据答题id查询答题模型
    path('showAnswer/byAnswerId/',SelectTestViews.ShowAnswerByAnswerIdView.as_view()),

    #根据certId和quesId查询答题模型
    path('showAnswer/byCertIdandQuesId/',SelectTestViews.ShowAnswerByCertIdAndQuesIdView.as_view()),

    #根据examId查询考试学生
    path('showCertify/byExamId/',SelectTestViews.ShowCertifyByExamIdView.as_view()),



    ###################-----考试删除-------############################

    #根据题型id删除题型
    path('delete/QuesKind/byQuesKindId/', DeleteTestView.DeleteQuesKindByQuesKindIdView.as_view()),
    #根据试题id删除试题
    path('delete/Ques/byQuesId/', DeleteTestView.DeleteQuesByQuesIdView.as_view()),
    #根据试卷id删除试卷
    path('delete/Paper/byPaperId/', DeleteTestView.DeletePaperByPaperIdView.as_view()),
    #根据考试id删除考试
    path('delete/Exam/byExamId/', DeleteTestView.DeleteExamByExamIdView.as_view()),
    #根据答题id删除答题模型
    path('delete/Answer/byAnswerId/', DeleteTestView.DeleteAnswerByAnswerIdView.as_view()),




    ###################-----阅卷-------############################


    #添加阅卷任务
    path('mark/add/',AddMarkViews.AddMarkView.as_view()),
    #添加打分结果
    path('mark/result/',AddMarkViews.MarkResultView.as_view()),
    #添加单卷分数
    path('score/addSheetScore/',AddMarkViews.AddSheetScoreView.as_view()),

    #教师查询阅卷题目
    path('mark/selectMarkBySysId/',SelectMarkViews.SelectMarkBySysIdView.as_view()),
    #根据answerId查询单题打分结果
    path('markResult/selectMarkResultByAnswerId/',SelectMarkViews.SelectMarkResultByAnswerIdView.as_view()),

    #根据id删除单题打分结果
    path('mark/deleteMarkResultById/',DeleteMarkViews.DeleteMarkResultByIdView.as_view()),

    #根据markId删除阅卷任务
    path('mark/deleteByMarkId/',DeleteMarkViews.DeleteMarkByMarkId.as_view()),

    #根据examId查询所有学生成绩
    path('score/selectAllByExamId/',SelectMarkViews.SelectAllScoreByExamIdView.as_view()),



    ###################-----分析结果-------############################
    #添加基本分析结果分数
    path('analyse/normal/',AnalyseViews.ScoreAnalyseView.as_view()),

]
