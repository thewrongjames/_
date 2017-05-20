import _

print(dir(_))
List = _.smart_compile('written_in_underscore/list._', \
    include_standard_library=False).run()['List']
