import xadmin
from apps.users.models import UserProFile

class UserProFileAdmin(object):
    '''
    用户表显示
    '''

    list_display = ['nick_name','gender','country','province','city'] #后台显示类型
    search_fields = ['nick_name','gender','country','province','city'] #设置搜索
    list_filter = ['nick_name','gender','country','province','city'] # 搜索过滤器


xadmin.site.unregister(UserProFile)
xadmin.site.register(UserProFile,UserProFileAdmin)