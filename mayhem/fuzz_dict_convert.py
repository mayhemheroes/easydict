#! /usr/bin/env python3
import atheris
import sys
import fuzz_helpers

with atheris.instrument_imports():
    import easydict

collection_choices = [dict, list, set, tuple]
prim_choices = [bytes, bytearray, str, float, bool, int]

allowed_dict_keys = [str]  # Mandated by easydict
allowed_dict_values = prim_choices + collection_choices
allowed_list_values = prim_choices + collection_choices
allowed_set_values = [bytes, str, float, bool, int]
allowed_tuple_values = prim_choices + collection_choices

def get_allowed_types(curr_choices):
    if not curr_choices:
        return allowed_dict_keys, allowed_dict_values

    recent = curr_choices[-1]
    if recent is dict:
        return allowed_dict_keys, allowed_dict_values
    elif recent is list:
        return allowed_list_values, []
    elif recent is set:
        return allowed_set_values, []
    elif recent is tuple:
        return allowed_tuple_values, []
    else:
        return [], []

@atheris.instrument_func
def get_random_elements(fdp: fuzz_helpers.EnhancedFuzzedDataProvider):
    elems = []
    for _ in range(fdp.ConsumeIntInRange(1, 10)):
        allowed_keys, allowed_values = get_allowed_types(elems)
        if allowed_keys:
            elems.append(fdp.PickValueInList(allowed_keys))
        if allowed_values:
            elems.append(fdp.PickValueInList(allowed_values))

        if not allowed_keys and not allowed_values:
            break
    return elems



def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    random_elems = get_random_elements(fdp)
    easydict.EasyDict(fuzz_helpers.build_fuzz_dict(fdp, random_elems))
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
