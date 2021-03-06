# -*- python-mode -*-
# -*- coding: UTF-8 -*-

## Copyright (C) 2012-2013  Daniel Pavel
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with this program; if not, write to the Free Software Foundation, Inc.,
## 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import absolute_import, division, print_function, unicode_literals

from collections import namedtuple
from logging import DEBUG as _DEBUG
from logging import getLogger

from . import hidpp10 as _hidpp10
from . import hidpp20 as _hidpp20
from . import special_keys as _special_keys
from .common import NamedInts as _NamedInts
from .common import bytes2int as _bytes2int
from .common import int2bytes as _int2bytes
from .common import unpack as _unpack
from .i18n import _
from .settings import BitFieldSetting as _BitFieldSetting
from .settings import BitFieldValidator as _BitFieldV
from .settings import BitFieldWithOffsetAndMaskSetting as _BitFieldOMSetting
from .settings import BitFieldWithOffsetAndMaskValidator as _BitFieldOMV
from .settings import BooleanValidator as _BooleanV
from .settings import ChoicesMapValidator as _ChoicesMapV
from .settings import ChoicesValidator as _ChoicesV
from .settings import FeatureRW as _FeatureRW
from .settings import FeatureRWMap as _FeatureRWMap
from .settings import LongSettings as _LongSettings
from .settings import MultipleRangeValidator as _MultipleRangeV
from .settings import RangeValidator as _RangeV
from .settings import RegisterRW as _RegisterRW
from .settings import Setting as _Setting
from .settings import Settings as _Settings
from .special_keys import DISABLE as _DKEY

_log = getLogger(__name__)
del getLogger

_DK = _hidpp10.DEVICE_KIND
_R = _hidpp10.REGISTERS
_F = _hidpp20.FEATURE

_GG = _hidpp20.GESTURE
_GP = _hidpp20.PARAM

#
# common strings for settings - name, string to display in main window, tool tip for main window
#

# yapf: disable
_HAND_DETECTION = ('hand-detection', _('Hand Detection'), _('Turn on illumination when the hands hover over the keyboard.'))
_SMOOTH_SCROLL = ('smooth-scroll', _('Smooth Scrolling'), _('High-sensitivity mode for vertical scroll with the wheel.'))
_SIDE_SCROLL = ('side-scroll', _('Side Scrolling'),
                _('When disabled, pushing the wheel sideways sends custom button events\n'
                  'instead of the standard side-scrolling events.'))
_HI_RES_SCROLL = ('hi-res-scroll', _('High Resolution Scrolling'),
                  _('High-sensitivity mode for vertical scroll with the wheel.'))
_LOW_RES_SCROLL = ('lowres-smooth-scroll', _('HID++ Scrolling'),
                   _('HID++ mode for vertical scroll with the wheel.') + '\n' +
                   _('Effectively turns off wheel scrolling in Linux.'))
_HIRES_INV = ('hires-smooth-invert', _('High Resolution Wheel Invert'),
              _('High-sensitivity wheel invert direction for vertical scroll.'))
_HIRES_RES = ('hires-smooth-resolution', _('Wheel Resolution'),
              _('High-sensitivity mode for vertical scroll with the wheel.'))
_FN_SWAP = ('fn-swap', _('Swap Fx function'),
            _('When set, the F1..F12 keys will activate their special function,\n'
              'and you must hold the FN key to activate their standard function.') + '\n\n' +
            _('When unset, the F1..F12 keys will activate their standard function,\n'
              'and you must hold the FN key to activate their special function.'))
_DPI = ('dpi', _('Sensitivity (DPI)'), None)
_POINTER_SPEED = ('pointer_speed', _('Sensitivity (Pointer Speed)'),
                  _('Speed multiplier for mouse (256 is normal multiplier).'))
_SMART_SHIFT = ('smart-shift', _('Smart Shift'),
                _('Automatically switch the mouse wheel between ratchet and freespin mode.\n'
                  'The mouse wheel is always free at 0, and always locked at 50'))
_BACKLIGHT = ('backlight', _('Backlight'), _('Turn illumination on or off on keyboard.'))
_REPROGRAMMABLE_KEYS = ('reprogrammable-keys', _('Actions'),
                        _('Change the action for the key or button.') + '\n' +
                        _('Changing important actions (such as for the left mouse button) can result in an unusable system.'))
