## TODO

- Make the whole library object-oriented
- Examples
- Short documentation in source & README

---

libyiban
	YiBanAccount
		__init__(self, username = None, password = None)
		login(self)
		logout(self)
		checkin(self)
		get_groups(self)
	YiBanGroup
		__init__(self, account, puid, gid)
		get_egpa(self)
		get_articles(self, count)
		new_article(self, title, content)
	YiBanArticle
		__init__(self, group, articleid)
		like(self)
		get_replies(self)
		get_content(self)
		new_reply(self, content, anonymous = False)

libyiban_ex
	IdiomSolitaire
		__init__(self, initial)
		get()
	XinHuaNews
		CATEGORY
			POLITICS
			...
		get(category, count = 1)

