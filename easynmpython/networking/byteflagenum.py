from enum import Enum
class ByteFlagEnum(Enum):
    @classmethod
    def getAllFlagsFor(cls, flag, gatherAll=False):
        caps = dict()
        allCaps = [(e.name, e.value) for e in cls]
        for cap in allCaps:
            if(flag == 0 and cap[1] == 0):
                caps[cap[0]] = True
            else:
                val = bool(flag & cap[1])
                if(gatherAll):
                    caps[cap[0]] = val
                else:
                    if(val):
                        caps[cap[0]] = val


        return caps