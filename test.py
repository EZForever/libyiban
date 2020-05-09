#!/usr/bin/env python3

import libyiban

with libyiban.YiBanAccount() as o:
    group = list(o.get_groups())[-1][1]
    print(group)
    for title, article in group.get_articles(10):
        print(title)
        for reply in article.get_replies(10):
            print('\t', reply)

