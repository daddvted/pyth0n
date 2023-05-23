import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

with open('crypto-config.yaml', 'r') as conf_fd, \
     open('stack.yaml', 'w') as stack_fd:
    config_data = yaml.load(conf_fd, yaml.Loader)

    env = Environment(loader=FileSystemLoader('./'), trim_blocks=True)
    try:
        template = env.get_template('fabric-tpl.jinja')
        stack_data = template.render(config_data)
        stack_fd.write(stack_data)
    except TemplateNotFound as e:
        print("{} Not Found".format(e))
