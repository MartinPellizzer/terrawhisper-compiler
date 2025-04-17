import g

def header():
    if 0:
        html = f'''
            <header class="header">
                <a class="text-black no-underline" href="/">TerraWhisper</a>
                <nav class="flex gap-16">
                    <a class="text-black no-underline" href="/remedies.html">Remedies</a>
                    <a class="text-black no-underline" href="/herbs.html">Herbs</a>
                    <a class="text-black no-underline" href="/about.html">About</a>
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
                <a class="text-black no-underline" href="/about.html">About</a>
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
                <a class="text-black no-underline" href="/about.html">About</a>
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
    table_of_contents_html += '<p class="toc-title">Table of Contents</p>'
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

def toc(html_in):
    html_out = ''
    json_toc = []
    index = 0
    for line in html_in.split('\n'):
        line = line.strip()
        if line.startswith('<h2'):
            json_toc.append({
                'tag': 'h2',
                'index': index,
                'headline': line.split('>')[1].split('<')[0],
            })
            line = (line.replace('<h2', f'<h2 id="{index}"'))
            index +=1
        html_out += line
        html_out += '\n'
    return html_out, json_toc

def toc_json_to_html_article(json_toc):
    html_toc = ''
    html_toc += '<ul>'
    for item_toc in json_toc:
        index = item_toc['index']
        headline = item_toc['headline']
        html_toc += f'<li><a href="#{index}">{headline}</a></li>'
    html_toc += '</ul>'
    return html_toc

def toc_json_to_html_sidebar(json_toc):
    html_toc_list = ''
    html_toc_list += '<ul>'
    for item_toc in json_toc:
        index = item_toc['index']
        headline = item_toc['headline']
        html_toc_list += f'''
            <li><a href="#{index}">{headline}</a></li>
        '''
    html_toc_list += '</ul>'
    html_toc = ''
    html_toc += f'''
        <div class="sidebar-toc">
            <div class="sidebar-toc-header">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>
                <p>On this page</p>
            </div>
                {html_toc_list}
            </ul>
        </div>
    '''
    return html_toc

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
    if 0:
        html = f'''
            <div class="flex items-center justify-between mb-16">
                <div class="flex items-center gap-8">
                    <img class="profile-pic-meta" width=64 height=64 src="/images-static/leen-randell.jpg" alt="profile picture of leen randell">
                    <p class="mb-0">By <a class="uppercase text-black no-underline font-bold" rel="author" href="">{g.AUTHOR_NAME}</a></p>
                </div>
                <p class="mb-0">Updated: {month} {day}, {year}</p>
            </div>
        '''
    if 1:
        html = f'''
            <div class="flex items-center justify-between mb-16">
                <div class="flex items-center gap-8">
                    <p class="mb-0 text-14">By <a class="uppercase text-black no-underline font-bold" rel="author" href="">{g.AUTHOR_NAME}</a></p>
                </div>
                <p class="mb-0">Updated: {month} {day}, {year}</p>
            </div>
        '''
    return html


#########################################################################
# ;study
#########################################################################
def study_snippet_html(study_snippet_text):
    html += f'''
        <div class="study" style="margin-bottom: 16px;">
            <div class="study-header">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
                </svg>
                <p>Related Study</p>
            </div>
            <p>
                {study_snippet_text}
            </p>
        </div>
    '''
    return html
