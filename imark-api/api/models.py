from django.db import models

#用户账号信息表
class Role(models.Model):
    roleId = models.CharField(verbose_name='工号',max_length=64)    #用于登录
    
    sysId = models.CharField(verbose_name='系统 ID',max_length=64,primary_key=True)  #主键   唯一 用于分配阅卷任务
    
    username = models.CharField(verbose_name='用户名',max_length=32)

    password = models.CharField(verbose_name='登录密码',max_length=64)
    
    avatar  = models.CharField(verbose_name='头像',max_length=255,default='https://tse2-mm.cn.bing.net/th/id/OIP-C.Bb-rbUYwAPIHdXKILp7T5wHaHa?w=188&h=188&c=7&r=0&o=5&dpr=1.3&pid=1.7')  #图片URL
 
 

'''
    考试模型
'''


#试题类型表    单选题 多选题 填空题 图表题 简答题 翻译题 作文题
class Ques_Kind(models.Model):
    quesKindId = models.AutoField(verbose_name='试题类型ID',primary_key=True )
    
    quesKindName = models.CharField(verbose_name='题型名称',max_length=64)



#试题模型表
class Ques(models.Model):
    quesId = models.CharField(verbose_name='试题 ID',max_length=64,primary_key=True)
    
    quesKindId  = models.IntegerField(verbose_name='题目类型')  
    
    quesContent  = models.TextField(verbose_name='题目内容')
    
    quesAnswer  = models.TextField(verbose_name='参考答案',max_length=255)
    
    quesDefaultScore  = models.FloatField(verbose_name='默认分值')
    
    quesLevel  = models.DecimalField(verbose_name='题目难度等级',max_digits=10,decimal_places=2,default=0)
    


#试卷模型表
class Paper(models.Model):
    paperId   = models.CharField(verbose_name='试卷 ID ',max_length=64,primary_key=True)
    
    paperName  = models.CharField(verbose_name='试卷名称',max_length=64)
    
    paperFullScore   = models.FloatField(verbose_name='试卷总分')
    
    paperLevel   = models.DecimalField(verbose_name='全卷难度等级',max_digits=10,decimal_places=2,default=0)
    
    quesKindIds   = models.TextField(verbose_name='试卷结构 ')
    
    quesIds   = models.TextField(verbose_name='包含试题')

    paperStasus = models.IntegerField(verbose_name='试卷状态',default=0)


    
   
    
#准考证-学号表
class Certify(models.Model):
    id = models.AutoField(verbose_name='记录 ID ',primary_key=True)
    
    examId = models.CharField(verbose_name='考试 ID ',max_length=64)
    
    certId = models.CharField(verbose_name='准考证号',max_length=64,null=True,blank=True)

    stuId = models.CharField(verbose_name='学号 ',max_length=64)
    
    stuName = models.CharField(verbose_name='姓名',max_length=64)



#考试基本信息表
class Exam(models.Model):
    examId  = models.CharField(verbose_name='考试ID',max_length=64,primary_key=True)
    
    examName = models.CharField(verbose_name='考试名称',max_length=64)
    
    paperIds = models.TextField(verbose_name='使用试卷')

    examTimes = models.TextField(verbose_name='考试时间')

    hasAnswers = models.IntegerField(verbose_name="上传答卷状态", default=0)
    # 该考试试卷上传答卷状态
    # 0是未上传 （默认）  1上传  2未批 3已批改

    
    
    
#答题模型表
class Answer(models.Model):
    answerId   = models.CharField(verbose_name='答题 ID',max_length=64,primary_key=True)
    
    examId   = models.CharField(verbose_name='考试 ID',max_length=64)
    
    paperId   = models.CharField(verbose_name='试卷 ID ',max_length=64)
    
    certId   = models.CharField(verbose_name='准考证号 ',max_length=64)
    
    quesId   = models.CharField(verbose_name='试题 ID ',max_length=64)
    
    ansImg   = models.TextField(verbose_name='截取内容')
    
    scanResult   = models.TextField(verbose_name='答题结果')



    
