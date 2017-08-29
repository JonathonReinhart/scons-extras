import itertools

class VariantActionBase(object):
    def __init__(self, **kw):
        self.kw = kw

    def Dump(self, indent=0):
        for k,v in self.kw.items():
            # TODO: This is bogus; it only applies to Append()
            print ' '*indent + '{0} += {1}'.format(k, v)


class AppendVariantAction(VariantActionBase):
    def Apply(self, env):
        env.Append(**self.kw)

class AppendUniqueVariantAction(VariantActionBase):
    def Apply(self, env):
        env.AppendUnique(**self.kw)

class SetDefaultVariantAction(VariantActionBase):
    def Apply(self, env):
        env.SetDefault(**self.kw)

class ToolVariantAction(VariantActionBase):
    def __init__(self, tool, toolpath=None, **kw):
        self.tool = tool
        self.toolpath = toolpath
        self.kw = kw

    def Apply(self, env):
        env.Tool(self.tool, toolpath=self.toolpath, **self.kw)

class Variant(object):
    def __init__(self, **kw):
        self.kw = kw
        self.actions = []

    def Append(self, **kw):
        self.actions.append(AppendVariantAction(**kw))

    def AppendUnique(self, **kw):
        self.actions.append(AppendUniqueVariantAction(**kw))

    def Replace(self, **kw):
        self.kw.update(kw)

    def SetDefault(self, **kw):
        self.actions.append(SetDefaultVariantAction(**kw))

    def Tool(self, tool, toolpath=None, **kw):
        self.actions.append(ToolVariantAction(tool, toolpath=toolpath, **kw))

    def Apply(self, env):
        for k,v in self.kw.items():
            env[k] = v
        for act in self.actions:
            act.Apply(env)

    def Dump(self, indent=0):
        for k,v in self.kw.items():
            print ' '*indent + '{0}: {1}'.format(k, v)
        for act in self.actions:
            act.Dump(indent=indent)

    def __repr__(self):
        return 'Variant("{0}")'.format(self.name)


class VariantSet(object):
    def __init__(self, name=None):
        self.name = name
        self.variants = []

    def AddVariant(self, **kw):
        v = Variant(**kw)
        self.variants.append(v)
        return v

    def Dump(self, indent=0):
        print ' '*indent + '"{0}" :: Variants:'.format(self.name)
        for n,v in enumerate(self.variants):
            print ' '*indent + '[{0}]'.format(n)
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
