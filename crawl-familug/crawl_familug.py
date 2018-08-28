#!/usr/bin/python3 
__doc__ = '''
Crawl tất cả các bài viết có label
Python(http://www.familug.org/search/label/Python), Command, sysadmin và 10 bài
viết mới nhất ở homepage của http://www.familug.org/

Tạo file `index.html`, chứa 4 cột tương ứng cho:

```
Python | Command | Sysadmin | Latest
```

Mỗi cột chứa các link bài viết, khi bấm vào sẽ mở ra bài gốc tại FAMILUG.org

Tham khảo giao diện tại:
- https://themes.getbootstrap.com/
- http://getskeleton.com/#examples

Push code lên GitLab repo, tạo 1 GitLab Page để view kết quả.
https://pages.gitlab.io/

Nâng cao: push code lên GitHub và tạo 1 GitHub Page: https://pages.github.com/
'''

from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BASE_URL = 'http://www.familug.org'
LABEL_URL = BASE_URL + '/search/label/'


@app.route('/')
def show_articles():
    return render_template('index.html', articles=articles)

def crawl_url(url):
    result = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    jump_links = soup.findAll(
        'div',
        attrs={'class': 'jump-link'}
    )

    for link in jump_links:
        link = link.find('a')
        result.append((link['title'], link['href'].strip()))
    return result


def crawl_10():
    url = BASE_URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    older_link = soup.find(
        'a',
        id = 'Blog1_blog-pager-older-link'
    )
    result = crawl_url(url)
    more_result = crawl_url(older_link['href'])
    result += more_result[:4]
    return result


def get_list(L, i, v=None):
    try:
        return L[i]
    except IndexError:
        return ''


def main():
    pythons = crawl_url(LABEL_URL + 'Python')
    commands = crawl_url(LABEL_URL + 'Command')
    sysadmins = crawl_url(LABEL_URL + 'sysadmin')
    top_ten = crawl_10()

    index = 0
    result = []
    while True:
        python = get_list(pythons, index)
        command = get_list(commands, index)
        sysadmin = get_list(sysadmins, index)
        latest = get_list(top_ten, index)
        index += 1
        if python == '' and command == '' and sysadmin == '' and latest == '':
            break
        result.append(
            {
                'Python': python,
                'Command': command,
                'Sysadmin': sysadmin,
                'Latest': latest
            })
    return result


if __name__ == "__main__":
    articles = main()
    app.run(debug=True)