_DISABLE_KEYS = ('disable-keyboard-keys', _('Disable keys'), _('Disable specific keyboard keys.'))
_PLATFORM = ('multiplatform', _('Set OS'), _('Change keys to match OS.'))
_CHANGE_HOST = ('change-host', _('Change Host'), _('Switch connection to a different host'))
_THUMB_SCROLL_MODE = ('thumb-scroll-mode', _('HID++ Thumb Scrolling'),
                      _('HID++ mode for horizontal scroll with the thumb wheel.') + '\n' +
                      _('Effectively turns off thumb scrolling in Linux.'))
_THUMB_SCROLL_INVERT = ('thumb-scroll-invert', _('Thumb Scroll Invert'), _('Invert thumb scroll direction.'))
_GESTURE2_GESTURES = ('gesture2-gestures', _('Gestures'), _('Tweaks the mouse/touchpad behaviour.'))
_GESTURE2_PARAMS = ('gesture2-params', _('Gesture params'), _('Changes numerical parameters of a mouse/touchpad.'))


_GESTURE2_GESTURES_LABELS = {
    _GG['Tap1Finger']: (_('Single tap'), _('Performs a left click.')),
    _GG['Tap2Finger']: (_('Double tap'), _('Performs a right click.')),
    _GG['Tap3Finger']: (_('Triple tap'), None),
    _GG['Click1Finger']: (None, None),
    _GG['Click2Finger']: (None, None),
    _GG['Click3Finger']: (None, None),
    _GG['DoubleTap1Finger']: (_('Double tap'), _('Performs a double click.')),
    _GG['DoubleTap2Finger']: (_('Double tap with two fingers'), None),
    _GG['DoubleTap3Finger']: (_('Double tap with three fingers'), None),
    _GG['Track1Finger']: (None, None),
    _GG['TrackingAcceleration']: (None, None),
    _GG['TapDrag1Finger']: (_('Tap and drag'), _('Drags items by dragging the finger after double tapping.')),
    _GG['TapDrag2Finger']: (_('Tap and drag with two fingers'),
                            _('Drags items by dragging the fingers after double tapping.')),
    _GG['Drag3Finger']: (_('Tap and drag with three fingers'), None),
    _GG['TapGestures']: (None, None),
    _GG['FnClickGestureSuppression']: (_('Suppress tap and edge gestures'),
                                       _('Disables tap and edge gestures (equivalent to pressing Fn+LeftClick).')),
    _GG['Scroll1Finger']: (_('Scroll with one finger'), _('Scrolls.')),
    _GG['Scroll2Finger']: (_('Scroll with two fingers'), _('Scrolls.')),
    _GG['Scroll2FingerHoriz']: (_('Scroll horizontally with two fingers'), _('Scrolls horizontally.')),
    _GG['Scroll2FingerVert']: (_('Scroll vertically with two fingers'), _('Scrolls vertically.')),
    _GG['Scroll2FingerStateless']: (_('Scroll with two fingers'), _('Scrolls.')),
    _GG['NaturalScrolling']: (_('Natural scrolling'), _('Inverts the scrolling direction.')),
    _GG['Thumbwheel']: (_('Thumbwheel'), _('Enables the thumbwheel.')),
    _GG['VScrollInertia']: (None, None),
    _GG['VScrollBallistics']: (None, None),
    _GG['Swipe2FingerHoriz']: (None, None),
    _GG['Swipe3FingerHoriz']: (None, None),
    _GG['Swipe4FingerHoriz']: (None, None),
    _GG['Swipe3FingerVert']: (None, None),
    _GG['Swipe4FingerVert']: (None, None),
    _GG['LeftEdgeSwipe1Finger']: (None, None),
    _GG['RightEdgeSwipe1Finger']: (None, None),
    _GG['BottomEdgeSwipe1Finger']: (None, None),
    _GG['TopEdgeSwipe1Finger']: (_('Swipe from the top edge'), None),
    _GG['LeftEdgeSwipe1Finger2']: (_('Swipe from the left edge'), None),
    _GG['RightEdgeSwipe1Finger2']: (_('Swipe from the right edge'), None),
    _GG['BottomEdgeSwipe1Finger2']: (_('Swipe from the bottom edge'), None),
    _GG['TopEdgeSwipe1Finger2']: (_('Swipe from the top edge'), None),
    _GG['LeftEdgeSwipe2Finger']: (_('Swipe two fingers from the left edge'), None),
    _GG['RightEdgeSwipe2Finger']: (_('Swipe two fingers from the right edge'), None),
    _GG['BottomEdgeSwipe2Finger']: (_('Swipe two fingers from the bottom edge'), None),
    _GG['TopEdgeSwipe2Finger']: (_('Swipe two fingers from the top edge'), None),
    _GG['Zoom2Finger']: (_('Zoom with two fingers.'), _('Pinch to zoom out; spread to zoom in.')),
    _GG['Zoom2FingerPinch']: (_('Pinch to zoom out.'), _('Pinch to zoom out.')),
    _GG['Zoom2FingerSpread']: (_('Spread to zoom in.'), _('Spread to zoom in.')),
    _GG['Zoom3Finger']: (_('Zoom with three fingers.'), None),
    _GG['Zoom2FingerStateless']: (_('Zoom with two fingers'), _('Pinch to zoom out; spread to zoom in.')),
    _GG['TwoFingersPresent']: (None, None),
    _GG['Rotate2Finger']: (None, None),
    _GG['Finger1']: (None, None),
    _GG['Finger2']: (None, None),
    _GG['Finger3']: (None, None),
    _GG['Finger4']: (None, None),
    _GG['Finger5']: (None, None),
    _GG['Finger6']: (None, None),
    _GG['Finger7']: (None, None),
    _GG['Finger8']: (None, None),
    _GG['Finger9']: (None, None),
    _GG['Finger10']: (None, None),
    _GG['DeviceSpecificRawData']: (None, None),
}

