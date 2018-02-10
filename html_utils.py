import re


def strip_html_tags(html, rules):
    """
    去除html标签
    s = __escape_html_tag("<script>alert('2333')</script>",['script.+'])
    s = ''
    s = __escape_html_tag("<h1 class='header1'>Header1</h1>",['h\d'])
    s = 'Header1'
    :param html:
    :param rules:
    :return:
    """
    for rule in rules:
        html = re.sub(r'</?{tag}.*?>'.format(tag=rule), "", html)
    return html
