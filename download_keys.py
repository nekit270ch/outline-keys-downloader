# bs4 sucks
import urllib.request, sys, re

def get_html(url):
    req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' })
    
    try:
        res = urllib.request.urlopen(req)
        if res.status != 200: raise Exception()
        return res.read().decode('utf-8').replace('\r', '').replace('\n', '')
    except Exception:
        print('Failed to download:', url)
        sys.exit(1)


def get_page_data(url):
    try:
        html = get_html(url)
        return {
            'url': re.search(r'\<textarea.*id="accessKey".*\>(.+)\</textarea\>', html)[1],
            'name': re.search(r'\<h1.*class="title-keys".*\>(.+)\</h1\>', html)[1],
            'ping': (re.search(r'\<span.*title="Ping".*\>([0-9\.]+)ms\</span\>', html) or (None, 'N/A'))[1]
        }
    except Exception as e:
        print('Failed to parse html:', url, e)
        sys.exit(1)


def get_url_list(url):
    try:
        html = get_html(url)
        lst = []

        for i in re.findall(r'\<a href="(/key/[0-9]+/)"', html):
            lst.append((url + i))
        
        return lst
    except Exception:
        print('Failed to parse html:', url)
        sys.exit(1)


if __name__ == '__main__':
    count = 0
    country = None
    format = 'txt'
    delim = ';'
    file_name = None

    if len(sys.argv) == 2 and sys.argv[1] == '--help':
        print(f'Outline Keys Downloader 0.1 by nekit270 (https://github.com/nekit270ch)\n\nUsage: {sys.argv[0]} [--out-file <path>] [--format <txt|csv>] [--count <count>] [--country <country name>] [--delim <csv delim>]')
        sys.exit()

    try:
        for i in range(len(sys.argv) - 1):
            arg = sys.argv[i]
            next_arg = sys.argv[i + 1]

            if arg == '--count':
                count = int(next_arg)
            elif arg == '--country':
                country = next_arg
            elif arg == '--format':
                format = next_arg
            elif arg == '--delim':
                delim = next_arg
            elif arg == '--out-file':
                file_name = next_arg
    except Exception:
        print('Invalid arguments')
        sys.exit(1)

    cnt = 0
    text = ''

    if format == 'csv':
        text = f'Name{delim}Ping{delim}URL\n'

    for url in get_url_list('https://outlinekeys.com' if country is None else 'https://outlinekeys.com/country/' + country):
        if count != 0 and cnt >= count:
            break

        data = get_page_data(url)

        if format == 'csv':
            text += f'{data["name"]}{delim}{data["ping"]}{delim}{data["url"]}\n'
        elif format == 'txt':
            text += data['url'] + '\n'

    if file_name is None:
        file_name = 'keys.' + ('csv' if format == 'csv' else 'txt')

    file = open(file_name, 'w', encoding='utf-8')
    file.write(text)
    file.close()