_GESTURE2_PARAMS_LABELS = {
    _GP['ExtraCapabilities']: (None, None),  # not supported
    _GP['PixelZone']: ('Pixel zone', None),  # TO DO: replace None with a short description
    _GP['RatioZone']: ('Ratio zone', None),  # TO DO: replace None with a short description
    _GP['ScaleFactor']: ('Scale factor', 'Sets the cursor speed.'),
}

_GESTURE2_PARAMS_LABELS_SUB = {
    'left': (_('Left'), _('Left-most coordinate.')),
    'top': (_('top'), _('Top-most coordinate.')),
    'width': (_('width'), _('Width.')),
    'height': (_('height'), _('Height.')),
    'scale': (_('Scale'), _('Cursor speed.')),
}

_DISABLE_KEYS_LABEL_SUB = _('Disables the %s key.')

# yapf: enable

# Setting template functions need to set up the setting itself, the validator, and the reader/writer.
# The reader/writer is responsible for reading raw values from the device and writing values to it.
# The validator is responsible for turning read raw values into Python data and Python data into raw values to be written.
# The setting keeps everything together and provides control.
#
# The _Setting class is for settings with simple values (booleans, numbers in a range, and symbolic choices).
# Its positional arguments are the strings for the setting and the reader/writer.
# The validator keyword (or third) argument is the validator, if the validator does not depend on information from the device.
# The callback keyword argument is a function that given a device as argument returns the validator or None.
# If the callback function returns None the setting is not created for the device.
# Either a validator or callback must be specified, but not both.
# The device_kind keyword argument (default None) says what kinds of devices can use the setting.
# (This argument is currently not used because keyboards with integrated trackpads break its abstraction.)
# The persist keyword argument (default True) says whether to store the value and apply it when setting up the device.
#
# There are two simple reader/writers - _RegisterRW and _FeatureRW.
# _RegisterRW is for register-based settings and takes the register name as argument.
# _FeatureRW is for feature-based settings and takes the feature name as positional argument plus the following:
#   read_fnid is the feature function (times 16) to read the value (default 0x00),
#   write_fnid is the feature function (times 16) to write the value (default 0x10),
#   no_reply is whether to wait for a reply (default false) (USE WITH EXTREME CAUTION).
#
# There are three simple validators - _BooleanV, _RangeV, and _ChoicesV
# _BooleanV is for boolean values.  It takes three keyword arguments that can be integers or byte strings:
#   true_value is the raw value for true (default 0x01),
#   false_value is the raw value for false (default 0x00),
#   mask is used to keep only some bits from a sequence of bits.
# _RangeV is for an integer in a range.  It takes three keyword arguments:
#   min_value is the minimum value for the setting,
#   max_value is the maximum value for the setting,
#   byte_count is number of bytes that the value is stored in (defaults to size of max_value).
# _ChoicesV is for symbolic choices.  It takes one positional and three keyword arguments:
#   the positional argument is a list of named integers that are the valid choices,
#   byte_count is the number of bytes for the integer (default size of largest choice integer),
#   read_skip_byte_count is the number of bytes to ignore at the beginning of the read value (default 0),
#   write_prefix_bytes is a byte string to write before the value (default empty).
#
# The _Settings class is for settings that are maps from keys to values.
# The _BitFieldSetting class is for settings that have multiple boolean values packed into a bit field.
# They have has same arguments as the _Setting class.
#
# _ChoicesMapV validator is for map settings that map onto symbolic choices.   It takes four keyword arguments:
#   the positional argument is the choices map
#   byte_count is as for _ChoicesV,
#   read_skip_byte_count is as for _ChoicesV,
#   write_prefix_bytes is as for _ChoicesV,
#   key_byte_count is the number of bytes for the key integer (default size of largest key),
#   extra_default is an extra raw value that is used as a default value (default None).
# _BitFieldV validator is for bit field settings.  It takes one positional and one keyword argument
#   the positional argument is the number of bits in the bit field
#   byte_count is the size of the bit field (default size of the bit field)


