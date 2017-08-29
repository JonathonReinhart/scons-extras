import itertools

def pystr(s):
    if isinstance(s, basestring):
        s = '"' + s + '"'
    return str(s)

def func_call_syntax(args, kwargs):
    kwargs = ['{}={}'.format(k, pystr(v)) for k,v in kwargs.items()]
    args = [pystr(a) for a in args]
    return ', '.join(args + kwargs)

class VariantAction(object):
    def __init__(self, method, *args, **kwargs):
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def Apply(self, env):
        getattr(env, self.method)(*self.args, **self.kwargs)

    def Dump(self, indent=0):
        print ' '*indent + '.{}({})'.format(self.method, func_call_syntax(self.args, self.kwargs))

class Variant(object):
    def __init__(self, **kw):
        self.kw = kw
        self.actions = []

    def Append(self, **kw):
        self.actions.append(VariantAction('Append', **kw))

    def AppendUnique(self, **kw):
        self.actions.append(VariantAction('AppendUnique', **kw))

    def Replace(self, **kw):
        self.kw.update(kw)

    def SetDefault(self, **kw):
        self.actions.append(VariantAction('SetDefault', **kw))

    def Tool(self, tool, toolpath=None, **kw):
        self.actions.append(VariantAction('Tool', tool, toolpath=toolpath, **kw))

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
            print ''


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
