#!/usr/bin/env python3

import random

import libyiban
import libyiban_ex

NEWS_K = 3

NEWS_CATEGORIES = [
    libyiban_ex.XinHuaNews.CATEGORY.TECH,
    libyiban_ex.XinHuaNews.CATEGORY.POLITICS,
    libyiban_ex.XinHuaNews.CATEGORY.ENG_SCITECH_INTERNET
]

def latest_news(count_per_category):
    '''
    Prettify latest news into raw HTML, for YiBanGroup.new_article
    '''
    for category in NEWS_CATEGORIES:
        for title, abstract, url in libyiban_ex.XinHuaNews.get(category, count_per_category):
            yield (title, '<p>%s<a href="%s">阅读全文&gt;&gt;</a></p>' % (abstract, url))

def main():
    '''
    Routine:
        0. Get random news
        1. Operate w/ a user-provided account (using `with`)
        2. Show a list of all groups, let user to choose one
        3. Show EGPA
        4. Post the news & like
        5. Post some replies regarding solitaire (reason: nostalgia)
    '''
    news = list(latest_news(NEWS_K))
    
    with libyiban.YiBanAccount() as account:
        groups = list(account.get_groups())
        print('[I] Available groups:')
        for i, group in enumerate(groups):
            print('\t#%d - "%s"' % (i, group[0]))
        print()
        group_idxs = map(int, input('[?] Input groups\' indexes: ').split())
        
        for i in group_idxs:
            print('[I] Now processing #%d - "%s"' % (i, groups[i][0]))
            group = groups[i][1]
            print('\tEGPA = %.2f' % group.get_egpa())
            
            for news_title, news_content in random.choices(news, k = NEWS_K):
                _, article = group.new_article(news_title, news_content)
                article.like()
                
                solitaire = libyiban_ex.IdiomSolitaire(news_title)
                for _ in range(NEWS_K):
                    article.new_reply(solitaire.get(), anonymous = True)
    
    return 0

if __name__ == '__main__':
    try:
        exit(main())
    except KeyboardInterrupt:
        exit(130)