def _register_hand_detection():
    validator = _BooleanV(true_value=b'\x00\x00\x00', false_value=b'\x00\x00\x30', mask=b'\x00\x00\xFF')
    return _Setting(_HAND_DETECTION, _RegisterRW(_R.keyboard_hand_detection), validator, device_kind=(_DK.keyboard, ))


def _register_fn_swap():
    validator = _BooleanV(true_value=b'\x00\x01', mask=b'\x00\x01')
    return _Setting(_FN_SWAP, _RegisterRW(_R.keyboard_fn_swap), validator, device_kind=(_DK.keyboard, ))


def _register_smooth_scroll():
    validator = _BooleanV(true_value=0x40, mask=0x40)
    return _Setting(_SMOOTH_SCROLL, _RegisterRW(_R.mouse_button_flags), validator, device_kind=(_DK.mouse, _DK.trackball))


def _register_side_scroll():
    validator = _BooleanV(true_value=0x02, mask=0x02)
    return _Setting(_SIDE_SCROLL, _RegisterRW(_R.mouse_button_flags), validator, device_kind=(_DK.mouse, _DK.trackball))


def _register_dpi(choices=None):
    return _Setting(_DPI, _RegisterRW(_R.mouse_dpi), _ChoicesV(choices), device_kind=(_DK.mouse, _DK.trackball))


def _feature_fn_swap():
    return _Setting(_FN_SWAP, _FeatureRW(_F.FN_INVERSION), _BooleanV(), device_kind=(_DK.keyboard, ))


def _feature_new_fn_swap():
    return _Setting(_FN_SWAP, _FeatureRW(_F.NEW_FN_INVERSION), _BooleanV(), device_kind=(_DK.keyboard, ))


# ignore the capabilities part of the feature - all devices should be able to swap Fn state
# just use the current host (first byte = 0xFF) part of the feature to read and set the Fn state
def _feature_k375s_fn_swap():
    validator = _BooleanV(true_value=b'\xFF\x01', false_value=b'\xFF\x00')
    return _Setting(_FN_SWAP, _FeatureRW(_F.K375S_FN_INVERSION), validator, device_kind=(_DK.keyboard, ))


# FIXME: This will enable all supported backlight settings,
# we should allow the users to select which settings they want to enable.
def _feature_backlight2():
    return _Setting(_BACKLIGHT, _FeatureRW(_F.BACKLIGHT2), _BooleanV(), device_kind=(_DK.keyboard, ))


