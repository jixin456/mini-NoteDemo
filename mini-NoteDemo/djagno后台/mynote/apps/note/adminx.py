import xadmin
from apps.note.models import NoteModel

class NoteAdmin(object):
    '''
    用户表显示
    '''

    list_display = ['user','content'] #后台显示类型




xadmin.site.register(NoteModel,NoteAdmin)