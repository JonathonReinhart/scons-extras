class VariantGen(object):
    def __init__(self, base_env):
        self.base_env = base_env

def generate(env):
    env.AddMethod(VariantGen, 'VariantGen')

def exists(env):
    return True