def _feature_hi_res_scroll():
    return _Setting(_HI_RES_SCROLL, _FeatureRW(_F.HI_RES_SCROLLING), _BooleanV(), device_kind=(_DK.mouse, _DK.trackball))


def _feature_lowres_smooth_scroll():
    return _Setting(_LOW_RES_SCROLL, _FeatureRW(_F.LOWRES_WHEEL), _BooleanV(), device_kind=(_DK.mouse, _DK.trackball))


def _feature_hires_smooth_invert():
    rw = _FeatureRW(_F.HIRES_WHEEL, read_fnid=0x10, write_fnid=0x20)
    validator = _BooleanV(true_value=0x04, mask=0x04)
    return _Setting(_HIRES_INV, rw, validator, device_kind=(_DK.mouse, _DK.trackball))


def _feature_hires_smooth_resolution():
    rw = _FeatureRW(_F.HIRES_WHEEL, read_fnid=0x10, write_fnid=0x20)
    validator = _BooleanV(true_value=0x02, mask=0x02)
    return _Setting(_HIRES_RES, rw, validator, device_kind=(_DK.mouse, _DK.trackball))


def _feature_smart_shift():
    _MIN_SMART_SHIFT_VALUE = 0
    _MAX_SMART_SHIFT_VALUE = 50

    class _SmartShiftRW(_FeatureRW):
        def __init__(self, feature):
            super(_SmartShiftRW, self).__init__(feature)

        def read(self, device):
            value = super(_SmartShiftRW, self).read(device)
            if _bytes2int(value[0:1]) == 1:
                # Mode = Freespin, map to minimum
                return _int2bytes(_MIN_SMART_SHIFT_VALUE, count=1)
            else:
                # Mode = smart shift, map to the value, capped at maximum
                threshold = min(_bytes2int(value[1:2]), _MAX_SMART_SHIFT_VALUE)
                return _int2bytes(threshold, count=1)

        def write(self, device, data_bytes):
            threshold = _bytes2int(data_bytes)
            # Freespin at minimum
            mode = 1 if threshold == _MIN_SMART_SHIFT_VALUE else 2
            # Ratchet at maximum
            if threshold == _MAX_SMART_SHIFT_VALUE:
                threshold = 255
            data = _int2bytes(mode, count=1) + _int2bytes(threshold, count=1) * 2
            return super(_SmartShiftRW, self).write(device, data)

    validator = _RangeV(_MIN_SMART_SHIFT_VALUE, _MAX_SMART_SHIFT_VALUE, 1)
    return _Setting(_SMART_SHIFT, _SmartShiftRW(_F.SMART_SHIFT), validator, device_kind=(_DK.mouse, _DK.trackball))


def _feature_adjustable_dpi_callback(device):
    # [1] getSensorDpiList(sensorIdx)
    reply = device.feature_request(_F.ADJUSTABLE_DPI, 0x10)
    # Should not happen, but might happen when the user unplugs device while the
    # query is being executed. TODO retry logic?
    assert reply, 'Oops, DPI list cannot be retrieved!'
    dpi_list = []
    step = None
    for val in _unpack('!7H', reply[1:1 + 14]):
        if val == 0:
            break
        if val >> 13 == 0b111:
            assert step is None and len(dpi_list) == 1, \
              'Invalid DPI list item: %r' % val
            step = val & 0x1fff
        else:
            dpi_list.append(val)
    if step:
        assert len(dpi_list) == 2, 'Invalid DPI list range: %r' % dpi_list
        dpi_list = range(dpi_list[0], dpi_list[1] + 1, step)
    return _ChoicesV(_NamedInts.list(dpi_list), byte_count=3) if dpi_list else None


def _feature_adjustable_dpi():
    """Pointer Speed feature"""
    # Assume sensorIdx 0 (there is only one sensor)
    # [2] getSensorDpi(sensorIdx) -> sensorIdx, dpiMSB, dpiLSB
    # [3] setSensorDpi(sensorIdx, dpi)
    rw = _FeatureRW(_F.ADJUSTABLE_DPI, read_fnid=0x20, write_fnid=0x30)
    return _Setting(_DPI, rw, callback=_feature_adjustable_dpi_callback, device_kind=(_DK.mouse, _DK.trackball))


