
class BaseEnum(object):
    def as_dict(self):
        return self.__dict__

    def values(self):
        return self.__dict__.values()

    def keys(self):
        return self.__dict__.keys()

    def value(self, key):
        return self.__dict__.get(key, '')


def _multiplexed_buffer_helper(buf):
    walker = 0
    while True:
        if len(buf[walker:]) < 8:
            break
        _, length = struct.unpack_from('>BxxxL', buf[walker:])
        start = walker + 8
        end = start + length
        walker = end
        yield buf[start:end]