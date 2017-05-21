import _


List = _.smart_compile('_/standard_library/written_in_underscore/list._', \
    running_underscore_standard_library=True).run()['List']

WRITTEN_IN_UNDERSCORE = {
    'List': List
}
