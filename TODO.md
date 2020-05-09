## TODO

- Make the whole library object-oriented
- Examples
- Short documentation in source & README

---

libyiban/
	YiBanAccount.YiBanAccount
		.__init__(self, username = None, password = None)
		.__del__(self)
		.__enter__(self)
		.__exit__(self, type, value, trace)
		.__addref(self)
		.__release(self)
		.login(self)
		.logout(self)
		.checkin(self)
		.get_groups(self)
	YiBanGroup.YiBanGroup
		.__init__(self, account, puid, gid)
		.__del__(self)
		.__get_channelid(self)
		.get_egpa(self)
		.get_articles(self, count)
		.new_article(self, title, content)
	YiBanArticle.YiBanArticle
		.__init__(self, group, articleid)
		.__del__(self)
		.like(self)
		.get_replies(self)
		.get_content(self)
		.new_reply(self, content, anonymous = False)

libyiban_ex/
	IdiomSolitaire.IdiomSolitaire
		.__init__(self, initial = None)
		.get()
	XinHuaNews
		CATEGORY
			.POLITICS
			...
		get(category, count = 1)

