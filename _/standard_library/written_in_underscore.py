import _

print(dir(_))
List = _.smart_compile('written_in_underscore/list._').run()['List']