def _feature_pointer_speed():
    """Pointer Speed feature"""
    # min and max values taken from usb traces of Win software
    validator = _RangeV(0x002e, 0x01ff, 2)
    rw = _FeatureRW(_F.POINTER_SPEED)
    return _Setting(_POINTER_SPEED, rw, validator, device_kind=(_DK.mouse, _DK.trackball))


# the keys for the choice map are Logitech controls (from special_keys)
# each choice value is a NamedInt with the string from a task (to be shown to the user)
# and the integer being the control number for that task (to be written to the device)
# Solaar only remaps keys (controlled by key gmask and group), not other key reprogramming
def _feature_reprogrammable_keys_callback(device):
    choices = {}
    for k in device.keys:
        tgts = k.remappable_to
        if len(tgts) > 1:
            choices[k.key] = tgts
    if not choices:
        return None
    return _ChoicesMapV(
        choices, key_byte_count=2, byte_count=2, read_skip_byte_count=1, write_prefix_bytes=b'\x00', extra_default=0
    )


def _feature_reprogrammable_keys():
    rw = _FeatureRWMap(_F.REPROG_CONTROLS_V4, read_fnid=0x20, write_fnid=0x30, key_byte_count=2)
    return _Settings(_REPROGRAMMABLE_KEYS, rw, callback=_feature_reprogrammable_keys_callback, device_kind=(_DK.keyboard, ))


def _feature_disable_keyboard_keys_callback(device):
    mask = device.feature_request(_F.KEYBOARD_DISABLE_KEYS)[0]
    options = [_special_keys.DISABLE[1 << i] for i in range(8) if mask & (1 << i)]
    return _BitFieldV(options) if options else None


def _feature_disable_keyboard_keys():
    rw = _FeatureRW(_F.KEYBOARD_DISABLE_KEYS, read_fnid=0x10, write_fnid=0x20)
    s = _BitFieldSetting(_DISABLE_KEYS, rw, callback=_feature_disable_keyboard_keys_callback, device_kind=(_DK.keyboard, ))
    s._labels = {k: (None, _DISABLE_KEYS_LABEL_SUB % k) for k in _DKEY}
    return s


# muultiplatform OS bits
OSS = [('Linux', 0x0400), ('MacOS', 0x2000), ('Windows', 0x0100), ('iOS', 0x4000), ('Android', 0x1000), ('WebOS', 0x8000),
       ('Chrome', 0x0800), ('WinEmb', 0x0200), ('Tizen', 0x0001)]


def _feature_multiplatform_callback(device):
    def _str_os_versions(low, high):
        def _str_os_version(version):
            if version == 0:
                return ''
            elif version & 0xFF:
                return str(version >> 8) + '.' + str(version & 0xFF)
            else:
                return str(version >> 8)

        return '' if low == 0 and high == 0 else ' ' + _str_os_version(low) + '-' + _str_os_version(high)

    infos = device.feature_request(_F.MULTIPLATFORM)
    assert infos, 'Oops, multiplatform count cannot be retrieved!'
    flags, _ignore, num_descriptors = _unpack('!BBB', infos[:3])
    if not (flags & 0x02):  # can't set platform so don't create setting
        return []
    descriptors = []
    for index in range(0, num_descriptors):
        descriptor = device.feature_request(_F.MULTIPLATFORM, 0x10, index)
        platform, _ignore, os_flags, low, high = _unpack('!BBHHH', descriptor[:8])
        descriptors.append((platform, os_flags, low, high))
    choices = _NamedInts()
    for os_name, os_bit in OSS:
        for platform, os_flags, low, high in descriptors:
            os = os_name + _str_os_versions(low, high)
            if os_bit & os_flags and platform not in choices and os not in choices:
                choices[platform] = os
    return _ChoicesV(choices, read_skip_byte_count=6, write_prefix_bytes=b'\xff') if choices else None


def _feature_multiplatform():
    rw = _FeatureRW(_F.MULTIPLATFORM, read_fnid=0x00, write_fnid=0x30)
    return _Setting(_PLATFORM, rw, callback=_feature_multiplatform_callback)


