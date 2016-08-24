import itertools

class VariantActionBase(object):
    def Dump(self, indent=0):
        for k,v in self.kw.items():
            print ' '*indent + '{0}: {1}'.format(k, v)


class AppendVariantAction(VariantActionBase):
    def __init__(self, **kw):
        self.kw = kw

    def Apply(self, env):
        env.Append(**self.kw)


class Variant(object):
    def __init__(self, name=None):
        self.name = name
        self.actions = []

    def Append(self, **kw):
        self.actions.append(AppendVariantAction(**kw))

    def Apply(self, env):
        for act in self.actions:
            act.Apply(env)

    def Dump(self, indent=0):
        print ' '*indent + '"{0}"'.format(self.name)
        for act in self.actions:
            act.Dump(indent=indent+4)

    def __repr__(self):
        return 'Variant("{0}")'.format(self.name)


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

    def __repr__(self):
        return 'VariantSet("{0}")'.format(self.name)


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


    def GenerateEnvironments(self):
        def gen():
            # Generate the Cartesian product of all variants in each variant set
            for variants in itertools.product(*[vs.variants for vs in self.variant_sets]):
                env = self.base_env.Clone()
                for v in variants:
                    v.Apply(env)
                yield env

        return list(gen())




def generate(env):
    env.AddMethod(VariantGen, 'VariantGen')

def exists(env):
    return True
