from django.contrib import admin
from .models import Post, Comment, latest_transactions, last_blocks


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
admin.site.register(Comment, CommentAdmin)

class LatestTxAdmin(admin.ModelAdmin):
    list_display = ('txid', 'amount', 'fee', 'height', 'senderid','recipientid','timestamp','txtype','confirmations')
    list_filter = ('txid', 'amount', 'fee', 'height', 'senderid','recipientid','timestamp','txtype','confirmations')
admin.site.register(latest_transactions, LatestTxAdmin)

class LastBlocksAdmin(admin.ModelAdmin):
    list_display = ('generator', 'height', 'blockid', 'reward', 'timestamp', 'totalamount', 'totalfee', 'totalforged', 'transactionscount', 'username', 'rank')
admin.site.register(last_blocks, LastBlocksAdmin)