PLATFORMS = _NamedInts()
PLATFORMS[0x00] = 'iOS, MacOS'
PLATFORMS[0x01] = 'Android, Windows'


def _feature_dualplatform():
    validator = _ChoicesV(PLATFORMS)
    rw = _FeatureRW(_F.DUALPLATFORM, read_fnid=0x00, write_fnid=0x20)
    return _Setting(_PLATFORM, rw, validator)


def _feature_change_host_callback(device):
    infos = device.feature_request(_F.CHANGE_HOST)
    assert infos, 'Oops, host count cannot be retrieved!'
    numHosts, currentHost = _unpack('!BB', infos[:2])
    hostNames = _hidpp20.get_host_names(device)
    hostNames = hostNames if hostNames is not None else {}
    if currentHost not in hostNames or hostNames[currentHost][1] == '':
        import socket  # find name of current host and use it
        hostNames[currentHost] = (True, socket.gethostname().partition('.')[0])
    choices = _NamedInts()
    for host in range(0, numHosts):
        _ignore, hostName = hostNames.get(host, (False, ''))
        choices[host] = str(host + 1) + ':' + hostName if hostName else str(host + 1)
    return _ChoicesV(choices, read_skip_byte_count=1) if choices else None


def _feature_change_host():
    rw = _FeatureRW(_F.CHANGE_HOST, read_fnid=0x00, write_fnid=0x10, no_reply=True)
    return _Setting(_CHANGE_HOST, rw, callback=_feature_change_host_callback, persist=False)


def _feature_thumb_mode():
    rw = _FeatureRW(_F.THUMB_WHEEL, read_fnid=0x10, write_fnid=0x20)
    validator = _BooleanV(true_value=b'\x01\x00', false_value=b'\x00\x00', mask=b'\x01\x00')
    return _Setting(_THUMB_SCROLL_MODE, rw, validator, device_kind=(_DK.mouse, _DK.trackball))


def _feature_thumb_invert():
    rw = _FeatureRW(_F.THUMB_WHEEL, read_fnid=0x10, write_fnid=0x20)
    validator = _BooleanV(true_value=b'\x00\x01', false_value=b'\x00\x00', mask=b'\x00\x01')
    return _Setting(_THUMB_SCROLL_INVERT, rw, validator, device_kind=(_DK.mouse, _DK.trackball))


def _feature_gesture2_gestures_callback(device):
    options = [g for g in _hidpp20.get_gestures(device).gestures.values() if g.can_be_enabled or g.default_enabled]
    return _BitFieldOMV(options) if options else None


def _feature_gesture2_gestures():
    rw = _FeatureRW(_F.GESTURE_2, read_fnid=0x10, write_fnid=0x20)
    s = _BitFieldOMSetting(
        _GESTURE2_GESTURES, rw, callback=_feature_gesture2_gestures_callback, device_kind=(_DK.touchpad, _DK.mouse)
    )
    s._labels = _GESTURE2_GESTURES_LABELS
    return s


def _feature_gesture2_params_callback(device):
    params = _hidpp20.get_gestures(device).params.values()
    items = [i for i in params if i.sub_params]
    if not items:
        return None
    sub_items = {i: i.sub_params for i in items}
    return _MultipleRangeV(items, sub_items)


def _feature_gesture2_params():
    rw = _FeatureRW(_F.GESTURE_2, read_fnid=0x70, write_fnid=0x80)
    s = _LongSettings(_GESTURE2_PARAMS, rw, callback=_feature_gesture2_params_callback, device_kind=(_DK.touchpad, _DK.mouse))

    class ParamWrapper:
        def get(self, name, default=None):
            return _GESTURE2_PARAMS_LABELS.get(name.param, default)

    s._labels = ParamWrapper()
    s._labels_sub = _GESTURE2_PARAMS_LABELS_SUB
    return s


#
#
#


def _S(name, featureID=None, featureFn=None, registerFn=None, identifier=None):
    return (name[0], featureID, featureFn, registerFn, identifier if identifier else name[0].replace('-', '_'))


