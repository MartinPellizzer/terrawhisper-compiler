import util


filepath_in = 'keywords/herbal_teas.txt'
filepath_out = 'keywords/herbal_teas_ailments.txt'

run = True
while run:
    keyword = input('>> ')

    if keyword == 'quit': break
    
    content = util.file_read(filepath_in)
    lines = content.split('\n')

    lines_keep = []
    lines_move = []
    for line in lines:
        if keyword.lower() in line.lower():
            lines_move.append(line)
        else:
            lines_keep.append(line)

    lines_keep_str = '\n'.join(lines_keep)
    lines_move_str = keyword + '\n    ' + '\n    '.join(lines_move) + '\n\n'

    util.file_write(filepath_in, lines_keep_str)
    util.file_append(filepath_out, lines_move_str)