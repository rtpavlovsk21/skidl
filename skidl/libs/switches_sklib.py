from skidl import Pin, Part, SchLib, SKIDL, TEMPLATE

SKIDL_lib_version = '0.0.1'

switches = SchLib(tool=SKIDL).add_parts(*[
        Part(name='SW_Coded',dest=TEMPLATE,tool=SKIDL,keywords='rotary hex',description='Rotary switch, 4-bit encoding',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='CM',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='D0',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='D1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='D2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='5',name='D3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_DIP_x01',dest=TEMPLATE,tool=SKIDL,keywords='dip switch',description='1x DIP Switch, Single Pole Single Throw (SPST) switch, small symbol',ref_prefix='SW',num_units=1,fplist=['SW?DIP?x1*'],do_erc=True,pins=[
            Pin(num='1',name='~',do_erc=True),
            Pin(num='2',name='~',do_erc=True)]),
        Part(name='SW_DIP_x02',dest=TEMPLATE,tool=SKIDL,keywords='dip switch',description='2x DIP Switch, Single Pole Single Throw (SPST) switch, small symbol',ref_prefix='SW',num_units=1,fplist=['SW?DIP?x2*'],do_erc=True,pins=[
            Pin(num='1',name='~',do_erc=True),
            Pin(num='2',name='~',do_erc=True),
            Pin(num='3',name='~',do_erc=True),
            Pin(num='4',name='~',do_erc=True)]),
        Part(name='SW_DIP_x03',dest=TEMPLATE,tool=SKIDL,keywords='dip switch',description='3x DIP Switch, Single Pole Single Throw (SPST) switch, small symbol',ref_prefix='SW',num_units=1,fplist=['SW?DIP?x3*'],do_erc=True,pins=[
            Pin(num='1',name='~',do_erc=True),
            Pin(num='2',name='~',do_erc=True),
            Pin(num='3',name='~',do_erc=True),
            Pin(num='4',name='~',do_erc=True),
            Pin(num='5',name='~',do_erc=True),
            Pin(num='6',name='~',do_erc=True)]),
        Part(name='SW_DIP_x04',dest=TEMPLATE,tool=SKIDL,keywords='dip switch',description='4x DIP Switch, Single Pole Single Throw (SPST) switch, small symbol',ref_prefix='SW',num_units=1,fplist=['SW?DIP?x4*'],do_erc=True,pins=[
            Pin(num='1',name='~',do_erc=True),
            Pin(num='2',name='~',do_erc=True),
            Pin(num='3',name='~',do_erc=True),
            Pin(num='4',name='~',do_erc=True),
            Pin(num='5',name='~',do_erc=True),
            Pin(num='6',name='~',do_erc=True),
            Pin(num='7',name='~',do_erc=True),
            Pin(num='8',name='~',do_erc=True)]),
        Part(name='SW_DIP_x05',dest=TEMPLATE,tool=SKIDL,keywords='dip switch',description='5x DIP Switch, Single Pole Single Throw (SPST) switch, small symbol',ref_prefix='SW',num_units=1,fplist=['SW?DIP?x5*'],do_erc=True,pins=[
            Pin(num='1',name='~',do_erc=True),
            Pin(num='2',name='~',do_erc=True),
            Pin(num='3',name='~',do_erc=True),
            Pin(num='4',name='~',do_erc=True),
            Pin(num='5',name='~',do_erc=True),
            Pin(num='6',name='~',do_erc=True),
            Pin(num='7',name='~',do_erc=True),
            Pin(num='8',name='~',do_erc=True),
            Pin(num='9',name='~',do_erc=True),
            Pin(num='10',name='~',do_erc=True)]),
        Part(name='SW_DIP_x06',dest=TEMPLATE,tool=SKIDL,keywords='dip switch',description='6x DIP Switch, Single Pole Single Throw (SPST) switch, small symbol',ref_prefix='SW',num_units=1,fplist=['SW?DIP?x6*'],do_erc=True,pins=[
            Pin(num='1',name='~',do_erc=True),
            Pin(num='2',name='~',do_erc=True),
            Pin(num='3',name='~',do_erc=True),
            Pin(num='4',name='~',do_erc=True),
            Pin(num='5',name='~',do_erc=True),
            Pin(num='6',name='~',do_erc=True),
            Pin(num='7',name='~',do_erc=True),
            Pin(num='8',name='~',do_erc=True),
            Pin(num='9',name='~',do_erc=True),
            Pin(num='10',name='~',do_erc=True),
            Pin(num='11',name='~',do_erc=True),
            Pin(num='12',name='~',do_erc=True)]),
        Part(name='SW_DIP_x07',dest=TEMPLATE,tool=SKIDL,keywords='dip switch',description='7x DIP Switch, Single Pole Single Throw (SPST) switch, small symbol',ref_prefix='SW',num_units=1,fplist=['SW?DIP?x7*'],do_erc=True,pins=[
            Pin(num='1',name='~',do_erc=True),
            Pin(num='2',name='~',do_erc=True),
            Pin(num='3',name='~',do_erc=True),
            Pin(num='4',name='~',do_erc=True),
            Pin(num='5',name='~',do_erc=True),
            Pin(num='6',name='~',do_erc=True),
            Pin(num='7',name='~',do_erc=True),
            Pin(num='8',name='~',do_erc=True),
            Pin(num='9',name='~',do_erc=True),
            Pin(num='10',name='~',do_erc=True),
            Pin(num='11',name='~',do_erc=True),
            Pin(num='12',name='~',do_erc=True),
            Pin(num='13',name='~',do_erc=True),
            Pin(num='14',name='~',do_erc=True)]),
        Part(name='SW_DIP_x08',dest=TEMPLATE,tool=SKIDL,keywords='dip switch',description='8x DIP Switch, Single Pole Single Throw (SPST) switch, small symbol',ref_prefix='SW',num_units=1,fplist=['SW?DIP?x8*'],do_erc=True,pins=[
            Pin(num='1',name='~',do_erc=True),
            Pin(num='2',name='~',do_erc=True),
            Pin(num='3',name='~',do_erc=True),
            Pin(num='4',name='~',do_erc=True),
            Pin(num='5',name='~',do_erc=True),
            Pin(num='6',name='~',do_erc=True),
            Pin(num='7',name='~',do_erc=True),
            Pin(num='8',name='~',do_erc=True),
            Pin(num='9',name='~',do_erc=True),
            Pin(num='10',name='~',do_erc=True),
            Pin(num='11',name='~',do_erc=True),
            Pin(num='12',name='~',do_erc=True),
            Pin(num='13',name='~',do_erc=True),
            Pin(num='14',name='~',do_erc=True),
            Pin(num='15',name='~',do_erc=True),
            Pin(num='16',name='~',do_erc=True)]),
        Part(name='SW_DIP_x09',dest=TEMPLATE,tool=SKIDL,keywords='dip switch',description='9x DIP Switch, Single Pole Single Throw (SPST) switch, small symbol',ref_prefix='SW',num_units=1,fplist=['SW?DIP?x9*'],do_erc=True,pins=[
            Pin(num='1',name='~',do_erc=True),
            Pin(num='2',name='~',do_erc=True),
            Pin(num='3',name='~',do_erc=True),
            Pin(num='4',name='~',do_erc=True),
            Pin(num='5',name='~',do_erc=True),
            Pin(num='6',name='~',do_erc=True),
            Pin(num='7',name='~',do_erc=True),
            Pin(num='8',name='~',do_erc=True),
            Pin(num='9',name='~',do_erc=True),
            Pin(num='10',name='~',do_erc=True),
            Pin(num='11',name='~',do_erc=True),
            Pin(num='12',name='~',do_erc=True),
            Pin(num='13',name='~',do_erc=True),
            Pin(num='14',name='~',do_erc=True),
            Pin(num='15',name='~',do_erc=True),
            Pin(num='16',name='~',do_erc=True),
            Pin(num='17',name='~',do_erc=True),
            Pin(num='18',name='~',do_erc=True)]),
        Part(name='SW_DIP_x10',dest=TEMPLATE,tool=SKIDL,keywords='dip switch',description='10x DIP Switch, Single Pole Single Throw (SPST) switch, small symbol',ref_prefix='SW',num_units=1,fplist=['SW?DIP?x10*'],do_erc=True,pins=[
            Pin(num='1',name='~',do_erc=True),
            Pin(num='2',name='~',do_erc=True),
            Pin(num='3',name='~',do_erc=True),
            Pin(num='4',name='~',do_erc=True),
            Pin(num='5',name='~',do_erc=True),
            Pin(num='6',name='~',do_erc=True),
            Pin(num='7',name='~',do_erc=True),
            Pin(num='8',name='~',do_erc=True),
            Pin(num='9',name='~',do_erc=True),
            Pin(num='10',name='~',do_erc=True),
            Pin(num='20',name='~',do_erc=True),
            Pin(num='11',name='~',do_erc=True),
            Pin(num='12',name='~',do_erc=True),
            Pin(num='13',name='~',do_erc=True),
            Pin(num='14',name='~',do_erc=True),
            Pin(num='15',name='~',do_erc=True),
            Pin(num='16',name='~',do_erc=True),
            Pin(num='17',name='~',do_erc=True),
            Pin(num='18',name='~',do_erc=True),
            Pin(num='19',name='~',do_erc=True)]),
        Part(name='SW_DIP_x11',dest=TEMPLATE,tool=SKIDL,keywords='dip switch',description='11x DIP Switch, Single Pole Single Throw (SPST) switch, small symbol',ref_prefix='SW',num_units=1,fplist=['SW?DIP?x11*'],do_erc=True,pins=[
            Pin(num='1',name='~',do_erc=True),
            Pin(num='2',name='~',do_erc=True),
            Pin(num='3',name='~',do_erc=True),
            Pin(num='4',name='~',do_erc=True),
            Pin(num='5',name='~',do_erc=True),
            Pin(num='6',name='~',do_erc=True),
            Pin(num='7',name='~',do_erc=True),
            Pin(num='8',name='~',do_erc=True),
            Pin(num='9',name='~',do_erc=True),
            Pin(num='10',name='~',do_erc=True),
            Pin(num='20',name='~',do_erc=True),
            Pin(num='11',name='~',do_erc=True),
            Pin(num='21',name='~',do_erc=True),
            Pin(num='12',name='~',do_erc=True),
            Pin(num='22',name='~',do_erc=True),
            Pin(num='13',name='~',do_erc=True),
            Pin(num='14',name='~',do_erc=True),
            Pin(num='15',name='~',do_erc=True),
            Pin(num='16',name='~',do_erc=True),
            Pin(num='17',name='~',do_erc=True),
            Pin(num='18',name='~',do_erc=True),
            Pin(num='19',name='~',do_erc=True)]),
        Part(name='SW_DIP_x12',dest=TEMPLATE,tool=SKIDL,keywords='dip switch',description='12x DIP Switch, Single Pole Single Throw (SPST) switch, small symbol',ref_prefix='SW',num_units=1,fplist=['SW?DIP?x12*'],do_erc=True,pins=[
            Pin(num='1',name='~',do_erc=True),
            Pin(num='2',name='~',do_erc=True),
            Pin(num='3',name='~',do_erc=True),
            Pin(num='4',name='~',do_erc=True),
            Pin(num='5',name='~',do_erc=True),
            Pin(num='6',name='~',do_erc=True),
            Pin(num='7',name='~',do_erc=True),
            Pin(num='8',name='~',do_erc=True),
            Pin(num='9',name='~',do_erc=True),
            Pin(num='10',name='~',do_erc=True),
            Pin(num='20',name='~',do_erc=True),
            Pin(num='11',name='~',do_erc=True),
            Pin(num='21',name='~',do_erc=True),
            Pin(num='12',name='~',do_erc=True),
            Pin(num='22',name='~',do_erc=True),
            Pin(num='13',name='~',do_erc=True),
            Pin(num='23',name='~',do_erc=True),
            Pin(num='14',name='~',do_erc=True),
            Pin(num='24',name='~',do_erc=True),
            Pin(num='15',name='~',do_erc=True),
            Pin(num='16',name='~',do_erc=True),
            Pin(num='17',name='~',do_erc=True),
            Pin(num='18',name='~',do_erc=True),
            Pin(num='19',name='~',do_erc=True)]),
        Part(name='SW_DPDT_x2',dest=TEMPLATE,tool=SKIDL,keywords='switch dual-pole double-throw DPDT spdt ON-ON',description='Switch, dual pole double throw, separate symbols',ref_prefix='SW',num_units=2,do_erc=True,pins=[
            Pin(num='1',name='A',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='B',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='C',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='A',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='B',func=Pin.PASSIVE,do_erc=True),
            Pin(num='5',name='C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_DPST',dest=TEMPLATE,tool=SKIDL,keywords='switch dual double-pole single-throw OFF-ON',description='Double Pole Single Throw (DPST) Switch',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',do_erc=True),
            Pin(num='2',name='2',do_erc=True),
            Pin(num='3',name='3',do_erc=True),
            Pin(num='4',name='4',do_erc=True)]),
        Part(name='SW_DPST_Temperature',dest=TEMPLATE,tool=SKIDL,keywords='temerature switch dual double-pole single-throw OFF-ON',description='Double Pole Single Throw (DPST) Switch, temperature dependent',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',do_erc=True),
            Pin(num='2',name='2',do_erc=True),
            Pin(num='3',name='3',do_erc=True),
            Pin(num='4',name='4',do_erc=True)]),
        Part(name='SW_DPST_x2',dest=TEMPLATE,tool=SKIDL,keywords='switch lever',description='Single Pole Single Throw (SPST) switch, separate symbol',ref_prefix='SW',num_units=2,do_erc=True,pins=[
            Pin(num='1',name='A',do_erc=True),
            Pin(num='2',name='B',do_erc=True),
            Pin(num='3',name='A',do_erc=True),
            Pin(num='4',name='B',do_erc=True)]),
        Part(name='SW_E3_SA3216',dest=TEMPLATE,tool=SKIDL,keywords='switch normally-open pushbutton push-button LCD',description='Push button switch with LCD screen',ref_prefix='SW',num_units=1,do_erc=True,aliases=['SW_E3_SA3624', 'SW_E3_SA6432', 'SW_MMI_Q5-100'],pins=[
            Pin(num='1',name='GND',func=Pin.PWRIN,do_erc=True),
            Pin(num='2',name='5V',func=Pin.PWRIN,do_erc=True),
            Pin(num='3',name='CLK',do_erc=True),
            Pin(num='4',name='DAT',do_erc=True),
            Pin(num='5',name='SW1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='6',name='SW2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Push',dest=TEMPLATE,tool=SKIDL,keywords='switch normally-open pushbutton push-button',description='Push button switch, generic, two pins',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Push_45deg',dest=TEMPLATE,tool=SKIDL,keywords='switch normally-open pushbutton push-button',description='Push button switch, normally open, two pins, 45° tilted',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Push_Dual',dest=TEMPLATE,tool=SKIDL,keywords='switch normally-open pushbutton push-button',description='Push button switch, generic, symbol, four pins',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='3',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='4',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Push_Dual_x2',dest=TEMPLATE,tool=SKIDL,keywords='switch normally-open pushbutton push-button',description='Push button switch, generic, separate symbols, four pins',ref_prefix='SW',num_units=2,do_erc=True,pins=[
            Pin(num='3',name='A',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='B',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Push_LED',dest=TEMPLATE,tool=SKIDL,keywords='switch normally-open pushbutton push-button LED',description='Push button switch with LED, generic',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='K',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Push_Lamp',dest=TEMPLATE,tool=SKIDL,keywords='switch normally-open pushbutton push-button Lamp',description='Push button switch with Signal Lamp, generic',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='L',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='L',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Push_Open',dest=TEMPLATE,tool=SKIDL,keywords='switch normally-closed pushbutton push-button',description='Push button switch, push-to-open, generic, two pins',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='A',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='B',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Push_Open_Dual',dest=TEMPLATE,tool=SKIDL,keywords='switch normally-closed pushbutton push-button',description='Push button switch, normally closed, generic, four pins',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='3',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='4',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Push_Open_Dual_x2',dest=TEMPLATE,tool=SKIDL,keywords='switch normally-closed pushbutton push-button',description='Push button switch, push-to-open, generic, two pins',ref_prefix='SW',num_units=2,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='2',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Push_SPDT',dest=TEMPLATE,tool=SKIDL,keywords='switch single-pole double-throw spdt ON-ON',description='Momentary Switch, single pole double throw',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='A',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='B',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Reed',dest=TEMPLATE,tool=SKIDL,keywords='reed magnetic switch',description='reed switch',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',do_erc=True),
            Pin(num='2',name='2',do_erc=True)]),
        Part(name='SW_Reed_Opener',dest=TEMPLATE,tool=SKIDL,keywords='reed magnetic switch',description='reed switch, default-closed',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',do_erc=True),
            Pin(num='2',name='2',do_erc=True)]),
        Part(name='SW_Reed_SPDT',dest=TEMPLATE,tool=SKIDL,keywords='reed magnetic switch SPDT',description='SPDT reed switch',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',do_erc=True),
            Pin(num='2',name='2',do_erc=True),
            Pin(num='3',name='3',do_erc=True)]),
        Part(name='SW_Rotary12',dest=TEMPLATE,tool=SKIDL,keywords='rotary switch',description='rotary switch with 12 positions',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='3',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='4',func=Pin.PASSIVE,do_erc=True),
            Pin(num='5',name='5',func=Pin.PASSIVE,do_erc=True),
            Pin(num='6',name='6',func=Pin.PASSIVE,do_erc=True),
            Pin(num='7',name='7',func=Pin.PASSIVE,do_erc=True),
            Pin(num='8',name='8',func=Pin.PASSIVE,do_erc=True),
            Pin(num='9',name='9',func=Pin.PASSIVE,do_erc=True),
            Pin(num='10',name='10',func=Pin.PASSIVE,do_erc=True),
            Pin(num='11',name='11',func=Pin.PASSIVE,do_erc=True),
            Pin(num='12',name='12',func=Pin.PASSIVE,do_erc=True),
            Pin(num='13',name='13',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Rotary2x6',dest=TEMPLATE,tool=SKIDL,keywords='rotary switch',description='2 rotary switch with 6 positions',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='3',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='4',func=Pin.PASSIVE,do_erc=True),
            Pin(num='5',name='5',func=Pin.PASSIVE,do_erc=True),
            Pin(num='6',name='6',func=Pin.PASSIVE,do_erc=True),
            Pin(num='7',name='7',func=Pin.PASSIVE,do_erc=True),
            Pin(num='8',name='8',func=Pin.PASSIVE,do_erc=True),
            Pin(num='9',name='9',func=Pin.PASSIVE,do_erc=True),
            Pin(num='10',name='10',func=Pin.PASSIVE,do_erc=True),
            Pin(num='11',name='11',func=Pin.PASSIVE,do_erc=True),
            Pin(num='12',name='12',func=Pin.PASSIVE,do_erc=True),
            Pin(num='13',name='13',func=Pin.PASSIVE,do_erc=True),
            Pin(num='14',name='14',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Rotary3x4',dest=TEMPLATE,tool=SKIDL,keywords='rotary switch',description='3 rotary switches with 4 positions',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='3',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='4',func=Pin.PASSIVE,do_erc=True),
            Pin(num='5',name='5',func=Pin.PASSIVE,do_erc=True),
            Pin(num='6',name='6',func=Pin.PASSIVE,do_erc=True),
            Pin(num='7',name='7',func=Pin.PASSIVE,do_erc=True),
            Pin(num='8',name='8',func=Pin.PASSIVE,do_erc=True),
            Pin(num='9',name='9',func=Pin.PASSIVE,do_erc=True),
            Pin(num='10',name='10',func=Pin.PASSIVE,do_erc=True),
            Pin(num='11',name='11',func=Pin.PASSIVE,do_erc=True),
            Pin(num='12',name='12',func=Pin.PASSIVE,do_erc=True),
            Pin(num='13',name='13',func=Pin.PASSIVE,do_erc=True),
            Pin(num='14',name='14',func=Pin.PASSIVE,do_erc=True),
            Pin(num='15',name='15',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_Rotary4x3',dest=TEMPLATE,tool=SKIDL,keywords='rotary switch',description='4 rotary switches with 3 positions',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='3',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='4',func=Pin.PASSIVE,do_erc=True),
            Pin(num='5',name='5',func=Pin.PASSIVE,do_erc=True),
            Pin(num='6',name='6',func=Pin.PASSIVE,do_erc=True),
            Pin(num='7',name='7',func=Pin.PASSIVE,do_erc=True),
            Pin(num='8',name='8',func=Pin.PASSIVE,do_erc=True),
            Pin(num='9',name='9',func=Pin.PASSIVE,do_erc=True),
            Pin(num='10',name='10',func=Pin.PASSIVE,do_erc=True),
            Pin(num='11',name='11',func=Pin.PASSIVE,do_erc=True),
            Pin(num='12',name='12',func=Pin.PASSIVE,do_erc=True),
            Pin(num='13',name='13',func=Pin.PASSIVE,do_erc=True),
            Pin(num='14',name='14',func=Pin.PASSIVE,do_erc=True),
            Pin(num='15',name='15',func=Pin.PASSIVE,do_erc=True),
            Pin(num='16',name='16',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_SP3T',dest=TEMPLATE,tool=SKIDL,keywords='switch sp3t ON-ON-ON',description='Switch, three position, single pole triple throw, 3 position switch, SP3T',ref_prefix='SW',num_units=1,fplist=['SW*', 'SP3T*'],do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='3',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='4',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_SPDT',dest=TEMPLATE,tool=SKIDL,keywords='switch single-pole double-throw spdt ON-ON',description='Switch, single pole double throw',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='A',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='B',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='C',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_SPDT_MSM',dest=TEMPLATE,tool=SKIDL,keywords='switch spdt single-pole double-throw ON-OFF-ON',description='Switch, single pole double throw, center OFF position',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='3',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_SPST',dest=TEMPLATE,tool=SKIDL,keywords='switch lever',description='Single Pole Single Throw (SPST) switch',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='A',do_erc=True),
            Pin(num='2',name='B',do_erc=True)]),
        Part(name='SW_SPST_LED',dest=TEMPLATE,tool=SKIDL,keywords='switch SPST LED OFF-ON',description='Single Pole Single Throw (SPST) switch with LED, generic',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='K',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='A',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_SPST_Lamp',dest=TEMPLATE,tool=SKIDL,keywords='switch SPST LED OFF-ON lamp',description='Single Pole Single Throw (SPST) switch with signal lamp, generic',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='1',func=Pin.PASSIVE,do_erc=True),
            Pin(num='2',name='2',func=Pin.PASSIVE,do_erc=True),
            Pin(num='3',name='L',func=Pin.PASSIVE,do_erc=True),
            Pin(num='4',name='L',func=Pin.PASSIVE,do_erc=True)]),
        Part(name='SW_SPST_Temperature',dest=TEMPLATE,tool=SKIDL,keywords='temperature switch',description='Single Pole Single Throw (SPST) switch, temperature dependent',ref_prefix='SW',num_units=1,do_erc=True,pins=[
            Pin(num='1',name='A',do_erc=True),
            Pin(num='2',name='B',do_erc=True)])])