_SETTINGS_TABLE = [
    _S(_HAND_DETECTION, registerFn=_register_hand_detection),
    _S(_SMOOTH_SCROLL, registerFn=_register_smooth_scroll),
    _S(_SIDE_SCROLL, registerFn=_register_side_scroll),
    _S(_HI_RES_SCROLL, _F.HI_RES_SCROLLING, _feature_hi_res_scroll),
    _S(_LOW_RES_SCROLL, _F.LOWRES_WHEEL, _feature_lowres_smooth_scroll),
    _S(_HIRES_INV, _F.HIRES_WHEEL, _feature_hires_smooth_invert),
    _S(_HIRES_RES, _F.HIRES_WHEEL, _feature_hires_smooth_resolution),
    _S(_FN_SWAP, _F.FN_INVERSION, _feature_fn_swap, registerFn=_register_fn_swap),
    _S(_FN_SWAP, _F.NEW_FN_INVERSION, _feature_new_fn_swap, identifier='new_fn_swap'),
    _S(_FN_SWAP, _F.K375S_FN_INVERSION, _feature_k375s_fn_swap, identifier='k375s_fn_swap'),
    _S(_DPI, _F.ADJUSTABLE_DPI, _feature_adjustable_dpi, registerFn=_register_dpi),
    _S(_POINTER_SPEED, _F.POINTER_SPEED, _feature_pointer_speed),
    _S(_SMART_SHIFT, _F.SMART_SHIFT, _feature_smart_shift),
    _S(_BACKLIGHT, _F.BACKLIGHT2, _feature_backlight2),
    _S(_REPROGRAMMABLE_KEYS, _F.REPROG_CONTROLS_V4, _feature_reprogrammable_keys),
    _S(_DISABLE_KEYS, _F.KEYBOARD_DISABLE_KEYS, _feature_disable_keyboard_keys),
    _S(_PLATFORM, _F.MULTIPLATFORM, _feature_multiplatform),
    _S(_PLATFORM, _F.DUALPLATFORM, _feature_dualplatform, identifier='dualplatform'),
    _S(_CHANGE_HOST, _F.CHANGE_HOST, _feature_change_host),
    _S(_THUMB_SCROLL_MODE, _F.THUMB_WHEEL, _feature_thumb_mode),
    _S(_THUMB_SCROLL_INVERT, _F.THUMB_WHEEL, _feature_thumb_invert),
    _S(_GESTURE2_GESTURES, _F.GESTURE_2, _feature_gesture2_gestures),
    _S(_GESTURE2_PARAMS, _F.GESTURE_2, _feature_gesture2_params),
]

_SETTINGS_LIST = namedtuple('_SETTINGS_LIST', [s[4] for s in _SETTINGS_TABLE])
RegisterSettings = _SETTINGS_LIST._make([s[3] for s in _SETTINGS_TABLE])
FeatureSettings = _SETTINGS_LIST._make([s[2] for s in _SETTINGS_TABLE])

del _SETTINGS_LIST

#
#
#


def check_feature(device, name, featureId, featureFn):
    """
    :param name: name for the setting
    :param featureId: the numeric Feature ID for this setting implementation
    :param featureFn: the function for this setting implementation
    """
    if featureId not in device.features:
        return
    try:
        detected = featureFn()(device)
        if _log.isEnabledFor(_DEBUG):
            _log.debug('check_feature[%s] detected %s', featureId, detected)
        return detected
    except Exception:
        from traceback import format_exc
        _log.error('check_feature[%s] inconsistent feature %s', featureId, format_exc())


# Returns True if device was queried to find features, False otherwise
def check_feature_settings(device, already_known):
    """Try to auto-detect device settings by the HID++ 2.0 features they have."""
    if device.features is None or not device.online:
        return False
    if device.protocol and device.protocol < 2.0:
        return False
    for name, featureId, featureFn, __, __ in _SETTINGS_TABLE:
        if featureId and featureFn:
            if not any(s.name == name for s in already_known):
                setting = check_feature(device, name, featureId, featureFn)
                if setting:
                    already_known.append(setting)
    return True


def check_feature_setting(device, setting_name):
    for name, featureId, featureFn, __, __ in _SETTINGS_TABLE:
        if name == setting_name and featureId and featureFn:
            feature = check_feature(device, name, featureId, featureFn)
            if feature:
                return feature
