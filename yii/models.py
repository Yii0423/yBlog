from django.db import models


# 字典表
class Dictionary(models.Model):
    pid = models.IntegerField('父类编号', default=0)
    ptype = models.CharField('父类型', max_length=500, default='')
    key = models.CharField('键', max_length=100, default='')
    value = models.CharField('值', max_length=500, default='')
    create = models.DateTimeField('创建时间', auto_now_add=True)
    modify = models.DateTimeField('修改时间', auto_now=True)
    remarks = models.TextField('备注', default='')
    sort = models.IntegerField('排序', default=0)
    isdel = models.BooleanField('是否删除', default=False)


# 用户表
class User(models.Model):
    tid = models.IntegerField('用户类型', default=0)
    email = models.CharField('邮箱', max_length=50, default='')
    phone = models.CharField('手机号', max_length=11, default='')
    nickname = models.CharField('用户昵称', max_length=25, default='')
    avatar = models.CharField('用户头像', max_length=25, default='/images/default-default-avatar.png')
    password = models.CharField('用户密码', max_length=32, default='e10adc3949ba59abbe56e057f20f883e')
    status = models.IntegerField('用户状态', default=1)
    create = models.DateTimeField('创建时间', auto_now_add=True)
    modify = models.DateTimeField('修改时间', auto_now=True)
    remarks = models.TextField('备注', default='')


# 关于表
class About(models.Model):
    title = models.CharField('标题', max_length=100, default='')
    imagesurl = models.CharField('图片链接', max_length=500, default='')
    leading = models.CharField('引导语', max_length=1000, default='')
    content = models.TextField('正文', default='')
    create = models.DateTimeField('创建时间', auto_now_add=True)
    modify = models.DateTimeField('修改时间', auto_now=True)

    def split2list(self):
        return self.imagesurl.split(',')


# 随笔表
class Essay(models.Model):
    categoryid = models.IntegerField('所属分类编号', default=0)
    category = models.CharField('所属分类', max_length=500, default='')
    typeid = models.IntegerField('文章类型编号', default=0)
    type = models.CharField('文章类型', max_length=500, default='')
    spiderid = models.CharField('采集编号', max_length=100, default='')
    seotitle = models.CharField('SEO标题', max_length=100, default='')
    seokeywords = models.CharField('SEO关键词', max_length=200, default='')
    seodescription = models.CharField('SEO描述', max_length=500, default='')
    sources = models.CharField('来源', max_length=50, default='yii')
    imagesurl = models.CharField('图片链接', max_length=500, default='')
    filesurl = models.CharField('文件链接', max_length=500, default='')
    visits = models.IntegerField('浏览数', default=0)
    agrees = models.IntegerField('赞数', default=0)
    disagrees = models.IntegerField('踩数', default=0)
    create = models.DateTimeField('创建时间', auto_now_add=True)
    modify = models.DateTimeField('修改时间', auto_now=True)
    remarks = models.TextField('正文', default='')
    sort = models.IntegerField('排序', default=0)
    isdel = models.BooleanField('是否删除', default=False)

    def shorttitle(self):
        return self.seotitle[:20]

    def split2list(self):
        return self.imagesurl.split(',')

    def clearimages(self):
        return self.imagesurl.replace(',', '')

    def clearfiles(self):
        return self.filesurl.replace(',', '')


# 收藏表
class Collection(models.Model):
    typeid = models.IntegerField('收藏类型编号', default=0)
    type = models.CharField('收藏类型', max_length=500, default=0)
    title = models.CharField('标题', max_length=100, default='')
    imagesurl = models.CharField('图片', max_length=500, default='')
    url = models.CharField('链接', max_length=500, default='')
    visits = models.IntegerField('浏览数', default=0)
    agrees = models.IntegerField('赞数', default=0)
    disagrees = models.IntegerField('踩数', default=0)
    create = models.DateTimeField('创建时间', auto_now_add=True)
    modify = models.DateTimeField('修改时间', auto_now=True)
    remarks = models.TextField('备注', default='')
    sort = models.IntegerField('排序', default=0)
    isdel = models.BooleanField('是否删除', default=False)

    def shorttitle(self):
        return self.title[:20]

    def clearimages(self):
        return self.imagesurl.replace(',', '')


# 留言表
class Feedback(models.Model):
    content = models.CharField('内容', max_length=500, default='')
    replycontent = models.CharField('回复', max_length=500, default='')
    ip = models.CharField('IP', max_length=50, default='')
    city = models.CharField('所在地', max_length=100, default='')
    create = models.DateTimeField('创建时间', auto_now_add=True)
    modify = models.DateTimeField('修改时间', auto_now=True)
    isdel = models.BooleanField('是否删除', default=False)


# 点赞历史表
class AgreeLog(models.Model):
    articleid = models.IntegerField('文章编号', default=0)
    ip = models.CharField('IP', max_length=50, default='')
    status = models.IntegerField('结果0-默认1-顶2-踩', default=0)
    create = models.DateTimeField('创建时间', auto_now_add=True)
    modify = models.DateTimeField('修改时间', auto_now=True)
