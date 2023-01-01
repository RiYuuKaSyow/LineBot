import yaml
import os

def changeVal(path, key, value):
    with open(path, 'r', encoding='utf-8') as f:
        lines = []
        for line in f.readlines():
            if line != '\n':
                lines.append(line)
        f.close()
    with open(path, 'w', encoding='utf-8') as f:
        response = 0
        for line in lines:
            if key in line and ('#' not in line):
                left = line.split(':')[0]
                newline = '{0}: {1}'.format(left, value)
                line = newline
                f.write('%s\n' % line)
                response = 1
            else:
                f.write('%s' % line)
        f.close()
        return response

key = ['djangoSecret', 'lineToken', 'lineSecret', 'weatherauth']
value = [  os.getenv('djangoSecret','test'), os.getenv('lineToken','test'), os.getenv('lineSecret','test'), os.getenv('weatherauth','test') ]
env = { key[i]: value[i] for i in range(len(key)) }

for k in env:
    f = changeVal('./app.yaml', k, env[k])
    print(f)