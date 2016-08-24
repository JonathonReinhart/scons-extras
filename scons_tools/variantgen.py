class VariantActionBase(object):
    def Dump(self, indent=0):
        for k,v in self.kw.items():
            print ' '*indent + '{0}: {1}'.format(k, v)


class AppendVariantAction(VariantActionBase):
    def __init__(self, **kw):
        self.kw = kw


class Variant(object):
    def __init__(self, name=None):
        self.name = name
        self.actions = []

    def Append(self, **kw):
        self.actions.append(AppendVariantAction(**kw))


    def Dump(self, indent=0):
        print ' '*indent + '"{0}"'.format(self.name)
        for act in self.actions:
            act.Dump(indent=indent+4)



class VariantSet(object):
    def __init__(self, name=None):
        self.name = name
        self.variants = []

    def AddVariant(self, name=None):
        v = Variant(name)
        self.variants.append(v)
        return v

    def Dump(self, indent=0):
        print ' '*indent + '"{0}" :: Variants:'.format(self.name)
        for v in self.variants:
            v.Dump(indent=indent+4)


class VariantGen(object):
    def __init__(self, base_env):
        self.base_env = base_env
        self.variant_sets = []

    def AddVariantSet(self, name=None):
        vs = VariantSet(name)
        self.variant_sets.append(vs)
        return vs

    def Dump(self, indent=0):
        print 'Variant Sets:'
        for vs in self.variant_sets:
            vs.Dump(indent=indent+4)    


def generate(env):
    env.AddMethod(VariantGen, 'VariantGen')

def exists(env):
    return True
