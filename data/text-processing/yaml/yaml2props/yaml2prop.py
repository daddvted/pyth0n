import re
import os.path
import argparse


def yaml2prop(filename, space_num=2):
    properties_file = '{}.properties'.format(filename)

    # Store properties list
    props = []
    with open(filename, 'r') as f,\
            open(properties_file, 'w') as p:
        for line in f:
            # Ignore comments, blank line and line with dash('-')
            ignore = re.search(r'^\s?[#-]', line)
            if ignore or not line.strip() or ':' not in line:
                continue

            # Get indent level
            ptn = re.compile(r'(\s{' + str(space_num) + r'})')
            indents = ptn.findall(line.split(':')[0])
            level = len(indents) if indents else 0

            # Get property name
            # Be careful about special character in line
            prop_name = line.split(':')[0].strip()

            # If current indent is 0,
            # initialize 'props' list with current property name
            # (Empty old props list)
            if level is 0:
                props = [prop_name]
            else:
                # Adjust element in 'props' list according to indent level
                while props and level < len(props):
                    props.pop()
                props.append(prop_name)

            # Get property value
            value_matched = re.search(r'(?<=:).+', line)
            if value_matched:
                prop_value = value_matched.group().strip()
                if prop_value:
                    # If text were literal list,
                    # i.e.:
                    # websvrs: ['192.168.100.1', '192.168.100.2']
                    # It needs to be process as:
                    # websrvs[0] = 192.168.100.1
                    # websrvs[1] = 192.168.100.2
                    if re.match(r'\[.+\]', prop_value):
                        items = re.findall(r'[\"\'](.+?)[\"\']', prop_value)
                        for i in range(len(items)):
                            new_line = '{}[{}]={}'.format('.'.join(props), i, items[i])
                            print(new_line, file=p)
                    else:
                        new_line = '{}={}'.format('.'.join(props), value_matched.group().strip())
                        print(new_line, file=p)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml", help='Specify a YAML to convert')
    args = parser.parse_args()

    if not os.path.exists(args.yaml):
        print("{} not exists".format(args.yaml))
        exit(-1)

    yaml2prop(args.yaml)
