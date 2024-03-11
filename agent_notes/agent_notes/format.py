
HEADER = '\n{0:^5}| {1:^40}| {2:^20}\n{3:-^70s}'.format('id','note','tags','-')
SEPARATOR = '\n{0:-^70s}'.format('-')

class colors:
    RED = '\x1b[31m'
    GREEN = '\x1b[32m'
    END = '\x1b[0m'

def wrap(string, width):
    return [string[i:i + width] for i in range(0, len(string), width)]

def splitted_text(text):
    result = []
    for i in range(len(text)):
        if len(text[i]) < 40:
            result.append('\n{0:5}| {1:40}| {2:20}'.format('', text[i],''))
        else:
            result.append('\n{0:5}| {1:49}| {2:20}'.format('', text[i],''))
    return result