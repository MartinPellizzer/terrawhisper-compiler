import g

def header():
    if 0:
        html = f'''
            <header class="header">
                <a class="text-black no-underline" href="/">TerraWhisper</a>
                <nav class="flex gap-16">
                    <a class="text-black no-underline" href="/remedies.html">Remedies</a>
                    <a class="text-black no-underline" href="/herbs.html">Herbs</a>
                    <a class="text-black no-underline" href="/about-us.html">About</a>
                    <a class="text-black no-underline" href="/contacts.html">Contacts</a>
                </nav>
            </header>
        '''
    html = f'''
        <header class="header">
            <a class="" href="/"><img height="128" src="/images-static/terrawhisper-logo.jpg" alt="logo of terrawhisper"></a>
            <nav class="flex gap-16">
                <a class="text-black no-underline" href="/remedies.html">Remedies</a>
                <a class="text-black no-underline" href="/herbs.html">Herbs</a>
                <a class="text-black no-underline" href="/about-us.html">About</a>
                <a class="text-black no-underline" href="/contacts.html">Contacts</a>
            </nav>
        </header>
    '''
    return html

def header_2():
    html = f'''
        <header class="header-2">
            <a class="" href="/"><img height="96" src="/images-static/terrawhisper-logo.jpg" alt="logo of terrawhisper"></a>
            <nav class="header-nav">
                <a class="text-black no-underline" href="/mission.html">Mission</a>
                <a class="text-black no-underline" href="/about-us.html">About</a>
                <a class="text-black no-underline" href="/contacts.html">Contacts</a>
                <a class="button-green-fill" href="/herbs.html">View Herbs</a>
            </nav>
        </header>
    '''
                # <a class="text-black no-underline" href="/introduction.html">Start Here</a>
    return html

def footer():
    html = f'''
        <footer class="footer">
            <span>© TerraWhisper.com 2024 | All Rights Reserved</span>
            <div class="flex gap-24">
                <a href="/privacy-policy.html">Privacy Policy</a>
                <a href="/cookie-policy.html">Cookie Policy</a>
            </div>
        </footer>
    '''
    return html

def footer_2():
    html = f'''
        <footer class="footer-2">
            <span>© TerraWhisper.com 2024 | All Rights Reserved</span>
            <div class="flex gap-24">
                <a href="/privacy-policy.html">Privacy Policy</a>
                <a href="/cookie-policy.html">Cookie Policy</a>
            </div>
        </footer>
    '''
    return html

def table_of_contents(content_html):
    table_of_contents_html = ''
    headers = []
    content_html_with_ids = ''
    current_id = 0
    for line in content_html.split('\n'):
        if '<h2>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h2>', f'<h2 id="{current_id}">'))
            current_id +=1
        elif '<h3>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h3>', f'<h3 id="{current_id}">'))
            current_id +=1
        elif '<h4>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h4>', f'<h4 id="{current_id}">'))
            current_id +=1
        elif '<h5>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h5>', f'<h5 id="{current_id}">'))
            current_id +=1
        elif '<h6>' in line:
            headers.append(line)
            content_html_with_ids += (line.replace('<h6>', f'<h6 id="{current_id}">'))
            current_id +=1
        else:
            content_html_with_ids += (line)
        content_html_with_ids += '\n'
    toc_li = []
    table_of_contents_html += '<div class="toc">'
    table_of_contents_html += '<span class="toc-title">Table of Contents</span>'
    table_of_contents_html += '<ul>'
    last_header = '<h2>'
    for i, line in enumerate(headers):
        insert_open_ul = False
        insert_close_ul = False
        if '<h2>' in line: 
            if last_header != '<h2>': 
                if int('<h2>'[2]) > int(last_header[2]): insert_open_ul = True
                else: insert_close_ul = True
            last_header = '<h2>'
            line = line.replace('<h2>', '').replace('</h2>', '')
        elif '<h3>' in line:
            if last_header != '<h3>':
                if int('<h3>'[2]) > int(last_header[2]): insert_open_ul = True
                else: insert_close_ul = True
            last_header = '<h3>'
            line = line.replace('<h3>', '').replace('</h3>', '')
        if insert_open_ul: table_of_contents_html += f'<ul>'
        if insert_close_ul: table_of_contents_html += f'</ul>'
        table_of_contents_html += f'<li><a href="#{i}">{line}</a></li>'
    table_of_contents_html += '</ul>'
    table_of_contents_html += '</div>'
    content_html_formatted = ''
    toc_inserted = False
    for line in content_html_with_ids.split('\n'):
        if not toc_inserted:
            if '<h2' in line:
                toc_inserted = True
                content_html_formatted += table_of_contents_html
                content_html_formatted += line
                continue
        content_html_formatted += line
    return content_html_formatted

def meta(content, lastmod):
    year = lastmod.split('-')[0]
    month = lastmod.split('-')[1]
    if month == '01': month = "Jan"
    if month == '02': month = "Feb"
    if month == '03': month = "Mar"
    if month == '04': month = "Apr"
    if month == '05': month = "May"
    if month == '06': month = "Jun"
    if month == '07': month = "Jul"
    if month == '08': month = "Aug"
    if month == '09': month = "Sep"
    if month == '10': month = "Oct"
    if month == '11': month = "Nov"
    if month == '12': month = "Dec"
    day = lastmod.split('-')[2]
    reading_time = str(len(content.split(' ')) // 200) + ' minutes'
    if False:
        html = f'''
            <div class="flex items-center justify-between mb-8">
                <div class="flex items-center gap-16">
                    <img src="/images-static/leen-randell.jpg" alt="profile picture of leen randell">
                    <address class="author">By <a rel="author" href="/about.html">{g.AUTHOR_NAME}</a></address>
                </div>
                <span>{reading_time}</span>
            </div>
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-16">
                    <p>Last updated: {month} {day}, {year}</p>
                </div>
                <span></span>
            </div>
        '''
    html = f'''
        <div class="flex items-center justify-between mb-16">
            <div class="flex items-center gap-8">
                <img class="profile-pic-meta" width=64 height=64 src="/images-static/leen-randell.jpg" alt="profile picture of leen randell">
                <p class="mb-0">By <a class="uppercase text-black no-underline font-bold" rel="author" href="">{g.AUTHOR_NAME}</a></p>
            </div>
            <p class="mb-0">Updated: {month} {day}, {year}</p>
        </div>
    '''
    return html

