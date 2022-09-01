"""
Unit tests for the field module.

Thomas Ogden <t@ogden.eu>

"""

import unittest

from maxwellbloch import field, t_funcs

class TestInit(unittest.TestCase):

    json_str_02 = ('{'
                   '  "coupled_levels": ['
                   '    ['
                   '      1,'
                   '      2'
                   '    ]'
                   '  ],'
                   '  "detuning": 0.0,'
                   '  "detuning_positive": true,'
                   '  "label": "coupling",'
                   '  "rabi_freq": 10.0,'
                   '  "rabi_freq_t_args": {'
                   '    "ampl_1": 1.0,'
                   '    "off_1": 0.7,'
                   '    "on_1": 0.3'
                   '  },'
                   '  "rabi_freq_t_func": "square_1"'
                   '}')

    field_02 = field.Field.from_json_str(json_str_02)

    def test_init_default(self):
        """  Test Default Initialise """

        field_00 = field.Field()

        self.assertEqual(field_00.coupled_levels, [])
        self.assertEqual(field_00.detuning, 0.0)
        self.assertEqual(field_00.detuning_positive, True)
        self.assertEqual(field_00.label, '')
        self.assertEqual(field_00.rabi_freq, 0.0)
        self.assertEqual(field_00.rabi_freq_t_args, {'ampl_1': 1.0,
            'on_1': 0.0, 'off_1': 1.0})
        self.assertEqual(field_00.rabi_freq_t_func, t_funcs.square_1)

    def test_to_from_json_str(self):

        field_00 = field.Field()
        field_01 = field.Field.from_json_str(field_00.to_json_str())

        self.assertEqual(field_00.to_json_str(),
                         field_01.to_json_str())

    def test_from_json_str(self):

        self.assertEqual(self.field_02.coupled_levels, [[1,2]])
        self.assertEqual(self.field_02.detuning, 0.0)
        self.assertEqual(self.field_02.detuning_positive, True)
        self.assertEqual(self.field_02.label, 'coupling')
        self.assertEqual(self.field_02.rabi_freq, 10.0)
        self.assertEqual(self.field_02.rabi_freq_t_args, {"ampl_1": 1.0,
                                                     "off_1": 0.7,
                                                     "on_1": 0.3})
        self.assertEqual(self.field_02.rabi_freq_t_func, t_funcs.square_1)

    def test_to_from_json(self):

        import os

        filepath = "test_field_02.json"

        self.field_02.to_json(filepath)

        field_03 = field.Field().from_json(filepath)
        os.remove(filepath)

        self.assertEqual(self.field_02.to_json_str(),
                         field_03.to_json_str())

class TestBuildRabiFreqTFunc(unittest.TestCase):

    field_00 = field.Field()

    def test_null(self):

        self.field_00.build_rabi_freq_t_func(None)
        self.assertEqual(self.field_00.rabi_freq_t_func, t_funcs.square_1)
        self.assertEqual(self.field_00.rabi_freq_t_args, {'ampl_1': 1.0,
            'on_1': 0.0, 'off_1': 1.0})

    def test_square_1(self):

        self.field_00.build_rabi_freq_t_func('square_1')
        self.assertEqual(self.field_00.rabi_freq_t_func, t_funcs.square_1)

    def test_ramp_onoff_2(self):

        self.field_00.build_rabi_freq_t_func('ramp_onoff_2')
        self.assertEqual(self.field_00.rabi_freq_t_func, t_funcs.ramp_onoff_2)

    def test_undefined_t_func(self):

        with self.assertRaises(AttributeError) as context:
            self.field_00.build_rabi_freq_t_func('f_1')

        self.assertTrue("module 'maxwellbloch.t_funcs' has no attribute 'f_1'"
                        in str(context.exception))

def main():
    unittest.main(verbosity=3)

if __name__ == "__main__":
    status = main()
    sys.exit(status)