'''
    阅卷任务
'''

#阅卷任务信息表
class Mark(models.Model):
    markId  = models.CharField(verbose_name='阅卷任务 ID',max_length=64,primary_key=True)
    
    examId   = models.CharField(verbose_name='所属考试 ID',max_length=64)
    
    paperId   = models.CharField(verbose_name='所属试卷 ID',max_length=64)
    
    taskAllos  = models.TextField(verbose_name='任务分配')


#按题打分结果模型表
class Mark_result(models.Model):
    id = models.CharField(verbose_name='记录 ID',max_length=64,primary_key=True)
    
    examId = models.CharField(verbose_name='考试 ID ',max_length=64)
    
    paperId = models.CharField(verbose_name='试卷 ID',max_length=64)
    
    quesId = models.CharField(verbose_name='试题 ID  ',max_length=64)
    
    answerId = models.CharField(verbose_name='答卷 ID ',max_length=64)
    
    markTime = models.DateTimeField(verbose_name='批阅时间',auto_now_add=True)
    
    teaId = models.CharField(verbose_name='批阅教师系统 ID',max_length=64)
    
    AIScore = models.FloatField(verbose_name='AI 评分')
    
    TeacherScore = models.FloatField(verbose_name='教师评分 ')
    
    AIComment = models.TextField(verbose_name='AI 意见 ')
    
    TeacherComment = models.TextField(verbose_name='教师意见 ')
    

#单卷分数表
class Paper_Score_Sheet(models.Model):
    id = models.CharField(verbose_name='表格 ID',max_length=64,primary_key=True)
    
    examId  = models.CharField(verbose_name='考试 ID',max_length=64)
    
    paperId  = models.CharField(verbose_name='试卷 ID',max_length=64)
    
    certId  = models.CharField(verbose_name='准考证号',max_length=64)
    
    
    detailScores  = models.TextField(verbose_name='得分详情')
    
    finalScore  = models.FloatField(verbose_name='总得分')



'''
    分析结果模型
'''

#基本分析结果分数表（自动计算或自动调用 AI 生成）
class Analyse(models.Model):
    analyseId  = models.CharField(verbose_name='分析 ID',max_length=64,primary_key=True)
    
    examId  = models.CharField(verbose_name='考试 ID ',max_length=64)
    
    paperId  = models.CharField(verbose_name='试卷 ID ',max_length=64)
    
    quesId  = models.CharField(verbose_name='试题 ID ',max_length=64)
    
    updateTime  = models.DateTimeField(verbose_name='最后更新时间',auto_now=True)
    
    topScore  = models.FloatField(verbose_name='最高分分数')
    
    topStu  = models.CharField(verbose_name='最高分考生',max_length=64)
    
    botScore  = models.FloatField(verbose_name='最低分分数')
    
    botStu  = models.CharField(verbose_name='最低分考生',max_length=64)
    
    avgScore  = models.FloatField(verbose_name='平均分')
    
    modScore  = models.FloatField(verbose_name='众数')
    
    variance  = models.DecimalField(verbose_name='方差',max_digits=10,decimal_places=2,default=0)
    
    
    
#高级分析结果分数表（用户请求后由 AI 根据基本分析结果生成）
class Analyse_Pro(models.Model):
    proId   = models.CharField(verbose_name='高级分析 ID',max_length=64,primary_key=True)
    
    requireTime   = models.DateTimeField(verbose_name='申请时间',auto_now_add=True)
    
    analyseId   = models.CharField(verbose_name='采用基本分析',max_length=64)
    
    isImg   = models.BooleanField(verbose_name='是否返回图片',default=False) #默认否
    prompt   = models.CharField(verbose_name='询问语句 ',max_length=255)
    
    description   = models.CharField(verbose_name='分析结果',max_length=255)